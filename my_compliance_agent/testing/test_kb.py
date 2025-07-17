import asyncio
import os
import argparse
from mcp_agent.app import MCPApp
from mcp_agent.config import (
    Settings,
    LoggerSettings,
    MCPSettings,
    MCPServerSettings,
    GoogleSettings,
    BedrockSettings
)
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm_bedrock import BedrockAugmentedLLM


from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def clean_response(response):
    """Extract only the actual data from LLM response, removing tool call descriptions"""
    try:
        if "[Calling tool" in response:
            parts = response.split("]", 1)
            if len(parts) > 1:
                clean_part = parts[1].strip()
                clean_part = clean_part.replace("\\n", " ").replace('\\"', '"')
                return clean_part
        
        return response.strip().replace("\\n", " ").replace('\\"', '"')
    except Exception as e:
        return response

# Minimal settings focused only on Bedrock KB testing
settings = Settings(
    execution_engine="asyncio",
    logger=LoggerSettings(type="console", level="info"),
    mcp=MCPSettings(
        servers={
            "bedrock_kb": MCPServerSettings(
                command="uvx",
                args=["awslabs.bedrock-kb-retrieval-mcp-server@latest"],
                env={
                    "AWS_PROFILE": "my-bedrock-profile",
                    "AWS_REGION": "ap-southeast-2",
                    "FASTMCP_LOG_LEVEL": "ERROR",
                    "BEDROCK_KB_RERANKING_ENABLED": "false"
                },
                disabled=False,
                auto_approve=[]
            ),
        }
    ),
    bedrock=BedrockSettings(
        aws_access_key_id=os.getenv("AWS_ACCESS_ID_KEY", ""),
        aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY", ""),
        aws_region="ap-southeast-2",
        # default_model="arn:aws:bedrock:ap-southeast-2:123012555573:inference-profile/apac.anthropic.claude-3-5-sonnet-20241022-v2:0",
        default_model="arn:aws:bedrock:ap-southeast-2:123012555573:inference-profile/apac.anthropic.claude-3-7-sonnet-20250219-v1:0",
    ),
    google=GoogleSettings(
        api_key=os.getenv("GOOGLE_API"),
        vertexai=False,
        default_model="gemini-2.5-flash-lite-preview-06-17"        
    ),
)

app = MCPApp(name="Bedrock KB Tester", settings=settings)

async def test_kb_discovery():
    """Test knowledge base discovery and listing"""
    async with app.run() as agent_app:
        
        discovery_agent = Agent(
            name="kb_discovery_agent",
            instruction="""You are a knowledge base discovery specialist. Your tasks:
                        1. List all available knowledge bases you can access
                        2. For each knowledge base found, show:
                        - Knowledge base name/ID
                        - Number of data sources
                        - Any metadata available
                        3. If no knowledge bases found, explain possible reasons:
                        - Missing required tags (mcp-multirag-kb: true)
                        - Permission issues
                        - Regional configuration problems
                        4. Be specific about what you can and cannot access""",
            server_names=["bedrock_kb"],
        )
        
        async with discovery_agent:
            llm = await discovery_agent.attach_llm(BedrockAugmentedLLM)
            
            print("🔍 Testing Knowledge Base Discovery...")
            
            try:
                discovery_response = await llm.generate_str(
                    "Discover and list all available knowledge bases. Show me everything you can access."
                )
                
                result = clean_response(discovery_response)
                print(f"📋 Discovery Result:")
                print(f"   {result}")
                
                # Simple check if discovery was successful
                success_indicators = ["knowledge base", "data source", "available"]
                has_results = any(indicator in result.lower() for indicator in success_indicators)
                
                return has_results, result
                
            except Exception as e:
                print(f"❌ Discovery failed: {e}")
                return False, str(e)

async def test_kb_query(query_text="PCI DSS compliance requirements"):
    """Test knowledge base querying functionality"""
    async with app.run() as agent_app:
        
        query_agent = Agent(
            name="kb_query_agent", 
            instruction="""You are a knowledge base query specialist. Your tasks:
                        1. Execute the provided query against available knowledge bases
                        2. Return the top 3-5 most relevant results
                        3. For each result, show:
                        - Relevance score (if available)
                        - Source document/data source
                        - Key excerpts or summaries
                        - Citation information
                        4. If no results found, explain why (empty KB, query too specific, etc.)
                        5. If multiple knowledge bases available, search all of them""",
            server_names=["bedrock_kb"],
        )
        
        async with query_agent:
            llm = await query_agent.attach_llm(BedrockAugmentedLLM)
            
            print(f"🔍 Testing Knowledge Base Query: '{query_text}'...")
            
            try:
                query_response = await llm.generate_str(
                    f"Use the QueryKnowledgeBases tool to search for: '{query_text}'. "
                    f"Execute the search immediately and return all results. "
                    f"First list available knowledge bases if needed, then query them all."
                )
                
                result = clean_response(query_response)
                print(f"📊 Query Result:")
                print(f"   {result}")
                
                # Check if we got meaningful results
                success_indicators = ["result", "found", "source", "document"]
                has_results = any(indicator in result.lower() for indicator in success_indicators)
                
                return has_results, result
                
            except Exception as e:
                print(f"❌ Query failed: {e}")
                return False, str(e)

async def test_kb_data_sources():
    """Test listing data sources for knowledge bases"""
    async with app.run() as agent_app:
        
        datasource_agent = Agent(
            name="kb_datasource_agent",
            instruction="""You are a data source analyzer. Your tasks:
                        1. List all data sources for each available knowledge base
                        2. For each data source, show:
                        - Data source name/ID
                        - Data source type (S3, web crawler, etc.)
                        - Status (active, syncing, error, etc.)
                        - Last sync time (if available)
                        3. Identify any data sources with issues
                        4. Show total number of documents/chunks if available""",
            server_names=["bedrock_kb"],
        )
        
        async with datasource_agent:
            llm = await datasource_agent.attach_llm(BedrockAugmentedLLM)
            
            print("🔍 Testing Data Source Discovery...")
            
            try:
                datasource_response = await llm.generate_str(
                    "List all data sources for the available knowledge bases. Show their status and details."
                )
                
                result = clean_response(datasource_response)
                print(f"📁 Data Sources:")
                print(f"   {result}")
                
                return True, result
                
            except Exception as e:
                print(f"❌ Data source discovery failed: {e}")
                return False, str(e)

async def run_comprehensive_test(custom_query=None):
    """Run all KB tests in sequence"""
    print("🚀 Bedrock Knowledge Base MCP Server Test Suite")
    print("=" * 60)
    
    all_tests_passed = True
    test_results = {}
    
    # Test 1: Discovery
    print("\n" + "=" * 40)
    print("TEST 1: KNOWLEDGE BASE DISCOVERY")
    print("=" * 40)
    
    discovery_success, discovery_result = await test_kb_discovery()
    test_results["discovery"] = {"success": discovery_success, "result": discovery_result}
    
    if discovery_success:
        print("✅ Knowledge base discovery: PASSED")
    else:
        print("❌ Knowledge base discovery: FAILED")
        all_tests_passed = False
    
    # Test 2: Data Sources (only if discovery passed)
    if discovery_success:
        print("\n" + "=" * 40)
        print("TEST 2: DATA SOURCE ANALYSIS")
        print("=" * 40)
        
        datasource_success, datasource_result = await test_kb_data_sources()
        test_results["datasources"] = {"success": datasource_success, "result": datasource_result}
        
        if datasource_success:
            print("✅ Data source analysis: PASSED")
        else:
            print("❌ Data source analysis: FAILED")
            all_tests_passed = False
    
    # Test 3: Querying (only if discovery passed)
    if discovery_success:
        print("\n" + "=" * 40)
        print("TEST 3: KNOWLEDGE BASE QUERYING")
        print("=" * 40)
        
        query_text = custom_query or "PCI DSS compliance requirements"
        query_success, query_result = await test_kb_query(query_text)
        test_results["querying"] = {"success": query_success, "result": query_result}
        
        if query_success:
            print("✅ Knowledge base querying: PASSED")
        else:
            print("❌ Knowledge base querying: FAILED")
            all_tests_passed = False
    
    # Final Summary
    print("\n" + "=" * 60)
    print("FINAL TEST SUMMARY")
    print("=" * 60)
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Your Bedrock KB MCP server is working correctly.")
        print("\n📋 Next Steps:")
        print("   - You can now integrate bedrock_kb into your main audit workflow")
        print("   - Add 'bedrock_kb' to server_names in your agents")
        print("   - Use KB queries to enhance your compliance audits")
    else:
        print("❌ SOME TESTS FAILED. Check the issues above.")
        print("\n🔧 Common Solutions:")
        if not test_results.get("discovery", {}).get("success"):
            print("   - Verify your knowledge base has tag: mcp-multirag-kb = true")
            print("   - Check AWS profile permissions for Bedrock")
            print("   - Ensure KB exists in ap-southeast-2 region")
        print("   - Review AWS credentials and profile configuration")
        print("   - Check if knowledge base has data sources with content")
    
    return all_tests_passed

async def main():
    parser = argparse.ArgumentParser(description='Test Bedrock Knowledge Base MCP Server')
    parser.add_argument('--query', help='Custom query to test (default: "PCI DSS compliance requirements")')
    parser.add_argument('--discovery-only', action='store_true', help='Run only discovery test')
    parser.add_argument('--query-only', help='Run only query test with specified query')
    
    args = parser.parse_args()
    
    try:
        if args.discovery_only:
            print("🔍 Running Discovery Test Only...")
            success, result = await test_kb_discovery()
            return 0 if success else 1
            
        elif args.query_only:
            print(f"🔍 Running Query Test Only: '{args.query_only}'")
            success, result = await test_kb_query(args.query_only)
            return 0 if success else 1
            
        else:
            # Run comprehensive test suite
            all_passed = await run_comprehensive_test(args.query)
            return 0 if all_passed else 1
            
    except Exception as e:
        print(f"❌ Critical error during testing: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
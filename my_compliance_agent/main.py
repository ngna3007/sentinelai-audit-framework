import asyncio
import os
import argparse
import re
import json
import shutil
import glob
from mcp_agent.app import MCPApp
from mcp_agent.config import (
    Settings,
    LoggerSettings,
    MCPSettings,
    MCPServerSettings,
    BedrockSettings,
    AnthropicSettings,
    GoogleSettings,
)
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_bedrock import BedrockAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

settings = Settings(
    execution_engine="asyncio",
    logger=LoggerSettings(type="console", level="info"),
    mcp=MCPSettings(
        servers={
            "supabase": MCPServerSettings(
                command="npx",
                args=[
                    "-y",
                    "@supabase/mcp-server-supabase@latest",
                    "--read-only",
                    "--project-ref=rqknorhfhwrdoahjtsce",
                ],
                env={"SUPABASE_ACCESS_TOKEN": os.getenv("SUPABASE_ACCESS_TOKEN", "")},
            ),
            "filesystem": MCPServerSettings(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem"],
            ),
            "bedrock_kb": MCPServerSettings(
                command="uvx",
                args= ["awslabs.bedrock-kb-retrieval-mcp-server@latest"],
                env={
                    "AWS_PROFILE": "my-bedrock-profile",
                    "AWS_REGION": "ap-southeast-2",
                    "FASTMCP_LOG_LEVEL": "ERROR",
                    "BEDROCK_KB_RERANKING_ENABLED": "true"
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
        default_model="arn:aws:bedrock:ap-southeast-2:123012555573:inference-profile/apac.anthropic.claude-3-5-sonnet-20241022-v2:0",
    ),
    anthropic=AnthropicSettings(
        api_key=os.getenv("ANTHROPIC_API"),
        # default_model="claude-3-haiku-20240307",
        default_model="claude-sonnet-4-20250514",
    ),
    google=GoogleSettings(
        api_key=os.getenv("GOOGLE_API"),
        vertexai= False,
    # project: str | None = None
    # location: str | None = None
        default_model="gemini-2.0-flash"        
    ),
)

app = MCPApp(name="Clean Requirement Fetcher", settings=settings)


def cleanup_folders():
    """Clean up requirement and evidence folders using pure Python"""
    
    print("🧹 Starting folder cleanup...")
    
    deleted_files = []
    
    try:
        # Clean requirement/ folder
        if os.path.exists("requirement"):
            req_files = glob.glob("requirement/*")
            for file_path in req_files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted_files.append(f"{file_path}/ (directory)")
            
            print(f"✅ Cleaned requirement/ folder ({len([f for f in req_files if os.path.exists(f) == False])} items deleted)")
        else:
            print("📁 requirement/ folder doesn't exist")
        
        # Clean evidence/ folder
        if os.path.exists("evidence"):
            ev_files = glob.glob("evidence/*")
            for file_path in ev_files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted_files.append(f"{file_path}/ (directory)")
            
            print(f"✅ Cleaned evidence/ folder ({len([f for f in ev_files if os.path.exists(f) == False])} items deleted)")
        else:
            print("📁 evidence/ folder doesn't exist")
        
        # Create directories if they don't exist
        os.makedirs("requirement", exist_ok=True)
        os.makedirs("evidence", exist_ok=True)
        
        print(f"📋 Total files/folders deleted: {len(deleted_files)}")
        if deleted_files:
            print("🗑️ Deleted items:")
            for item in deleted_files[:5]:  # Show first 5 items
                print(f"   - {item}")
            if len(deleted_files) > 5:
                print(f"   ... and {len(deleted_files) - 5} more items")
        
        return {
            "success": True,
            "deleted_count": len(deleted_files),
            "deleted_files": deleted_files
        }
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "deleted_count": len(deleted_files)
        }

def clean_response(response):
    """Extract only the actual data from LLM response, removing tool call descriptions"""
    try:
        # Remove the tool call part if present
        if "[Calling tool" in response:
            # Find where the tool call ends and actual content begins
            parts = response.split("]", 1)
            if len(parts) > 1:
                clean_part = parts[1].strip()
                # Remove any remaining tool artifacts
                clean_part = clean_part.replace("\\n", " ").replace('\\"', '"')
                return clean_part
        
        # If no tool call prefix, return as-is but clean up
        return response.strip().replace("\\n", " ").replace('\\"', '"')
        
    except Exception as e:
        return response
def extract_json_from_response(response):
    """Extract and parse JSON data from LLM response"""
    try:
        # Look for JSON array in the response
        if '[{' in response and '}]' in response:
            # Find the JSON array
            start = response.find('[{')
            end = response.rfind('}]') + 2
            json_str = response[start:end]
            
            # Clean up escaped characters
            json_str = json_str.replace('\\"', '"').replace('\\n', '\n')
            
            # Try to parse as JSON
            try:
                parsed_json = json.loads(json_str)
                # If it's an array, format it nicely
                return json.dumps(parsed_json, indent=2)
            except json.JSONDecodeError:
                # If parsing fails, return cleaned string
                return json_str
        
        # If no JSON found, try to extract from quotes
        elif '"' in response:
            # Look for quoted content
            lines = response.split('\n')
            for line in lines:
                if line.strip().startswith('"') and line.strip().endswith('"'):
                    return line.strip().strip('"')
        
        return clean_response(response)
        
    except Exception as e:
        return clean_response(response)
    
async def fetch_requirement_data(control_id):
    """Fetch requirement data with clean responses"""
    
    async with app.run() as agent_app:
        context = agent_app.context
        
        # Fix filesystem server configuration
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
        
        print(f"🎯 Fetching data for control ID: {control_id}")
        
        # Create agent with very specific instructions
        data_agent = Agent(
            name="data_fetcher_and_editor",
            instruction="""You are a SQL executor and file editor. Your tasks:
                        1. Execute SQL queries to get data from database
                        2. When saving to requirement/ directory (filename like 1_2_5.json):
                        - If file already exists, READ it first and MERGE new data with existing data
                        - If file doesn't exist, create new file
                        - NEVER replace/overwrite existing data - always merge/combine
                        3. The final JSON structure should contain ALL data:
                        - Keep existing requirement text if already present
                        - Add config_rules data to the same file
                        - Merge data so we have ONE complete JSON file with both requirement and config_rules
                        4. Fix any formatting issues:
                        - Convert escaped JSON strings to proper JSON objects/arrays
                        - Remove extra quotes around text values
                        - Ensure config_rules is a proper JSON array, not a string
                        5. Save the corrected file with clean, readable JSON formatting
                        6. Return confirmation when file is properly formatted with ALL data preserved""",
            server_names=["supabase", "filesystem"],
        )
        
        async with data_agent:
            llm = await data_agent.attach_llm(GoogleAugmentedLLM)
            
            # Fetch requirement text
            print("📋 Getting requirement...")
            await asyncio.sleep(5)
            
            try:
                req_response = await llm.generate_str(
                    f"Execute: SELECT requirement FROM pci_dss_controls WHERE control_id = '{control_id}';"
                )
                requirement = clean_response(req_response)
                # requirement = req_response
            except Exception as e:
                print(f"❌ Requirement fetch failed: {e}")
                requirement = f"Error: {str(e)}"
            
            # Fetch config rules  
            print("🔧 Getting config rules...")
            await asyncio.sleep(15)
            
            try:
                rules_response = await llm.generate_str(
                    f"Execute: SELECT config_rules FROM pci_aws_config_rule_mappings WHERE control_id = '{control_id}';"
                )
                # config_rules = clean_response(rules_response)
                # config_rules = extract_json_from_response(rules_response)
                config_rules = rules_response
            except Exception as e:
                print(f"❌ Config rules fetch failed: {e}")
                config_rules = f"Error: {str(e)}"
            if config_rules and requirement:
                return {"success": True}
            else:
                return {"success": False}


async def fetch_evidence_data():
    """Draft function that always returns True - placeholder for evidence fetching"""
    print("📊 Fetching evidence data...")
    await asyncio.sleep(2)
    print("✅ Evidence data fetched (placeholder)")
    return True

async def check_compliance():
    """Perform audition and return compliance result"""
    
    async with app.run() as agent_app:
        context = agent_app.context
        
        # Fix filesystem server configuration
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
                
        # Create agent with very specific instructions
        auditor_agent = Agent(
            name="pci_auditor",
            instruction="""You are a PCI DSS compliance auditor with expert knowledge access. Your task:
                        1. FIRST: Query the bedrock knowledge base for expert guidance on this specific PCI DSS control - ask for compliance best practices, common pitfalls, and assessment criteria
                        2. READ the requirement file from requirement/ directory to understand the specific control requirements
                        3. READ the evidence files from evidence/ directory to see actual AWS config rule results
                        4. ANALYZE using BOTH the expert KB guidance AND the local file data to make informed compliance decisions
                        5. CREATE audit_result/ directory if it doesn't exist
                        6. SAVE compliance assessment as JSON in audit_result/ directory
                        7. RETURN the JSON compliance assessment with expert-level precision""",
            server_names=["filesystem", "bedrock_kb"],
        )
        
        async with auditor_agent:
            llm = await auditor_agent.attach_llm(GoogleAugmentedLLM)
            
            print("🔍 Starting compliance audit...")
            await asyncio.sleep(5)
            
            try:
                # Ask agent to analyze compliance
                audit_response = await llm.generate_str(
                    f"""Perform PCI DSS compliance audit for control {args.id}:
                    1. First, query the bedrock knowledge base for expert guidance on PCI DSS control {args.id}
                    2. Read the requirement file from requirement/ directory
                    3. Read all evidence files from evidence/ directory  
                    4. Combine KB expert guidance with file analysis
                    5. Calculate compliance rate and provide detailed assessment
                    6. Save results to audit_result/ directory as JSON
                    7. Return the compliance assessment JSON"""
                )
                
                compliance_result = clean_response(audit_response)
                print(f"✅ Compliance audit completed")
                
                # Try to parse as JSON to validate format
                try:
                    import json
                    compliance_data = json.loads(compliance_result)
                    
                    return {
                        "success": True,
                        "compliance_data": compliance_data,
                        "raw_response": compliance_result
                    }
                    
                except json.JSONDecodeError:
                    # If not valid JSON, return raw response
                    print("⚠️ Response not in JSON format, returning raw")
                    return {
                        "success": True,
                        "compliance_data": None,
                        "raw_response": compliance_result
                    }
                
            except Exception as e:
                print(f"❌ Compliance audit failed: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "compliance_data": None
                }

async def main():
    print("🚀 PCI DSS Compliance Auditor\n")
    
    parser = argparse.ArgumentParser(description='Fetch requirement data and perform compliance audit')
    parser.add_argument('id', help='Control ID (e.g., 1.2.5)')
    args = parser.parse_args()
    
    try:
        # Step 1: Fetch requirement data
        print("=" * 50)
        print("STEP 1: FETCHING REQUIREMENT DATA")
        print("=" * 50)
        
        req_fetch_result = await fetch_requirement_data(args.id)
        
        if req_fetch_result["success"]:
            print(f"✅ Requirement fetched successfully")
            print(f"📁 File saved: {req_fetch_result['filename']}")
            
            # Step 2: Fetch evidence data (placeholder)
            print("\n" + "=" * 50)
            print("STEP 2: FETCHING EVIDENCE DATA")
            print("=" * 50)
            
            evidence_fetch_result = await fetch_evidence_data()
            
            if evidence_fetch_result:
                print("✅ Evidence data ready")
                
                # Step 3: Perform compliance audit
                print("\n" + "=" * 50)
                print("STEP 3: PERFORMING COMPLIANCE AUDIT")
                print("=" * 50)
                
                compliance_result = await check_compliance()
                
                if compliance_result["success"]:
                    print("✅ Compliance audit completed")
                    
                    if compliance_result["compliance_data"]:
                        # Display compliance results
                        comp_data = compliance_result["compliance_data"]
                        print(f"\n📊 COMPLIANCE RESULTS:")
                        print(f"   Compliant Rules: {comp_data.get('compliant_rules', 'N/A')}")
                        print(f"   Total Rules: {comp_data.get('total_rules', 'N/A')}")
                        print(f"   Compliance Rate: {comp_data.get('compliance_rate', 'N/A'):.1%}")
                        print(f"   Status: {comp_data.get('status', 'N/A')}")
                        
                        final_status = comp_data.get('status') == 'COMPLIANT'
                    else:
                        print(f"⚠️ Compliance data in unexpected format:")
                        print(f"   Raw response: {compliance_result['raw_response'][:200]}...")
                        final_status = False
                else:
                    print(f"❌ Compliance audit failed: {compliance_result.get('error', 'Unknown error')}")
                    final_status = False
                
                # Final summary
                print(f"\n🎯 FINAL RESULT:")
                if final_status:
                    print(f"✅ Control {args.id} is COMPLIANT")
                else:
                    print(f"❌ Control {args.id} is NON-COMPLIANT or audit failed")
                
                
                print("CLEANING UP FOR NEXT RUN")
                print("=" * 50)
                # cleanup_result = cleanup_folders()
                return 0 if final_status else 1
                
            else:
                print("❌ Evidence fetch failed")
                return 1
        else:
            print(f"❌ Requirement fetch failed: {req_fetch_result.get('error', 'Unknown error')}")
            return 1
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
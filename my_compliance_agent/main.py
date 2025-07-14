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
    
async def fetch_requirement_data(control_id):
    """Fetch requirement data with clean responses"""
    
    async with app.run() as agent_app:
        context = agent_app.context
        
        # Fix filesystem server configuration
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
        
        print(f"🎯 Fetching data for control ID: {control_id}")
        
        # Create agent with very specific instructions
        data_agent = Agent(
            name="accurate_data_fetcher",
            instruction="""You are a precise SQL executor. CRITICAL RULES:
                        1. Execute the SQL query EXACTLY as provided
                        2. Return the EXACT data from the database - DO NOT modify, summarize, or interpret
                        3. If the result is JSON, return the complete JSON exactly as stored
                        4. If the result is text, return the exact text
                        5. DO NOT add quotes around the result unless they are in the original data
                        6. DO NOT translate or simplify complex data
                        7. Return the raw database value with no changes whatsoever
                        8. NO commentary, explanations, or descriptions - just the raw data""",
            server_names=["supabase", "filesystem"],
        )
        
        async with data_agent:
            llm = await data_agent.attach_llm(AnthropicAugmentedLLM)
            
            # Fetch requirement text
            print("📋 Getting requirement...")
            await asyncio.sleep(5)
            
            try:
                req_response = await llm.generate_str(
                    f"SELECT requirement FROM pci_dss_controls WHERE control_id = '{control_id}';"
                )
                requirement = clean_response(req_response)
            except Exception as e:
                print(f"❌ Requirement fetch failed: {e}")
                requirement = f"Error: {str(e)}"
            
            # Fetch config rules  
            print("🔧 Getting config rules...")
            await asyncio.sleep(15)
            
            try:
                rules_response = await llm.generate_str(
                    f"SELECT config_rules FROM pci_aws_config_rule_mappings WHERE control_id = '{control_id}';"
                )
                config_rules = clean_response(rules_response)
            except Exception as e:
                print(f"❌ Config rules fetch failed: {e}")
                config_rules = f"Error: {str(e)}"
            
            # Create clean data structure
            data = {
                "control_id": control_id,
                "requirement": requirement,
                "config_rules": config_rules,
                "timestamp": "2025-07-14",
                "status": "fetched"
            }
            
            # Save file directly with Python (no LLM needed)
            print("💾 Saving file...")
            
            try:
                os.makedirs("requirement", exist_ok=True)
                filename = f"requirement/requirement_{control_id.replace('.', '_')}.json"
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"✅ Saved to: {filename}")
                
                return {
                    "success": True,
                    "data": data,
                    "filename": filename
                }
                
            except Exception as e:
                print(f"❌ File save failed: {e}")
                return {
                    "success": False,
                    "data": data,
                    "error": str(e)
                }

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
            instruction="""You are a PCI DSS compliance auditor. Your task:
                        1. READ the requirement file from requirement/ directory to understand what needs to be checked
                        2. READ the evidence files from evidence/ directory to see the actual AWS config rule results
                        3. ANALYZE each config rule result against the requirement guidance
                        4. COUNT how many rules are COMPLIANT vs total rules
                        5. RETURN ONLY a JSON object with this exact format:
                        {
                        "compliant_rules": <number of compliant rules>,
                        "total_rules": <total number of rules>,
                        "compliance_rate": <compliant_rules/total_rules as decimal>,
                        "status": "COMPLIANT" or "NON_COMPLIANT",
                        "details": ["list of rule names and their status"]
                        }
                        NO other text, just the JSON object.""",
            server_names=["filesystem"],
        )
        
        async with auditor_agent:
            llm = await auditor_agent.attach_llm(AnthropicAugmentedLLM)
            
            print("🔍 Starting compliance audit...")
            await asyncio.sleep(5)
            
            try:
                # Ask agent to analyze compliance
                audit_response = await llm.generate_str(
                    """Perform PCI DSS compliance audit:
                    1. Read the requirement file from requirement/ directory
                    2. Read all evidence files from evidence/ directory  
                    3. Compare evidence against requirement guidance
                    4. Calculate compliance rate
                    5. Return JSON with compliance results"""
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
                cleanup_result = cleanup_folders()
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
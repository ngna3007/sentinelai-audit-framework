# Alternative solution to current appoach - Hybrid of parallel and sequential flow
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
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM

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
        # default_model="arn:aws:bedrock:ap-southeast-2:123012555573:inference-profile/apac.anthropic.claude-3-5-sonnet-20241022-v2:0",
        default_model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    ),
    anthropic=AnthropicSettings(
        api_key=os.getenv("ANTHROPIC_API"),
        # default_model="claude-3-haiku-20240307",
        # default_model="claude-sonnet-4-20250514",
        default_model="claude-3-5-haiku-20241022",
    ),
    google=GoogleSettings(
        api_key=os.getenv("GOOGLE_API"),
        vertexai= False,
    # project: str | None = None
    # location: str | None = None
        default_model="gemini-2.5-flash"        
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
    
async def two_phase_parallel_workflow(control_id):
    """Execute workflow in 2 phases: Phase 1 (data + evidence in parallel), Phase 2 (compliance audit)"""
    
    async with app.run() as agent_app:
        context = agent_app.context
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
        
        print(f"🚀 Starting two-phase parallel workflow for control {control_id}")
        
        # PHASE 1: Data Collection (can run in parallel)
        print("⚡ Phase 1: Parallel data collection...")
        
        # Agent 1: Data Fetcher
        data_fetcher = Agent(
            name="data_fetcher_and_editor",
            instruction="""You are a SQL executor and file editor. Your tasks:
                        1. Execute SQL queries to get data from database
                        2. When saving to requirement/ directory with file name as requirement id with underscore between them, for example (1_2_5.json)):
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
        
        # Agent 2: Evidence Fetcher  
        evidence_fetcher = Agent(
            name="evidence_fetcher", 
            instruction=f"""You are an AWS Config evidence collector for control {control_id}. Your tasks:
                        1. Simulate fetching AWS Config rule evaluation results for PCI DSS control {control_id}
                        2. Create evidence files in evidence/ directory
                        3. Generate realistic compliance evidence data
                        4. Save evidence as evidence/pci_dss_control_{control_id.replace('.', '_')}_audit_result.json
                        5. Return confirmation: "Evidence collected and saved successfully for control {control_id}" """,
            server_names=["filesystem"],
        )
        
        # Phase 1 coordinator
        phase1_coordinator = Agent(
            name="phase1_coordinator",
            instruction=f"""You coordinate data and evidence collection for control {control_id}.
                        
                        TASK: Confirm both data fetcher and evidence fetcher completed successfully.
                        
                        PROCESS:
                        1. Receive confirmations from data_fetcher and evidence_fetcher
                        2. Verify both completed successfully  
                        3. Return: "Phase 1 completed - data and evidence ready for control {control_id}" """,
            server_names=["filesystem"],
        )
        
        # Execute Phase 1 in parallel
        phase1_parallel = ParallelLLM(
            fan_in_agent=phase1_coordinator,
            fan_out_agents=[data_fetcher, evidence_fetcher],
            llm_factory=AnthropicAugmentedLLM,
        )
        
        try:
            phase1_result = await phase1_parallel.generate_str(
                message=f"""Execute Phase 1 for control {control_id}:
                
                DATA FETCHER: Fetch requirement and config rules from database, save to requirement/ directory
                EVIDENCE FETCHER: Collect AWS Config evidence, save to evidence/ directory
                
                Both agents should work simultaneously."""
            )
            
            print("✅ Phase 1 completed - data and evidence ready")
            
            # PHASE 2: Compliance Analysis (depends on Phase 1)
            print("⚡ Phase 2: Compliance analysis...")
            
            compliance_auditor = Agent(
                name="compliance_auditor",
                instruction=f"""You are a PCI DSS compliance auditor for control {control_id}. Your task:
                            1. READ requirement/{control_id.replace('.', '_')}.json for requirements and config rules
                            2. READ evidence files from evidence/ directory
                            3. Generate structured compliance assessment in this EXACT format:
                            {{
                              "control_id": "{control_id}",
                              "requirement": "<requirement text>",
                              "compliance_assessment": {{
                                "<rule_name>": {{
                                  "status": "COMPLIANT|NON_COMPLIANT|NOT_APPLICABLE",
                                  "details": "<detailed explanation>"
                                }}
                              }},
                              "compliance_summary": {{
                                "compliant_rules": <number>,
                                "non_compliant_rules": <number>,
                                "not_applicable_rules": <number>,
                                "total_rules_in_scope": <number>,
                                "compliance_rate": "<percentage>"
                              }}
                            }}
                            4. Save assessment to audit_result/{control_id.replace('.', '_')}_audit.json
                            5. Return the complete JSON assessment""",
                server_names=["filesystem"],
            )
            
            async with compliance_auditor:
                llm = await compliance_auditor.attach_llm(BedrockAugmentedLLM)
                
                phase2_result = await llm.generate_str(
                    f"""Perform compliance audit for control {control_id}:
                    
                    1. Read requirement/{control_id.replace('.', '_')}.json to get requirements and config rules
                    2. Read evidence files from evidence/ directory
                    3. Analyze each config rule and determine compliance status
                    4. Generate structured JSON assessment
                    5. Save to audit_result/ directory
                    6. Return the complete assessment"""
                )
            
            print("✅ Phase 2 completed - compliance assessment ready")
            
            # Parse final results
            try:
                import json
                compliance_data = json.loads(clean_response(phase2_result))
                
                return {
                    "success": True,
                    "phase1_result": phase1_result,
                    "compliance_data": compliance_data,
                    "raw_response": phase2_result
                }
                
            except json.JSONDecodeError:
                print("⚠️ Phase 2 response not in JSON format")
                return {
                    "success": True,
                    "phase1_result": phase1_result,
                    "compliance_data": None,
                    "raw_response": phase2_result
                }
                
        except Exception as e:
            print(f"❌ Two-phase workflow failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "compliance_data": None
            }

# Updated main function to use two-phase parallel workflow
async def main():
    print("🚀 PCI DSS Compliance Auditor (Two-Phase Parallel Mode)\n")
    
    parser = argparse.ArgumentParser(description='Fetch requirement data and perform compliance audit')
    parser.add_argument('id', help='Control ID (e.g., 1.2.5)')
    args = parser.parse_args()
    
    try:
        print("=" * 50)
        print("TWO-PHASE PARALLEL WORKFLOW")
        print("=" * 50)
        
        # Execute workflow: Phase 1 (parallel) + Phase 2 (sequential)
        workflow_result = await two_phase_parallel_workflow(args.id)
        
        if workflow_result["success"]:
            print("✅ Two-phase workflow completed successfully")
            
            if workflow_result["compliance_data"]:
                comp_data = workflow_result["compliance_data"]
                comp_summary = comp_data.get("compliance_summary", {})
                
                print(f"\n📊 COMPLIANCE RESULTS:")
                print(f"   Compliant Rules: {comp_summary.get('compliant_rules', 'N/A')}")
                print(f"   Non-Compliant Rules: {comp_summary.get('non_compliant_rules', 'N/A')}")
                print(f"   Not Applicable Rules: {comp_summary.get('not_applicable_rules', 'N/A')}")
                print(f"   Total Rules: {comp_summary.get('total_rules_in_scope', 'N/A')}")
                print(f"   Compliance Rate: {comp_summary.get('compliance_rate', 'N/A')}")
                
                # Determine final status
                compliance_rate = comp_summary.get('compliance_rate', '0%')
                try:
                    rate_value = float(compliance_rate.replace('%', '')) if '%' in compliance_rate else 0
                    final_status = rate_value >= 80  # 80% threshold for compliance
                except:
                    final_status = False
                    
            else:
                print("⚠️ Compliance data in unexpected format:")
                print(f"   Raw response: {workflow_result['raw_response'][:200]}...")
                final_status = False
                
            # Final summary
            print(f"\n🎯 FINAL RESULT:")
            if final_status:
                print(f"✅ Control {args.id} is COMPLIANT")
            else:
                print(f"❌ Control {args.id} is NON-COMPLIANT or workflow incomplete")
                
            print(f"\n📋 Phase 1 Summary: {workflow_result.get('phase1_result', 'N/A')[:100]}...")
            
            return 0 if final_status else 1
            
        else:
            print(f"❌ Two-phase workflow failed: {workflow_result.get('error', 'Unknown error')}")
            return 1
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return 1
if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
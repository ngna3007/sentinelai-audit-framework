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
    GroqSettings,  # Add Groq settings import
)
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_bedrock import BedrockAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm_groq import GroqAugmentedLLM  # Add Groq import
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
        default_model="arn:aws:bedrock:ap-southeast-2:123012555573:inference-profile/apac.anthropic.claude-3-7-sonnet-20250219-v1:0",
    ),
    anthropic=AnthropicSettings(
        api_key=os.getenv("ANTHROPIC_API"),
        default_model="claude-3-5-haiku-20241022",
    ),
    google=GoogleSettings(
        api_key=os.getenv("GOOGLE_API"),
        vertexai= False,
        default_model="gemini-2.5-flash-lite-preview-06-17"        
    ),
    groq=GroqSettings(  # Add Groq settings
        api_key=os.getenv("GROQ_API_KEY", ""),
        default_model="mixtral-8x7b-32768",  # or "llama2-70b-4096"
    ),
)

app = MCPApp(name="Clean Requirement Fetcher", settings=settings)

def cleanup_folders():
    """Clean up requirement and audit_result folders using pure Python"""
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
            
            print(f"✅ Cleaned requirement/ folder ({len([f for f in req_files if not os.path.exists(f)])} items deleted)")
        else:
            print("📁 requirement/ folder doesn't exist")
        
        # Clean audit_result/ folder
        if os.path.exists("audit_result"):
            audit_files = glob.glob("audit_result/*")
            for file_path in audit_files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted_files.append(f"{file_path}/ (directory)")
            
            print(f"✅ Cleaned audit_result/ folder ({len([f for f in audit_files if not os.path.exists(f)])} items deleted)")
        else:
            print("📁 audit_result/ folder doesn't exist")
        
        # Create directories if they don't exist
        os.makedirs("requirement", exist_ok=True)
        os.makedirs("audit_result", exist_ok=True)
        
        print(f"📋 Total files/folders deleted: {len(deleted_files)}")
        if deleted_files:
            print("🗑️ Deleted items:")
            for item in deleted_files[:10]:  # Show first 10 items
                print(f"   - {item}")
            if len(deleted_files) > 10:
                print(f"   ... and {len(deleted_files) - 10} more items")
        
        return True
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False

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
    
async def fetch_requirement_data(control_id):
    """Fetch requirement data with clean responses"""
    async with app.run() as agent_app:
        context = agent_app.context
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
        
        print(f"🎯 Fetching data for control ID: {control_id}")
        
        data_agent = Agent(
            name="data_fetcher_and_editor",
            instruction="""You are a SQL executor and file editor. Your tasks:
                        1. Create file name as requirement id with underscore between them, for example 1_2_5.json for requirement 1.2.5, in requirement/ directory
                        2. Execute SQL queries to get data from database
                        3. When saving to requirement/ directory:
                        - If file already exists, READ it first and MERGE new data with existing data
                        - If file doesn't exist, create new file
                        - NEVER replace/overwrite existing data - always merge/combine
                        4. The final JSON structure should contain ALL data:
                        - Keep existing requirement text if already present
                        - Add config_rules data to the same file
                        - Merge data so we have ONE complete JSON file with both requirement and config_rules
                        5. Fix any formatting issues:
                        - Convert escaped JSON strings to proper JSON objects/arrays
                        - Remove extra quotes around text values
                        - Ensure config_rules is a proper JSON array, not a string
                        6. Save the corrected file with clean, readable JSON formatting
                        7. Return confirmation when file is properly formatted with ALL data preserved""",
            server_names=["supabase", "filesystem"],
        )
        
        async with data_agent:
            llm = await data_agent.attach_llm(GoogleAugmentedLLM)
            
            print("📋 Getting requirement...")
            
            try:
                req_response = await llm.generate_str(
                    f"Execute: SELECT requirement FROM pci_dss_controls WHERE control_id = '{control_id}';"
                )
                requirement = clean_response(req_response)
            except Exception as e:
                print(f"❌ Requirement fetch failed: {e}")
                return False
            
            print("🔧 Getting config rules...")
            
            try:
                rules_response = await llm.generate_str(
                    f"Execute: SELECT config_rules FROM pci_aws_config_rule_mappings WHERE control_id = '{control_id}';"
                )
                config_rules = rules_response
            except Exception as e:
                print(f"❌ Config rules fetch failed: {e}")
                return False
            
            return True

async def fetch_evidence_data():
    """Draft function that always returns True - placeholder for evidence fetching"""
    print("📊 Fetching evidence data...")
    await asyncio.sleep(2)
    print("✅ Evidence data fetched (placeholder)")
    return True

async def check_compliance(control_id, aws_account_id='aws-account-001'):
    """Perform audition and return compliance result - UPDATED"""
    
    async with app.run() as agent_app:
        context = agent_app.context
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
                
        # Create agent with very specific instructions - UPDATED
        auditor_agent = Agent(
            name="pci_auditor",
            instruction=f"""You are a PCI DSS compliance auditor. Your task is to generate a structured compliance assessment in EXACT JSON format.

                        REQUIRED OUTPUT FORMAT:
                        {{
                        "control_id": "{control_id}",
                        "requirement": "<requirement text from requirement file>",
                        "compliance_assessment": {{
                            "<rule_name>": {{
                            "status": "COMPLIANT|NON_COMPLIANT|NOT_APPLICABLE",
                            "details": "<detailed explanation>",
                            "fetched_evidences": ["<evidence_file_1>", "<evidence_file_2>", "..."],
                            "remediation": "<specific remediation steps and recommendations>"
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

                        PROCESS:
                        1. READ the requirement file from requirement/ directory
                        2. READ all evidence files from evidence/ directory
                        3. For EACH config rule, determine status based on evidence
                        4. For EACH config rule, include:
                           - status: COMPLIANT/NON_COMPLIANT/NOT_APPLICABLE
                           - details: detailed explanation of the assessment
                           - fetched_evidences: array of evidence file names that were analyzed
                           - remediation: specific steps to fix non-compliant items or maintain compliance
                        5. Calculate compliance metrics
                        6. CREATE audit_result/ directory if needed
                        7. SAVE the JSON assessment to audit_result/{control_id.replace('.', '_')}_audit.json
                        8. RETURN ONLY the complete JSON object - no extra text""",
            server_names=["filesystem"],
        )
        
        async with auditor_agent:
            # Use Groq for the audit process
            llm = await auditor_agent.attach_llm(GroqAugmentedLLM)
            
            print("🔍 Starting compliance audit...")
            
            try:
                audit_response = await llm.generate_str(
                    f"""Perform PCI DSS compliance audit for control {control_id}:

                        1. Read requirement/{control_id.replace('.', '_')}.json to get requirement text and config_rules list
                        2. Read all files in evidence/ directory to get AWS Config rule evaluation results
                        3. For each config rule in the requirement file:
                        - Analyze the corresponding evidence
                        - Determine status: COMPLIANT/NON_COMPLIANT/NOT_APPLICABLE
                        - Provide detailed explanation
                        - List the evidence files that were analyzed for this rule
                        - Provide specific remediation steps for non-compliant items or maintenance recommendations for compliant items
                        4. Calculate compliance metrics
                        5. Save complete JSON assessment to audit_result/ directory
                        6. Return the structured JSON assessment

                        IMPORTANT: For each rule assessment, include:
                        - status: compliance status
                        - details: detailed explanation
                        - fetched_evidences: array of evidence file names analyzed
                        - remediation: specific remediation steps and recommendations

                        Return ONLY the JSON object - no additional text."""
                )
                
                compliance_result = clean_response(audit_response)
                print(f"✅ Compliance audit completed")
                
                audit_file_path = f"audit_result/{control_id.replace('.', '_')}_audit.json"
                
                if os.path.exists(audit_file_path):
                    # Try to validate the JSON file
                    try:
                        with open(audit_file_path, 'r') as f:
                            json.load(f)  # Just validate it's valid JSON
                        print(f"✅ Valid audit result file created: {audit_file_path}")
                        return True
                    except json.JSONDecodeError:
                        print(f"❌ Invalid JSON in audit file: {audit_file_path}")
                        return False
                else:
                    print(f"❌ Audit result file not created: {audit_file_path}")
                    return False
                
            except Exception as e:
                print(f"❌ Compliance audit failed: {e}")
                return False
            
async def upload_and_process_audit_result(control_id, aws_account_id='aws-account-001'):
    """Upload audit_result.json and determine compliance status using MCP agent"""
    
    async with app.run() as agent_app:
        context = agent_app.context
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
        
        # Create specialized agent for processing audit results
        audit_processor_agent = Agent(
            name="audit_result_processor",
            instruction=f"""You are an audit result processor and database updater. Your tasks:
                        
                        1. READ the audit result file from audit_result/ directory:
                        - Look for file named {control_id.replace('.', '_')}_audit.json
                        - Read the complete JSON content
                        
                        2. EXTRACT compliance information:
                        - Get the compliance_summary section
                        - Extract the compliance_rate value (like "100%" or "85%")
                        
                        3. DETERMINE compliance status:
                        - If compliance_rate is exactly "100%" -> status = "compliant"
                        - If compliance_rate is anything else (99%, 85%, 0%, etc.) -> status = "non_compliant"
                        
                        4. UPDATE the database using SQL:
                        - Execute UPDATE statement on requirement_status table
                        - Set audit_result column = the complete JSON object (properly escaped for SQL)
                        - Set status column = determined status ("compliant" or "non_compliant")
                        - Set last_evaluated = current timestamp
                        - Set updated_at = current timestamp
                        - WHERE control_id = '{control_id}' AND aws_account_id = '{aws_account_id}'
                        
                        5. EXAMPLE SQL UPDATE format:
                        UPDATE requirement_status 
                        SET 
                            audit_result = '{{json content here}}',
                            status = 'compliant',
                            last_evaluated = NOW(),
                            updated_at = NOW()
                        WHERE control_id = '{control_id}' AND aws_account_id = '{aws_account_id}';
                        
                        6. RETURN status:
                        - Return "SUCCESS: Updated status to [compliant/non_compliant]" if database update completed
                        - Return "FAILED: [reason]" if any step failed
                        
                        IMPORTANT:
                        - Only 100% compliance rate means "compliant"
                        - Everything else means "non_compliant"
                        - Properly escape JSON for SQL insertion
                        - Use single quotes around JSON string in SQL
                        - Always update timestamps to current time""",
            server_names=["supabase", "filesystem"],
        )
        
        async with audit_processor_agent:
            llm = await audit_processor_agent.attach_llm(BedrockAugmentedLLM)
            
            print(f"📤 Processing audit result for control {control_id}...")
            
            try:
                # Ask agent to process the audit result file and update database
                process_response = await llm.generate_str(
                    f"""Process audit result and update database for control {control_id}:

                        Step 1: Read audit_result/{control_id.replace('.', '_')}_audit.json file
                        Step 2: Extract compliance_rate from compliance_summary section
                        Step 3: Determine status:
                        - compliance_rate = "100%" -> status = "compliant"  
                        - compliance_rate = anything else -> status = "non_compliant"
                        Step 4: Execute SQL UPDATE on requirement_status table:
                        - Set audit_result = complete JSON (properly escaped)
                        - Set status = determined status
                        - Set last_evaluated = NOW()
                        - Set updated_at = NOW()
                        - WHERE control_id = '{control_id}' AND aws_account_id = '{aws_account_id}'
                        
                        Return "SUCCESS: Updated status to [status]" or "FAILED: [reason]" """
                )
                
                result = clean_response(process_response)
                print(f"📊 Audit result processing: {result}")
                
                # Check if agent reports success
                if "SUCCESS" in result.upper():
                    print(f"✅ Audit result uploaded and status updated for {control_id}")
                    return True
                else:
                    print(f"❌ Audit result processing failed for {control_id}")
                    print(f"   Response: {result}")
                    return False
                
            except Exception as e:
                print(f"❌ Audit result processing failed: {e}")
                return False
                
async def main():
    print("🚀 PCI DSS Compliance Auditor\n")
    
    parser = argparse.ArgumentParser(description='Fetch requirement data and perform compliance audit')
    parser.add_argument('id', help='Control ID (e.g., 1.2.5)')
    parser.add_argument('--aws-account', default='aws-account-001', help='AWS Account ID')
    args = parser.parse_args()
    
    try:
        # Step 1: Fetch requirement data
        print("=" * 50)
        print("STEP 1: FETCHING REQUIREMENT DATA")
        print("=" * 50)
        
        req_fetch_result = await fetch_requirement_data(args.id)
        
        if req_fetch_result:
            print(f"✅ Requirement fetched successfully")
            
            # Step 2: Fetch evidence data (placeholder)
            print("\n" + "=" * 50)
            print("STEP 2: FETCHING EVIDENCE DATA")
            print("=" * 50)
            
            evidence_fetch_result = await fetch_evidence_data()
            
            if evidence_fetch_result:
                print("✅ Evidence data ready")
                
                # Step 3: Perform compliance audit (generates audit_result.json)
                print("\n" + "=" * 50)
                print("STEP 3: PERFORMING COMPLIANCE AUDIT")
                print("=" * 50)
                
                compliance_result = await check_compliance(args.id)
                
                if compliance_result:
                    print("✅ Compliance audit completed - audit_result.json generated")
                    
                    # Step 4: NEW - Upload audit result and update status
                    print("\n" + "=" * 50)
                    print("STEP 4: UPLOADING AUDIT RESULT TO DATABASE")
                    print("=" * 50)
                    
                    upload_result = await upload_and_process_audit_result(args.id, args.aws_account)
                    
                    if upload_result:
                        print("✅ Audit result uploaded and status updated")
                        final_status = True
                    else:
                        print("❌ Failed to upload audit result")
                        final_status = False
                        
                else:
                    print("❌ Compliance audit failed")
                    final_status = False
                
                # Final summary
                print(f"\n🎯 FINAL RESULT:")
                if final_status:
                    print(f"✅ Complete audit workflow successful for control {args.id}")
                else:
                    print(f"❌ Audit workflow failed for control {args.id}")
                
                # Step 5: Cleanup for next run
                print("\n" + "=" * 50)
                print("STEP 5: CLEANING UP FOR NEXT RUN")
                print("=" * 50)
                cleanup_result = cleanup_folders()
                
                return 0 if final_status else 1
                
            else:
                print("❌ Evidence fetch failed")
                return 1
        else:
            print("❌ Requirement fetch failed")
            return 1
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
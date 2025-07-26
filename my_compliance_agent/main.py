
import asyncio
import os
import argparse
import re
import json
import shutil
import glob
import boto3
from botocore.exceptions import ClientError
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
                    "KB_INCLUSION_TAG_KEY": "mcp-multirag-kb",
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
        # default_model="claude-3-7-sonnet-20250219",
    ),
    google=GoogleSettings(
        api_key=os.getenv("GOOGLE_API"),
        vertexai= False,
        default_model="gemini-2.5-flash"        
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
        
        # Clean evidence/ folder
        if os.path.exists("evidence"):
            audit_files = glob.glob("evidence/*")
            for file_path in audit_files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted_files.append(f"{file_path}/ (directory)")
            
            print(f"✅ Cleaned evidence/ folder ({len([f for f in audit_files if not os.path.exists(f)])} items deleted)")
        else:
            print("📁 evidence/ folder doesn't exist")        
        #     # Clean audit_result/ folder
        # if os.path.exists("audit_result"):
        #     audit_files = glob.glob("audit_result/*")
        #     for file_path in audit_files:
        #         if os.path.isfile(file_path):
        #             os.remove(file_path)
        #             deleted_files.append(file_path)
        #         elif os.path.isdir(file_path):
        #             shutil.rmtree(file_path)
        #             deleted_files.append(f"{file_path}/ (directory)")
            
        #     print(f"✅ Cleaned audit_result/ folder ({len([f for f in audit_files if not os.path.exists(f)])} items deleted)")
        # else:
        #     print("📁 audit_result/ folder doesn't exist")
        
        # Create directories if they don't exist
        os.makedirs("requirement", exist_ok=True)
        os.makedirs("evidence", exist_ok=True)
        
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
            instruction=f"""Create JSON file for control {control_id}.

            1. Get requirement: SELECT requirement FROM pci_dss_controls WHERE control_id = '{control_id}';
            2. Get config rules: SELECT config_rules FROM pci_aws_config_rule_mappings WHERE control_id = '{control_id}';
            3. Save as requirement/{control_id.replace('.', '_')}.json with this structure:
            {{
                "control_id": "{control_id}",
                "requirement": "<requirement_text>",
                "config_rules": <config_rules_array>
            }}
            4. Return: "SUCCESS: Created file with X config rules" """,
            server_names=["supabase", "filesystem"],
        )
        
        async with data_agent:
            llm = await data_agent.attach_llm(AnthropicAugmentedLLM)
            
            print("📋 Getting requirement...")
            await asyncio.sleep(5)

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
        
def fetch_evidence_data_direct(control_id):
    """Direct Python evidence collection - Fast and reliable"""
    print("🔧 Direct Evidence Collection (Fast & Reliable)")
    print("=" * 50)
    
    # Build requirement file path
    req_file_path = f"requirement/{control_id.replace('.', '_')}.json"
    
    # Read config rules from requirement file
    try:
        if not os.path.exists(req_file_path):
            print(f"❌ Requirement file not found: {req_file_path}")
            return False
            
        with open(req_file_path, 'r') as f:
            data = json.load(f)
        
        config_rules = data.get('config_rules', [])
        rule_names = []
        
        for rule in config_rules:
            if isinstance(rule, dict) and 'rule_name' in rule:
                rule_names.append(rule['rule_name'])
        
        print(f"📋 Found {len(rule_names)} config rules in {control_id}")
        
        if not rule_names:
            print(f"❌ No config rules found in {req_file_path}")
            return False
        
    except Exception as e:
        print(f"❌ Error reading requirement file: {e}")
        return False
    
    # Check AWS credentials
    try:
        session = boto3.Session()
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS credentials valid - Account: {identity['Account']}")
    except Exception as e:
        print(f"❌ AWS credentials issue: {e}")
        return False
    
    # Connect to AWS Config
    try:
        config_client = session.client('config')
        print("✅ Connected to AWS Config")
        
    except Exception as e:
        print(f"❌ Failed to connect to AWS Config: {e}")
        return False
    
    # Collect evidence for each rule
    all_evidence = {}
    success_count = 0
    error_count = 0
    
    print(f"\n🔍 Querying {len(rule_names)} AWS Config rules...")
    
    for i, rule_name in enumerate(rule_names, 1):
        try:
            print(f"   {i}/{len(rule_names)}: {rule_name}...", end="")
            
            compliance_details = config_client.get_compliance_details_by_config_rule(
                ConfigRuleName=rule_name
            )
            
            all_evidence[rule_name] = compliance_details
            success_count += 1
            print(" ✅")
            
        except ClientError as e:
            all_evidence[rule_name] = {"error": str(e)}
            error_count += 1
            if 'NoSuchConfigRuleException' in str(e):
                print(" ❌ (rule not found)")
            else:
                print(f" ❌ ({str(e)[:50]}...)")
        except Exception as e:
            all_evidence[rule_name] = {"error": str(e)}
            error_count += 1
            print(f" ❌ ({str(e)[:50]}...)")
    
    # Save evidence
    os.makedirs("evidence", exist_ok=True)
    evidence_file = "evidence/all_evidence.json"
    
    try:
        with open(evidence_file, 'w') as f:
            json.dump(all_evidence, f, indent=2, default=str)
        
        print(f"\n📊 Evidence Collection Summary:")
        print(f"   ✅ Successful: {success_count}")
        print(f"   ❌ Failed: {error_count}")
        print(f"   📈 Success rate: {(success_count/(success_count+error_count))*100:.1f}%")
        print(f"   💾 Saved to: {evidence_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving evidence file: {e}")
        return False

async def check_compliance(control_id, aws_account_id='aws-account-001'):
    """Perform audition and return compliance result - UPDATED to process ALL rules"""
    
    async with app.run() as agent_app:
        context = agent_app.context
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
                
        # Create agent with very specific instructions for COMPLETE analysis
        auditor_agent = Agent(
            name="pci_auditor",
            instruction=f"""Expert PCI DSS compliance auditor. CRITICAL: You must analyze EVERY SINGLE config rule individually.

        MANDATORY PROCESS:
        1. Query KB for PCI DSS {control_id} requirements and implementation guidance
        2. Read requirement/{control_id.replace('.', '_')}.json and evidence/all_evidence.json files
        3. ANALYZE EACH AND EVERY config rule individually - DO NOT SKIP ANY
        4. For EACH rule, determine COMPLIANT/NON_COMPLIANT/NOT_APPLICABLE with detailed reasoning
        5. Save JSON to audit_result/{control_id.replace('.', '_')}_audit.json

        CRITICAL REQUIREMENTS:
        - EVERY config rule from the requirement file MUST appear in compliance_assessment
        - Do NOT summarize or group rules together
        - Do NOT mark rules as "not applicable" unless you have specific evidence they don't apply
        - Process rules individually, one by one
        - If evidence shows "error" or "NoSuchConfigRuleException", mark as NOT_APPLICABLE
        - If evidence shows actual compliance data, analyze it properly

        OUTPUT JSON FORMAT (EVERY RULE MUST BE INCLUDED):
        {{
            "control_id": "{control_id}",
            "requirement": "<from requirement file>",
            "compliance_assessment": {{
                "<rule_name_1>": {{
                    "status": "COMPLIANT|NON_COMPLIANT|NOT_APPLICABLE",
                    "evidence": "<specific technical findings for this rule>",
                    "analysis": "<PCI DSS compliance reasoning for this specific rule>",
                    "recommendations": "<specific remediation if needed>"
                }},
                "<rule_name_2>": {{
                    "status": "COMPLIANT|NON_COMPLIANT|NOT_APPLICABLE",
                    "evidence": "<specific technical findings for this rule>",
                    "analysis": "<PCI DSS compliance reasoning for this specific rule>",
                    "recommendations": "<specific remediation if needed>"
                }},
                "... CONTINUE FOR ALL RULES - DO NOT STOP EARLY ..."
            }},
            "compliance_summary": {{
                "compliant_rules": <number>,
                "non_compliant_rules": <number>,
                "not_applicable_rules": <number>,
                "total_rules_in_scope": <number>,
                "compliance_rate": "<percentage>"
            }}
        }}

        VERIFICATION: Count the rules in requirement file and ensure compliance_assessment has the SAME number of entries.""",
            server_names=["filesystem", "bedrock_kb"],
        )
        
        async with auditor_agent:
            llm = await auditor_agent.attach_llm(AnthropicAugmentedLLM)
            
            print("🔍 Starting compliance audit...")
            
            try:
                audit_response = await llm.generate_str(
                    f"""Perform COMPLETE PCI DSS compliance audit for control {control_id}:

                        STEP 1: Read requirement/{control_id.replace('.', '_')}.json
                        - Extract the complete list of config_rules
                        - Count how many rules there are total
                        
                        STEP 2: Read evidence/all_evidence.json
                        - Find evidence for each config rule
                        
                        
                        STEP 3: ANALYZE EVERY SINGLE RULE (DO NOT SKIP ANY)
                        For each config rule in the requirement file:
                        a) Look up its evidence in all_evidence.json
                        b) If evidence has "error" or "NoSuchConfigRuleException" → NOT_APPLICABLE
                        c) If evidence has "EvaluationResults" → analyze ComplianceType
                        d) Determine status and provide specific analysis
                        e) Add to compliance_assessment with detailed reasoning
                        
                        STEP 4: Verify completeness
                        - Ensure compliance_assessment contains ALL rules from requirement file
                        - Calculate accurate compliance metrics
                        
                        STEP 5: Save complete JSON assessment to audit_result/ directory
                        
                        CRITICAL: The compliance_assessment section must contain an entry for EVERY config rule from the requirement file. Do not truncate or summarize.
                        
                        Return ONLY the complete JSON object - no additional text."""
                )
                
                compliance_result = clean_response(audit_response)
                print(f"✅ Compliance audit completed")
                
                audit_file_path = f"audit_result/{control_id.replace('.', '_')}_audit.json"
                
                if os.path.exists(audit_file_path):
                    # Validate the JSON file and check completeness
                    try:
                        with open(audit_file_path, 'r') as f:
                            audit_data = json.load(f)
                        
                        # Check if all rules were analyzed
                        req_file_path = f"requirement/{control_id.replace('.', '_')}.json"
                        if os.path.exists(req_file_path):
                            with open(req_file_path, 'r') as f:
                                req_data = json.load(f)
                            
                            total_rules = len(req_data.get('config_rules', []))
                            analyzed_rules = len(audit_data.get('compliance_assessment', {}))
                            
                            print(f"📊 Rules analysis: {analyzed_rules}/{total_rules} rules processed")
                            
                            if analyzed_rules < total_rules:
                                print(f"⚠️  Warning: Only {analyzed_rules} out of {total_rules} rules were analyzed")
                            else:
                                print(f"✅ All {total_rules} rules were analyzed")
                        
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
       
       # Detailed but action-focused agent
       audit_processor_agent = Agent(
           name="audit_result_processor",
           instruction=f"""Database updater for audit results. Execute these specific actions:

                       REQUIRED ACTIONS:
                       1. READ file: audit_result/{control_id.replace('.', '_')}_audit.json
                       2. EXTRACT: compliance_rate from compliance_summary section
                       3. DETERMINE status: compliance_rate="100%" → "compliant", otherwise → "non_compliant"
                       4. EXECUTE SQL UPDATE on requirement_status table:
                          - audit_result = complete JSON (escape quotes properly)
                          - evidence = complete JSON file named all_evidence.json in evidence/ directory
                          - status = determined status
                          - last_evaluated = NOW()
                          - updated_at = NOW() 
                          - WHERE control_id = '{control_id}' AND aws_account_id = '{aws_account_id}'
                       5. RETURN: "SUCCESS: Updated status to [status]" or "FAILED: [error]"

                       IMPORTANT REQUIREMENTS:
                       - Only "100%" compliance_rate means "compliant"
                       - All other values (99%, 62.5%, etc.) mean "non_compliant" 
                       - Properly escape JSON content for SQL insertion
                       - Use single quotes around JSON in SQL
                       - Execute the UPDATE immediately - do not just describe it""",
           server_names=["supabase", "filesystem"],
       )
       
       async with audit_processor_agent:
           llm = await audit_processor_agent.attach_llm(AnthropicAugmentedLLM)
           
           print(f"📤 Processing audit result for control {control_id}...")
           
           try:
               # Specific but direct instruction
               process_response = await llm.generate_str(
                   f"""Execute database update for control {control_id}:

                       1. Read audit_result/{control_id.replace('.', '_')}_audit.json
                       2. Extract compliance_rate from compliance_summary section
                       3. Determine status: "100%" = "compliant", else = "non_compliant"
                       4. Execute SQL UPDATE on requirement_status table:
                          SET audit_result=JSON, status=determined_status, last_evaluated=NOW(), updated_at=NOW()
                          WHERE control_id='{control_id}' AND aws_account_id='{aws_account_id}'
                       5. Return SUCCESS or FAILED
                       
                       Execute the SQL UPDATE now - do not explain, just do it."""
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
    print("🚀 PCI DSS Compliance Auditor (Updated with Direct Evidence Collection)\n")
    
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
            
            # Delay after Step 1
            print("⏳ Waiting 10 seconds before evidence collection...")
            
            # Step 2: Fetch evidence data using DIRECT approach (fast & reliable)
            print("\n" + "=" * 50)
            print("STEP 2: FETCHING EVIDENCE DATA (DIRECT METHOD)")
            print("=" * 50)
            
            evidence_fetch_result = fetch_evidence_data_direct(args.id)
            
            if evidence_fetch_result:
                print("✅ Evidence data ready")
                
                # Delay after Step 2
                print("⏳ Waiting 10 seconds before compliance audit...")
                
                # Step 3: Perform compliance audit (generates audit_result.json)
                print("\n" + "=" * 50)
                print("STEP 3: PERFORMING COMPLIANCE AUDIT")
                print("=" * 50)
                
                await asyncio.sleep(20)

                compliance_result = await check_compliance(args.id)
                
                if compliance_result:
                    print("✅ Compliance audit completed - audit_result.json generated")
                    
                    # Delay before Step 4
                    print("⏳ Waiting 10 seconds before database upload...")
                    await asyncio.sleep(20)
                    
                    # Step 4: Upload audit result and update status
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
                cleanup = cleanup_folders()
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
    
import asyncio
import os
import json
import boto3
from mcp_agent.app import MCPApp
from mcp_agent.config import (
    Settings,
    LoggerSettings,
    MCPSettings,
    MCPServerSettings,
    GoogleSettings,
)
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simplified settings - ONLY filesystem, no Docker needed
settings = Settings(
    execution_engine="asyncio",
    logger=LoggerSettings(type="console", level="info"),
    mcp=MCPSettings(
        servers={
            "filesystem": MCPServerSettings(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem"],
            ),
        }
    ),
    google=GoogleSettings(
        api_key=os.getenv("GOOGLE_API"),
        vertexai=False,
        default_model="gemini-2.5-flash"        
    ),
)

app = MCPApp(name="No Docker Evidence Fetcher", settings=settings)

def check_aws_credentials():
    """Check if AWS credentials are available"""
    try:
        session = boto3.Session()
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS credentials valid - Account: {identity['Account']}")
        return True
    except Exception as e:
        print(f"❌ AWS credentials issue: {e}")
        print("   Make sure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set")
        return False

def collect_evidence_direct():
    """Direct Python evidence collection without Docker"""
    print("🔧 Direct Evidence Collection (No Docker)")
    print("=" * 50)
    
    # Read config rules from requirement file
    try:
        with open("requirement/10_2_1_2.json", 'r') as f:
            data = json.load(f)
        
        config_rules = data.get('config_rules', [])
        rule_names = []
        
        for rule in config_rules:
            if isinstance(rule, dict) and 'rule_name' in rule:
                rule_names.append(rule['rule_name'])
        
        print(f"📋 Found {len(rule_names)} config rules to query")
        
    except Exception as e:
        print(f"❌ Error reading requirement file: {e}")
        return False
    
    # Connect to AWS Config
    try:
        session = boto3.Session()
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
            
        except Exception as e:
            all_evidence[rule_name] = {"error": str(e)}
            error_count += 1
            print(f" ❌ ({str(e)[:50]}...)")
    
    # Save evidence
    os.makedirs("evidence", exist_ok=True)
    evidence_file = "evidence/all_evidence.json"
    
    with open(evidence_file, 'w') as f:
        json.dump(all_evidence, f, indent=2, default=str)
    
    print(f"\n📊 Evidence Collection Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {error_count}")
    print(f"   📈 Success rate: {(success_count/(success_count+error_count))*100:.1f}%")
    print(f"   💾 Saved to: {evidence_file}")
    
    return True

async def collect_evidence_with_agent():
    """Use MCP agent but with direct boto3 instructions (no Docker)"""
    
    async with app.run() as agent_app:
        context = agent_app.context
        context.config.mcp.servers["filesystem"].args.extend([os.getcwd()])
        
        print("⏳ Waiting for filesystem server...")
        await asyncio.sleep(3)

        # Evidence collector that uses direct boto3 (no MCP aws-resources)
        evidence_collector = Agent(
            name="direct_boto3_collector",
            instruction="""Evidence collector using direct boto3 calls (no Docker MCP server needed).
            
            Your tasks:
            1. Read requirement/10_2_1_2.json 
            2. Extract rule_name from each config_rules object
            3. Use direct boto3 to query AWS Config for each rule
            4. Save evidence to evidence/all_evidence.json
            5. Report results
            
            IMPORTANT: Use this exact Python code pattern:
            
            import boto3
            session = boto3.Session()
            config_client = session.client('config')
            
            # Don't use MCP aws-resources - use direct boto3
            for rule_name in extracted_rule_names:
                try:
                    result = config_client.get_compliance_details_by_config_rule(ConfigRuleName=rule_name)
                    evidence[rule_name] = result
                except Exception as e:
                    evidence[rule_name] = {"error": str(e)}
            """,
            server_names=["filesystem"],  # Only filesystem, no aws-resources
        )
        
        async with evidence_collector:
            llm = await evidence_collector.attach_llm(GoogleAugmentedLLM)
            
            print("🤖 Using MCP agent with direct boto3...")
            
            try:
                response = await llm.generate_str(
                    """Collect AWS Config evidence using direct boto3:
                    
                    1. Read requirement/10_2_1_2.json file
                    2. Extract rule_name values from config_rules array (each is an object)
                    3. Execute this Python code directly (no MCP server needed):
                    
                    import boto3
                    import json
                    
                    # Read requirement file
                    with open('requirement/10_2_1_2.json', 'r') as f:
                        data = json.load(f)
                    
                    rule_names = [rule['rule_name'] for rule in data['config_rules']]
                    
                    # Direct AWS Config queries
                    session = boto3.Session()
                    config_client = session.client('config')
                    all_evidence = {}
                    
                    for rule_name in rule_names:
                        try:
                            compliance_details = config_client.get_compliance_details_by_config_rule(
                                ConfigRuleName=rule_name
                            )
                            all_evidence[rule_name] = compliance_details
                        except Exception as e:
                            all_evidence[rule_name] = {"error": str(e)}
                    
                    # Save to evidence directory
                    import os
                    os.makedirs('evidence', exist_ok=True)
                    with open('evidence/all_evidence.json', 'w') as f:
                        json.dump(all_evidence, f, indent=2, default=str)
                    
                    4. Return success confirmation with count of rules processed
                    """
                )
                
                print(f"📋 Agent response: {response}")
                
                # Check if evidence file was created
                evidence_file = "evidence/all_evidence.json"
                if os.path.exists(evidence_file):
                    with open(evidence_file, 'r') as f:
                        evidence_data = json.load(f)
                    
                    print(f"✅ Agent successfully created evidence file!")
                    print(f"📊 Rules processed: {len(evidence_data)}")
                    return True
                else:
                    print("❌ Agent did not create evidence file")
                    return False
                
            except Exception as e:
                print(f"❌ Agent evidence collection failed: {e}")
                return False

def main():
    print("🚀 Evidence Collection Test (No Docker Required)")
    print("=" * 60)
    
    # Check AWS credentials
    if not check_aws_credentials():
        print("\n❌ AWS credentials not configured properly")
        return 1
    
    # Give user choice
    print(f"\nChoose collection method:")
    print(f"1. Direct Python (recommended)")
    print(f"2. MCP Agent with direct boto3")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    try:
        if choice == "1":
            print(f"\n{'='*50}")
            print("DIRECT PYTHON EVIDENCE COLLECTION")
            print(f"{'='*50}")
            success = collect_evidence_direct()
            
        elif choice == "2":
            print(f"\n{'='*50}")
            print("MCP AGENT EVIDENCE COLLECTION")
            print(f"{'='*50}")
            success = asyncio.run(collect_evidence_with_agent())
            
        else:
            print("Invalid choice")
            return 1
        
        if success:
            print(f"\n🎉 SUCCESS! Evidence collection completed")
            print(f"📁 Check evidence/all_evidence.json for results")
        else:
            print(f"\n❌ Evidence collection failed")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
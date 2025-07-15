import asyncio
import os
import argparse
import re
import json
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
        default_model="claude-3-haiku-20240307",
        # default_model="claude-sonnet-4-20250514",
    ),
    google=GoogleSettings(
        api_key=os.getenv("GOOGLE_API"),
        vertexai= False,
    # project: str | None = None
    # location: str | None = None
        default_model="gemini-2.0-flash"        
    ),
)

app = MCPApp(name="Table Finder", settings=settings)


def extract_table_names(response):
    """Extract table names from the SQL response"""
    try:
        # Look for the JSON data in the tool result
        if '"tablename"' in response:
            # Find all tablename values
            table_matches = re.findall(r'"tablename":"([^"]+)"', response)
            return table_matches
        elif '"table_name"' in response:
            # Alternative column name
            table_matches = re.findall(r'"table_name":"([^"]+)"', response)
            return table_matches
        else:
            return []
    except Exception as e:
        print(f"Error extracting table names: {e}")
        return []


async def get_table_names():
    """Get just the table names from the database"""
    
    async with app.run() as agent_app:
        
        # Create simple agent
        agent = Agent(
            name="table_finder",
            instruction="Execute SQL queries to find table names.",
            server_names=["supabase"],
        )
        
        async with agent:
            llm = await agent.attach_llm(GoogleAugmentedLLM)
            
            print("🔍 Getting table names from database...")
            
            # Add delay to avoid throttling based on previous patterns
            print("⏳ Waiting 10 seconds to avoid throttling...")
            await asyncio.sleep(10)
            
            try:
                # Simple query to get table names
                response = await llm.generate_str(
                    "Execute: SELECT * FROM pci_dss_controls WHERE control_id='1.2.5';"
                )
                
                print(f"🔍 Raw LLM Response:")
                print(f"   {response}")
                print(f"   Length: {len(response)} characters")
                
                # Extract table names from response
                if response:
                
                    return True
                
            except Exception as e:
                print(f"❌ Failed to get table names: {str(e)}")
                return []


async def main():
    print("🚀 Fetching Table Names\n")
    
    try:
        table_names = await get_table_names()
        
        if table_names:
            print("✅ Tables found:")
            print("=" * 30)
            for i, table in enumerate(table_names, 1):
                print(f"{i}. {table}")
            
            print(f"\n📊 Total tables: {len(table_names)}")
            print(f"📋 Table list: {table_names}")
            
        else:
            print("❌ No tables found or query failed")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
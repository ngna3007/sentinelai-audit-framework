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
    BedrockSettings,
)
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_bedrock import BedrockAugmentedLLM

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
                    "--project-ref=<rqknorhfhwrdoahjtsce>",
                ],
                env={"SUPABASE_ACCESS_TOKEN": os.getenv("SUPABASE_ACCESS_TOKEN", "")},
            ),
        }
    ),
    bedrock=BedrockSettings(
        aws_region="ap-southeast-2",
        profile="default",
        # default_model="anthropic.claude-3-5-sonnet-20241022-v2:0",
        default_model="arn:aws:bedrock:ap-southeast-2:123012555573:inference-profile/apac.anthropic.claude-3-sonnet-20240229-v1:0",
    ),
)

app = MCPApp(name="Simple Test System", settings=settings)


async def test_connections():
    """Test both Supabase and Bedrock LLM connections"""
    async with app.run() as agent_app:
        logger = agent_app.logger

        # Test 1: Basic agent creation and LLM attachment
        logger.info("🧪 Testing agent creation and LLM attachment...")
        test_agent = Agent(
            name="test_agent",
            instruction="You are a simple test agent. Respond with 'LLM CONNECTION SUCCESSFUL' when prompted.",
            server_names=["supabase"],
        )

        async with test_agent:
            try:
                # Test 2: LLM connection
                logger.info("🧪 Testing Bedrock LLM connection...")
                llm = await test_agent.attach_llm(BedrockAugmentedLLM)
                logger.info("✅ LLM attached successfully")

                # Test 3: Simple LLM response
                logger.info("🧪 Testing LLM response generation...")
                response = await llm.generate_str(
                    "Please respond with exactly: LLM CONNECTION SUCCESSFUL"
                )
                logger.info(f"✅ LLM Response: {response}")

                # Test 4: Supabase connection (if LLM works)
                logger.info("🧪 Testing Supabase database connection...")
                db_response = await llm.generate_str("""
                Test the database connection by running a simple query like:
                SELECT 1 as test_connection;
                
                If successful, respond with: DATABASE CONNECTION SUCCESSFUL
                If failed, respond with: DATABASE CONNECTION FAILED
                """)
                logger.info(f"✅ Database test: {db_response}")

                return {
                    "success": True,
                    "llm_connection": "SUCCESS",
                    "llm_response": response.strip(),
                    "database_test": db_response.strip(),
                    "message": "All connections tested successfully",
                }

            except Exception as e:
                logger.error(f"❌ Connection test failed: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "Connection test failed",
                }


async def main():
    try:
        result = await test_connections()
        print(json.dumps(result, indent=2))
        return 0 if result["success"] else 1

    except Exception as e:
        print(
            json.dumps(
                {"success": False, "error": str(e), "message": "System test failed"},
                indent=2,
            )
        )
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)

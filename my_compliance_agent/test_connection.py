import asyncio
import os
import json
import boto3
from botocore.exceptions import ClientError
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
        profile="my-bedrock-profile",
        default_model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    ),
)

app = MCPApp(name="Simple Test System", settings=settings)


async def llm_generate_with_retry(llm, prompt, max_retries=2, base_delay=5):
    """Generate LLM response with targeted handling for Bedrock on-demand throttling"""
    for attempt in range(max_retries):
        try:
            return await llm.generate_str(prompt)
        except Exception as e:
            error_str = str(e).lower()

            if "throttling" in error_str or "too many requests" in error_str:
                if attempt < max_retries - 1:
                    delay = base_delay * (2**attempt)  # Exponential backoff
                    print(
                        f"⏳ Bedrock throttling detected (likely on-demand pricing tier), waiting {delay}s before retry {attempt + 1}/{max_retries}"
                    )
                    await asyncio.sleep(delay)
                    continue
                else:
                    # Provide specific guidance for this known issue
                    bedrock_config_msg = (
                        "BEDROCK CONFIGURATION ISSUE: You're hitting rate limits with 'on-demand' pricing. "
                        "Switch to 'Inference Profiles' in your Bedrock model configuration for higher throughput. "
                        f"Original error: {str(e)}"
                    )
                    raise Exception(bedrock_config_msg)
            else:
                # Non-throttling error, re-raise immediately
                raise e

    raise Exception("Unexpected error in retry logic")


async def test_connections():
    """Test both Supabase and Bedrock LLM connections with throttling protection"""
    result = {
        "success": False,
        "llm_connection": None,
        "llm_response": None,
        "database_test": None,
        "supabase_connection": None,
        "errors": [],
        "warnings": [],
    }

    async with app.run() as agent_app:
        logger = agent_app.logger

        try:
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
                    result["llm_connection"] = "SUCCESS"

                    # Test 3: Simple LLM response with retry logic
                    logger.info("🧪 Testing LLM response generation...")
                    try:
                        response = await llm_generate_with_retry(
                            llm,
                            "Please respond with exactly: LLM CONNECTION SUCCESSFUL",
                            max_retries=3,
                            base_delay=2,
                        )
                        logger.info(f"✅ LLM Response: {response}")
                        result["llm_response"] = response.strip()
                    except Exception as e:
                        # Check if this is the known Bedrock configuration issue
                        error_str = str(e).lower()
                        if "bedrock configuration issue" in error_str:
                            result["errors"].append(str(e))
                            result["warnings"].append(
                                "💡 SOLUTION: Change Bedrock pricing from 'On-demand' to 'Inference Profiles' for higher rate limits"
                            )
                        else:
                            error_msg = f"LLM response failed after retries: {str(e)}"
                            result["errors"].append(error_msg)

                        logger.error(f"❌ LLM response failed: {str(e)}")
                        result["llm_response"] = "FAILED"

                    # Test 4: Supabase connection status
                    logger.info("🧪 Checking Supabase connection status...")

                    # Check if Supabase MCP server is connected (from logs)
                    supabase_token = os.getenv("SUPABASE_ACCESS_TOKEN", "")
                    if not supabase_token:
                        result["supabase_connection"] = "MISSING_TOKEN"
                        result["errors"].append(
                            "SUPABASE_ACCESS_TOKEN environment variable is missing"
                        )
                    elif "supabase: Up and running" in str(logger):
                        result["supabase_connection"] = "CONNECTED"
                    else:
                        result["supabase_connection"] = "UNKNOWN"
                        result["warnings"].append(
                            "Could not determine Supabase connection status from logs"
                        )

                    # Test 5: Database query (only if LLM response worked)
                    if result["llm_response"] and result["llm_response"] != "FAILED":
                        logger.info("🧪 Testing Supabase database connection...")
                        try:
                            db_response = await llm_generate_with_retry(
                                llm,
                                """Test the database connection by running a simple query like:
                                SELECT 1 as test_connection;
                                
                                If successful, respond with: DATABASE CONNECTION SUCCESSFUL
                                If failed, respond with: DATABASE CONNECTION FAILED""",
                                max_retries=2,
                                base_delay=3,
                            )
                            logger.info(f"✅ Database test: {db_response}")
                            result["database_test"] = (
                                db_response.strip()
                                if db_response.strip()
                                else "EMPTY_RESPONSE"
                            )
                        except Exception as e:
                            # Check if this is the known Bedrock configuration issue
                            error_str = str(e).lower()
                            if "bedrock configuration issue" in error_str:
                                result["errors"].append(str(e))
                                result["warnings"].append(
                                    "💡 SOLUTION: Change Bedrock pricing from 'On-demand' to 'Inference Profiles' for higher rate limits"
                                )
                            else:
                                error_msg = f"Database test failed: {str(e)}"
                                result["errors"].append(error_msg)

                            logger.error(f"❌ Database test failed: {str(e)}")
                            result["database_test"] = "FAILED"
                    else:
                        result["database_test"] = "SKIPPED_DUE_TO_LLM_FAILURE"

                    # Determine overall success
                    critical_failures = [
                        result["llm_connection"] != "SUCCESS",
                        result["llm_response"] == "FAILED",
                    ]

                    if any(critical_failures):
                        result["success"] = False
                        result["message"] = "Critical connection failures detected"
                    elif result["errors"]:
                        result["success"] = False
                        result["message"] = (
                            "Some tests failed but basic functionality works"
                        )
                    else:
                        result["success"] = True
                        result["message"] = "All connections tested successfully"

                except Exception as e:
                    error_msg = f"Agent/LLM setup failed: {str(e)}"
                    logger.error(f"❌ {error_msg}")
                    result["errors"].append(error_msg)
                    result["message"] = "Failed to set up agent or LLM"

        except Exception as e:
            error_msg = f"App initialization failed: {str(e)}"
            logger.error(f"❌ {error_msg}")
            result["errors"].append(error_msg)
            result["message"] = "Failed to initialize MCP app"

    return result


async def main():
    print("🚀 Starting connection tests with throttling protection...\n")

    try:
        result = await test_connections()

        # Enhanced result display
        print("=" * 70)
        print("CONNECTION TEST RESULTS")
        print("=" * 70)

        # Status summary
        print(f"Overall Success: {'✅ YES' if result['success'] else '❌ NO'}")
        print(
            f"LLM Connection: {'✅' if result['llm_connection'] == 'SUCCESS' else '❌'} {result['llm_connection']}"
        )
        print(
            f"LLM Response: {'✅' if result['llm_response'] not in ['FAILED', None] else '❌'} {result['llm_response']}"
        )
        print(
            f"Supabase Status: {'✅' if result['supabase_connection'] == 'CONNECTED' else '⚠️'} {result['supabase_connection']}"
        )
        print(
            f"Database Test: {'✅' if result['database_test'] not in ['FAILED', 'SKIPPED_DUE_TO_LLM_FAILURE', None] else '❌'} {result['database_test']}"
        )

        if result["errors"]:
            print(f"\n🚨 Errors ({len(result['errors'])}):")
            for i, error in enumerate(result["errors"], 1):
                print(f"  {i}. {error}")

        if result["warnings"]:
            print(f"\n💡 Configuration Recommendations ({len(result['warnings'])}):")
            for i, warning in enumerate(result["warnings"], 1):
                print(f"  {i}. {warning}")

        print(f"\n📝 Message: {result['message']}")

        # Full JSON output
        print("\n" + "=" * 70)
        print("DETAILED JSON OUTPUT")
        print("=" * 70)
        print(json.dumps(result, indent=2))

        return 0 if result["success"] else 1

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        print(
            json.dumps(
                {
                    "success": False,
                    "error": str(e),
                    "message": "System test failed with critical error",
                },
                indent=2,
            )
        )
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)

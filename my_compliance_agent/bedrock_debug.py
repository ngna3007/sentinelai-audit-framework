#!/usr/bin/env python3
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()


def test_direct_bedrock():
    """Test Bedrock directly with boto3 to verify model IDs work"""
    print("🔍 STEP 1: Testing direct Bedrock connection...")

    # Test with your exact profile and region
    session = boto3.Session(profile_name="my-bedrock-profile")
    bedrock = session.client("bedrock-runtime", region_name="ap-southeast-2")

    # Get all available models first
    bedrock_control = session.client("bedrock", region_name="ap-southeast-2")

    try:
        models = bedrock_control.list_foundation_models()
        print("✅ Bedrock connection successful")

        anthropic_models = [
            model
            for model in models["modelSummaries"]
            if model["providerName"] == "Anthropic"
        ]

        print(f"📋 Found {len(anthropic_models)} Anthropic models:")
        for model in anthropic_models:
            print(f"   - {model['modelId']} ({model['modelName']})")

        # Test each model
        print("\n🧪 Testing each model...")
        working_models = []

        for model in anthropic_models:
            model_id = model["modelId"]
            try:
                response = bedrock.converse(
                    modelId=model_id,
                    messages=[{"role": "user", "content": [{"text": "Hello"}]}],
                    inferenceConfig={"maxTokens": 10, "temperature": 0.1},
                )
                print(f"✅ {model_id} - WORKS")
                working_models.append(model_id)
            except Exception as e:
                print(f"❌ {model_id} - FAILED: {str(e)[:50]}...")

        return working_models

    except Exception as e:
        print(f"❌ Bedrock connection failed: {e}")
        return []


def inspect_bedrockaugmentedllm():
    """Try to inspect how BedrockAugmentedLLM works"""
    print("\n🔍 STEP 2: Inspecting BedrockAugmentedLLM class...")

    try:
        from mcp_agent.workflows.llm.augmented_llm_bedrock import BedrockAugmentedLLM

        # Check if it has any class attributes or defaults
        print(f"📁 BedrockAugmentedLLM class found")
        print(f"📁 Class: {BedrockAugmentedLLM}")

        # Try to inspect the class
        import inspect

        # Get the __init__ method signature
        init_signature = inspect.signature(BedrockAugmentedLLM.__init__)
        print(f"📋 __init__ parameters: {init_signature}")

        # Check for class attributes
        for attr in dir(BedrockAugmentedLLM):
            if not attr.startswith("_"):
                value = getattr(BedrockAugmentedLLM, attr)
                if isinstance(value, str) and "model" in attr.lower():
                    print(f"📋 Found model-related attribute: {attr} = {value}")

        # Try to find the source file
        source_file = inspect.getfile(BedrockAugmentedLLM)
        print(f"📁 Source file: {source_file}")

        return True

    except Exception as e:
        print(f"❌ Failed to inspect BedrockAugmentedLLM: {e}")
        return False


def test_bedrocksettings():
    """Test if BedrockSettings is working correctly"""
    print("\n🔍 STEP 3: Testing BedrockSettings configuration...")

    try:
        from mcp_agent.config import BedrockSettings

        # Create settings like in your code
        settings = BedrockSettings(
            aws_region="ap-southeast-2",
            profile="my-bedrock-profile",
            model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
        )

        print(f"✅ BedrockSettings created successfully")
        print(f"📋 Settings: {settings}")

        # Check all attributes
        for attr in dir(settings):
            if not attr.startswith("_"):
                value = getattr(settings, attr)
                if not callable(value):
                    print(f"   {attr}: {value}")

        return settings

    except Exception as e:
        print(f"❌ BedrockSettings failed: {e}")
        return None


def find_source_code():
    """Try to find and read the BedrockAugmentedLLM source code"""
    print("\n🔍 STEP 4: Looking for BedrockAugmentedLLM source code...")

    try:
        from mcp_agent.workflows.llm.augmented_llm_bedrock import BedrockAugmentedLLM
        import inspect

        source_file = inspect.getfile(BedrockAugmentedLLM)
        print(f"📁 Found source: {source_file}")

        # Try to read the source
        with open(source_file, "r") as f:
            content = f.read()

        # Look for model-related code
        lines = content.split("\n")
        model_lines = []

        for i, line in enumerate(lines):
            if any(
                keyword in line.lower() for keyword in ["model", "claude", "anthropic"]
            ):
                model_lines.append(f"{i + 1}: {line.strip()}")

        if model_lines:
            print("📋 Model-related code found:")
            for line in model_lines[:10]:  # Show first 10 matches
                print(f"   {line}")

        return content

    except Exception as e:
        print(f"❌ Could not read source: {e}")
        return None


if __name__ == "__main__":
    print("🚀 DEBUGGING BEDROCK MODEL IDENTIFIER ISSUE\n")

    # Step 1: Test direct Bedrock
    working_models = test_direct_bedrock()

    # Step 2: Inspect the class
    inspect_bedrockaugmentedllm()

    # Step 3: Test settings
    test_bedrocksettings()

    # Step 4: Find source code
    find_source_code()

    print(f"\n🎯 SUMMARY:")
    if working_models:
        print(f"✅ These model IDs work with direct boto3:")
        for model in working_models:
            print(f"   - {model}")
        print(f"\n💡 Use one of these in your BedrockSettings!")
    else:
        print(f"❌ No models work with direct boto3 - check AWS permissions!")

    print(
        f"\n🔧 Next step: Check BedrockAugmentedLLM source code to see how it uses model_id"
    )

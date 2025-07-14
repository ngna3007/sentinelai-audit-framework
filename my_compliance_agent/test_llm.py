#!/usr/bin/env python3
import boto3
import json


def test_bedrock_model():
    """Test Bedrock model connectivity with exact model IDs"""

    # Initialize session with your profile
    session = boto3.Session(profile_name="my-bedrock-profile")
    bedrock = session.client("bedrock-runtime", region_name="ap-southeast-2")

    # Test different model ID formats
    test_models = [
        "arn:aws:bedrock:ap-southeast-2:123012555573:inference-profile/apac.anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-7-sonnet-20240620-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "anthropic.claude-3-5-sonnet-20241022-v2:0",
    ]

    for model_id in test_models:
        try:
            print(f"\n🧪 Testing model: {model_id}")

            response = bedrock.converse(
                modelId=model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"text": "Hello, can you respond with just 'SUCCESS'?"}
                        ],
                    }
                ],
                inferenceConfig={"maxTokens": 10, "temperature": 0.1},
            )

            # Extract response
            response_text = response["output"]["message"]["content"][0]["text"]
            print(f"✅ SUCCESS: {model_id}")
            print(f"   Response: {response_text}")
            return model_id  # Return the working model ID

        except Exception as e:
            print(f"❌ FAILED: {model_id}")
            print(f"   Error: {str(e)[:100]}...")

    print(f"\n❌ No working model found!")
    return None


if __name__ == "__main__":
    working_model = test_bedrock_model()
    if working_model:
        print(f"\n🎯 Use this model ID in your code: {working_model}")

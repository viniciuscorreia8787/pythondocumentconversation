import boto3
import json

from botocore.exceptions import ClientError

def call_genai_text(input_prompt):
    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Titan Text Premier.
    model_id = "amazon.titan-text-premier-v1:0"

    # Format the request payload using the model's native structure.
    native_request = {
        "inputText": input_prompt,
        "textGenerationConfig": {
            "maxTokenCount": 512,
            "temperature": 0.5,
        },
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["results"][0]["outputText"]
    return response_text
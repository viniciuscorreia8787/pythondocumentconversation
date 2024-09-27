import boto3
import json

def create_embedding(input_text):
    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Titan Text Embeddings V2.
    model_id = "amazon.titan-embed-text-v2:0"

    # The text to convert to an embedding.
    #input_text = "Please recommend books with a theme similar to the movie 'Inception'."

    # Create the request for the model.
    native_request = {"inputText": input_text}

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=request)

    # Decode the model's native response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the generated embedding and the input text token count.
    embedding = model_response["embedding"]
    input_token_count = model_response["inputTextTokenCount"]

    #print("\nYour input:")
    #print(input_text)
    #print(f"Number of input tokens: {input_token_count}")
    #print(f"Size of the generated embedding: {len(embedding)}")
    #print("Embedding:")
    #print(embedding)

    return input_token_count, len(embedding), embedding

def save_embedding(input_text, input_token_count, embedding, embedding_length, page_number, file_name):
    print("page " + str(page_number))
    print("saved")
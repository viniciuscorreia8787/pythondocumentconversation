import boto3
import json
import psycopg2
import pandas as pd
import numpy as np

from pgvector.psycopg2 import register_vector

# Connect to PostgreSQL database in Tessell using connection string
conn=psycopg2.connect(
database="postgres",
user="postgres",
host="172.18.0.3",
password="password"
)

def create_embedding(input_text):
    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Titan Text Embeddings V2.
    model_id = "amazon.titan-embed-text-v2:0"

    # Limit input_text in 4500 chars
    input_text=input_text[:4500]
    
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

# Save embeddings and metadata into Postgres Vector DB 
def save_embedding(text, token_count, embedding, embedding_length, page_number, file_name):

    # Insert row with embeddings and metadata
    insert_row_command = """ INSERT INTO file_embeddings (file_name, page_number, text, token_count, embedding_length, embedding) VALUES (%s, %s, %s, %s, %s, %s) """
    
    # Prepare row to insert into database
    cur = conn.cursor()     

    cur.execute(insert_row_command, (file_name,
                                    page_number,
                                    text,
                                    token_count,
                                    embedding_length,
                                    embedding))
    conn.commit()
    cur.close() 

    print("page " + str(page_number) + " saved")

# Get top 3 most similar documents from the database
def get_top_similar_rows(query_embedding):

    # array_result = []
    embedding_array = np.array(query_embedding)
    register_vector(conn)
    cur = conn.cursor()

    # Get the top 5 most similar documents using the KNN <=> operator
    cur.execute("SELECT file_name, page_number, text FROM file_embeddings WHERE file_name = 'DA_Imperial_MeltShopv10.1.pdf' ORDER BY embedding <=> %s LIMIT 3", (embedding_array,))
    similar_pages = cur.fetchall()

    # Extend seach on similar pages
    #for page in similar_pages:

        # print("Searching page  = " + str(page[1]))
        # print("Including pages between" + str(page[1]) + " and " + str(page[1] + 2))

        # Include next 2 rows (pages) on result set
        #cur.execute("SELECT %s as original_page, file_name, page_number, text FROM file_embeddings WHERE page_number >= %s and page_number <= %s ORDER BY id LIMIT 5", (page[1], page[1], page[1] + 2))
        #extended_similar_pages = cur.fetchall()

        #for extended_page in extended_similar_pages:
        #    array_result.append(extended_page)

    #return array_result
    return similar_pages
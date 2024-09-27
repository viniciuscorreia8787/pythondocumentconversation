from embeddings_handle import *
from pdf_data_load_pymupdf import *

icont=0
file_path = "/workspaces/python/.devcontainer/documentconversation/supportfiles/"
file_name = "DA_Imperial_MeltShopv10.1.pdf"

# Read PDF and create array of text . 1 item per page
array_text = read_pdf(file_path + file_name)

# For each page
for text in array_text:
    icont+=1

    # Create embeddigs for page
    input_token_count, embedding_length, embedding = create_embedding(text)
    
    # Store page info on vector db
    save_embedding(text, input_token_count, embedding, embedding_length, icont, file_name )
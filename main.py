from embeddings_handle import *
from pdf_data_read_pypdf2 import *
from genai_text import *

icont=0
file_path = "/workspaces/python/.devcontainer/pythondocumentconversation/supportfiles/"
file_name = "DA_Imperial_MeltShopv10.1.pdf"

def import_document():
    file_name = input("Document name: ")

    print("Data load start...")
    icont=0

    # Read PDF and create array of text . 1 item per page
    array_text = read_pdf(file_path + file_name)
    
    # For each page
    for text in array_text:
        icont+=1

        # Create embeddigs for page
        input_token_count, embedding_length, embedding = create_embedding(text)
        #input_token_count= 10
        #embedding = None
        #embedding_length=10

        # Store page info on vector db
        save_embedding(text, input_token_count, embedding, embedding_length, icont, file_name )
    
    print("Data load completed")

def talk_to_document():

    original_pages = []
    while 1>0:
        input_text = input("\nAsk me anything about the document: ")

        icont = 0
        # Create embbedings from prompt
        input_token_count, embedding_length, embedding = create_embedding(input_text)
        
        # Get pages similar to the requested prompt
        top_pages = get_top_similar_rows(embedding)

        # Create prompt for GenAI, incluing user request and the list of similar pages
        genai_text_prompt= "You are an experienced analyst about financial data and mining of one of the greatest mining companies in the world. You are interacting with the high executive level of the company. Based on the following chunks of a document, explain briefly " + input_text + "."

        original_pages = []
        for page in top_pages:
            icont+=1
            genai_text_prompt += " document chunk " + str(icont) + " [[" + page[2] + "]]"

            if page[0] not in original_pages:
                original_pages.append(page[1])

        genai_answer = call_genai_text(genai_text_prompt) + "\nInformation found on pages "
        
        for item in original_pages:
            genai_answer += str(item) +  " - "       

        print("Response: " + genai_answer)


###TEST###
#file_name = "tabela.pdf"
#1array_text = read_pdf(file_path + file_name)

menu_selection = input("What do you want to do? [1] Import document, [2] talk to document: ")

while 1>0:

    if menu_selection=="1":
        import_document()
    if menu_selection=="2":
        talk_to_document()
    else:
        print("see ya!")
        break
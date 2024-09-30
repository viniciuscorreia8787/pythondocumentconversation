import fitz

def read_pdf(filepath):

    doc = fitz.open(filepath) # open a document
    out = open("/workspaces/python/.devcontainer/pythondocumentconversation/supportfiles/pdftext.log", "w")
    array_text = []
    icont=0

    for page in doc: # iterate the document pages

        icont+=1
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)

        out.write("*** Page " + str(icont) + " ***")
        out.write("\n")

        out.write(str(text)) # write text of page
        out.write("\n")

        array_text.append(str(text))
    out.close()
    return array_text
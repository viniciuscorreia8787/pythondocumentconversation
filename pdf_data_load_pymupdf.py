import fitz

def read_pdf(filepath):

    doc = fitz.open(filepath) # open a document
    out = open("/workspaces/python/.devcontainer/documentconversation/supportfiles/pdftext.txt", "wb")
    array_text = []
    icont=0

    for page in doc: # iterate the document pages

        icont+=1
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)

        out.write(bytes("*** Page " + str(icont) + " ***", "utf8"))
        out.write(bytes("\n", "utf8"))

        out.write(text) # write text of page
        out.write(bytes("\n", "utf8"))

        array_text.append(str(text))
    out.close()
    return array_text
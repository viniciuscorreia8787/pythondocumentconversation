from PyPDF2 import PdfReader

def read_pdf(filepath):

    array_text = []
    icont=0
    reader = PdfReader(filepath)

    out = open("/workspaces/python/.devcontainer/pythondocumentconversation/supportfiles/pdftext.log", "w")

    text = ""
    for page in reader.pages:
        icont+=1
        array_text.append(page.extract_text())
        out.write("*** Page " + str(icont) + " ***\n")
        out.write(page.extract_text()) # write text of page
        out.write("\n")


    out.close()
    return array_text
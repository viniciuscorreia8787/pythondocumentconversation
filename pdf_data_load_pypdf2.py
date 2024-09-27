from PyPDF2 import PdfReader

print("Process Start")

reader = PdfReader("/workspaces/python/.devcontainer/documentconversation/supportfiles/DA_Imperial_MeltShopv10.1.pdf")

text = ""
for page in reader.pages:
    print(page.extract_text())
    text += page.extract_text() + "\n"

f = open("/workspaces/python/.devcontainer/documentconversation/supportfiles/DA_Imperial_MeltShopv10.1.txt", "w")
f.write(text)
f.close()
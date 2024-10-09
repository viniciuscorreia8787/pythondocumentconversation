from PyPDF2 import PdfReader
from img2table.document import Image
from img2table.ocr import TesseractOCR
from img2table.document import PDF

def read_pdf(filepath):

    # Text Extraction
    array_text = []

    icont1=0
    reader = PdfReader(filepath)
    out = open("/workspaces/python/.devcontainer/pythondocumentconversation/supportfiles/pdftext.log", "w")
    ocr = TesseractOCR(n_threads=1, lang="eng")
    
    # Iterate Pages From PDF
    for page in reader.pages:
        icont1+=1
                
        out.write("*** Page [" + str(icont1) + "] ***\n")
        out.write(page.extract_text()) # write text of page
        out.write("\n")

        icont2=0
        tableListHTMLContent=""

        # Iterate images from each page 
        for image in page.images:
            
            icont2+=1

            image = Image(image.data, 
                          detect_rotation=False)
            
            # Extract tables from each image
            try:
                extracted_tables = image.extract_tables(ocr=ocr,
                                      implicit_rows=False,
                                      implicit_columns=False,
                                      borderless_tables=False,
                                      min_confidence=1)

                icont3=0
                for table in extracted_tables:
                    icont3+=1
                    out.write("\n ** Table [" + str(icont1) + "]["  + str(icont2) + "][" + str(icont3) + "] **\n")
                    out.write(table.html_repr()) # write text of page
                    out.write("\n")

                tableListHTMLContent+= "\n ** Table [" + str(icont2) + "][" + str(icont3) + "] **\n" + table.html_repr()

            except:
                print("Error page processing page " + str(icont1) + " image " + str(icont2) + " table " + str(icont3))

        # Push one single item containing all text for each page    
        array_text.append(page.extract_text() + tableListHTMLContent)

    out.close()
    return array_text
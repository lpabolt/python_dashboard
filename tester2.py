from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
'''import logging

logging.getLogger().setLevel(logging.ERROR)'''

pdf_list = []

## C:/WORK/53043/MB3S project/MB3S project/(PCA)Schematic/DOC0000321499-A1.pdf
## C:/WORK/53017/Roadrunner T90\Roadrunner T90/T90-1001_003.pdf
fp = open('C:/WORK/53043/MB3S project/MB3S project/(PCA)Schematic/DOC0000321499-A1.pdf', 'rb')
parser = PDFParser(fp)

doc = PDFDocument()
parser.set_document(doc)
doc.set_parser(parser)
doc.initialize('')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in doc.get_pages():
    interpreter.process_page(page)
    layout = device.get_result()
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            pdf_list.append(lt_obj.get_text())

## pdf_list NOW CONTAINS ALL TEXT FROM THE CHOSEN PDF.
## EACH LIST ELEMENT ENDS WITH ~ TO EASILY DIFFERENTIATE THE ACTUAL COMPONENTS FROM ANY OTHER MENTION OF THEIR NAME
pdf_list = [w.replace('\n', '~') for w in pdf_list]
print (pdf_list)

from PyPDF2 import PdfFileReader, PdfFileWriter

infile = PdfFileReader('c:/tmp/simon.pdf','rb')
output = PdfFileWriter()

for i in range(infile.getNumPages()):
    p = infile.getPage(i)
    if i != 5:
        output.addPage(p)

with open('c:/tmp/simon1.pdf','wb') as f:
    output.write(f)

## Program to merge some pdfs.
import glob
from PyPDF2 import PdfFileMerger

merger = PdfFileMerger()
directory = '.../desktop/folder'
for i in glob.glob(directory, '*.pdf'):
    ## alternatively: for i in ['pdf1_path.pdf', 'pdf2_path.pdf' ...]
    merger.append(i)
 
merger.write(directory + '/output_name.pdf')
merger.close()

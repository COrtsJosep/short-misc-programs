## Program to merge some pdfs.
import glob
import os
from PyPDF2 import PdfFileMerger

wd = os.getcwd()
os.chdir(wd)

merger = PdfFileMerger()
for i in glob.glob('*.pdf'):
    ## alternatively: for i in ['pdf1_path.pdf', 'pdf2_path.pdf' ...]
    merger.append(i)
 
merger.write('output_name.pdf')
merger.close()

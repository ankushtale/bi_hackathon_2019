from PyPDF2 import PdfFileReader
import os


def is_annotation_present(path):

    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()

        for i in range(number_of_pages):
            page = pdf.getPage(i)
            try:
                for annot in page['/Annots']:
                    if annot.getObject()['/Subtype'] == '/Text':
                        return True
                return False
            except:
                return False

def are_annotations_present(files_to_read):
    annotations_present = dict()

    for file in files_to_read:
        annotations_present[os.path.basename(file)] = is_annotation_present(file)

    return annotations_present

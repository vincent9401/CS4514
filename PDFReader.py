from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from cStringIO import StringIO

class PDFReader:

    def convert_pdf_to_txt(self, file_path):
        # PDF resource manager stores shared resources
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        # Open the PDF file
        fp = file(file_path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pagenos = set()
        maxpages = 0
        password = ""
        caching = True

        i = 0
        # Process each page in document
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            i = i + 1
            # Skip the first page of data dictionary
            if i == 1:
                continue
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()

        print text

        # HK 1980 Grid Coordinates, HK 1980 Geodetic Coordinates,
        # WGS84 Latitude and Longitude (ITRF96), UTM Grid Coordinate or UTM Grid Reference (ITRF96)
        # https://www.geodetic.gov.hk/smo/gsi/programs/en/GSS/grid/transformation.htm
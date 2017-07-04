import os
from DataExtraction import DataExtraction
from PDFReader import PDFReader


class Main:
    def __init__(self):
        pass

    def main(self):
        # Extraction the TSM data spec
        PDFReader().convert_pdf_to_txt('data/tsm_dataspec.pdf')

        # Extraction the TSM data for each time
        for xmlfile in os.listdir("data"):
            if xmlfile.endswith(".xml"):
                print('Reading ' + os.path.join("data/", xmlfile))

                # Start performing data extraction
                DataExtraction().modify_xml(os.path.join("data/", xmlfile))
                DataExtraction().read_xml(os.path.join("data/", xmlfile))

                print('Reading end.\n')


Main().main()


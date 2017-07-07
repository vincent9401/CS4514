import os

from DataCollector import DataCollector
from DataExtraction import DataExtraction
from DataVisualization import DataVisualization
from MongoDBConnection import MongoDBConnection
from PDFReader import PDFReader


class Main:
    def __init__(self):
        pass

    def main(self):
        # Extraction the TSM data spec
        data_spec_path = 'data/tsm_dataspec.pdf'
        PDFReader().convert_pdf_to_txt(data_spec_path)
        DataExtraction().extract_data_spec("data/tsm_link_and_node_info_v2.csv")

        # Extraction the TSM data for each time
        for xmlfile in os.listdir("data/tsm/"):
            if xmlfile.endswith(".xml"):
                print('Reading ' + os.path.join("data/tsm/", xmlfile))

                # Start performing data extraction
                DataExtraction().modify_xml(os.path.join("data/tsm/", xmlfile))
                DataExtraction().extract_tsm(os.path.join("data/tsm/", xmlfile))

                print('Reading end.\n')

#DataCollector().data_download()
Main().main()
DataVisualization().plot_live_heat_map()
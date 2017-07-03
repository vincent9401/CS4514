import os
from DataExtraction import DataExtraction

class Main:

    def main(self):
        for xmlfile in os.listdir("data"):
            if xmlfile.endswith(".xml"):
                print('Reading ' + os.path.join("data/", xmlfile))

                # Start performing data extraction
                DataExtraction().modifyXML(os.path.join("data/", xmlfile))
                DataExtraction().readXML(os.path.join("data/", xmlfile))

                print('Reading end.\n')


Main().main()
import xml.etree.ElementTree as ET
import fileinput

class DataExtraction:

    def readXML(self, file):
        tree = ET.parse(file)
        root = tree.getroot()

        print('Tag: ')
        print root.tag
        print('Attribute: ')
        print root.attrib

        print ('Data:')
        for speedmap in root.findall('jtis_speedmap'):
            link_id = speedmap.find('LINK_ID').text
            region = speedmap.find('REGION').text
            road_type = speedmap.find('ROAD_TYPE').text
            road_saturation_level = speedmap.find('ROAD_SATURATION_LEVEL').text
            traffic_speed = speedmap.find('TRAFFIC_SPEED').text
            capture_date = speedmap.find('CAPTURE_DATE').text

            print link_id, region, road_type, road_saturation_level, traffic_speed, capture_date


    def modifyXML(self, xmlfile):
        keyword = ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://data.one.gov.hk/td ' \
                  'http://data.one.gov.hk/xsd/td/speedmap.xsd" xmlns="http://data.one.gov.hk/td"'

        for line in fileinput.input(xmlfile, inplace=True):
            line = line.rstrip()
            if keyword in line:
                line = line.replace(keyword, '')
            print line
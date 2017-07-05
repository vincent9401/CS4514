import xml.etree.ElementTree as ET
import fileinput
import csv

from MongoDBConnection import MongoDBConnection


class DataExtraction:
    def __init__(self):
        pass

    def modify_xml(self, xmlfile):
        keyword = ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://data.one.gov.hk/td ' \
                  'http://data.one.gov.hk/xsd/td/speedmap.xsd" xmlns="http://data.one.gov.hk/td"'

        for line in fileinput.input(xmlfile, inplace=True):
            line = line.rstrip()
            if keyword in line:
                line = line.replace(keyword, '')
            print line

    def extract_tsm(self, filepath):
        tree = ET.parse(filepath)
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

    def extract_data_spec(self, filepath):
        # total number of lines
        row_count = sum(1 for row in csv.reader(open(filepath, 'r')))
        # Connect MongoDB, put the document into collection
        mongodb_connection = MongoDBConnection()
        mongodb = mongodb_connection.connect_db()
        collection = mongodb_connection.use_collection_tsm_spec(mongodb)
        collection_count = mongodb_connection.get_collection_size(collection)

        if collection_count != (row_count - 1):
            print 'Remove old data specification.'
            mongodb_connection.remove_all_document(collection)

            # Read the data spec
            csvfile = open(filepath, 'r')
            for row in csv.DictReader(csvfile.read().splitlines()):
                # Prepare the document
                speed_map = {"Link ID": row['Link ID'],
                             "Start Node": row['Start Node'],
                             "Start Node Eastings": row['Start Node Eastings'],
                             "Start Node Northings": row['Start Node Northings'],
                             "Start Node Latitude": row['Start Node Latitude'],
                             "Start Node Longitude": row['Start Node Longitude'],
                             "End Node": row['End Node'],
                             "End Node Eastings": row['End Node Eastings'],
                             "End Node Northings": row['End Node Northings'],
                             "End Node Latitude": row['End Node Latitude'],
                             "End Node Longitude": row['End Node Longitude'],
                             "Region": row['Region'],
                             "Road Type": row['Road Type']}

                print 'Update data specification.'
                mongodb_connection.insert_document(collection, speed_map)
                print 'Data specification - [{}] inserts into database.'.format(row['Link ID'])

                # print (row['Link ID'], row['Start Node'],
                #       row['Start Node Eastings'], row['Start Node Northings'],
                #       row['Start Node Latitude'], row['Start Node Longitude'],
                #       row['End Node'],
                #       row['End Node Eastings'], row['End Node Northings'],
                #       row['End Node Latitude'], row['End Node Longitude'],
                #       row['Region'], row['Road Type'])

            csvfile.close()
        else:
            print 'Data specification is up to date.'

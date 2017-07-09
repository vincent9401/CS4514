import os
import webbrowser
import xml.etree.ElementTree as ET

from DataCollector import DataCollector
from DataExtraction import DataExtraction
from MongoDBConnection import MongoDBConnection


class DataVisualization:

    def __init__(self):
        pass

    def retrieve_live_data(self):
        live_data = 'web/live_speedmap.xml'
        if os.path.isfile(live_data):
            DataCollector().remove_old_live_tsm()
        DataCollector().download_live_tsm()
        DataExtraction().modify_xml(live_data)

        tree = ET.parse(live_data)
        root = tree.getroot()

        speed_map = []
        for speedmap in root.findall('jtis_speedmap'):
            link_id = speedmap.find('LINK_ID').text
            region = speedmap.find('REGION').text
            road_type = speedmap.find('ROAD_TYPE').text
            road_saturation_level = speedmap.find('ROAD_SATURATION_LEVEL').text
            traffic_speed = speedmap.find('TRAFFIC_SPEED').text
            capture_date = speedmap.find('CAPTURE_DATE').text

            speed_map.append({ "Link ID": link_id,
                          "Region": region,
                          "Road Type": road_type,
                          "Road Saturation Level": road_saturation_level,
                          "Traffic Speed": traffic_speed,
                          "Capture Date": capture_date })
        return speed_map

    def plot_live_heat_map(self):
        # Connect MongoDB
        mongodb_connection = MongoDBConnection()
        mongodb = mongodb_connection.connect_db()
        collection = mongodb_connection.use_collection_tsm_spec(mongodb)
        documents = mongodb_connection.query_all_document(collection)

        heat_map_point = ''
        speed_map = self.retrieve_live_data()
        for value in documents:
            for node_detail in speed_map:
                if node_detail.get('Link ID') == value.get('Link ID'):
                    print 'Link ID [{}] found.'.format(node_detail.get('Link ID'))

                    sn_latitude = value.get('Start Node Latitude')
                    sn_longitude = value.get('Start Node Longitude')
                    en_latitude = value.get('End Node Latitude')
                    en_longitude = value.get('End Node Longitude')

                    weight = 0
                    if node_detail.get('Road Saturation Level') == 'TRAFFIC GOOD':
                        weight = 0.5
                    elif node_detail.get('Road Saturation Level') == 'TRAFFIC AVERAGE':
                        weight = 2
                    elif node_detail.get('Road Saturation Level') == 'TRAFFIC BAD':
                        weight = 4

                    heat_map_point = heat_map_point + \
                                     '{{location: new google.maps.LatLng({}, {}), weight: {}}},\n'.format(sn_latitude, sn_longitude, weight)
                    heat_map_point = heat_map_point + \
                                     '{{location: new google.maps.LatLng({}, {}), weight: {}}},\n'.format(en_latitude, en_longitude, weight)

        # Provide the point detail to the html file
        html_file = open('web/heat_map_template.html', 'r')
        with open('web/traffic_heat_map.html', 'w') as new_file:
            for row in html_file:
                if '/* Provide the point detail */' in row:
                    row = row.replace('/* Provide the point detail */', heat_map_point)
                new_file.write(row)
            html_file.close()
        new_file.close()

        # Open the browser to show the live map
        webbrowser.open('file://' + os.path.realpath('web/traffic_heat_map.html'), new=2)
        print 'Finish rendering live heat map.'
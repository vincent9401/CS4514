import os
import webbrowser

from MongoDBConnection import MongoDBConnection
from random import randint


class DataVisualization:

    def plot_live_heat_map(self):
        mongodb_connection = MongoDBConnection()
        mongodb = mongodb_connection.connect_db()
        collection = mongodb_connection.use_collection_tsm_spec(mongodb)
        documents = mongodb_connection.query_all_document(collection)

        heat_map_point = ''
        for value in documents:
            sn_latitude = value.get('Start Node Latitude')
            sn_longitude = value.get('Start Node Longitude')
            en_latitude = value.get('End Node Latitude')
            en_longitude = value.get('End Node Longitude')
            weight = randint(0, 5)

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

DataVisualization().plot_live_heat_map()
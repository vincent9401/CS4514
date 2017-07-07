import os
import urllib2


class DataCollector:

    def __init__(self):
        pass

    def data_download_with_api_string(self):
        query_string = open('data/tsm_api_query_string.txt', 'r')
        i = 0
        for row in query_string:
            i = i + 1
            if i % 2 == 1:
                response = urllib2.urlopen(row)
                data = response.read()

                # Write data to file
                filename = 'data/tsm/{}.xml'.format(row[-14:-1])
                file = open(filename, 'w')
                file.write(data)
                file.close()

    def download_live_tsm(self):
        response = urllib2.urlopen('http://resource.data.one.gov.hk/td/speedmap.xml')
        data = response.read()

        # Write data to file
        filename = 'web/live_speedmap.xml'
        file = open(filename, 'w')
        file.write(data)
        file.close()

    def remove_old_live_tsm(self):
        os.remove('web/live_speedmap.xml')
        print 'Old traffic speed map removed.'

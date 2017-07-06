import urllib2

class DataCollector:

    def data_download(self):
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
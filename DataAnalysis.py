import sklearn.datasets
import numpy as np
from sklearn import svm
from sklearn.datasets import load_svmlight_file

from sklearn.feature_extraction import DictVectorizer
from MongoDBConnection import MongoDBConnection


class DataAnalysis:

    def data_preprocessing(self):
        # Connect MongoDB
        mongodb_connection = MongoDBConnection()
        mongodb = mongodb_connection.connect_db()
        collection = mongodb_connection.use_collection_tsm(mongodb)
        documents = mongodb_connection.query_all_document(collection)

        with open('data/tsm.csv', 'w') as new_file:
            for speed_map in documents:
                link_id = speed_map.get('Link ID')
                region = speed_map.get('Region')
                road_type = speed_map.get('Road Type')
                road_saturation_level = speed_map.get('Road Saturation Level')
                traffic_speed = speed_map.get('Traffic Speed')
                capture_date = speed_map.get('Capture Date')

                region_ = 0
                if region == 'TM':
                    region_ = 1
                elif region == 'ST':
                    region_ = 2
                elif region == 'K':
                    region_ = 3
                elif region == 'HK':
                    region_ = 4

                road_type_ = 0
                if road_type == 'MAJOR ROUTE':
                    road_type_ = 0
                elif road_type == 'URBAN ROAD':
                    road_type_ = 1

                capture_date_ = 0
                if int(capture_date[-8:-6]) >= 21:
                    capture_date_ = 8
                elif int(capture_date[-8:-6]) >= 18:
                    capture_date_ = 7
                elif int(capture_date[-8:-6]) >= 15:
                    capture_date_ = 6
                elif int(capture_date[-8:-6]) >= 12:
                    capture_date_ = 5
                elif int(capture_date[-8:-6]) >= 9:
                    capture_date_ = 4
                elif int(capture_date[-8:-6]) >= 6:
                    capture_date_ = 3
                elif int(capture_date[-8:-6]) >= 3:
                    capture_date_ = 2
                elif int(capture_date[-8:-6]) >= 0:
                    capture_date_ = 1

                level = 0
                if road_saturation_level == 'TRAFFIC GOOD':
                    level = 3
                elif road_saturation_level == 'TRAFFIC AVERAGE':
                    level = 2
                elif road_saturation_level == 'TRAFFIC BAD':
                    level = 1

                new_file.write('{},{},{},{},{}\n'.format(region_, road_type_, traffic_speed, capture_date_, level))
            new_file.close()

    # http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.DictVectorizer.html
    def data_covert(self):
        # Connect MongoDB
        mongodb_connection = MongoDBConnection()
        mongodb = mongodb_connection.connect_db()
        collection = mongodb_connection.use_collection_tsm_test(mongodb)
        documents = mongodb_connection.query_all_document(collection)

        measurement = []
        for speed_map in documents:
            link_id = speed_map.get('Link ID')
            region = speed_map.get('Region')
            road_type = speed_map.get('Road Type')
            road_saturation_level = speed_map.get('Road Saturation Level')
            traffic_speed = speed_map.get('Traffic Speed')
            capture_date = speed_map.get('Capture Date')

            meas = {'Region': region,
                    'Road Type': road_type,
                    'Level': road_saturation_level,
                    'Traffic Speed': int(traffic_speed),
                    'Time': capture_date[-8:-6]}

            measurement.append(meas)

        vec = DictVectorizer(sparse=False)
        X = vec.fit_transform(measurement)

        feature_names = vec.get_feature_names()
        print "Feature_names: " + str(feature_names)

        y = np.ones(len(X))
        sklearn.datasets.dump_svmlight_file(X, y, 'data/tsm_train.svm', zero_based=True, comment=None, query_id=None, multilabel=False)
        #print X

    def get_data(self):
        data = load_svmlight_file("data/tsm_train.svm")
        return data[0], data[1]

    def training(self):
        X_train, y_train = self.get_data()
        clf = svm.SVC(kernel='linear')
        clf.fit(X_train, y_train)

DataAnalysis().data_covert()


'''
    def data_loading(self):
        import numpy as np

        raw_data = open('data/tsm_link_and_node_info_v2.csv', 'r')
        # load the CSV file as a numpy matrix
        dataset = np.loadtxt(raw_data, delimiter=",")
        # separate the data from the target attributes
        X = dataset[:, 0:8]
        y = dataset[:, 8]
'''
'''
    def scikit_nb(self):
        from sklearn.naive_bayes import GaussianNB
        import pandas as pd
        import numpy as np

        # create data frame containing your data, each column can be accessed # by df['column   name']
        df = pd.read_csv('/your/path/yourFile.csv')

        target_names = np.array(['Positives', 'Negatives'])

        # add columns to your data frame
        df['is_train'] = np.random.uniform(0, 1, len(df)) <= 0.75
        df['Type'] = pd.Factor(targets, target_names)
        df['Targets'] = targets

        # define training and test sets
        train = df[df['is_train'] == True]
        test = df[df['is_train'] == False]

        trainTargets = np.array(train['Targets']).astype(int)
        testTargets = np.array(test['Targets']).astype(int)

        # columns you want to model
        features = df.columns[0:7]

        # call Gaussian Naive Bayesian class with default parameters
        gnb = GaussianNB()

        # train model
        y_gnb = gnb.fit(train[features], trainTargets).predict(train[features])
'''
from MongoDBConnection import MongoDBConnection


class DataAnalysis:

    def data_preprocessing(self):
        # Connect MongoDB
        mongodb_connection = MongoDBConnection()
        mongodb = mongodb_connection.connect_db()
        collection = mongodb_connection.use_collection_tsm(mongodb)
        documents = mongodb_connection.query_all_document(collection)

        for speed_map in documents:
            link_id = speed_map.get('Link ID')
            region = speed_map.get('Region')
            road_type = speed_map.get('Road Type')
            road_saturation_level = speed_map.get('Road Saturation Level')
            traffic_speed = speed_map.get('Traffic Speed')
            capture_date = speed_map.get('Capture Date')

    def data_loading(self):
        import numpy as np

        raw_data = open('data/tsm_link_and_node_info_v2.csv', 'r')
        # load the CSV file as a numpy matrix
        dataset = np.loadtxt(raw_data, delimiter=",")
        # separate the data from the target attributes
        X = dataset[:, 0:8]
        y = dataset[:, 8]
'''
    def scikit(self):
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

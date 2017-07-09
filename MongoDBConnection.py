from pymongo import MongoClient


class MongoDBConnection:

    def __init__(self):
        pass

    def connect_db(self):
        # Provide connection detail
        client = MongoClient('localhost', 27017)
        db = client.trafficdata
        return db

    def use_collection_tsm_spec(self, db):
        collection = db.tsm_spec
        return collection

    def use_collection_tsm(self, db):
        collection = db.traffic_speed_map
        return collection

    def use_collection_traffic_accidents(self, db):
        collection = db.traffic_accidents
        return collection

    def use_collection_tsm_test(self, db):
        collection = db.tsm_test
        return collection

    def insert_document(self, collection, document):
        collection.insert(document)

    def remove_document(self, collection, document):
        collection.remove(document)

    def remove_all_document(self, collection):
        collection.remove()

    def query_document(self, collection, keyword):
        return collection.find(keyword)

    def query_all_document(self, collection):
        return collection.find()

    def query_document_number(self, collection, document):
        no_of_document = collection.find(document).count()
        return no_of_document

    def get_collection_size(self, collection):
        collection_size = collection.find().count()
        return collection_size

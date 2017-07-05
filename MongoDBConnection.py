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

    def insert_document(self, collection, document):
        collection.insert(document)

    def remove_document(self, collection, document):
        collection.remove(document)

    def remove_all_document(self, collection):
        collection.remove()

    def get_collection_size(self, collection):
        return collection.find().count()

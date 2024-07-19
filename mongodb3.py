from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class mongodb_helper:
    def __init__(self , collection = 'users'):
        uri = "mongodb+srv://disha:301818@cluster0.wadelgh.mongodb.net/?appName=Cluster0"

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = client['disha']
        self.collection = self.db[collection]

    def insert(self , document):
        result = self.collection.insert_one(document)
        print("Document inserted in Collection ," , self.collection.name)
        return result

    def fetch(self, query ="") :
        documents = self.collection.find(query)
        return list(documents)
    
    def delete(self , query=""):
        result = self.collection.delete_one(query)
        print("result is",result)
        return result

    
    def update(self ,document_to_update , query=""):
        document_to_update = {"$set" : document_to_update}
        result = self.collection.update_one(query,document_to_update)
        print("the result is ," , result)
        return result



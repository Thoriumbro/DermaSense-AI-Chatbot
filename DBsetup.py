
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def setup_database(d1,d2):
    uri = "mongodb+srv://rishabh24461:7yV0j1ljI9ays7ou@cluster0.u36nq.mongodb.net/"

    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client["medical_records"]  
    collection = db["patients"]  

    patient_data = {"Demographic_Data": d1, "Symptoms_Data": d2}
    result = collection.insert_one(patient_data)

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ashnaz:lhjLdZGdBtthtT2S@cluster0.gae6w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client.diagnose_symptoms_diseases
patient_collection = db['patients']
doctor_collection = db['doctors']
doctor_availability = db['availability']

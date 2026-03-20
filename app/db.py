from pymongo import MongoClient
from app.config import MONGODB_URL, DATABASE_NAME

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

patients_collection = db["patients"]
snapshots_collection = db["snapshots"]
conflicts_collection = db["conflicts"]
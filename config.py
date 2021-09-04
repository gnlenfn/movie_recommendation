from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

MONGODB_PASSWORD=os.getenv('PASSWORD')
MONGODB_USERNAME=os.getenv('USERNAME')
MONGODB_URI=os.getenv("MONGODB_URI")
MONGO_URI=f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_URI}"

mongo = MongoClient(MONGO_URI)
SECRET_KEY=os.getenv('SECRET_KEY')


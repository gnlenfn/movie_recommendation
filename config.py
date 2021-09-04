from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

MONGODB_PASSWORD=os.getenv('PASSWORD')
MONGODB_USERNAME=os.getenv('USERNAME')
MONGO_URI=f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.vlbhg.mongodb.net/movies?retryWrites=true&w=majority"

mongo = MongoClient(MONGO_URI)
SECRET_KEY=os.getenv('SECRET_KEY')


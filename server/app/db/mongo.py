from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)

# Database
db = client["ai_doc_qa"]

# Collections
files_collection = db["files"]
chat_collection = db["chats"]
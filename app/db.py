from pymongo import MongoClient
from config.config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client["MomentumDB"] #cluster name 
files_data = db["Files"] # collection name 
repositories_data = db["Repositories"] 
functions_data = db["Functions"]

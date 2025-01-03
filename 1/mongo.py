from pymongo import MongoClient

# Connect to local MongoDB
local_client = MongoClient('mongodb://localhost:27017/')
local_db = local_client['phishing_database']  # Replace with your local database name
local_collection = local_db['phishing_urls']  # Replace with your local collection name

# Connect to MongoDB Atlas
atlas_client = MongoClient('mongodb+srv://arnavmodi23:yjtuexaqQAYCCdSL@cluster0.t7a9j.mongodb.net/')
atlas_db = atlas_client['phishing_database']  # Replace with your Atlas database name
atlas_collection = atlas_db['phishing_urls']  # Replace with your Atlas collection name

# Fetch data from local MongoDB
data = list(local_collection.find())

# Insert data into MongoDB Atlas
if data:
    atlas_collection.insert_many(data)
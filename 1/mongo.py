import pandas as pd
from pymongo import MongoClient

# Read the CSV file
csv_file_path = r'C:\Coding\Phishing-Website\1\phishing_site_urls.csv'
df = pd.read_csv(csv_file_path)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string if different
db = client['phishing_database']  # Replace with your database name
collection = db['phishing_urls']  # Replace with your collection name

# Convert DataFrame to dictionary and insert into MongoDB
data = df.to_dict(orient='records')
collection.insert_many(data)

print("Data inserted successfully!")
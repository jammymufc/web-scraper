from pymongo import MongoClient

# Initialize a MongoDB client
client = MongoClient("mongodb://localhost:27017/")

# Access your database and collection
db = client["clickRepellent"]
collection = db["valid"]

# Find and print all documents in the collection
cursor = collection.find({})
for document in cursor:
    print(document)

# Close the MongoDB client
client.close()
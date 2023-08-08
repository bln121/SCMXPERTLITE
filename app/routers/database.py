from pymongo import MongoClient


# client = MongoClient("mongodb://localhost:27017")
client = MongoClient("mongodb+srv://narayana:Narayana1234@cluster0.zcvlydb.mongodb.net/")

# Access the desired database
db = client["shipment_db"]
# Access the collection where you want to store user details
collection_users = db["shipment_users"]
collection_shipment_data=db["shipment_data"]
collection_stream_data=db["stream_data"]
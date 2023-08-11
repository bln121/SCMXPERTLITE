from kafka import KafkaConsumer
import json
from pymongo import MongoClient
import os

from dotenv import load_dotenv

load_dotenv()


client = MongoClient("mongodb+srv://narayana:Narayana1234@cluster0.zcvlydb.mongodb.net/")

db = client["shipment_db"]

# Access the collection where you want to store user details
collection_stream_data=db["stream_data"]


#bootstrap_servers = ['kafka:9092']
bootstrap_servers =os.getenv("bootstrap_servers")  

#topic_name = 'server_data'
topic_name=os.getenv("topic_name")

#data received from producer is decoded.
consumer = KafkaConsumer(topic_name,
                         bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),api_version=(0,11,5))

for message in consumer:
    #print("Received:", message.value)
    for data_dict in message.value:
        collection_stream_data.insert_one(data_dict)
    
    print("Received:", message.value)

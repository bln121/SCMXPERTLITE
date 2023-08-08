import socket
import json
import os
from kafka import KafkaProducer
#from config.config import SETTING
from dotenv import load_dotenv

load_dotenv()

# Socket client configuration
socket_conn = socket.socket()


host=os.getenv("host")
port=os.getenv("port")

#Connect to the localhost with port number 23532
#server_address = ('localhost', 23532)
server_address=(host,int(port))
socket_conn.connect(server_address)

# Kafka producer configuration
bootstrap_servers = ['localhost:9092']

#Topics enable the publisher-producer to send data to Kafka and the consumer-subscriber to read data from Kafka.
#topic_name = 'server_data'
topic_name=os.getenv("topic_name")

#bootstrap_servers: This parameter specifies the list of Kafka brokers to which the producer should connect. 
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

while True:
    try:
         # Receive data from the socket server
        #The 4096 parameter specifies the maximum number of bytes to be received in one call.
        #recv() may not always receive the entire message in one call, so recv() is called in loop.
        data = socket_conn.recv(4096) 
        if not data:
            break

        # Decode the received data and parse it as JSON
        data = json.loads(data.decode('utf-8'))
        print(data)
        # Sending the received data to the Kafka topic
        producer.send(topic_name, value=data)

    except Exception as e:
        print("Error:", e)
        break

# Close the Kafka producer and socket connection
producer.close()
socket_conn.close()

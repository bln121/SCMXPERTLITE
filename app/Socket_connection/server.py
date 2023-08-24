import socket
import json
import time
import random

#Creating connection with the socket
#By default socket() method takes parameters as ipv4 and TCP
socket_conn = socket.socket()
print("Socket Created")

#Bind the localhost with some port no. of range(0-65535)
socket_conn.bind(('',23532))

#It will have buffer for 3 connections
socket_conn.listen(3)
print("waiting for connections")

#accept() returns the client address
#addr: This is a tuple containing the address and port of the connected client. 
#client is the new socket object returned by the accept(). It is used to send data to the client
client, addr = socket_conn.accept()


while True:
    try:
        print("connected with", addr)
        

        #random.uniform() method to return a random float number in given range
        #round() is to return no. of decimal number to return.
        data =[{
        "Battery_Level":round(random.uniform(5,6),2),
        "Device_Id":1156053076,
        "First_Sensor_temperature":round(random.uniform(20,22),2) ,
        "Route_From":"{}, India".format(random.choice(["Hyderabad","Delhi","Tirupati","Mumbai","Visakhapatnam","Pune","Chennai","Trivendram","Ahmedabad","Kolkata"])),
        "Route_To":"{}, USA".format(random.choice(["Louisville","Los Angeles","Chicago","New York","North Las Vegas","Houston","Dallas","Austin","Washington","San Francisco","Philadelphia"]))
        },
        {
        "Battery_Level":round(random.uniform(5,6),2),
        "Device_Id":1156053077,
        "First_Sensor_temperature":round(random.uniform(20,22),2) ,
        "Route_From":"{}, India".format(random.choice(["Hyderabad","Delhi","Tirupati","Mumbai","Visakhapatnam","Pune","Chennai","Trivendram","Ahmedabad","Kolkata"])),
        "Route_To":"{}, USA".format(random.choice(["Louisville","Los Angeles","Chicago","New York","North Las Vegas","Houston","Dallas","Austin","Washington","San Francisco","Philadelphia"]))
        }]


        userdata = (json.dumps(data)+"\n").encode('utf-8')  #json.dumps() converts data into the json format as kafka accepts only json format
        print(userdata)
        client.send(userdata)
        time.sleep(100)
    except Exception as e:
        print(e)
        client.close()



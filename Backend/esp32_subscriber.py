import paho.mqtt.client as mqttClient
import time
import requests
import json
import ast
from elasticsearch import Elasticsearch
 
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
 
def on_message(client, userdata, message):
	print("Message received:" + message.payload);
	data=ast.literal_eval(json.loads(json.dumps(message.payload)));
	dbdata = {}
	dbdata['deviceValue'] = data['temperature'];
	dbdata['deviceParameter'] = 'Temperature';
	dbdata['deviceId'] = data['deviceId'];
	dbdata['@timestamp'] = long(str(time.time()).split('.')[0]) * 1000;
	print(dbdata);
	tt=es.index(index='sensordata', doc_type='readings', body=dbdata);
	dbdata['deviceValue'] = data['humidity'];
	dbdata['deviceParameter'] = 'Humidity';
	tt=es.index(index='sensordata', doc_type='readings', body=dbdata);
	print(dbdata);
	#print(tt);

Connected = False   #global variable for the state of the connection
 
broker_address= "localhost"  #Broker address
port = 1883                         #Broker port
 
client = mqttClient.Client("seecat_broker")               #create new instance
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe("deviceID/+/sensorData");
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()

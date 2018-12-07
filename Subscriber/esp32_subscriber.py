import paho.mqtt.client as mqtt
import time
import requests
import json
import ast
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'dbserver', 'port': 9200}])

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to broker')
        global Connected                #Use global variable
        Connected = True                #Signal connection
    else:
        print('Connection failed')

def on_message(client, userdata, message):
	print('Message received:' + message.payload.decode('utf8'));
	data=json.loads(message.payload.decode('utf8'));
	dbdata = {}
	dbdata['deviceValue'] = data['temperature'];
	dbdata['deviceParameter'] = 'Temperature';
	dbdata['deviceId'] = data['deviceId'];
	dbdata['@timestamp'] = data[timeStamp] * 1000;
	print(dbdata);
	tt=es.index(index='sensordata', doc_type='readings', body=dbdata);
	dbdata['deviceValue'] = data['humidity'];
	dbdata['deviceParameter'] = 'Humidity';
	dbdata['@timestamp'] = data[timeStamp] * 1000;
	tt=es.index(index='sensordata', doc_type='readings', body=dbdata);
	print(dbdata);
	client.publish('sensorData/update', 'data updated' ,0)
	#print(tt);

def on_subscribe(client, userdata, mid, granted_qos):
    print('Subscribed: ' + str(mid) + ' ' + str(granted_qos))

def on_log(mqttc, userdata, level, string):
    print(string)

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe
#Uncomment to enable debug messages
#client.on_log = on_log

Connected = False   #global variable for the state of the connection

client.connect('mqttbroker', 1883, 60)

#while Connected != True:    #Wait for connection
#    time.sleep(0.1)

client.subscribe('deviceID/+/sensorData', 0);

try:
	client.loop_forever()

except KeyboardInterrupt:
    print('exiting')
    client.disconnect()
    client.loop_stop()

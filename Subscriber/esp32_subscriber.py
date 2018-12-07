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

def myfunction_test(listener=None):
    '''handling functions'''
    def do_work(data):
	print(data);
        if listener is not None:
            listener('Hello123')
        return data
    return do_work

def stream_processor():
    state = []
    subscriptions = []
    def process_stream(client, userdata, message):
        nonlocal state
        stream_message = json.loads(message.payload.decode('utf-8'))
        print(stream_message)
        if len(state) < 5:
            state = [*state, stream_message]
        else:
            state = [*state[1:], stream_message]
            for subscriber in subscriptions:
                subscriber(state)
    def subscribe(fn):
        def unsubscribe():
            subscriptions.remove(fn)
        subscriptions.append(fn)
        return unsubscribe
    return process_stream, subscribe

def log_event_data(*args, **kwargs):
    print('Event Data:', *args, **kwargs)

def prediction_listener(prediction):
    print('listened prediction:', prediction)
    client.publish('predictionData/update', json.dumps(prediction), 0)

process_stream, subscribe_sensor = stream_processor()
subscribe_sensor(myfunction_test(listener=prediction_listener))
subscribe_sensor(log_event_data)

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

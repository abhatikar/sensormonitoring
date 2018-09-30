import paho.mqtt.client as paho
import json
import random
import datetime
import time

deviceNames = ['SBS01', 'SBS02', 'SBS03', 'SBS04', 'SBS05']

broker="localhost"
port=1883
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
client1= paho.Client("normal")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker,port)                                 #establish connection


# generate Light values
def getLightValues():
    data = {}
    data['deviceValue'] = random.randint(60, 100)
    data['deviceParameter'] = 'Light'
    data['deviceId'] = random.choice(deviceNames)
    data['@timestamp'] = long(str(time.time()).split('.')[0]) * 1000
    return data

# generate Temperature values
def getTemperatureValues():
    data = {}
    data['deviceValue'] = random.randint(15, 35)
    data['deviceParameter'] = 'Temperature'
    data['deviceId'] = random.choice(deviceNames)
    data['@timestamp'] = long(str(time.time()).split('.')[0]) * 1000
    return data

# generate Humidity values
def getHumidityValues():
    data = {}
    data['deviceValue'] = random.randint(50, 90)
    data['deviceParameter'] = 'Humidity'
    data['deviceId'] = random.choice(deviceNames)
    data['@timestamp'] = long(str(time.time()).split('.')[0]) * 1000
    return data

# generate Shock values
def getShockValues():
    data = {}
    data['deviceValue'] = random.randint(100, 140)
    data['deviceParameter'] = 'Shock'
    data['deviceId'] = random.choice(deviceNames)
    data['@timestamp'] = long(str(time.time()).split('.')[0]) * 1000
    return data

# Generate each parameter's data input in varying proportions
while True:
    time.sleep(1)
    rnd = random.random()
    if (0 <= rnd < 0.20):
        data = json.dumps(getLightValues())
        print data
	ret = client1.publish("/sbs/devicedata/light", data)                   #publish
    elif (0.20<= rnd < 0.55):
        data = json.dumps(getTemperatureValues())
        print data
	ret = client1.publish("/sbs/devicedata/temperature", data)                   #publish
    elif (0.55<= rnd < 0.70):
        data = json.dumps(getHumidityValues())
        print data
	ret = client1.publish("/sbs/devicedata/humidity", data)                   #publish
    else:
        data = json.dumps(getShockValues())
        print data
	ret = client1.publish("/sbs/devicedata/shock", data)                   #publish

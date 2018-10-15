#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import time
import requests
import json
import ast
from elasticsearch import Elasticsearch
import dateutil.parser as dp

 
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

app = Flask(__name__)
api = Api(app)

class SensorData(Resource):
	def get(self, start_idx):
		res=es.search(index='sensordata',body={ "sort" : [ { "@timestamp" : {"order" : "asc"} } ],'size' : 1000, 'from' : start_idx, 'query':{ 'match_all':{} }}) 
		return res['hits']['hits']

class SensorDataDate(Resource):
	def get(self, start_date, end_date):
		print(start_date);
		print(end_date);
		sdate=dp.parse(start_date);
		edate=dp.parse(end_date);
		stimestamp=sdate.strftime('%s');
		etimestamp=edate.strftime('%s');
		print(int(stimestamp)*1000);
		print(int(etimestamp)*1000);
		res=es.search(index='sensordata',body={ "sort" : [ { "@timestamp" : {"order" : "asc"} } ],'size' : 1000, 'from' : 0, 'query':{ 'range':{ "@timestamp" : { "gte": int(stimestamp)*1000, "lte": int(etimestamp)*1000 }} }})
		return res['hits']['hits']

api.add_resource(SensorData, '/sensordata/<start_idx>') # Route_1
api.add_resource(SensorDataDate, '/sensordata/<start_date>/<end_date>') # Route_2

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)

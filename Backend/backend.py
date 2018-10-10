#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import time
import requests
import json
import ast
from elasticsearch import Elasticsearch
 
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

app = Flask(__name__)
api = Api(app)

class SensorData(Resource):
	def get(self, start_idx):
		res=es.search(index='sensordata',body={ "sort" : [ { "@timestamp" : {"order" : "asc"} } ],'size' : 1000, 'from' : start_idx, 'query':{ 'match_all':{} }}) 
		return res['hits']['hits']
    
	def post(self):
		return {'status':'success'}

class Tracks(Resource):
	def get(self):
		res=es.search(index='sensordata',body={
        'query':{
            'bool':{
                'must':{
                    'match':{
                        'deviceId':'SBS01'
                    }
                },
                "filter":{
                    "range":{
                        "deviceValue":{
                            "gt":25
                        }
                    }
                }
            }
        }
    })

		return {'hello': 'world'}
    
class Employees_Name(Resource):
	def get(self, id_1):
		return {'hello3': id_1}
#    def get(self, employee_id):
#        conn = db_connect.connect()
#        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
#        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#        return jsonify(result)


api.add_resource(SensorData, '/sensordata/<start_idx>') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<id_1>') # Route_3


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)

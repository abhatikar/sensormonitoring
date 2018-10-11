#!/usr/bin/python3
from json import dumps
import json
from elasticsearch import Elasticsearch
 
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


dbdata = { 
      "properties":{
        "deviceParameter": {"type" : "keyword"},
        "deviceValue" : {"type": "float"},
        "deviceId" : {"type" : "keyword"},
        "@timestamp": {
          "type" : "date", 
          "format" : "epoch_millis"
        }
      }
    }

print(dbdata);
tt=es.indices.put_mapping(index='sensordata_test',doc_type="readings", body=dbdata);
print(tt);


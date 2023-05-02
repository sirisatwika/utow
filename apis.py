

import requests
import json
from datetime import datetime, timedelta
import time
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from createcacert import createX509
from createsymkey import createSymKey
from influxdb import InfluxDBClient
from flask_httpauth import HTTPBasicAuth

# creating a Flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
auth = HTTPBasicAuth()

# InfluxDB configuration
INFLUXDB_HOST = 'localhost'
INFLUXDB_PORT = 8086
INFLUXDB_USERNAME = 'admin'
INFLUXDB_PASSWORD = 'admin'
INFLUXDB_DATABASE = 'sensors'


# Create InfluxDB client
client = InfluxDBClient(host=INFLUXDB_HOST,port=INFLUXDB_PORT,username=INFLUXDB_USERNAME,
password=INFLUXDB_PASSWORD,
database=INFLUXDB_DATABASE)

@app.route('/api/v1/gateway/data/linegraph/<devicename>', methods=['GET'])
@cross_origin()
def getdataline(devicename):
    try:
        query = 'SELECT data FROM '+devicename+';'
        result = client.query(query)
        lst = []
        for point in result.get_points():
            res = point['data']
            res2 = float(res)
            num = '{0:.2f}'.format(res2)
            lst.append(num)
            print(num)
        r = { devicename : lst }
        return json.dumps(r)
    except Exception as e:
        return str(e)

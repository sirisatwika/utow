import requests
import json
from datetime import datetime, timedelta
import time
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from createcacert import createX509
from createsymkey import createSymKey


# creating a Flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

  
@app.route('/')
@cross_origin()
def home():
    return "Welcome to Inteligent Edge!!!"
  
@app.route('/api/v1/gateway/provisionx509cert')
@cross_origin()
def provisiongatewaycertx509():
    try:
        createX509()
        return 'Success'
    except Exception as e:
        return e

@app.route('/api/v1/gateway/provisionsymkey')
def provisiongatewaysymmetrickey():
    try:
        symkey = createSymKey()
        return 'Success'
    except Exception as e:
        return e

@app.route('/api/v1/device/provisionx509cert')
@cross_origin()
def provisiondevicecertx509():
    try:
        createX509()
        return 'Success'
    except Exception as e:
        return e

@app.route('/api/v1/device/provisionsymkey')
@cross_origin()
def provisiondevicesymmetrickey():
    try:
        symkey = createSymKey()
        return symkey
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/provisioned')
@cross_origin()
def getgatewayprovcount():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        gatewaycount = response.json()['totalCount']
        return str(gatewaycount)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/unprovisioned')
def getgatewayunprovcount():
    try:
        apiurl_prov = "http://localhost:59881/api/v2/device/all"
        response_prov = requests.get(apiurl_prov)
        gatewaycount_prov = response_prov.json()['totalCount']
        
        apiurl_tot = "http://localhost:59881/api/v2/deviceprofile/all"
        response_tot = requests.get(apiurl_tot)
        gatewaycount_tot = response_tot.json()['totalCount']
        return str(gatewaycount_tot - gatewaycount_prov)
    except Exception as e:
        return e
        
@app.route('/api/v1/gateway/count/total')
@cross_origin()
def getgatewaytotalcount():
    try:
        apiurl_tot = "http://localhost:59881/api/v2/deviceprofile/all"
        response_tot = requests.get(apiurl_tot)
        gatewaycount_tot = response_tot.json()['totalCount']
        return str(gatewaycount_tot)
    except Exception as e:
        return e


@app.route('/api/v1/gateway/count/online')
@cross_origin()
def getonlinecount():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        devicelist = response.json()['devices']
        cnt = 0
        for d in devicelist:
            if d['operatingState'] == "UP":
                cnt += 1
        return str(cnt)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/offline')
@cross_origin()
def getofflinecount():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        devicelist = response.json()['devices']
        cnt = 0
        for d in devicelist:
            if d['operatingState'] == "DOWN":
                cnt += 1
        return str(cnt)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/active')
@cross_origin()
def getactivecount():
    try:
        curr_time = time.time_ns()
        #print(curr_time)
        prev_time = datetime.now() - timedelta(seconds = 2)
        prev_ns = int(time.mktime(prev_time.timetuple()) * pow(10, 9))
        #print(prev_ns)
        apiurl = "http://localhost:59880/api/v2/event/start/"+ str(prev_ns)+"/end/"+ str(curr_time)
        response = requests.get(apiurl)
        #print(response.json())
        events = response.json()['events']
        devnameset = set({})
        for e in events:
            devname =e['deviceName']
            devnameset.add(devname)
        return str(len(devnameset))
    except Exception as e:
        return e
        
@app.route('/api/v1/gateway/count/inactive')
@cross_origin()
def getinactivecount():
    try:
        apiurl_prov = "http://localhost:59881/api/v2/device/all"
        response_prov = requests.get(apiurl_prov)
        gatewaycount_prov = response_prov.json()['totalCount']
        
        curr_time = time.time_ns()
        #print(curr_time)
        prev_time = datetime.now() - timedelta(seconds = 2)
        prev_ns = int(time.mktime(prev_time.timetuple()) * pow(10, 9))
        #print(prev_ns)
        apiurl = "http://localhost:59880/api/v2/event/start/"+ str(prev_ns)+"/end/"+ str(curr_time)
        response = requests.get(apiurl)
        #print(response.json())
        events = response.json()['events']
        devnameset = set({})
        for e in events:
            devname =e['deviceName']
            devnameset.add(devname)
        activecnt = len(devnameset)
        cnt = gatewaycount_prov - activecnt
        return str(cnt)
    except Exception as e:
        return e    

@app.route('/api/v1/gateway/name/getdevicenames')
@cross_origin()
def getdevicenames():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        devicelist = response.json()['devices']
        cnt = 0
        devnameset = set({})
        for d in devicelist:
            devnameset.add(d['name'])
        return str(devnameset)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/name/getdevicedetails/all')
@cross_origin()
def getdevicedataall():
    unique_device_names = set()
    devices_info = []
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        deviceslist = response.json()['devices']
        for device in deviceslist:
            device_name = device['name']
            if device_name not in unique_device_names:
                unique_device_names.add(device_name)
                status = ''
                if devices['operatingState'] == "UP":
                    status = 'online'
                else:
                    status = 'offline'
		device_info = {
                    'id': device['id'],
                    'serviceName': device['serviceName'],
                    'profileName': device['profileName'],
                    'description':device['description'],
                    'location' : 'Hyderabad',
                    'associatedGateway' : 'Lenovo Gateway',
                    'associatedGwID' : device['id'],
                    'status' : status
		
                }
                devices_info.append(device_info)
        return str(devices_info)
    except Exception as e:
        return str(e), 500
            
#@app.route('/api/v1/gateway/telemetrydata/<devicename>')
#@cross_origin()
#def gettelemetrydata(devicename):
#    try:
#        apiurl = "http://localhost:59880/api/v2/reading/device/name/"+str(devicename)
#        response = requests.get(apiurl)
#        readingslist = response.json()['readings']
#        print(type(readingslist))
#        print(readingslist[0])
#        r = []

#	 curr_time = time.time_ns()
        #print(curr_time)
#        prev_time = datetime.now() - timedelta(seconds = 2)
#        prev_ns = int(time.mktime(prev_time.timetuple()) * pow(10, 9))
#        #print(prev_ns)
#        apiurl = "http://localhost:59880/api/v2/event/start/"+ str(prev_ns)+"/end/"+ str(curr_time)
#        response = requests.get(apiurl)
        #print(response.json())
#        events = response.json()['events']
#        devnameset = set({})
#        for e in events:
#            devname =e['deviceName']
#            devnameset.add(devname)
        
#        for rl in readingslist:
#            resource_name = rl['resourceName']
#            res = rl['value'] 
#            res2 = float(res)
#            print(res, type(res))
#            num = '{0:.2f}'.format(res2)		
#            print(num)
#            r.append({ resource_name : num })    		   
#            print(json.dumps(r))
#        return json.dumps(r)
#    except Exception as e:
#        return e 
        
@app.route('/api/v1/gateway/telemetrydata/<devicename>')
@cross_origin()
def gettelemetrydata(devicename):
    try:
        apiurl = "http://localhost:59880/api/v2/reading/device/name/"+str(devicename)
        response = requests.get(apiurl)
        readingslist = response.json()['readings']
        print(type(readingslist))
        print(readingslist[0])
        resource_name = readingslist[0]['resourceName']
        res = readingslist[0]['value'] 
        res2 = float(res)
        print(res, type(res))
        num = '{0:.2f}'.format(res2)
        print(num)
        r = {
        resource_name : num
        }
        return str(r)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/gatewaywrtmanu')
@cross_origin()
def getgatewaywrtmanu():
    try:
        apiurl = "http://localhost:59881/api/v2/deviceprofile/all"
        response = requests.get(apiurl)
        devicelist = response.json()['profiles']
        mp = {}
        cnt = 0
        for d in devicelist:
            if d['manufacturer'] in mp:
                mp[d['manufacturer']] += 1
            else:
                mp[d['manufacturer']] = 1
        print(mp) 
        print(str(mp))
        print("______________________________________________________________")
        print(json.dumps(mp))
        print(str(json.dumps(mp)))        
        return json.dumps(mp)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/gatewaywrtservice')
@cross_origin()
def getgatewaywrtservice():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        devicelist = response.json()['devices']
        mp = {}
        cnt = 0
        for d in devicelist:
            if d['serviceName'] in mp:
                mp[d['serviceName']] += 1
            else:
                mp[d['serviceName']] = 1
        print(mp)         
        return json.dumps(mp)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/gatewayconfigdata')
@cross_origin()
def getgatewayconfigdata():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        devicelist = response.json()['devices']
        mp = {}
        listd = []
        for d in devicelist:
            id_val =d['id']
            name = d['name']
            desc = d['description']
            service = d['servieName']
            profile = d['profileName']
            listd.append({"id": id_val,"name":name})
        print(listd)         
        return str(listd)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/profiles')
@cross_origin()
def getgatewayprofilelist():
    try:
        apiurl = "http://localhost:59881/api/v2/deviceprofile/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return e
        
@app.route('/api/v1/gateway/services')
@cross_origin()
def getgatewaydeviceservicelist():
    try:
        apiurl = "http://localhost:59881/api/v2/deviceservice/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return e      
                 
if __name__ == '__main__':
    app.run('0.0.0.0',5000,debug = True)

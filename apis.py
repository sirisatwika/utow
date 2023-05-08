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
from collections import OrderedDict

# creating a Flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
auth = HTTPBasicAuth()

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
        return eSS

        
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
            #print('active' + devname)
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
        apiurl = "http://localhost:59881/api/v2/device/all?limit=-1"
        response = requests.get(apiurl)
        devicelist = response.json()['devices']
        cnt = 0
        mp = {}
        cnt = 0
        for d in devicelist:
            if d['name'] in mp:
                mp[d['name']] += 1
            else:
                mp[d['name']] = 1
        #print(mp)
        lst = []         
        for k,v in mp.items():
            t = {'name':k,'data':v}
            lst.append(t)                                                                        
        return lst
    except Exception as e:
        return e
        

@app.route('/api/v1/gateway/name/getdevicenames/all')
@cross_origin()
def getdevicenamesall():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all?limit=-1"
        response = requests.get(apiurl)
        devicelist = response.json()['devices']
        lst = []
        for d in devicelist:
            lst.append(d['name'])
        return lst
    except Exception as e:
        return e

@app.route('/api/v1/gateway/name/getgatewaydetails/all')
@cross_origin()
def getgatewaydataall():
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
                createdtime = device['created']
                #print(createdtime)
                time_in_sec = createdtime / pow(10,9)
                dt = datetime.fromtimestamp(time_in_sec)
                form_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
                modifiedtime = device['modified']
                #print(modifiedtime)
                time_in_sec_m = modifiedtime / pow(10,9)
                dt_m = datetime.fromtimestamp(time_in_sec_m)
                form_dt_m = dt_m.strftime('%Y-%m-%d %H:%M:%S')

                if device['operatingState'] == "UP":
                    status = 'online'
                else:
                    status = 'offline'
                device_info = [
                    device['id'],
                    'Lenovo Gateway',
                    device.get('protocols',{}).get('modbus-tcp',{}).get('Address',''),
                    device.get('protocols',{}).get('modbus-tcp',{}).get('Port',''), 
                    'Hyderabad',
                    '00:25:96:FF:FE:12:34:56',
                    '748676',
                    'LT',
                    device['profileName'],
                    device['serviceName'],
                    device['description'],
                    status,
                    '',
                    '',
                    form_dt,
                    '',
                    form_dt_m,
                    '',
                    'Ubuntu 22.04',
                    'TLS 1.4/ SSL- 1.0',
                    'Active',
                    '23.45.67',
                    'Active'                    
                ]
                devices_info.append(device_info)
        return devices_info
    except Exception as e:
        return str(e), 500

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
                address = ''
                port = ''
                createdtime = device['created']
                #print(createdtime)
                time_in_sec = createdtime / pow(10,9)
                dt = datetime.fromtimestamp(time_in_sec)
                form_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
                modifiedtime = device['modified']
                #print(modifiedtime)
                time_in_sec_m = modifiedtime / pow(10,9)
                dt_m = datetime.fromtimestamp(time_in_sec_m)
                form_dt_m = dt_m.strftime('%Y-%m-%d %H:%M:%S')
                if device['operatingState'] == "UP":
                    status = 'online'
                else:
                    status = 'offline'
                device_info = [
                    device['id'],
                    device['name'],
                    device['description'],
                    device.get('protocols',{}).get('modbus-tcp',{}).get('Address',''),
                    device.get('protocols',{}).get('modbus-tcp',{}).get('Port',''),
                    'Hyderabad',
                    'Lenovo Gateway',
                    device['id'],
                    device['serviceName'],
                    device['profileName'],
                    status,
                    '',
                    '',
                    form_dt,
                    '',
                    form_dt_m                    
                ]
                devices_info.append(device_info)
        return devices_info
    except Exception as e:
        return str(e), 500
 

@app.route('/api/v1/gateway/name/getgatewaydetailsconfig/all')
@cross_origin()
def getgatewaydataallconfig():
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
                createdtime = device['created']
                #print(createdtime)
                time_in_sec = createdtime / pow(10,9)
                dt = datetime.fromtimestamp(time_in_sec)
                form_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
                modifiedtime = device['modified']
                #print(modifiedtime)
                time_in_sec_m = modifiedtime / pow(10,9)
                dt_m = datetime.fromtimestamp(time_in_sec_m)
                form_dt_m = dt_m.strftime('%Y-%m-%d %H:%M:%S')
                if device['operatingState'] == "UP":
                    status = 'online'
                else:
                    status = 'offline'
                device_info = [
                    device['id'],
                    'Lenovo Gateway',
                    device.get('protocols',{}).get('modbus-tcp',{}).get('Address',''),
                    device.get('protocols',{}).get('modbus-tcp',{}).get('Port',''), 
                    'Hyderabad',
                    device['profileName'],
                    device['serviceName'],
                    device['description'],
                    status,
                    '',
                    '',
                    form_dt,
                    '',
                    form_dt_m,
                    '',
                    '',
                    '',
                    'Ubuntu 22.04',
                    '',
                    'TLS 1.4/ SSL- 1.0',
                    '',
                    '23.45.67',
                    ''                   
                ]
                devices_info.append(device_info)
        return devices_info
    except Exception as e:
        return str(e), 500
    
    
@app.route('/api/v1/gateway/name/getdevicedetailsconfig/all')
@cross_origin()
def getdevicedataallconfig():
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
                createdtime = device['created']
                #print(createdtime)
                time_in_sec = createdtime / pow(10,9)
                dt = datetime.fromtimestamp(time_in_sec)
                form_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
                modifiedtime = device['modified']
                #print(modifiedtime)
                time_in_sec_m = modifiedtime / pow(10,9)
                dt_m = datetime.fromtimestamp(time_in_sec_m)
                form_dt_m = dt_m.strftime('%Y-%m-%d %H:%M:%S')
                if device['operatingState'] == "UP":
                    status = 'online'
                else:
                    status = 'offline'
                device_info = {
                    'IotDeviceID': device['id'],
                    'IOTDeviceName' : device['name'],
                    'IPAddress' :device.get('protocols',{}).get('modbus-tcp',{}).get('Address',''),
                    'PortNumber' :device.get('protocols',{}).get('modbus-tcp',{}).get('Port',''),
                    'location':'Hyderabad',
                    'AssociatedServiceProtocol':device['serviceName'],
                    'AssociatedGatewayProfile':device['profileName'],
                    'description':device['description'],
                    'Status':status,
                    'ProvisionedStatus':'',
                    'ProvisionedMethod':'',
                    'ProvisionedDateTime':form_dt,
                    'ActiveInactive':'',
                    'LastCommunicatedTime':form_dt_m,
                    'LastCommunicatedTime':''                    
                }
                devices_info.append(device_info)
        return devices_info
    except Exception as e:
        return str(e), 500

@app.route('/api/v1/gateway/telemetrydata/all')
@cross_origin()
def gettelemetrydataall():
    unique_device_names = set({})
    devices_info = []
    try:
        apiurlmain = "http://localhost:59881/api/v2/device/all?limit=-1"
        responsemain = requests.get(apiurlmain)
        #print(responsemain.json())
        devicelistmain = responsemain.json()['devices']
        #print(devicelistmain)
        for device in devicelistmain:
            device_name = device['name']
            #print(device)
            if device_name not in unique_device_names:
                unique_device_names.add(device_name)
                #print(unique_device_names)
                devproname = device['profileName']  
                apiurl2 = "http://localhost:59881/api/v2/deviceprofile/name/"+str(devproname)
                resdevproname = requests.get(apiurl2)
                #print(resdevproname)
                devresname = resdevproname.json()['profile']['deviceResources']
                devrescnt = len(devresname)  
                #print(devrescnt)              
                apiurl = "http://localhost:59880/api/v2/reading/device/name/"+str(device_name)
                response = requests.get(apiurl)
                readingslist = response.json()['readings']
                #print(readingslist)
                i = 0
                lst = []
                while i < devrescnt and readingslist != []:
                    resource_name = readingslist[i]['resourceName']
                    res = readingslist[i]['value'] 
                    num = res
                    if 'units' in readingslist[i]:
                        units = readingslist[i]['units']
                    else:
                        units = ""
                    #print(units)
                    print(type(res))
                    if '.' in res:
                       num = '{0:.2f}'.format(float(res))
                    r = [
                    	device_name,
                        resource_name,
                        num,
                        units
                    ]
                    i = i + 1
                    devices_info.append(r)
                #print(devices_info)
        return json.dumps(devices_info)
    except Exception as e:
        return e


     
@app.route('/api/v1/gateway/telemetrydata/<devicename>')
@cross_origin()
def gettelemetrydata(devicename):
    try:
        apiurl1 = "http://localhost:59881/api/v2/device/name/"+str(devicename)
        resdevname = requests.get(apiurl1)
        devproname = resdevname.json()['device']['profileName']  
        apiurl2 = "http://localhost:59881/api/v2/deviceprofile/name/"+str(devproname)
        resdevproname = requests.get(apiurl2)
        devresname = resdevproname.json()['profile']['deviceResources']
        devrescnt = len(devresname)
        
        apiurl = "http://localhost:59880/api/v2/reading/device/name/"+str(devicename)
        response = requests.get(apiurl)
        readingslist = response.json()['readings']
        #print(type(readingslist))
        #print(readingslist[0])
        i = 0
        lst = []
        while i < devrescnt:
            resource_name = readingslist[i]['resourceName']
            res = readingslist[i]['value'] 
            res2 = float(res)
            if 'units' in readingslist[i]:
                units = readingslist[i]['units']
            else:
                units = ""
            print(units)
            num = '{0:.2f}'.format(res2)
            r = {
             resource_name : [num, units] 
            }
            i = i + 1
            lst.append(r)
        return json.dumps(lst)
    except Exception as e:
        return e


# InfluxDB configuration
INFLUXDB_HOST = 'localhost'
INFLUXDB_PORT = 8086
INFLUXDB_USERNAME = 'admin'
INFLUXDB_PASSWORD = 'admin'
INFLUXDB_DATABASE = 'sensorsedgex'

# Create InfluxDB client
client = InfluxDBClient(host=INFLUXDB_HOST,port=INFLUXDB_PORT,username=INFLUXDB_USERNAME,
password=INFLUXDB_PASSWORD,
database=INFLUXDB_DATABASE)

@app.route('/api/v1/gateway/data/linegraph/<devicename>', methods=['GET'])
@cross_origin()
def getdataline(devicename):
    try:
        query = 'SELECT data,timestamp FROM '+devicename+';'
        result = client.query(query)
        lst = []
        for point in result.get_points():
            res = point['data']
            ts = point['timestamp']
            res2 = float(res)
            #num = '{0:.2f}'.format(res2)
            lgdata = {'value' : res2, 'timestamp' : ts}
            lst.append(lgdata)
            #print(num)
        #r = { devicename : lst }
        #print(type(r))
        od = OrderedDict()
        for d in sorted(lst, key = lambda x : x['timestamp']):
            od[d['timestamp']] = d['value']
        return jsonify(od)
    except Exception as e:
        return str(e)
        

@app.route('/api/v1/gateway/data/minmax/<devicename>')
@cross_origin()
def getdataminmax(devicename):
    try:
        apiurl = "http://localhost:59881/api/v2/deviceprofile/name/"+str(devicename)
        response = requests.get(apiurl)
        pro = response.json()['profile']
        lst = []
        maximum = pro['deviceResources'][0]['properties']['maximum']
        minimum = pro['deviceResources'][0]['properties']['minimum']
        lst.append(minimum)
        lst.append(maximum)
        r = {
        devicename : lst
        }
        return json.dumps(r)
    except Exception as e:
        return str(e)


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
        #print(mp) 
        #print(str(mp))
        #print("______________________________________________________________")
        #print(json.dumps(mp))
        #print(str(json.dumps(mp)))        
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
        #print(mp)         
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
        #print(listd)         
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
Footer


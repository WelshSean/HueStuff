#!/usr/bin/env python3

import json
import requests
import os
#HUE_BRIDGE=os.environ["HUE_BRIDGE"]
#USER_ID=os.environ["USER_ID"]
HUE_DETAILS=os.environ["HUE_DETAILS"]


#SENSOR_URL = 'http://' + HUE_BRIDGE + '/api/' + USER_ID + '/sensors'

def getSensorInfo(sensor_url):
  try:
    response = requests.get(sensor_url)
    json_data = json.loads(response.text)
    return json_data
  except:
    logger.exception("exception occurred")

def printSensorInfo(sensor_url):
    print( json.dumps(getSensorInfo(sensor_url), indent=4, sort_keys=True))


def findSensorByType(sensortype,sensor_url):
    ids=[]
    for (key, data) in getSensorInfo(sensor_url).items():
        if data["type"] == sensortype:
            ids.append((key,data))
    return ids

def getTemps():
    temps=[]
    for detail in HUE_DETAILS.split():
        print("DETAIL: "+detail)
        (HUE_BRIDGE,USER_ID)=detail.split(':') 
        sensor_url = 'http://' + HUE_BRIDGE + '/api/' + USER_ID + '/sensors'
        # Get mappings of UUID to Human Friendly name
        mappings = getID2NameMapping(sensor_url)
        #print(mappings)
        sensors = findSensorByType("ZLLTemperature", sensor_url)
        if sensors is not None:
            for sensor in sensors:
                if sensor[1]["state"]["temperature"] is None:
                    #print("Found None value - skipping")
                    continue
                #print(sensor)
                tempdict={}
                temp_id=sensor[1]["uniqueid"]
                tempdict["name"]=mappings[temp_id[:-5]]
                tempdict["temperature"]=sensor[1]["state"]["temperature"]/100
                temps.append(tempdict)
        else:
            print("list empty")
    return temps

def getID2NameMapping(sensor_url):
    mappings={}
    sensors = findSensorByType("ZLLPresence", sensor_url)
    for sensor in sensors:
        mappings[sensor[1]["uniqueid"][:-5]] = sensor[1]["name"]
    return mappings

if __name__ == "__main__":
    #print(getID2NameMapping())
    print(json.dumps(getTemps()))

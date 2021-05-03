#!/usr/bin/env python3

import json
import requests
import os
HUE_BRIDGE=os.environ["HUE_BRIDGE"]
USER_ID=os.environ["USER_ID"]



SENSOR_URL = 'http://' + HUE_BRIDGE + '/api/' + USER_ID + '/sensors'

def getSensorInfo():
  try:
    response = requests.get(SENSOR_URL)
    json_data = json.loads(response.text)
    return json_data
  except:
    logger.exception("exception occurred")

def printSensorInfo():
    print( json.dumps(getSensorInfo(), indent=4, sort_keys=True))


def findSensorByType(sensortype):
    ids=[]
    for (key, data) in getSensorInfo().items():
        if data["type"] == sensortype:
            ids.append((key,data))
    return ids

def getTemps():
    temps=[]
    # Get mappings of UUID to Human Friendly name
    mappings = getID2NameMapping()
    #print(mappings)
    sensors = findSensorByType("ZLLTemperature")
    if sensors is not None:
        for sensor in sensors:
            tempdict={}
            temp_id=sensor[1]["uniqueid"]
            tempdict["name"]=mappings[temp_id[:-5]]
            tempdict["temperature"]=sensor[1]["state"]["temperature"]/100
            temps.append(tempdict)
    else:
        print("list empty")
    return temps

def getID2NameMapping():
    mappings={}
    sensors = findSensorByType("ZLLPresence")
    for sensor in sensors:
        mappings[sensor[1]["uniqueid"][:-5]] = sensor[1]["name"]
    return mappings

if __name__ == "__main__":
    #print(getID2NameMapping())
    print(json.dumps(getTemps()))

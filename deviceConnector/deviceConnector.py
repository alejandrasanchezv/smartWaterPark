import paho.mqtt.client as PahoMQTT
import time
import json
import requests
import cherrypy

from mqttClass import *
from devices import *

database = "devices.json"
resourceCatUrl = 'http://resource_catalog:8080'
#counterID = 0
#airID = 0
#waterLevelID = 0
#phID = 0
#airpumpID = 0
#valveID = 0
#chlorineValveID = 0
#lightsID = 0
#fansID = 0
#callMaintID = 0

class DatabaseClass(object):
  def POST(self, *path, **queries):
    global database, usrID, rideID

    input = json.loads(cherrypy.reques.body.read())

    with open(database, "r") as file:
      db = json.load(file)
    
    try:
      typeStrat = input['typeStrategy']
      db['strategies'][typeStrat]
    except:
      raise cherrypy.HTTPError(400, 'Strategy not found')
    
    if typeStrat == "maintenance":
      try:
        stratID = input["strategyID"]
      except:
        raise cherrypy.HTTPError(400, 'Strategy ID not found')
      else:
        stratTopic = "smartWaterPark/maintenance/strategy/"+ str(stratID) +"/user_" + str(usrID) + "/ride_" + str(rideID) + "/#"
        devMqtt.subscribe(stratTopic)
        db['strategies'][typeStrat].append(stratTopic)
    elif typeStrat == "water":
      try:
        stratID = input["strategyID"]
      except:
        raise cherrypy.HTTPError(400, 'Strategy ID not found')
      else:
        stratTopic = "smartWaterPark/water/strategy/"+ str(stratID) +"/user_" + str(usrID) + "/ride_" + str(rideID) + "/#"
        devMqtt.subscribe(stratTopic)
        db['strategies'][typeStrat].append(stratTopic)
    elif typeStrat == "comfort":
      try:
        stratID = input["strategyID"]
      except:
        raise cherrypy.HTTPError(400, 'Strategy ID not found')
      else:
        stratTopic = "smartWaterPark/comfort/strategy/"+ str(stratID) +"/user_" + str(usrID) + "/ride_" + str(rideID) + "/#"
        devMqtt.subscribe(stratTopic)
        db['strategies'][typeStrat].append(stratTopic)
    else:
      stratTopic = "smartWaterPark/" + str(typeStrat) + "/user_" + str(usrID) + "/ride_" + str(rideID) + "/#"
      devMqtt.subscribe(stratTopic)
      db['strategies'][typeStrat].append(stratTopic)

    with open(database, "w") as file:
      json.dump(db, file, indent=3)

    result = {
      "typeStrategy": typeStrat
    }
    
    return result
  
  def DELETE(self, *path, **queries):
    global database

    with open(database, "r") as file:
      db = json.load(file)

    try:
      typeStrat = queries['typeStrategy']
      db['strategies'][typeStrat]
    except:
      raise cherrypy.HTTPError(400, 'Strategy type not found')
    
    try:
      if typeStrat == "maintenance":
        try:
          stratID = queries['stratID']
        except:
          db['strategies']['maintenance'] = []
        else:
          for topic in range(len(db['strategies']['maintenance'])):
            topic_levels = topic.split('/')[1]
            if int(topic_levels[4]) == int(stratID):
              #ELIMINARLA
              devMqtt.unsubscribe(topic)
              break
      elif typeStrat == "water":
        devMqtt.unsubscribe(topic)
        db["strategies"]["water"] = []
      else:
        devMqtt.unsubscribe(topic)
        db["strategies"][typeStrat] = []

      with open(database, "w") as file:
        json.load(db, file, indent=3)
      
      result = {
        "typeStrategy": typeStrat
      }
      
      return result
    except:
      print('No strategy registered')
              
class Publisher(object):
  def __init__(self, sensors, actuators, strategies):
    global database#, counterID, airID, waterLevelID, phID,\
      #airpumpID, valveID, chlorineValveID, lightsID, fansID, callMaintID

    self.sensorsList = sensors
    self.actuatorsList = actuators
    self.strategies = strategies
    
    self.sensorsMaintenance = []
    self.sensorsWater = []
    sensorID = 0

    for sensor in self.sensorsList:
      if sensor == "counterRides":
        self.sensorsMaintenance.append(Sensor(sensorID, sensor))
      elif sensor == "airWeight":
        self.sensorsMaintenance.append(Sensor(sensorID, sensor))
      elif sensor == "waterLevel":
        self.sensorsWater.append(Sensor(sensorID, sensor))
      elif sensor == "phSensor":
        self.sensorsWater.append(Sensor(sensorID, sensor))
      sensorID += 1

    self.actuatorsMaintenance = []
    self.actuatorsWater = []
    self.actuatorsComfort = []
    actuatorID = 0

    # Actuator are always initialized as off
    for actuator in self.actuatorsList: 
      if actuator == "airPump":
        self.actuatorsMaintenance.append(Actuator(actuatorID, False, actuator))
      elif actuator == "maintenanceCall":
        self.actuatorsMaintenance.append(Actuator(actuatorID, False, actuator))
      elif actuator == "waterValve":
        self.actuatorsWater.append(Actuator(actuatorID, False, actuator))
      elif actuator == "chlorineValve":
        self.actuatorsWater.append(Actuator(actuatorID, False, actuator))
      elif actuator == "lights":
        self.actuatorsComfort.append(Actuator(actuatorID, False, actuator))
      elif actuator == "fans":
        self.actuatorsComfort.append(Actuator(actuatorID, False, actuator))
      actuatorID += 1

    self.maintenance = Maintenance(self.sensorsMaintenance, self.actuatorsMaintenance)
    self.water = Water(self.sensorsWater, self.actuatorsWater)
    self.comfort = Comfort(self.actuatorsComfort, "Turin")

  def onMsgReceived(device1, userdata, msg):
    print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")

  def publishSensorReading(self, sensorType):
    global database, usrID, rideID

    with open(database, "r") as file:
      db = json.load(file)

    strategy = ""
    for sensor in self.sensorsList:
      if sensor == "counterRides":
        strategy = "maintenance"
      elif sensor == "airWeight":
        strategy = "maintenance"
      elif sensor == "waterLevel":
        strategy = "water"
      elif sensor == "phSensor":
        strategy = "water"
      sensor.readvalue(sensorType)

    if strategy == "":
      print('Sensor type not reccognized')
      return
    else:
      sensorTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/" + strategy + "/sensors/"+ sensorType
      #sensor.readvalue(sensorType)
      devMqtt.publish(sensorTopic, sensor.value[sensorType])


def postFunc():
  global database

  with open(database, "r") as file:
    db = json.load(file)

  payload = {
    "userID": db['userID'],
    "rideID": db['rideID'],
    "sensors": db['devices']['sensors'],
    "actuators": db['devices']['actuators']
  }

  url = resourceCatUrl +'/device_connectors'
  requests.post(url, json.dumps(payload))

if __name__ == "__main__":
  conf = {
      '/': {
          'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
          'tools.sessions.on': True,
      }
  }
  cherrypy.tree.mount(DatabaseClass(), '/dbTopic', conf)
  cherrypy.config.update({'server.socket_host': '0.0.0.0'})
  cherrypy.engine.start()

  with open(database, "r") as file:
      db = json.load(file)

  usrID = db["userID"]
  rideID = db["rideID"]
  topic = "smartWaterPark/devConnector/user_" + str(usrID) + "/ride_" + str(rideID) + "/#"
  client = "devConnector" + str(usrID)
  devMqtt = ClientMQTT(client, [topic],onMessageReceived=Publisher.onMsgReceived)
  devMqtt.start()

  sensors = db["devices"]["sensors"]
  actuators = db["devices"]["actuators"]
  strategies = db["strategies"]

  devConnector = Publisher(sensors, actuators, strategies)
  timeLastDB = time.time()
  timeLastSensors = time.time()
  timeLimitSensors = 6 # number in seconds
  timeLimitDB = 15 # number in seconds
  while True:
    timeNow = time.time()
    if (timeNow - timeLastDB) >= timeLimitDB:
      postFunc()
      timeLastDB = timeNow
    elif (timeNow - timeLastSensors) >= timeLimitSensors:
      for sensortype in sensors:
        devConnector.publishSensorReading(sensortype)
        time.sleep(0.5)
      timeLastSensors = time.time()

    time.sleep(3)
    #devMqtt.publish('temp/iot/deviceConnector', 23.4)
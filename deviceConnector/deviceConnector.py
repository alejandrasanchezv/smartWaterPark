import paho.mqtt.client as PahoMQTT
import time
import json
import requests
import cherrypy

from mqttClass import *
from devices import *

database = "./devices.json"
resourceCatUrl = 'http://127.0.0.1:8080'
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
  exposed = True

  def POST(self, **params):
    global database, usrID, rideID

    input = params

    print(params)

    with open(database, "r") as file:
      db = json.load(file)
    
    try:
      typeStrat = input['typeStrategy']
      db['strategies'][typeStrat]
    except:
      raise cherrypy.HTTPError(400, 'Strategy not found')
    
    if typeStrat == "maintenance":
      stratTopicSensor1 = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/maintenance/sensors/counterRides/#"
      stratTopicSensor2 = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/maintenance/sensors/airWeight/#"
      devMqtt.subscribe(stratTopicSensor1)
      db['strategies'][typeStrat].append(stratTopicSensor1)
      devMqtt.subscribe(stratTopicSensor2)
      db['strategies'][typeStrat].append(stratTopicSensor2)
    elif typeStrat == "water":
      stratTopicSensor1 = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/water/sensors/waterLevel/#"
      stratTopicSensor2 = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/water/sensors/phSensor/#"
      devMqtt.subscribe(stratTopicSensor1)
      db['strategies'][typeStrat].append(stratTopicSensor1)
      devMqtt.subscribe(stratTopicSensor2)
      db['strategies'][typeStrat].append(stratTopicSensor2)
    elif typeStrat == "comfort":
      stratTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/comfort/#"
      devMqtt.subscribe(stratTopic)
      db['strategies'][typeStrat].append(stratTopic)
    else:
      stratTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/" + str(typeStrat) + "/#"
      devMqtt.subscribe(stratTopic)
      db['strategies'][typeStrat].append(stratTopic)

    with open(database, "w") as file:
      json.dump(db, file, indent=3)

    result = {
      "typeStrategy": typeStrat
    }
    
    return result
  
  def DELETE(self, **params):
    global database

    with open(database, "r") as file:
      db = json.load(file)

    try:
      typeStrat = params['typeStrategy']
      db['strategies'][typeStrat]
    except:
      raise cherrypy.HTTPError(400, 'Strategy type not found')
    
    try:
      if typeStrat == "maintenance":
        for topic in db['strategies']['maintenance']:
          devMqtt.unsubscribe(topic)
        db["strategies"]["maintenance"] = []
      elif typeStrat == "water":
        for topic in db['strategies']['water']:
          devMqtt.unsubscribe(topic)
        db["strategies"]["water"] = []
      else:
        for topic in db['strategies'][typeStrat]:
          devMqtt.unsubscribe(topic)
        db["strategies"][typeStrat] = []

      print(f'db: {db}')
      with open(database, "w") as file:
        json.dump(db, file, indent=3)
      
      result = {
        "typeStrategy": typeStrat
      }
      
      return result
    except:
      print('No strategy registered')
              
class Publisher(object):
  def __init__(self, sensors, actuators, strategies):
    global database

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

    sensorTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/"
    for sensor in self.sensorsList:
      if sensor == "counterRides":
        for sensorM in self.sensorsMaintenance:
          sensorM.readvalue(sensorM)
          topic = sensorTopic + "maintenance/sensors/counterRides/sensorid/"+ str(sensorM.id)
          devMqtt.publish(topic, sensorM.value)
      elif sensor == "airWeight":
        for sensorM in self.sensorsMaintenance:
          sensorM.readvalue(sensorM)
          topic = sensorTopic + "maintenance/sensors/airWeight/sensorid/"+ str(sensorM.id)
          devMqtt.publish(topic, sensorM.value)
      elif sensor == "waterLevel":
        for sensorw in self.sensorsWater:
          sensorw.readvalue(sensorw)
          topic = sensorTopic + "water/sensors/waterLevel/sensorid/"+ str(sensorw.id)
          devMqtt.publish(topic, sensorw.value)
      elif sensor == "phSensor":
        for sensorw in self.sensorsWater:
          sensorw.readvalue(sensorw)
          topic = sensorTopic + "water/sensors/phSensor/sensorid/"+ str(sensorw.id)
          devMqtt.publish(topic, sensorw.value)

    print('End publishing')
    

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

  url = resourceCatUrl +'/device_connector'
  requests.post(url, json.dumps(payload))

if __name__ == "__main__":
  conf = {
      '/': {
          'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
          'tools.sessions.on': True,
      }
  }
  cherrypy.tree.mount(DatabaseClass(), '/dbTopic', conf)
  cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': 8099})
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
  timeLimitSensors = 30 # number in seconds
  timeLimitDB = 75 # number in seconds
  postFunc()
  while True:
    timeNow = time.time()
    if (timeNow - timeLastDB) >= timeLimitDB:
      postFunc()
      timeLastDB = timeNow
    elif (timeNow - timeLastSensors) >= timeLimitSensors:
      for sensortype in sensors:
        devConnector.publishSensorReading(sensortype)
        #print(sensortype)
        time.sleep(1)
      timeLastSensors = time.time()

    time.sleep(3)
    #devMqtt.publish('temp/iot/deviceConnector', 23.4)
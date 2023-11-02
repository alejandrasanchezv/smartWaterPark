import paho.mqtt.client as PahoMQTT
import time
import json
#import requests
#import cherrypy

from mqttClass import *
from devices import *

database = "devices.json"
counterID = 0
airID = 0
waterLevelID = 0
phID = 0
airpumpID = 0
valveID = 0
chlorineValveID = 0
lightsID = 0
fansID = 0
callMaintID = 0

class Publisher(object):
  def __init__(self, sensors, actuators, strategies):
    global database, counterID, airID, waterLevelID, phID,\
      airpumpID, valveID, chlorineValveID, lightsID, fansID, callMaintID

    self.sensorsList = sensors
    self.actuatorsList = actuators
    self.strategies = strategies
    
    self.sensorsMaintenance = []
    self.sensorsWater = []

    for sensor in self.sensorsList:
      if sensor == "counterRides":
        self.sensorsMaintenance.append(Sensor(counterID, sensor))
      elif sensor == "airWeight":
        self.sensorsMaintenance.append(Sensor(airID, sensor))
      elif sensor == "waterLevel":
        self.sensorsWater.append(Sensor(waterLevelID, sensor))
      elif sensor == "phSensor":
        self.sensorsWater.append(Sensor(phID, sensor))

    self.actuatorsMaintenance = []
    self.actuatorsWater = []
    self.actuatorsComfort = []

    # Actuator are always initialized as off
    for actuator in self.actuatorsList: 
      if actuator == "airPump":
        self.actuatorsMaintenance.append(Actuator(airpumpID, False, actuator))
      elif actuator == "maintenanceCall":
        self.actuatorsMaintenance.append(Actuator(callMaintID, False, actuator))
      elif actuator == "waterValve":
        self.actuatorsWater.append(Actuator(valveID, False, actuator))
      elif actuator == "chlorineValve":
        self.actuatorsWater.append(Actuator(chlorineValveID, False, actuator))
      elif actuator == "lights":
        self.actuatorsComfort.append(Actuator(lightsID, False, actuator))
      elif actuator == "fans":
        self.actuatorsComfort.append(Actuator(fansID, False, actuator))

    self.maintenance = Maintenance(self.sensorsMaintenance, self.actuatorsMaintenance)
    self.water = Water(self.sensorsWater, self.actuatorsWater)
    self.comfort = Comfort(self.actuatorsComfort, "Turin")

  def onMsgReceived(device1, userdata, msg):
    print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")




if __name__ == "__main__":
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
	
  while True:
    time.sleep(3)
    devMqtt.publish('temp/iot/deviceConnector', 23.4)
    #pass
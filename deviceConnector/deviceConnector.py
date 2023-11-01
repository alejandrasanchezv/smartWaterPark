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
  def __init__(self, client):
    global database, counterID, airID, waterLevelID, phID,\
      airpumpID, valveID, chlorineValveID, lightsID, fansID, callMaintID
    
    with open(database, "r") as file:
      db = json.load(file)

    usrID = db["userID"]
    rideID = db["rideID"]
    self.topic = "smartWaterPark/devConnector/user_" + str(usrID) + "/ride_" + str(rideID) + "/#"
    self.client = client + str(usrID)
    self.mqttClient = ClientMQTT(self.client, [self.topic],onMessageReceived=onMsgReceived)

    self.sensorsList = db["devices"]["sensors"]
    self.actuatorsList = db["devices"]["actuators"]
    self.strategies = db["strategies"]
    self.sensors = []
    self.actuators = []

    for sensor in self.sensorsList:
      if sensor == "counterRides":
        self.sensors.append(Sensor(counterID, sensor))
      elif sensor == "airWeight":
        self.sensors.append(Sensor(airID, sensor))
      elif sensor == "waterLevel":
        self.sensors.append(Sensor(waterLevelID, sensor))
      elif sensor == "phSensor":
        self.sensors.append(Sensor(phID, sensor))

    # Actuator are always initialized as off
    for actuator in self.actuatorsList: 
      if actuator == "airPump":
        self.actuators.append(Actuator(airpumpID, False, actuator))
      elif actuator == "maintenanceCall":
        self.actuators.append(Actuator(callMaintID, False, actuator))
      elif actuator == "waterValve":
        self.actuators.append(Actuator(valveID, False, actuator))
      elif actuator == "chlorineValve":
        self.actuators.append(Actuator(chlorineValveID, False, actuator))
      elif actuator == "lights":
        self.actuators.append(Actuator(lightsID, False, actuator))
      elif actuator == "fans":
        self.actuators.append(Actuator(fansID, False, actuator))

  def onMsgReceived(device1, userdata, msg):
    print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")




if __name__ == "__main__":

  devMqtt = Publisher("devConnector")
  devMqtt.start()
	
  while True:
    time.sleep(3)
    devMqtt.publish('temp/iot/deviceConnector', 23.4)
    #pass
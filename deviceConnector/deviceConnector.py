import paho.mqtt.client as PahoMQTT
import time
import json
#import requests
#import cherrypy

from mqttClass import *

database = "devices.json"

class publisher(object):
  def __init__(self):
    global database, usrID, rideID

    self.sensors = db["devices"]["sensors"]
    self.actuators = db["devices"]["actuators"]
    self.strategies = db["strategies"]


  

def onMsgReceived(device1, userdata, msg):
    print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")

with open(database, "r") as file:
  db = json.load(file)

usrID = db["userID"]
rideID = db["rideID"]


if __name__ == "__main__":
  topic = "smartWaterPark/devConnector/user_" + str(usrID) + "/ride_" + str(rideID) + "/#"
  client = "devConnector" + str(usrID)
  devMqtt = ClientMQTT(client, [topic],onMessageReceived=onMsgReceived)

  devMqtt.start()
	
  while True:
    time.sleep(3)
    devMqtt.publish('temp/iot/deviceConnector', 23.4)
    #pass
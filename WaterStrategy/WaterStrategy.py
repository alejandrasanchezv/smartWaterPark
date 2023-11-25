import paho.mqtt.client as PahoMQTT
import time
import json
import requests
import cherrypy

from mqttClass import *
database = "./waterDB.json"

resCatEndpoints = "http://127.0.0.1:8080"

class WaterStrategy(object):
    exposed = True

    def POST(self, **params):
        global database, db, newStrat

        input = params
        print(params)

        try:
            usrID = input['userID']
            rideID = input['rideID']
            stratID = input['strategyID']
            stratStatus = input['strategyStatus']
        except:
            raise cherrypy.HTTPError(400, 'Wrong input')
        
        stratTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/water/" + str(stratID)

        with open(database, "r") as file:
            db = json.load(file)

        newStrat = {
            "topic": stratTopic, 
            "status": stratStatus, 
            "timestamp": time.time()
        }
        db["strategies"].append(newStrat)

with open(database, "r") as file:
    db = json.load(file)

if __name__ == "__main__":
  conf = {
      '/': {
          'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
          'tools.sessions.on': True,
      }
  }
  cherrypy.tree.mount(WaterStrategy(), '/dbTopic', conf)
  cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': 8099})
  cherrypy.engine.start()
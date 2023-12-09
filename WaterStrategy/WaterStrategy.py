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
        """
        Registers a new strategy for a specific user and ride
        Updates the state of the strategy on the ride
        """
        global database, db, newStrat, dbTest

        input = params
        print(params)

        try:
            usrID = input['userID']
            rideID = input['rideID']
            stratID = input['strategyID']
            stratStatus = input['strategyStatus']
            stratActive = input['strategies']
        except:
            raise cherrypy.HTTPError(400, 'Wrong input')
        
        stratTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/water/" + str(stratID)

        with open(database, "r") as file:
            db = json.load(file)

        newStrat = {
            "topic": stratTopic, 
            "status": stratStatus, 
            "strat": stratActive,
            "timestamp": time.time()
        }
        db['strategies'].append(newStrat)

        if stratStatus == False:
            user = "user_" + str(usrID)
            ride = "ride_" + str(rideID)
            for strat in db['strategies']:
                root_topic = strat['topic'].split('/')
                if root_topic[1] == user and root_topic[2] == ride:
                    strat['strategyStatus'] = stratStatus

        with open(database, "w") as file:
            json.dump(db, file, indent=3)

        with open(database, "r") as file:
            dbTest = json.load(file)

        result = {
            "userID": usrID,
            "rideID": rideID,
            "status": stratStatus,
            "timestamp": time.time()
        }

        return result
    
    def PUT(self, **params):
        """
        Modify the strategy state of a ride owned by the specified user
        """
        global database, db, newStrat, dbTest

        input = params
        print(params)

        with open(database, "r") as file:
            db = json.load(file)

        try:
            usrID = input['userID']
            rideID = input['rideID']
            stratStatus = input['strategyStatus']
        except:
            raise cherrypy.HTTPError(400, 'Wrong input')
        
        try:
            stratID = input['strategyID']
        except:
            user = "user_" + str(usrID)
            ride = "ride_" + str(rideID)
            for strat in db['strategies']:
                root_topic = strat['topic'].split('/')
                if root_topic[1] == user and root_topic[2] == ride:
                    strat['strategyStatus'] = stratStatus
        else:
            user = "user_" + str(usrID)
            ride = "ride_" + str(rideID)
            for strat in db['strategies']:
                root_topic = strat['topic'].split('/')
                if root_topic[1] == user and root_topic[2] == ride and int(root_topic[4]) == int(stratID):
                    strat['strategyStatus'] = stratStatus

        with open(database, "w") as file:
            json.dump(db, file, indent=3)

        with open(database, "r") as file:
            dbTest = json.load(file)

        result = {
            "userID": usrID,
            "rideID": rideID,
            "status": stratStatus,
            "timestamp": time.time()
        }

        return result
    
    def DELETE(self, **params):
        """
        Registers a new strategy for a specific user and ride
        Updates the state of the strategy on the ride
        """
        global database, db, newStrat, dbTest

        input = params
        print(params)

        try:
            usrID = input['userID']
            rideID = input['rideID']
            stratID = input['strategyID']
        except:
            try :
                usrID = input['userID']
                rideID = input['rideID']
            except:
                raise cherrypy.HTTPError(400, 'Bad request')
            else:
                # No stratID -> it means that all the strategies must be eliminated
                with open(database, "r") as file:
                    db = json.load(file)

                index = []
                user = "user_" + str(usrID)
                ride = "ride_" + str(rideID)
                for i, strat in enumerate(db['strategies']):
                    root_topic = strat['topic'].split('/')
                    if root_topic[1] == user and root_topic[2] == ride:
                       index.append(i)

                index.sort(reverse=True) #decendign order
                for i in index:
                    db['strategies'].pop(i)

                with open(database, "w") as file:
                    json.dump(db, file, indent=3)

                with open(database, "r") as file:
                    dbTest = json.load(file)

                return
        else:
            stratTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/water/" + str(stratID)
            
            with open(database, "r") as file:
                db = json.load(file)

            i = 0
            for strat in db['strategies']:
                if strat['topic'] != stratTopic:
                    i += 1

            try:
                db['strategies'].pop(i)

                ##################################################################
                for strat in db['strategies']:
                    root_topic = strat['topic'].split('/')
                    if root_topic[1] == user and root_topic[2] == ride and int(root_topic[4]) > int(stratID):
                        stid = int(root_topic[4]) - 1
                        stratTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/water/" + str(stid)

                with open(database, "w") as file:
                    json.dump(db, file, indent=3)

                with open(database, "r") as file:
                    dbTest = json.load(file)

            except:
                print('NO STRATEGY REGISTERED')

            result = {
                "userID": usrID,
                "rideID": rideID,
                "timestamp": time.time()
            }
                
            return result
        
class waterPublisher(object):

    def __init__(self) -> None:
        pass

    def onMsgReceived(device1, userdata, msg):
        print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")

with open(database, "r") as file:
    db = json.load(file)

with open(database, "r") as file:
    dbTest = json.load(file)

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
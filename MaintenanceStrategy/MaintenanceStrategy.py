import paho.mqtt.client as PahoMQTT
import time
import json
import requests
import cherrypy

from mqttClass import *
database = "maintenanceDB.json"

resCatEndpoints = "http://127.0.0.1:8080"

class MaintenanceStrategy(object):
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
        
        stratTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/maintenance/" + str(stratID)

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

        """
        result = {
            "userID": usrID,
            "rideID": rideID,
            "stratID": stratStatus,
            "status": stratStatus,
            "topic": topic,
            "isinMaint": false,
            "numMaint": 0,
            "alert": 0,
            "timestamp": time.time()
        } 
        """

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
            stratTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/maintenance/" + str(stratID)
            
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
                        stratTopic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/maintenance/" + str(stid)

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
        
class maintenancePublisher(object):

    def __init__(self) -> None:
        pass

    def onMsgReceived(self, userdata, msg):
        print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")
        value = json.loads(msg.payload)
        topic = msg.topic

        user_topic = topic.split('/')[1]
        ride_topic = topic.split('/')[2]

        with open(database, "r") as file:
            db = json.load(file)

        try:
            for strat in db['strategies']:
                user = "user_" + str(strat['userID'])
                ride = "ride_" + str(strat['rideID'])

                if user_topic == user and ride_topic == ride:
                    chosenstrat = strat
                    userid = strat['userID']
                    rideid = strat['rideID']
                    break

            maxRides = db['strategies'][chosenstrat]['maxRides']
            counterRides = db['strategies'][chosenstrat]['counterRides']
        except:
            raise cherrypy.HTTPError(400, 'User not found')

        if user == user_topic:
            if ride == ride_topic:
                sensor_topic = topic.split('/')[5]
                if sensor_topic == "sensors":
                    for sensor in db['sensors']:
                        if sensor == "counterRides":
                            counterRides += value
                            alertStatus = 0
                            alertTopic = "smartWaterPark/thingSpeak/user/" + str(userid) + "/ride/" + str(rideid) + "/stateAlert"
                            if counterRides >= round(maxRides*0.95):
                                alertStatus = 3
                            elif counterRides >= round(maxRides*0.9):
                                alertStatus = 2
                            elif counterRides >= round(maxRides*0.8):
                                alertStatus = 1
                            else:
                                print('No alert')
                                alertStatus = 0
                            self.publish(alertTopic, alertStatus)   
                        elif sensor == "airWeight":
                            pass

with open(database, "r") as file:
    db = json.load(file)


if __name__ == "__main__":
  conf = {
      '/': {
          'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
          'tools.sessions.on': True,
      }
  }
  cherrypy.tree.mount(MaintenanceStrategy(), '/dbTopic', conf)
  cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': 8094})
  cherrypy.engine.start()

  
  with open(database, "r") as file:
    db = json.load(file)

  usrID = 1 #db["userID"]
  rideID = 0 #db["rideID"]
  topic = "smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/maintenance/#"
  client = "devConnector" + str(usrID)
  maintMqtt = ClientMQTT(client, [topic],onMessageReceived=maintenancePublisher.onMsgReceived)
  maintMqtt.start()
  
  alertTopicEx = "smartWaterPark/thingSpeak/user/" + str(usrID) + "/ride/" + str(rideID)

  time.sleep(2)

  alertEx = alertTopicEx + "/stateAlert"
  maintMqtt.publish(alertEx, 2)

  time.sleep(12)

  numEx =  alertTopicEx + "/numMaint"
  maintMqtt.publish(numEx, 1)

  time.sleep(12)

  inMaintEx =  alertTopicEx + "/isinMaint"
  maintMqtt.publish(inMaintEx, 0)

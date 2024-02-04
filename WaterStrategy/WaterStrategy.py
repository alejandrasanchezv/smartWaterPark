import paho.mqtt.client as PahoMQTT
import time
import json
import requests
import cherrypy

from mqttClass import *
database = "waterDB.json"

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
            db = json.dump(db, file, indent=3)

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
        
class WaterPublisher(object):

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

        
        for strat in db['strategies']:
            user = "user_" + str(strat['userID'])
            ride = "ride_" + str(strat['rideID'])

            if user_topic == user and ride_topic == ride:
                chosenstrat = strat
                userid = strat['userID']
                rideid = strat['rideID']
                break
        
        try:
            waterThreshold = db['strategies'][chosenstrat]['waterThreshold']
            phThreshold = db['strategies'][chosenstrat]['phThreshold']
            strategyStatus = db['strategies'][chosenstrat]['strategyStatus']
        except:
            raise cherrypy.HTTPError(400, 'User not found')

        if strategyStatus:
            if user == user_topic:
                if ride == ride_topic:
                    sensor_topic = topic.split('/')[5]
                    if sensor_topic == "sensors":
                        for sensor in db['sensors']:
                            if sensor == "waterLevel":
                                waterLevel = float(value)
                                valveStatus = False
                                if (waterThreshold + 0.1*waterThreshold) >= waterLevel:
                                    # Water level is too high -> valve should be closed
                                    valveStatus = False
                                elif (waterThreshold - 0.1*waterThreshold) >= waterLevel:
                                    # Water level is too high -> valve should be opened
                                    valveStatus = True
                                else:
                                    print('WATER IS IN NORMAL RANGE') # we don't need the valve to be opened
                                    valveStatus = False

                                dcTopic = "smartWaterPark/devConnector/user_" + str(usrID) + "/ride_" + str(rideID) + "/waterValve"
                                self.publish(dcTopic, valveStatus)
        else:
            print('STRATEGY IS NOT ACTIVE') 

def postFunc():
    with open(database, "r") as file:
        db = json.load(file)

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
  cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': 8094})
  cherrypy.engine.start()

  with open(database, "r") as file:
    db = json.load(file)

  usrID = 1 #db["userID"]
  rideID = 1 #db["rideID"]
  
  url = resCatEndpoints + "/device_connector"
  stratDB = requests.get(url, params = {"userID": usrID, "parkRideID": rideID, "strategyType": "water"})
  stratTopic = stratDB.json()
  print(stratTopic)
  client = "water" + str(usrID)
  maintMqtt = ClientMQTT(client, stratTopic,onMessageReceived=WaterPublisher.onMsgReceived)
  maintMqtt.start()

  timeLastDB = time.time()
  timeLimitDB = 60 # number in seconds
  postFunc()
  
  while True:
    timeNow = time.time()
    if (timeNow - timeLastDB) >= timeLimitDB:
      postFunc()
      timeLastDB = timeNow
    time.sleep(5)
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
        
class MaintenancePublisher(object):

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
            isinMaint = db['strategies'][chosenstrat]["isinMaint"]
        except:
            raise cherrypy.HTTPError(400, 'User not found')

        if user == user_topic:
            if ride == ride_topic:
                sensor_topic = topic.split('/')[5]
                if sensor_topic == "sensors":
                    for sensor in db['sensors']:
                        if sensor == "counterRides":
                            counterRides += value
                            if isinMaint:
                                maintenanceOn(userid, rideid, counterRides)
                            else:
                                alertStatus = 0
                                alertTopic = "smartWaterPark/thingSpeak/user/" + str(userid) + "/ride/" + str(rideid) + "/stateAlert"
                                if counterRides > round(maxRides*0.99):
                                    print('MAXIMUM NUMBER OF RIDES: ENTERING THE RIDE IN MAINTENANCE')
                                    alertStatus = 3
                                    maintenanceOn(userid, rideid, counterRides)
                                elif counterRides >= round(maxRides*0.95):
                                    alertStatus = 2
                                elif counterRides >= round(maxRides*0.9):
                                    alertStatus = 1
                                else:
                                    print('No alert')
                                    alertStatus = 0
                                self.publish(alertTopic, alertStatus)  

        for i in db["strategies"]:
            userdb = i["userID"]
            ridedb = i["rideID"]       
            if userid == userdb and rideid == ridedb:
                stratDB = i
                break

        stratDB["alert"] = alertStatus
        stratDB["counterRides"] = counterRides

        with open(database, "w") as file:
            json.dump(db, file, indent=3)
         

def maintenanceOn(userid, rideid, counterRides):
    maintTopic = "smartWaterPark/thingSpeak/user/" + str(userid) + "/ride/" + str(rideid)

    with open(database, "r") as file:
        db = json.load(file)

    for i in db["strategies"]:
        user = i["userID"]
        ride = i["rideID"]       
        if user == userid and ride == rideid:
            stratDB = i
            break

    try:
        numMaint = stratDB["numMaint"]
        inMaint = stratDB["isinMaint"]
    except:
        raise 'ERROR user not registered'
    else:
        if inMaint:
            print('Ride still in maintenance')
        else:
            numMaint += 1

    numMaintTopic =  maintTopic + "/numMaint"
    maintMqtt.publish(numMaintTopic, numMaint)
    stratDB["numMaint"] = numMaint

    inMaintTopic =  maintTopic + "/isinMaint"
    maintMqtt.publish(inMaintTopic, 1)
    stratDB["isinMaint"] = True

    alertTopic = maintTopic + "/stateAlert"
    maintMqtt.publish(alertTopic, 3)
    stratDB["alert"] = 3

    stratDB["counterRides"] = counterRides

    with open(database, "w") as file:
      json.dump(db, file, indent=3)

def postFunc():
    with open(database, "r") as file:
        db = json.load(file)

    for i in db["strategies"]:
        user = i["userID"]
        ride = i["rideID"]       
        if user == usrID and ride == rideID:
            stratDB = i
            break
    
    payload = {
        "userID": stratDB['userID'],
        "rideID": stratDB['rideID'],
        "topic": stratDB['topic'],
        "isinMaint": stratDB['isinMaint'],
        "numMaint": stratDB['numMaint'],
        "alert": stratDB['alert'],
        "counterRides": stratDB['counterRides'],
        "timestamp": time.time()
    }

    url = resCatEndpoints +'/maintenance_strategy'
    requests.post(url, json.dumps(payload))


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
  rideID = 1 #db["rideID"]
  
  url = resCatEndpoints + "/maintenance_strategy"
  stratDB = requests.get(url, params = {"userID": usrID, "parkRideID": rideID})
  stratTopic = stratDB.json()
  print(stratTopic)
  #stratTopic = ["smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/maintenance/#"]
  client = "maintenance" + str(usrID)
  maintMqtt = ClientMQTT(client, stratTopic,onMessageReceived=MaintenancePublisher.onMsgReceived)
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
  
  """
  alertTopicEx = "smartWaterPark/telegram/user/" + str(usrID) + "/ride/" + str(rideID)

  time.sleep(2)

  alertEx = alertTopicEx 
  maintMqtt.publish(alertEx, 1)

  time.sleep(12)

  numEx =  alertTopicEx
  maintMqtt.publish(numEx, 2)

  time.sleep(12)

  inMaintEx =  alertTopicEx
  maintMqtt.publish(inMaintEx, 3)
  """
  

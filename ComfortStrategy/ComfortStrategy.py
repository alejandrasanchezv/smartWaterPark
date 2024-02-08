import paho.mqtt.client as PahoMQTT
import time
import json
import requests
import cherrypy

from mqttClass import *
database = "comfortDB.json"

resCatEndpoints = "http://127.0.0.1:8080"

class ComfortStrategy(object):
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
        
class ComfortPublisher(object):

    def __init__(self):
        """
        with open(database, "r") as file:
            db = json.load(file)

        actuators = db["actuators"]

        topic = "smartWaterPark/devConnector/user_" + str(usrID) + "/ride_" + str(rideID) + "/"
        topic_list = []
        for i in actuators:
            topicAct = topic + str(i)
            topic_list.append(topicAct)

        for strat in db['strategies']:
            user = strat['userID']
            ride = strat['rideID']

            if usrID == user and rideID == ride:
                chosenstrat = strat
                break
        
        db['strategies'][chosenstrat]['topic'] = topic_list
        with open(database, "w") as file:
            json.dump(db, file, indent=3)
        """

    def onMsgReceived(self, userdata, msg):
        print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")
        value = msg.payload
        topic = msg.topic

        #"smartWaterPark/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/control/sensors/readApi"
        user_topic = topic.split('/')[1]
        ride_topic = topic.split('/')[2]
        sensors = topic.split('/')[5]

        if sensors ==  "sensors":
            weatherApi()


def weatherApi():
    with open(database, "r") as file:
        db = json.load(file)

    for i in db["strategies"]:
        user = i["userID"]
        ride = i["rideID"]       
        if user == usrID and ride == rideID:
            stratDB = i
            break

    try:
        city = stratDB['city']
        api = stratDB['API']
        tempThr = stratDB['tempThreshold']
    except:
        raise 'USER NOT REGISTERED'
    
    url = 'http://api.weatherapi.com/v1/current.json?key='+ api +'&q='+ city

    request = requests.get(url)
    data = request.json()
    temp = data['current']['feelslike_c'] #THERMAL SENSATION
    isday = data['current']['is_day']

    if temp >= tempThr:
        fans = True
    else:
        fans = False

    if isday == 0:
        lights = True
    else:
        lights = False

    fansTopic = "smartWaterPark/devConnector/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/comfort/actuator/fans"
    comfortMqtt.publish(fansTopic, fans)
    lightsTopic = "smartWaterPark/devConnector/user_" + str(usrID) + "/ride_" + str(rideID) + "/strategy/comfort/actuator/lights"
    comfortMqtt.publish(lightsTopic, lights)

    stratDB['temp'] = temp
    stratDB['isday'] = isday
    stratDB['lights'] = lights
    stratDB['fans'] = fans

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
        "temp": stratDB['temp'],
        "isday": stratDB['isday'],
        "lights": stratDB['lights'],
        "fans": stratDB['fans'],
        "timestamp": time.time()
    }

    url = resCatEndpoints +'/comfort_strategy'
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
  cherrypy.tree.mount(ComfortStrategy(), '/dbTopic', conf)
  cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': 8096})
  cherrypy.engine.start()

  with open(database, "r") as file:
    db = json.load(file)

  usrID = 1 #db["userID"]
  rideID = 1 #db["rideID"]
  
  url = resCatEndpoints + "/comfort_strategy"
  stratDB = requests.get(url, params = {"userID": usrID, "parkRideID": rideID, "strategyType": "comfort"})
  stratTopic = stratDB.json()
  print(stratTopic)
  client = "comfort" + str(usrID)
  comfortMqtt = ClientMQTT(client, stratTopic,onMessageReceived=ComfortPublisher.onMsgReceived)
  comfortMqtt.start()

  timeLastDB = time.time()
  timeLimitDB = 60 # number in seconds
  postFunc()
  weatherApi()
  while True:
    timeNow = time.time()
    if (timeNow - timeLastDB) >= timeLimitDB:
      postFunc()
      timeLastDB = timeNow
    time.sleep(5)

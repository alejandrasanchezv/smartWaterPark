import cherrypy
import requests
import time
import json
import paho.mqtt.client as mqtt

from mqttClass import *

database = "thingSpeakDB.json"
resCatEndpoints = "http://127.0.0.1:8080"
url_thingspeak = "https://api.thingspeak.com/update?api_key="

maintData = {
    "isinMaint": -1,
    "numMaint": -1,
    "stateAlert": -1
}

class ThingSpeakAdaptor(object):
    exposed = True

    def POST(self, **params):
        """
        Registers a new topic
        """
        global database, db, thingsSpeakMqtt

        input = params
        print(params)

        try:
            usrID = input['userID']
            rideID = input['rideID']
        except:
            raise cherrypy.HTTPError(400, 'Wrong input')
        
        topic = "smartWaterPark/thingSpeak/user/" + str(usrID) + "/ride/" + str(rideID) + "/#"
        newTopic = {
            "topic": topic
        }

        db["topics"].append(newTopic)
        thingsSpeakMqtt.subscribe(topic)

        with open(database, "w") as file:
            json.dump(db, file, indent=3)

        result = {
            "userID": usrID,
            "rideID": rideID
        }

        return result
    
    def DELETE(self, **params):
        """
        Deletes a new topic
        """

        global database, thingsSpeakMqtt

        with open(database, "r") as file:
            db = json.load(file)

        input = params
        print(params)

        try:
            usrID = input['userID']
            rideID = input['rideID']
        except:
            raise cherrypy.HTTPError(400, 'Wrong input')
        
        index = []
        user = str(usrID)
        ride = str(rideID)
        for i, topic in enumerate(db['topics']):
            root_topic = topic['topic'].split('/')
            if root_topic[3] == user and root_topic[5] == ride:
                index.append(i)
                thingsSpeakMqtt.unsubscribe(topic['topic'])

        index.sort(reverse=True) #decendign order
        for i in index:
            db['topics'].pop(i)

        with open(database, "w") as file:
            json.dump(db, file, indent=3)

        result = {
            "userID": usrID,
            "rideID": rideID
        }

        return result
    
class ThingSpeakmqtt(object):
    def __init__(self) -> None:
        pass

    def onMsgReceived(device1, userdata, msg):
        print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")
        data = msg.payload
        topic = msg.topic

        #"smartWaterPark/maintenance/user/" + str(userid) + "/ride/" + str(rideid) + "/stateAlert"

        userID = topic.split("/")[3]
        print(f'userID: {userID}')
        rideID = topic.split("/")[5]
        print(f'rideID: {rideID}')
        dataType = topic.split("/")[6]
        print(f'dataType: {dataType}')
        

        for user in db["users"]:
            if user["userID"] == int(userID):
                for ride in user["rides"]:
                    if ride["rideID"] == int(rideID):
                        sendThingSpeak(userID, rideID, dataType, data)
                        time.sleep(3)

def sendThingSpeak(userID, rideID, dataType, data):
    """
    Sends the information received from 
    a MQTT topic to Thingspeak using REST (post)
    """

    global database

    with open(database, "r") as file:
        db = json.load(file)

    maintData[dataType] = int(data)

    for user in db["users"]:
        if user["userID"] == int(userID):
            for ride in user["rides"]:
                if ride["rideID"] == int(rideID):
                    apiKey = ride["API_KEY"]

                    if maintData["isinMaint"] >= 0:
                        field_inMaint = ride["isinMaint"]
                        RequestToThingspeak = str(url_thingspeak + apiKey + field_inMaint).format(int(maintData["isinMaint"]))
                        requests.post(RequestToThingspeak)
                        print(RequestToThingspeak)
                        time.sleep(3)
                        maintData["isinMaint"] = -1
                    
                    if maintData["numMaint"] >= 0:
                        field_numMaint = ride["numMaint"]
                        RequestToThingspeak = str(url_thingspeak + apiKey + field_numMaint).format(int(maintData["numMaint"]))
                        requests.post(RequestToThingspeak)
                        print(RequestToThingspeak)
                        time.sleep(3)
                        maintData["numMaint"] = -1

                    if maintData["stateAlert"] >= 0:
                        field_alert = ride["stateAlert"]
                        RequestToThingspeak = str(url_thingspeak + apiKey + field_alert).format(int(maintData["stateAlert"]))
                        requests.post(RequestToThingspeak)
                        print(RequestToThingspeak)
                        time.sleep(3)
                        maintData["stateAlert"] = -1

                    #RequestToThingspeak = str(url_thingspeak + apiKey + field_inMaint + field_numMaint + field_alert).format(int(maintData["isinMaint"]), int(maintData["numMaint"]), int(maintData["stateAlert"]))
                    #requests.post(RequestToThingspeak)
                    #print(RequestToThingspeak)

                    #maintData["isinMaint"] = -1
                    #maintData["numMaint"] = -1
                    #maintData["stateAlert"] = -1

                    with open(database, "w") as file:
                        json.dump(db, file, indent=3)
                    #RequestToThingspeak = str(url_thingspeak + apiKey + field_inMaint + field_numMaint + field_alert).format(int(maintData["isinMaint"]), int(maintData["numMaint"]), int(maintData["stateAlert"]))
                    #requests.post(RequestToThingspeak)

def postFunc():
  global database

  with open(database, "r") as file:
    db = json.load(file)

  payload = {
    "userID": db['userID'],
    "rideID": db['rideID'],
  }

  url = resCatEndpoints +'/thingSpeakAdaptor'
  #requests.post(url, json.dumps(payload))

def getTopics():
    """
    Retrieves all the topics registered in the Resource Catalog
    """
    global database



    #url = resCatEndpoints +'/thingSpeakAdaptor'




if __name__ == "__main__":

    #time.sleep(10)

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }
    cherrypy.tree.mount(ThingSpeakAdaptor(), '/dbTopic', conf)
    cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': 8099})
    cherrypy.engine.start()

    with open(database, "r") as file:
        db = json.load(file)

    usrID = 1 #db["userID"]
    rideID = 1 #db["rideID"]
    topic = "smartWaterPark/maintenance/user/" + str(usrID) + "/ride/" + str(rideID) + "/#"
    client = "thingSpeak" + str(usrID)
    thingsSpeakMqtt = ClientMQTT(client, [topic],onMessageReceived=ThingSpeakmqtt.onMsgReceived)
    thingsSpeakMqtt.start()

    #postFunc()
    timeLimitDB = 60 # number in seconds
    timeLastDB = time.time()

    while True:
        timeNow = time.time()
        if (timeNow - timeLastDB) >= timeLimitDB:
            postFunc()
            timeLastDB = timeNow
    #thingsSpeakMqtt.stop()

    #exampleData = {
    #    "isinMaint": 1,
    #    "numMaint": 1,
    #    "stateAlert": 0
    #}

    #time.sleep(5)

    #topicTest = "smartWaterPark/thingSpeak/user/" + str(usrID) + "/ride/" + str(rideID) + "/isinMaint"
    #sendThingSpeak(topicTest, exampleData)

    #time.sleep(15)

    #topicTest = "smartWaterPark/thingSpeak/user/" + str(usrID) + "/ride/" + str(rideID) + "/numMaint"
    #sendThingSpeak(topicTest, exampleData)

    #time.sleep(15)

    #topicTest = "smartWaterPark/thingSpeak/user/" + str(usrID) + "/ride/" + str(rideID) + "/stateAlert"
    #sendThingSpeak(topicTest, exampleData)
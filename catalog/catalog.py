import json
import cherrypy


class User(object):
    exposed = True

    def GET(self,**params):
        with open('db/catalog.json', 'r') as file:
            db = json.load(file)

        users = db["users"]
        userID=int(params["userID"])
        if userID is None:
            return('No user ID was given')

        for user in users:
            #if user['id'] == int(id):
            if user['id'] == int(userID):
                return json.dumps(user, indent=3)
        else:
            return ('User ID not found')
        

    def POST(self):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)

        users=db["users"]
        new_user={
            "id": 1,
            "userName": "newUser",
            "password": "123456",
            "email": "aleja@gmail.com",
            "city": "Milano",
            "parkRides": [
                {
                    "rideID": 1,
                    "rideName": "Atlantis",
                    "state": "OFF",
                    "maintenanceTime": "2 weeks",
                    "maxRides": 500
                }
            ]
        }

        # Read the data from the body
        body=cherrypy.request.body.read()
        json_body=json.loads(body)

        new_user["id"] = int(json_body["userID"])
        new_user["userName"] = json_body["userName"]
        new_user["password"] = json_body["password"]
        new_user["email"] = json_body["email"]
        new_user["city"] = json_body["city"]

        
        users.append(new_user)
        db["users"] = users

        with open("db/catalog.json", "w") as file:
            json.dump(db, file, indent=3)

        return "User sucessfully registered"
    
    def PUT(self):

        with open("db/catalog.json", "r") as file:
            db = json.load(file)
        
        users=db["users"]

        body=cherrypy.request.body.read()
        json_body=json.loads(body)

        #User Information to update
         #json_body['userName']
         #json_body['email']
        #json_body ['city']

        #UserID of the user to modify
        userID = int(json_body['userID'])
        print(userID)

        for user in users:
            print(user['id'])
            if user["id"] == userID:
                user['userName'] = json_body['userName']
                user["email"] = json_body['email']
                user["city"] = json_body ['city']

                #Save the information in the db
                db["users"] = users
                with open("db/catalog.json", "w") as file:
                    json.dump(db, file, indent=3)

                return "The information has been updated succesfully"
            
        return "User ID not found, please try again"

    def DELETE(self,**params):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
        
        users=db["users"]
        userID=int(params["userID"])
    
        for index, user in enumerate(users):
            if user["id"] == userID:
                print(index)
                users.pop(index)
                db["users"] = users
                with open("db/catalog.json", "w") as file:
                    json.dump(db, file, indent=3)
                
                return "The user was successfully deleted"
        
        return "No User ID was found"

class ParkRide(object):
    exposed = True
    def GET(self,**params):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
        
        users = db["users"]
        
        userID=int(params["userID"])
        parkRideID=int(params["parkRideID"])
        print("typo de userID",type(userID))
        print("typo de parkRide",type(parkRideID))

        
        
        if parkRideID is None:
            return "No rideID was given"
        for user in users:
            if user["id"] == userID:
                for ride in user["parkRides"]:
                    if ride["rideID"] == parkRideID:
                        return json.dumps(ride,indent=3)
                
                return "Park ride does not exits"
            
    def POST(self):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)

        
        
        users=db["users"]
        

        newRide={
               "rideID": 5,
               "rideName": "Kraken",
               "state": True,
               "maintenanceTime": 2,
               "maxRides": 500,
               "deviceConnectors":[]
        }

        # Read the data from the body
        body=cherrypy.request.body.read()
        json_body=json.loads(body)

        userID=int(json_body["userID"]) #id of the user to add the new ride
        newRide["rideID"] = int(json_body["rideParkID"])
        newRide["rideName"] = json_body["rideParkName"]
        newRide["maintenanceTime"] =int(json_body["maintenance"])

        for user in users:
            if user["id"] == userID:
                user['parkRides'].append(newRide)

                db["users"] = users

                with open("db/catalog.json", "w") as file:
                    json.dump(db, file, indent=3)

                return "New ride succesfully added to the user"
            
        return "No userID found"
    
    def PUT(self):
        body=cherrypy.request.body.read()
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
        
        users=db["users"]

        json_body=json.loads(body)
  
        userID= int(json_body["userID"])
        parkRideID= int(json_body["parkRideID"])
        #print(f'USERIDE VALUE: {userID} and PARKRIDEID VALUE: {parkRideID}' )
        #response="The keys are {}, and the values are {}".format([x for x in json_body.keys()],[x for x in json_body.values()])
        #return response

        for user in users:
            if user["id"] == userID:
                rides = user["parkRides"]
                for ride in rides:
                    print(ride["rideID"])
                    print(type(ride["rideID"]))
                    print(parkRideID)
                    print(type(parkRideID))
        
                    if ride["rideID"] == parkRideID:
                        ride["rideName"] = json_body["parkRideName"]
                        ride["maintenanceTime"] = json_body["maintenance"]



                        with open("db/catalog.json", "w") as file:
                            json.dump(db, file, indent=3)

                        return "New ride succesfully added to the user"
                    
                return "No Park Ride ID found"
            
        return "No userID found"

    def DELETE(self,**params):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)

        users=db["users"]
        userID=int(params["userID"])
        parkRideID=int(params["parkRideID"])
        print("typo de userID",type(userID))
        print("typo de parkRide",type(parkRideID))

  
        for user in users:
            if user["id"] == userID:
                rides = user["parkRides"]
                for index,ride in enumerate(rides):
                    if ride["rideID"] == parkRideID:
                        rides.pop(index)
                        db["users"] = users
                        with open("db/catalog.json", "w") as file:
                            json.dump(db, file, indent=3)
                
                        return "The park ride was successfully deleted"


                
                return "Park ride does not exits"
        return "No user ID was found"

class DeviceConnector(object):
    exposed = True
    
    def GET(self,**params):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
        
        #users = db["users"]
        
        #userID=int(params["userID"])
        #parkRideID=int(params["parkRideID"])
        #strategyType=params["strategyType"]

    def POST (self):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
    
        json_body = json.loads(cherrypy.request.body.read())

        userID = json_body["userID"]
        parkRideID = json_body["rideID"]
        sensors = json_body["sensors"]
        actuators = json_body["actuators"]
        strategies = json_body["strategies"]

        new_dev_connector = {
            "devices": {
                "sensors": sensors,
                "actuators": actuators
            }
        }
        for user in db["users"]:
            if user["id"] == int(userID):
                for parkRide in user["parkRides"]:
                    if parkRide["rideID"] == int(parkRideID):
                        update = False
                        if parkRide["deviceConnectors"] == []:
                            print("is empty, then i can add a new element")
                            parkRide["deviceConnectors"].append(new_dev_connector)  
                        else:
                            print("new element replaced")
                            parkRide["deviceConnectors"] = []
                            parkRide["deviceConnectors"].append(new_dev_connector)

                        parkRide["strategies"] = strategies

                with open("db/catalog.json", "w") as file:
                        json.dump(db, file, indent=3)
                return                   

class MaintenanceStrategy(object):
    exposed = True

    def GET(self,**params):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
        users = db["users"]

        userID=int(params["userID"])
        parkRideID=int(params["parkRideID"])
        strategyType="maintenance"


        if parkRideID is None:
            return "No rideID was given"
        for user in users:
            if user["id"] == userID:
                for ride in user["parkRides"]:
                    if ride["rideID"] == parkRideID:
                        for strategy in ride['strategies']:
                            if strategy == strategyType:
                                return json.dumps(ride["strategies"][strategy],indent=3)
                        return "Strategy does not exist in the db"
    
    def POST (self):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)

        json_body = json.loads(cherrypy.request.body.read())

        userID = json_body['userID']
        parkRideID = json_body['rideID']
        topic = json_body['topic']
        isinMaint = json_body['isinMaint']
        numMaint = json_body['numMaint']
        alert = json_body['alert']
        counterRides = json_body['counterRides']
        timestamp = json_body['timestamp']

        maintenance_params = {
        "topic": topic,
        "isinMaint": isinMaint,
        "numMaint": numMaint,
        "alert": alert,
        "counterRides": counterRides,
        "timestamp": timestamp
        }

        for user in db["users"]:
            if user["id"] == int(userID):
                rides = user["parkRides"]
                for ride in rides:
                    if ride['rideID'] == parkRideID:
                        ride['maintenance_params'] = maintenance_params
                        if isinMaint == False:
                            ride['state']=isinMaint
                        
                with open("db/catalog.json", "w") as file:
                            json.dump(db, file, indent=3)
                return 'maintenance_params added succesfully'

class ComfortStrategy(object):
    exposed = True

    def GET(self,**params):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
        
        users = db["users"]
        
        userID=int(params["userID"])
        parkRideID=int(params["parkRideID"])
        strategyType="comfort"
        
        if parkRideID is None:
            return "No rideID was given"
        for user in users:
            if user["id"] == userID:
                for ride in user["parkRides"]:
                    if ride["rideID"] == parkRideID:
                        for strategy in ride['strategies']:
                            if strategy == strategyType:
                                return json.dumps(ride["strategies"][strategy],indent=3)
                        return "Strategy does not exist in the db"

    def POST (self):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)

        json_body = json.loads(cherrypy.request.body.read())

        userID = json_body['userID']
        parkRideID = json_body['rideID']
        topic = json_body['topic']
        temp = json_body['temp']
        isday = json_body['isday']
        lights = json_body['lights']
        fans = json_body['fans']
        timestamp = json_body['timestamp']

        comfort_params = {
        "topic": topic,
        "temp": temp,
        "isday": isday,
        "lights": lights,
        "fans": fans,
        "timestamp": timestamp
        }

        for user in db["users"]:
            if user["id"] == int(userID):
                rides = user["parkRides"]
                for ride in rides:
                    if ride['rideID'] == parkRideID:
                        ride['comfort_params'] = comfort_params
                        
                with open("db/catalog.json", "w") as file:
                            json.dump(db, file, indent=3)
                return 'maintenance_params added succesfully'

class WaterStrategy(object):
    exposed = True
    def GET(self,**params):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
        
        users = db["users"]
        
        userID=int(params["userID"])
        parkRideID=int(params["parkRideID"])
        strategyType="water"
        
        for user in users:
            if user["id"] == userID:
                for ride in user["parkRides"]:
                    if ride["rideID"] == parkRideID:
                        for strategy in ride['strategies']:
                            if strategy == strategyType:
                                return json.dumps(ride["strategies"][strategy],indent=3)
                        return "Strategy does not exist in the db"
                
    def POST (self):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)

        json_body = json.loads(cherrypy.request.body.read())

        userID = json_body['userID']
        parkRideID = json_body['rideID']
        topic = json_body['topic']
        waterLevel = json_body['waterLevel']
        phSensor = json_body['phSensor']
        waterValve = json_body['waterValve']
        chlorineValve = json_body['chlorineValve']
        timestamp = json_body['timestamp']

        water_params = {
        "topic": topic,
        "waterLevel": waterLevel,
        "phSensor": phSensor,
        "waterValve": waterValve,
        "chlorineValve": chlorineValve,
        "timestamp": timestamp
        }

        for user in db["users"]:
            if user["id"] == int(userID):
                rides = user["parkRides"]
                for ride in rides:
                    if ride['rideID'] == parkRideID:
                        ride['water_params'] = water_params
                        
                with open("db/catalog.json", "w") as file:
                            json.dump(db, file, indent=3)
                return 'maintenance_params added succesfully'

                                
if __name__ == '__main__':

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }

    cherrypy.tree.mount(User(), '/user', conf)
    cherrypy.tree.mount(ParkRide(), '/parkride', conf)
    cherrypy.tree.mount(DeviceConnector(), '/device_connector', conf)
    cherrypy.tree.mount(MaintenanceStrategy(),'/maintenance_strategy',conf)
    cherrypy.tree.mount(ComfortStrategy(),'/comfort_strategy',conf)
    cherrypy.tree.mount(WaterStrategy(),'/water_strategy',conf)

    cherrypy.config.update({ 'server.shutdown_timeout': 1 })
    cherrypy.engine.start()
    cherrypy.engine.block()

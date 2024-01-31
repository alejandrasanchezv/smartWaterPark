import json
import cherrypy

#https://stackoverflow.com/questions/48650658/cherrypy-405-method-not-allowed-specified-method-is-invalid-for-this-resource
#https://programtalk.com/python-examples/cherrypy.request.params/
#https://docs.cherrypy.dev/en/latest/tutorials.html#tutorial-7-give-us-a-rest


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
               "state": 1,
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

    def POST (self):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
    
        json_body = json.loads(cherrypy.request.body.read())
        #print(body)
        #json_body=json.loads(body)
        print(json_body)

        userID = json_body["userID"]
        parkRideID = json_body["rideID"]
        #ip = json_body["ip"]
        #port = json_body["port"]
        sensors = json_body["sensors"]
        actuators = json_body["actuators"]

        new_dev_connector = {
            #"ip": ip,
            #"port": port,
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

                        #parkRide["deviceConnectors"].append(new_dev_connector)
                        if parkRide["deviceConnectors"] == []:
                            
                            print("is empty, then i can add the elements")
                            parkRide["deviceConnectors"].append(new_dev_connector)
                            
                        else:
                            print("It's occupied")
                            
                        '''
                        else:
                            for dev_connector in parkRide["deviceConnetors"]:
                                #if dev_connector["ip"] == ip and dev_connector["port"] == port:
                                dev_connector["devices"]["sensors"] = sensors
                                dev_connector["devices"]["actuators"] = actuators
                                update = True
                            if update == False:
                                parkRide["deviceConnectors"].append(new_dev_connector)
                        
                        
                        '''
                        
                        with open("db/catalog.json", "w") as file:
                                json.dump(db, file, indent=3)

                        return                   
'''
                        if update == False:
                                # I assume that there is just one Adaptor
                                url_adaptor = db["thingspeak_adaptors"][0]["ip"]+":"+str(db["thingspeak_adaptors"][0]["port"])+"/"+db["thingspeak_adaptors"][0]["functions"][0]
                                payload = {
                                    "userID": userID,
                                    "greenHouseID": greenHouseID,
                                    "sensors": sensors
                                }
                                requests.post(url_adaptor, json.dumps(payload))
'''
                                
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

    cherrypy.config.update({ 'server.shutdown_timeout': 1 })
    cherrypy.engine.start()
    cherrypy.engine.block()

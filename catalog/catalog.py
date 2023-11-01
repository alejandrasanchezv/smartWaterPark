import json
import cherrypy

#https://stackoverflow.com/questions/48650658/cherrypy-405-method-not-allowed-specified-method-is-invalid-for-this-resource
#https://programtalk.com/python-examples/cherrypy.request.params/
#https://docs.cherrypy.dev/en/latest/tutorials.html#tutorial-7-give-us-a-rest


class User(object):
    exposed = True

    def GET(self,userID=None):
        with open('db/catalog.json', 'r') as file:
            db = json.load(file)

        users = db["users"]
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
        #We need to find a better way to pass the user ID, Maybe with the use of queries
        
        id=2 #id of the user
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
                        return "Park ride Found: ", json.dumps(ride,indent=3)
                
                return "Park ride does not exits"
            
    def POST(self):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)

        
        
        users=db["users"]
        id=2 #id of the user

        newRide={
               "rideID": 5,
               "rideName": "Kraken",
               "state": "ON",
               "maintenanceTime": "2 weeks",
               "maxRides": 500
        }

        

        for user in users:
            if user["id"] == int(id):
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
        print(json_body)
        print(type(json_body))
        userID= int(json_body["userID"])
        parkRideID= int(json_body["parkRideID"])
        print(f'USERIDE VALUE: {userID} and PARKRIDEID VALUE: {parkRideID}' )

        response="The keys are {}, and the values are {}".format([x for x in json_body.keys()],[x for x in json_body.values()])
        return response

if __name__ == '__main__':

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }

    cherrypy.tree.mount(User(), '/user', conf)
    cherrypy.tree.mount(ParkRide(), '/parkride', conf)

    cherrypy.config.update({ 'server.shutdown_timeout': 1 })
    cherrypy.engine.start()
    cherrypy.engine.block()

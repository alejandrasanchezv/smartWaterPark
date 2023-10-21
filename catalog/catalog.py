import json
import cherrypy

#https://stackoverflow.com/questions/48650658/cherrypy-405-method-not-allowed-specified-method-is-invalid-for-this-resource
#https://programtalk.com/python-examples/cherrypy.request.params/
#https://docs.cherrypy.dev/en/latest/tutorials.html#tutorial-7-give-us-a-rest


class User(object):
    exposed = True

    def GET(self,userID=None):
        with open("db/catalog.json", "r") as file:
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
            "id": 4,
            "userName": "new5",
            "password": "123456",
            "email": "aleja@gmail.com",
            "city": "Milano",
            "parkRides": [
                {
                    "rideID": "1",
                    "rideName": "Atlantis",
                    "state": "ON",
                    "maintenanceTime": "2 weeks",
                    "maxRides": 500
                }
            ]
        }
        
        users.append(new_user)
        db["users"] = users

        with open("db/catalog.json", "w") as file:
            json.dump(db, file, indent=3)

        return "User sucessfully registered"


class ParkRide(object):
    exposed = True
    def GET(self,parkRideID=None):
        with open("db/catalog.json", "r") as file:
            db = json.load(file)
        
        users = db["users"]
        #We need to find a better way to pass the user ID, Maybe with the use of queries
        
        id=2 #id of the user
        
        if parkRideID is None:
            return "No rideID was given"
        for user in users:
            if user["id"] == int(id):
                for ride in user["parkRides"]:
                    if ride["rideID"] == int(parkRideID):
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

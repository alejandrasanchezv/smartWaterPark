# Smart WaterPark
IoT project final project

## User definition
User registration based on the following data structure:

- **Name:** string – assigned by the user
- **ID:** unique number (int) – assigned by the system
- **Password:** string – assigned by the user
- **Mail:** string – given by the user
- **City:** string (weather api) – given by the user
- **Rides:** array composed by each of the rides assigned to the user – each ride has its own characteristics
```
User = {
	“id”: 001,
	“userName”: “kids”,
	“password”: “K!dsarea312”,
	“email”: info@kidsarea.it,
	“city”: “Torino”,
	“parkRides”: { …}
}
```

## Ride Definition
Each user will have park rides registered with the following variables:

- **Name:** string – assigned by the user
- **ID:** unique number (int) – assigned by the system
- **State:** bool – determines if the ride is open (true) or closed (false) – ride can be closed do to weather condition or maintenance revision
- **Max rides:** number (int) – determines the maximum rides the ride can do without a maintenance revision
- **Device connectors:** array composed by each sensor/actuator registered under the ride ID, defined by their id, type and value/state
- **Control Strategies:** array composed by each of the strategies assigned to the ride
- **Strategies:** array composed by the topics where the device connector will publish the sensor readings
- **Maintenance/Comfort/Water paramenters:** array composed by the last parameters posted by each strategy
```
Rides = {
	“ride1”: {
	“name”: “river”,
	“id”: 1,
	“state”: True,
	“maintenance_time”: “2 weeks”,
	“mx_rides”: 500,
	“deviceConnectors”: [ …],
	“control_strategies”: [ …],
	“strategies”: [ …],
	“maintenance_params”: [ …],
	“comfort_params”: [ …],
	“water_params”: [ …],
	},
	“ride2”: { … }
}
```

### Control Strategies
Each strategy has its own sensors and actuators – strategies determine what variables are being controlled on the system.

#### Maintenance
Maintenance strategy is in charge of determine whether a ride should stop functioning and get a revision or continue functioning normally. This strategy is assigned to all rides, so all rides should always have the state in true.

- **State:** bool – determines if the strategy is activated for this ride
- **Sensors:** array with each sensor assigned to this ride by this strategy:
	- **Number of rides sensor:** counts the number of rounds this ride has done
- **Actuators:** array with each actuator assigned to this ride by this strategy:
	- **Maintenance call:** alert sent when the ride needs to close and got to revision – determined by time or number of rides (maybe weather) – assignes the ride state to False
 - **Strategies:** array with each value obatained by the sensors on a specific park ride
```
 "maintenanceControl" = {
	“state”: True/False,
	“sensors”: {
		“sensorRidesID”: 0
	},
	“actuators”: {
		“maintenanceCallID": 0
	},
	"strategies": []
}
```

### Water
Water strategy is in charge of assuring the water is in optimal conditions. This strategy is assigned to rides who are active meaning the ride state is true, so if the ride is in revision (ride state = false) then this strategy has its own state equal to false.

- **State:** bool – determines if the strategy is activated for this ride
- **Sensors:** array with each sensor assigned to this ride by this strategy:
	- **Water level sensor:** measure if the water level on the ride
	- **PH sensor:** used to determine if the quality of the wateris in optimal conditions
- **Actuators:** array with each actuator assigned to this ride by this strategy:
	- **Valve:** used to insert more wáter to the ride – becomes activated when the water level is too low
	- **Activator:** used to insert more chemicals (chlorine) to the water – becomes activated when the ph sensor measures a high PH level
 - **Strategies:** array with each value obatained by the sensors and actuators on a specific park ride, it also contains the threshold value for each sensor reading
	- **ph threshold:** float - maximum ideal ph level before needing to activate the chlorine valve
  	- **water threshold:** float - minimum ideal water level before needing to activate the water valve
```
“waterControl" = {
	“state”: True/False,
	“sensors”: {
		“waterSensorID”: 0,
		“phSensorID”: 0
	},
	“actuators”: {
		“valveID”: 0,
		“activatorID": 0
	},
	"strategies": []
}
```
### Comfort
Comfort strategy is in charge of assuring the water park user’s are comfortable while they’re in queue for the ride. This strategy is assigned to rides who are active meaning the ride state is true, so if the ride is in revision (ride state = false) then this strategy has its own state equal to false. By comfort we assure the lights are on when its too dark and fans are on when its too hot outside.

- **State:** bool – determines if the strategy is activated for this ride
- **Weather API:** City’s weather conditions obtained from a web page
- **Sensors:** array with each sensor assigned to this ride by this strategy:
	- **Light sensor:** measure the light intensity
- **Actuators:** array with each actuator assigned to this ride by this strategy:
	- **Lights:** becomes activated when the light intensity on the premises is too low
	- **Fans:** used to cool down the area – becomes activated when the weather conditions determines the city’s temperatura is over 26°C.
 - **Strategies:** array with each the user's city and API to determining the temperature and day/night, it also contains the temperature threshold value and the actuators' current state 
	- **temperature threshold:** float - maximum ideal temperature value before needing to activate the fans
```
“comfortControl" = {
	“state”: True/False,
	“weatherAPI”: [],
	“sensors”: {
		“lightSensorID”: 0	},
	“actuators”: {
		“lightsID”: 0,
		“fansID": 0
	},
	"strategies": []
}
```
## NODE RED
Used to create/register a new user or ride

## TELEGRAM BOT
Used by the maintenance startegy to inform an employee that a ride needs to be closed to go to revision

3 alerts:
- **ALERT 1:** a ride is about to need a revision soon – the ride has done 80% of its máximum rides 
- **ALERT 2:** a ride is about to need a revision very very soon – the ride has done 90% of its maximum rides
- **ALERT 3:** a ride is closed because it has to go to revision, mainly just to inform its already closed – this alert shouldn’t be a surprise because alert 1 should have warned the employee

## THINGSPEAK
Used to show the Admin (user) the registry of the maintence's schedule. Used to have a registry on 3 variables related to the park ride's value
- **IS IN MAINT:** bool - states if the park ride is currently on maintenance or not 
- **NUM MAINT:** int - number of times that the park ride has closed due to maintenance
- **STATE ALERT:** int [0, 1, 2, 3] -  states the curret park ride's alert according to the maximum rides 

```
user : {
		"name": "kids",
		"id": 1,
		"password": "stringPS",
		"mail": "stringmail",
		"city": "Torino",
		"rides" : {
				"ride1": {
						"name": "river",
						"id": 1,
						"state": true/false,
						"maintenance_time": "2 weeks",
						"max_rides": 500,
						"control_strategies": {
								"maintenanceControl": {
										"state": true/false,
										"sensors": {
												"sensorRidesID": 0
										},
										"actuators": {
												"maintenanceCallID": 0
										}
								}
								"waterControl": {
										"state": true/false,
										"sensors": {
												"waterSensorID": 0,
												"phSensorID": 0
										}
										"actuators": {
												"valveID": 0,
												"activatorID": 0
										}
								}
								"comfortControl": {
										"state": true/false,
										"weatherAPI": [],
										"sensors": {
												"lightSensorID": 0
										}
										"actuators": {
												"lightsID": 0,
												"fansID": 0
										}
								}
						}
				},
				"ride2": { ... }
		}
}
```

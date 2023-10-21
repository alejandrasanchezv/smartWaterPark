# Smart WaterPark
IoT project

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
	“name”: “kids”,
	“id”: 001,
	“password”: “K!dsarea312”,
	“mail”: info@kidsarea.it,
	“city”: “Torino”,
	“rides”: { …}
}
```

## Ride Definition
Each user will have park rides registered with the following variables:

- **Name:** string – assigned by the user
- **ID:** unique number (int) – assigned by the system
- **State:** bool – determines if the ride is open (true) or closed (false) – ride can be closed do to weather condition or maintenance revision
- **Maintenance time:** string – determines the maximum time the ride can stay without a maintenance revision
- **Max rides:** number (int) – determines the maximum rides the ride can do without a maintenance revision
- **Control Strategies:** array composed by each of the strategies assigned to the ride
```
Rides = {
	“ride1”: {
	“name”: “river”,
	“id”: 001,
	“state”: True,
	“maintenance_time”: “2 weeks”,
	“mx_rides”: 500,
	“control_strategies”: { …}
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
	- **Weight:** used to determine if the water float id inflated enough
- **Actuators:** array with each actuator assigned to this ride by this strategy:
	- **Air pump:** used to inflate the water float – becomes activated when the float’s weight is too low
	- **Maintenance call:** alert sent when the ride needs to close and got to revision – determined by time or number of rides (maybe weather) – assignes the ride state to False
```
 "maintenanceControl" = {
	“state”: True/False,
	“sensors”: {
		“sensorRidesID”: 0,
		“weightID”: 0
	},
	“actuators”: {
		“airpumpID”: 0,
		“maintenanceCallID": 0
	}
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
	}
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

```
“comfortControl" = {
	“state”: True/False,
	“weatherAPI”: [],
	“sensors”: {
		“lightSensorID”: 0	},
	“actuators”: {
		“lightsID”: 0,
		“fansID": 0
	}
}
```

## Thingspeak Adaptor
Used to show the Admin (user) the variables measured by each strategy

Used by the water park clients to see the state of the queue of each ride.

## NODE RED
Used to create/register a new user or ride (?) creo

## TELEGRAM BOT
Used by the maintenance startedy to inform an employee that a ride needs to be closed to go to revision

3 alerts:
- **ALERT 1:** a ride is about to need a revision soon – the ride has done 80% of its máximum rides or maximum time finishes in 2 days
- **ALERT 2:** a ride is closed because it has to go to revision, mainly just to inform its already closed – this alert shouldn’t be a surprise because alert 1 should have warned the employee
- **ALERT 3:** not really an alert just a notice to inform a ride has made its revision and is back on. 

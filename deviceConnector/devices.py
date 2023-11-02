import time
import json
from random import uniform

class Actuator(object):
    def __init__(self, id, state, type) -> None:
        self.id = id
        self.state = state
        self.type = type
        if self.type == "airPump" or self.type == "waterValve" or self.type == "chlorineValve":
            self.value = 0

    def turnOn(self):
        self.state = True
    
    def turnOff(self):
        self.state = False

    def setValue(self, value):
        self.value = value
        if self.value == 0:
            self.state = False
        else:
            self.state = True

class Sensor(object):
    def __init__(self, id, type) -> None:
        self.id = id
        self.type = type
        self.value = 0
    
    def readvalue(self, type):
        if type == "counterRides":
            self.value += uniform(10,50)
        elif type == "airWeight":
            self.value = uniform(10,30)
        elif type == "waterLevel":
            self.value = uniform(10.3,20.0)
        elif type == "phSensor":
            self.value = uniform(6.8,8.5) #Ideal between 7.2 amd 7.4
        else:
            self.value = 0
            print('Invalid sensor type')
        print(f'Sensor {self.type} with id {self.id} set value {self.value}')

class Comfort(object):
    def __init__(self, actuators, city):
        self.city = city
        self.actuators = actuators
        self.api = 'API'
    
    def comfortActuatorOn(self, id):
        for actuator in self.actuators:
            if actuator.id == id:
                actuator.turnOn()
                return f'Comfort Actuator {actuator.type} with ID {id} is on'
        
    def comfortActuatorOff(self, id):
        for actuator in self.actuators:
            if actuator.id == id:
                actuator.turnOff()
                return f'Comfort Actuator {actuator.type} with ID {id} is off'

class Maintenance(object):
    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def sensorRead(self, id):
        for sensor in self.sensors:
            if sensor.id == id:
                sensor.readvalue(sensor.type)
                return sensor.value

    def airPumpOn(self, id):
        for actuator in self.actuators:
            if actuator.id == id:
                actuator.turnOn()
                return f'Comfort Actuator {actuator.type} with ID {id} is on'
        
    def airPumpOff(self, id):
        for actuator in self.actuators:
            if actuator.id == id:
                actuator.turnOff()
                return f'Comfort Actuator {actuator.type} with ID {id} is off'
            
    def callMaintenance(self, userid, rideid, level = 3):
        if level == 1:
            print(f'Ride with ID {rideid} registered under user {userid}, almost time for maintance')
        elif level == 2:
            print(f'Ride with ID {rideid} registered under user {userid}, will need maintance shortly')
        else:
            print(f'Ride with ID {rideid} registered under user {userid} needs maintance: RIDE {rideid} IS CLOSED')

class Water(object):
    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def sensorRead(self, id):
        for sensor in self.sensors:
            if sensor.id == id:
                sensor.readvalue(sensor.type)
                return sensor.value
            
    def setValueActuator(self, id, value):
        for actuator in self.actuators:
            if actuator.id == id:
                actuator.setValue(value)

if __name__ == "__main__":
    numCounters = 1
    numAirWeight = 1
    numWaterLevel = 1
    numPh = 1
    id = 0

    sensorsMaintenance = []
    sensorsWater = []

    for counter in range(numCounters):
        sensorsMaintenance.append(Sensor(id, "counterRides"))
        id += 1
    for airW in range(numAirWeight):
        sensorsMaintenance.append(Sensor(id, "airWeight"))
        id += 1
    for waterL in range(numWaterLevel):
        sensorsWater.append(Sensor(id, "waterLevel"))
        id += 1
    for ph in range(numPh):
        sensorsWater.append(Sensor(id, "phSensor"))
        id += 1

    actuatorsMaintenance = []
    actuatorsWater = []
    actuatorsComfort = []
    numAir = 1
    numMaint = 1
    numValves = 1
    numChlo = 1
    numLights = 1
    numFans = 1
    idA = 0

    for pump in range(numAir):
        actuatorsMaintenance.append(Actuator(idA, False, "airPump"))
        idA += 1
    for maint in range(numMaint):
        actuatorsMaintenance.append(Actuator(idA, False, "maintenanceCall"))
        idA += 1
    for valve in range(numValves):
        actuatorsWater.append(Actuator(idA, False, "waterValve"))
        idA += 1
    for chlo in range(numChlo):
        actuatorsWater.append(Actuator(idA, False, "chlorineValve"))
        idA += 1
    for light in range(numLights):
        actuatorsComfort.append(Actuator(idA, False, "lights"))
        idA += 1
    for fan in range(numFans):
        actuatorsComfort.append(Actuator(idA, False, "fans"))
        idA += 1
    
    maintenance = Maintenance(sensorsMaintenance, actuatorsMaintenance)
    water = Water(sensorsWater, actuatorsWater)
    comfort = Comfort(actuatorsComfort, "Turin")

    timeLastWater = time.time()
    timeLastMant = time.time()
    timeLimitWater = 7 # number in seconds
    timeLimitMant = 10 # number in seconds
    while True:
        timeNow = time.time()
        if (timeNow - timeLastWater) >= timeLimitWater:
            sensorsWater = water.sensorRead(2)
            print(f'Water measurement sensor 2: {sensorsWater}')
            sensorsWater = water.sensorRead(3)
            print(f'Water measurement sensor 3: {sensorsWater}')
            timeLastWater = timeNow
        elif (timeNow - timeLastMant) >= timeLimitMant:
            sensorsMant = maintenance.sensorRead(0)
            print(f'Maintenance measurement sensor 0: {sensorsMant}')
            sensorsMant = maintenance.sensorRead(1)
            print(f'Maintenance measurement sensor 1: {sensorsMant}')
            timeLimitMant = timeNow
        #time.sleep(3)
        #device1.publish('temp/iot/deviceConnector', 23.4)
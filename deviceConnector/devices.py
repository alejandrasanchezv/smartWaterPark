import time
import json
import requests
from random import uniform

class Actuator(object):
    def __init__(self, id, state, type) -> None:
        self.id = id
        self.state = state
        self.type = type

    def turnOn(self):
        self.state = True
    
    def turnOff(self):
        self.state = False

class AirPump(Actuator):
    def __init__(self, id, state, type) -> None:
        super().__init__(id, state, type)
        self.value = 0

    def setValue(self, value):
        self.value = value
        if self.value == 0:
            self.state = False
        else:
            self.state = True

class WaterValve(Actuator):
    def __init__(self, id, state, type) -> None:
        super().__init__(id, state, type)
        self.value = 0

    def setValue(self, value):
        self.value = value
        if self.value == 0:
            self.turnOff()
        else:
            self.turnOn()

class ChlorineValve(Actuator):
    def __init__(self, id, state, type) -> None:
        super().__init__(id, state, type)
        self.value = 0

    def setValue(self, value):
        self.value = value
        if self.value == 0:
            self.turnOff()
        else:
            self.turnOn()

class Lights(Actuator):
    def __init__(self, id, state, type) -> None:
        super().__init__(id, state, type)

class Fans(Actuator):
    def __init__(self, id, state, type) -> None:
        super().__init__(id, state, type)

class MaintenanceCall(Actuator):
    def __init__(self, id, state, type) -> None:
        super().__init__(id, state, type)
        self.warning = 0

    def callMaintenance(self, userid, rideid, level = 3):
        if level == 1:
            print(f'Ride with ID {rideid} registered under user {userid}, almost time for maintance')
            self.warning = 1
            self.turnOn()
        elif level == 2:
            print(f'Ride with ID {rideid} registered under user {userid}, will need maintance shortly')
            self.warning = 2
            self.turnOn()
        elif level == 3:
            print(f'Ride with ID {rideid} registered under user {userid} needs maintance: RIDE {rideid} IS CLOSED')
            self.warning = 3
            self.turnOn()
        else:
            print(f'Ride with ID {rideid} registered under user {userid} is out of maintance: RIDE {rideid} IS OPEN')
            self.warning = 0
            self.turnOff()

class Sensor(object):
    def __init__(self, id, type) -> None:
        self.id = id
        self.type = type
        self.value = 0
    
    def readvalue(self, sensor):
        if sensor.type == "counterRides":
            sensor.value += uniform(10,50)
        elif sensor.type == "airWeight":
            sensor.value = uniform(10,30)
        elif sensor.type == "waterLevel":
            sensor.value = uniform(10.3,20.0)
        elif sensor.type == "phSensor":
            sensor.value = uniform(6.8,8.5) #Ideal between 7.2 amd 7.4
        else:
            sensor.value = 0
            print('Invalid sensor type')
        print(f'Sensor {sensor.type} with id {sensor.id} set value {sensor.value}')

class Comfort(object):
    def __init__(self, actuators, city):
        self.city = city
        self.actuators = actuators
        self.api = '2782492787784b98814165302230711'
        self.temperature = 18
        self.isday = 1
        self.flag = True
        self.lastTime = time.time()

    def weatherApi(self):
        url = 'http://api.weatherapi.com/v1/current.json?key='+ self.api +'&q='+ self.city
        request = requests.get(url)
        data = request.json()

        temp = data['current']['feelslike_c'] #THERMAL SENSATION
        isday = data['current']['is_day']

        self.temperature = temp
        self.isday = isday

        return temp, isday
    
    def updateData(self):
        #actualTime = time.time()
        for actuator in  self.actuators:
            if isinstance(actuator, Lights):
                if self.isday:
                    self.comfortActuatorOn(actuator.id)
                else:
                    self.comfortActuatorOff(actuator.id)
            elif isinstance(actuator, Fans):
                if self.temperature >= 25:
                    self.comfortActuatorOn(actuator.id)
                else:
                    self.comfortActuatorOff(actuator.id)


        if self.flag:
            self.temperature, self.isday = self.weatherApi()
            self.flag = False

        return

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
                sensor.readvalue(sensor)
                return round(sensor.value,2)

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

class Water(object):
    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def sensorRead(self, id):
        for sensor in self.sensors:
            if sensor.id == id:
                sensor.readvalue(sensor)
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
    # WEATHER API
    temp, day = comfort.weatherApi()
    print(temp)
    print(day)
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
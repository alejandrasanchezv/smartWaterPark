import time
import json
from random import uniform
import paho.mqtt.client as PahoMQTT

from mqttClass import *

class Actuator(object):
    def __init__(self, id, state, type) -> None:
        self.id = id
        self.state = state
        self.type = type
        if self.type == "airPump" or self.type == "waterValve" or self.type == "chlorineValve":
            self.value = 0

    def actuatorOn(self):
        self.state = True
    
    def actuatorOff(self):
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
            return 'Invalid sensor type'

class Weather(object):
    pass

class Maintenance(object):
    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def comfortActuatorOn(self, id):
        for actuator in self.actuators:
            if actuator.id == id:
                actuator.actuatorOn()
                return f'Comfort Actuator {actuator.type} with ID {id} is on'
        
    def comfortActuatorOff(self, id):
        for actuator in self.actuators:
            if actuator.id == id:
                actuator.actuatorOff()
                return f'Comfort Actuator {actuator.type} with ID {id} is off'
            
    def sensorRead(self, id):
        for sensor in self.sensors:
            if sensor.id == id:
                typeSensor = sensor.type
                typeSensor.readValue()
                return sensor.value
            
    def callMaintenance(self, userid, rideid):
        print(f'Ride with ID {rideid} registered unser user {userid}, needs maintance')

class Comfort(object):
    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def comfortActuatorOn(self, id):
        for actuator in self.actuators:
            if actuator.id == id:
                actuator.actuatorOn()
                return f'Comfort Actuator {actuator.type} with ID {id} is on'
        
    def comfortActuatorOff(self, id):
        for actuator in self.actuators:
            if actuator.id == id:
                actuator.actuatorOff()
                return f'Comfort Actuator {actuator.type} with ID {id} is off'

def onMsgReceived(device1, userdata, msg):
    print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")


if __name__ == "__main__":
    device1 = ClientMQTT('device1', ['temp/iot/#'], onMessageReceived=onMsgReceived)

    device1.start()

    while True:
        #time.sleep(3)
        #device1.publish('temp/iot/deviceConnector', 23.4)
        pass
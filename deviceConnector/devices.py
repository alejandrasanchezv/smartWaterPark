import time
import json
import paho.mqtt.client as PahoMQTT

from mqttClass import *

class Weather(object):
    pass

class Actuator(object):
    def __init__(self, id, state, type) -> None:
        self.id = id
        self.state = state
        self.type = type
    
    def actuatorOn(self):
        self.state = True
    
    def actuatorOff(self):
        self.state = False

class Sensor(object):
    def __init__(self, id, type) -> None:
        self.id = id
        self.type = type

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
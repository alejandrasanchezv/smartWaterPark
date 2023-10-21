import time
import json

from deviceConnector import *

def onMsgReceived(device1, userdata, msg):
    print(f"Message received. Topic:{msg.topic}, QoS:{msg.qos}s, Message:{msg.payload}")



if __name__ == "__main__":
    device1 = ClientMQTT('device1', ['temp/iot/#'])

    device1.start()

    while True:
        #time.sleep(3)
        #device1.publish('temp/iot/deviceConnector', 23.4)
        pass
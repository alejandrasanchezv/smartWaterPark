import paho.mqtt.client as PahoMQTT
import time

class ClientMQTT:
    def __init__(self, clientID, topics, broker='mqtt.eclipseprojects.io', port=1883, qos=2, onMessageReceived= '', ble=''):
        print(f"[{clientID}] Instantiating mqtt_client")
        self.clientID = clientID
		# create an instance of paho.mqtt.client
        if ble == '':
          self._paho_mqtt = PahoMQTT.Client(clientID, clean_session= True)   #  the broker will remove all information about this client when it disconnects 
        else:
           self._paho_mqtt = PahoMQTT.Client(clientID, userdata=ble)

		# register the callback
        #self._paho_mqtt.on_connect = self.myOnConnect
        if onMessageReceived == '':
          self._paho_mqtt.on_message = self.onMessageReceived
        else:
          self._paho_mqtt.on_message = onMessageReceived
        self._paho_mqtt.on_connect = self.myOnConnect
        #if onMessageReceived != '':
        #  self._paho_mqtt.on_message = onMessageReceived
        self.topics = topics
        self.broker = broker
        self.port = port
        self.qos = qos

    def start (self):
		# manage connection to broker
       print(f"[{self.clientID}] Connecting to broker {self.broker}:{self.port}")
       self._paho_mqtt.connect(self.broker, self.port)
		# subscribe to topics
       self._paho_mqtt.subscribe([(x, self.qos) for x in self.topics])
       self._paho_mqtt.loop_start()

    def stop (self):
       print(f"[{self.clientID}] Unsubscribing and disconnecting from broker")
       self._paho_mqtt.unsubscribe(self.topics)
       self._paho_mqtt.loop_stop()
       self._paho_mqtt.disconnect()

    def myOnConnect (self, paho_mqtt, userdata, flags, rc):
       print(f"['{self.clientID}'] Connected to '{self.broker}' with result code: '{rc}'")
       #print ("Connected to %s with result code: %d" % (self.broker, rc))
		#print('Message received')

    def subscribe(self, topic):
       self._paho_mqtt.subscribe(topic)

    def unsubscribe(self, topic):
       self._paho_mqtt.unsubscribe(topic)
	
    def publish(self, topic, message):
       print(f"[{self.clientID}] Publishing message: '{message}'; topic: '{topic}'")
       self._paho_mqtt.publish(topic, message, self.qos, retain=False)

    def onMessageReceived(self, paho_mqtt , userdata, msg):
		## A new message is received
        print ("Topic:'" + msg.topic+"', QoS: '"+str(msg.qos)+"' Message: '"+str(msg.payload) + "'")

if __name__ == "__main__":

    testClass = ClientMQTT("mqttClass", ["temp/iot/deviceConnector"])

    testClass.start()
	
    while True:
        time.sleep(3)
        testClass.publish('temp/iot/deviceConnector', 23.4)
        #pass
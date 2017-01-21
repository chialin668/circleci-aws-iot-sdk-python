from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt

host='a1arqmop0meczp.iot.us-west-2.amazonaws.com'
rootCAPath='./ssl/root-CA.crt'
certificatePath='./ssl/MyThing02.cert.pem'
privateKeyPath='./ssl/MyThing02.private.key'
useWebsocket=False

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

def callback(client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

# Init AWSIoTMQTTClient
client = None
if useWebsocket:
        client = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
        client.configureEndpoint(host, 443)
        client.configureCredentials(rootCAPath)
else:
        client = AWSIoTMQTTClient("basicPubSub")
        client.configureEndpoint(host, 8883)
        client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
client.connect()
client.subscribe("sdk/test/Python", 1, callback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
        client.publish("sdk/test/Python", "New Message " + str(loopCount), 1)
        loopCount += 1
        time.sleep(60)


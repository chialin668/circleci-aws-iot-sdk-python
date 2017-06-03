#!/usr/bin/env python

import paho.mqtt.client as mqtt
import ssl, time

host='a1arqmop0meczp.iot.us-west-2.amazonaws.com'
rootCAPath='./ssl/root-CA.crt'
certificatePath='./ssl/MyThing02.cert.pem'
privateKeyPath='./ssl/MyThing02.private.key'

def on_connect(mosq, obj, rc):
    client.subscribe('sdk/test/Python', 0)

def on_message(mosq, obj, msg):
    print 'topic: ' + str(msg.topic)
    print 'QoS: ' + str(msg.qos)
    print 'Payload: ' + str(msg.payload)

def on_subcribe(mosq, obj, mid, granted_qos):
    print('subscribe...')

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_subcribe = on_subcribe

client.tls_set(rootCAPath, certfile=certificatePath, keyfile=privateKeyPath, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


client.connect(host, 8883, 45)
client.loop_start()

while True:
    print('.')
    time.sleep(2)

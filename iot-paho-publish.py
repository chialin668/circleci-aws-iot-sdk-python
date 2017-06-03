#!/usr/bin/env python

import paho.mqtt.client as mqtt
import ssl, time

host='a1arqmop0meczp.iot.us-west-2.amazonaws.com'
rootCAPath='./ssl/root-CA.crt'
certificatePath='./ssl/MyThing02.cert.pem'
privateKeyPath='./ssl/MyThing02.private.key'


def on_publish(client, userdata, mid):
    print 'message published'

client = mqtt.Client()
client.on_publish = on_publish
client.tls_set(rootCAPath, certfile=certificatePath, keyfile=privateKeyPath, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

client.connect(host, 8883, 45)
client.loop_start()

counter = 0
while True:
    client.publish('sdk/test/Python', 'msg' + str(counter), qos=1)
    counter += 1
    time.sleep(2)

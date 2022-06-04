import paho.mqtt.client as mqtt
import time

local_mqtt_host = "mosquitto-service"
mqtt_port= 1883
mqtt_topic= "test_topic"

remote_mqtt_host = "10.43.54.170"
remote_mqtt_port = 30142

def on_connect_local(local_client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        local_client.subscribe(mqtt_topic)

def on_connect_remote(remote_client, userdata, flags, rc):
        print("connected to remote broker with rc: " + str(rc))
        #remote_client.subscribe(mqtt_topic)

def on_message(client,userdata, msg):
  try:
    #print("message received: ",str(msg.payload.decode("utf-8")))
    print("message received: ",str(msg.payload))
    # if we wanted to re-publish this message, something like this should work
    msg = msg.payload
    remote_client.connect(remote_mqtt_host,remote_mqtt_port,60)
    remote_client.publish(mqtt_topic, payload=msg, qos=0, retain=False)
  except Exception as e:
    print("Unexpected error:", e)

#Create client object for local and remote
remote_client = mqtt.Client("forwarderRemote")
local_client = mqtt.Client("forwarderLocal")

#Callback connect
local_client.on_connect = on_connect_local
remote_client.on_connect = on_connect_remote

#connect to broker
local_client.connect(local_mqtt_host, mqtt_port, 60)
remote_client.connect(remote_mqtt_host,remote_mqtt_port,60)
#remote_client.publish(mqtt_topic, payload="Connection to cloud successful", qos=0, retain=False)
#Local client, does this on message
local_client.on_message = on_message

# go into a loop
remote_client.loop_start()
local_client.loop_forever()

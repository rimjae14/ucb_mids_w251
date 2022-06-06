import paho.mqtt.client as mqtt
from ast import expr_context
import cv2, sys, numpy, os
import time

LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT= 1883
LOCAL_MQTT_TOPIC="test_topic"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

#publish the message
# local_mqttclient.publish(LOCAL_MQTT_TOPIC,"HI LOL")

#GOING TO FACE DETECTOR COMPONENT
seconds_of_running = 5

# defining the size of images
(width, height) = (150, 150)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
webcam = cv2.VideoCapture(0)

# The program loops until it has 30 images of the face.
end_time = time.time() + seconds_of_running
image_count = 0
print("Running face detector for",seconds_of_running,"seconds.")
while time.time() < end_time:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        # face_resize = cv2.resize(face, (width, height))

        #Writing the image to file
        image_string = "face_{}.png".format(image_count+1)
        #Imencode takes the image and encodes it. We will use this to send to the cloud.
        rc,png = cv2.imencode('.png', face)
        # rc,png = cv2.imencode('.png', face_resize)
        msg = png.tobytes()

        #SEND TO LOGGER - THIS IS THE MESSAGE LOGGER
        local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=msg, qos=0, retain=False)
        # print(msg)
        image_count += 1

    # cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
    if key == 27:
	    break

webcam.release()
cv2.destroyAllWindows()
print("Face Detector Finished.")
print("Captured",image_count,"faces in",seconds_of_running,"seconds.")

local_mqttclient.loop_forever()

FROM alpine:latest
# this is needed to make sure we can see the log output
RUN apk add mosquitto
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apk update
RUN apk add py3-pip
RUN pip3 install paho-mqtt
#RUN a command to intall the MQTT python client 
# Copy your mosquitto_facedetector file into the container
COPY mqtt_forwarder.py mqtt_forwarder.py
CMD python3 mqtt_forwarder.py

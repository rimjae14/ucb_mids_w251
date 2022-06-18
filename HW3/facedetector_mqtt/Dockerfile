FROM ubuntu:latest
# this is needed to make sure we can see the log output
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y python3 python3-pip
#RUN a command to intall the MQTT python client 
# Copy your mosquitto_facedetector file into the container
CMD python3 mosquitto_facedetector.py

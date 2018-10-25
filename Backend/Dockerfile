FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim git python3-pip
RUN apt-get install -y build-essential mosquitto-clients  curl

# update pip
RUN pip3 install pip --upgrade
RUN pip3 install paho-mqtt python-dateutil flask flask_restful requests elasticsearch
RUN git clone -b development https://github.com/abhatikar/sensormonitoring.git
RUN ls sensormonitoring/Backend
EXPOSE 5000
CMD python3 sensormonitoring/Backend/backend.py
#RUN python3.6 -m pip install wheel

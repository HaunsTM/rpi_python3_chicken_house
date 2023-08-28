# RPI hen house
## Overview - the Pyhton part
This project aims to make different kinds of measurements from computer status and other sensors in a henhouse available in a home automation system. More specifically, it involves reading sensors for temperatures (to control a heat lamp), and a position indicator (LIDAR) for an entrance hatch (a guillotine-type hatch that is raised up and down with a relay-controlled motor) as well.

In the henhouse, the sensors are managed by a Raspberry Pi and it is also on this that the Python code executes. The Python script in turn communicates with a Node red application (javascript) where the data is refined before being published as MQTT for interested consumers in the home automation network. 

## MQTT
Topics:
iot/hen_house/hatch/lidar/data
iot/hen_house/hatch/lidar/heart_beat

iot/hen_house/cpu/load/data
iot/hen_house/cpu/temperature/data
iot/hen_house/system/diskSpace/data
iot/hen_house/system/memory/data

iot/hen_house/temperature/data
iot/hen_house/temperature/heart_beat

## API
In addition to publishing messages to the MQTT broker used in the home automation network, the Node red application is tasked with providing API endpoints such as
/openHatch
/pullActuator
/stopActuator
/pushActuator
/closeHatch

# Architecture
I have chosen this architecture (Python - Node red) because I found it most efficient and practical to communicate with external hardware so in my home automation network.

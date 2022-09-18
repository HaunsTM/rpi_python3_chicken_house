# -*- coding: utf-8 -*
import argparse
import serial
import random
import string
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import glob
import time
import os
import sys
#  An Example Reading from /sys/bus/w1/devices/<ds18b20-id>/w1_slave
#  a6 01 4b 46 7f ff 0c 10 5c : crc=5c YES
#  a6 01 4b 46 7f ff 0c 10 5c t=26375

import RPi.GPIO as GPIO


parser = argparse.ArgumentParser(description = 'Usage of ds18b20-script')
parser.add_argument("--broker_address", default = "localhost", type = str, help = "broker address")
parser.add_argument("--mqtt_topic_ds18b20_message", default = "ds18b20Message", type = str, help = "mqtt topic to publish lidar data on")
parser.add_argument("--mqtt_topic_heart_beat_message", default="heartBeat", type = str, help = "mqtt topic to publish heart beat on")
parser.add_argument("--heart_beat_frequency_ms", default = 2 * 1000, type = int, help="the frequency (1/ms) at which heartbeats are sent")
parser.add_argument("--gpio_pull_up_resistor", default = 27, type = int, help = "GPIO of pull up resistor")

args = parser.parse_args()

#  Set Pullup mode on GPIO4 first.
GPIO_PIN_NUMBER = args.gpio_pull_up_resistor
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def ds18b20_read_sensors():
  rtn = {}
  w1_devices = []
  w1_devices = os.listdir("/sys/bus/w1/devices/")
  for deviceid in w1_devices:
    rtn[deviceid] = {}
    rtn[deviceid]['temp_c'] = None
    device_data_file = "/sys/bus/w1/devices/" + deviceid + "/w1_slave"
    if os.path.isfile(device_data_file):
      try:
         f = open(device_data_file, "r")
         data = f.read()
         f.close()
         if "YES" in data:
           (discard, sep, reading) = data.partition(' t=')
           rtn[deviceid]['temp_c'] = float(reading) / float(1000.0)
         else:
           rtn[deviceid]['error'] = 'No YES flag: bad data.'
      except Exception as e:
         rtn[deviceid]['error'] = 'Exception during file parsing: ' + str(e)
    else:
      rtn[deviceid]['error'] = 'w1_slave file not found.'
  return rtn;

while True:
  temp_readings = ds18b20_read_sensors()
  for t in temp_readings:
    if not 'error' in temp_readings[t]:
      print(u"Device id '%s' reads %.3f +/- 0.5 °C" % (t, temp_readings[t]['temp_c']))
  #time.sleep(1.0)
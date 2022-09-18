# -*- coding: utf-8 -*
import argparse
from ds18b20 import ds18b20
import sys, os
sys.path.insert(0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.mqtt_client import mqtt_client
del sys.path[0]

import RPi.GPIO as GPIO


parser = argparse.ArgumentParser(description = 'Usage of ds18b20-script')
parser.add_argument("--broker_address", default = "localhost", type = str, help = "broker address")
parser.add_argument("--mqtt_topic_ds18b20_message", default = "ds18b20Message", type = str, help = "mqtt topic to publish lidar data on")
parser.add_argument("--mqtt_topic_heart_beat_message", default="ds18b20HeartBeat", type = str, help = "mqtt topic to publish heart beat on")
parser.add_argument("--heart_beat_frequency_ms", default = 2 * 1000, type = int, help="the frequency (1/ms) at which heartbeats are sent")
parser.add_argument("--gpio_pull_up_resistors", default = "4,17,27", type = str, help = "GPIO of pull up resistors, GPIO-list separated by ,")

args = parser.parse_args()

gpio_pull_up_resistors = [int(n) for n in args.gpio_pull_up_resistors.split(",")]


set_pullup_mode_on_current_resistors = ds18b20.set_pullup_mode_on_current_resistors(gpio_pull_up_resistors)

all_temperature_sensors_infos = ds18b20.all_temperature_sensors_infos()

all_sensor_data_collectors = list(map(ds18b20,all_temperature_sensors_infos))

mq = mqtt_client(args.broker_address, args.mqtt_topic_heart_beat_message)



while True:
    for sensor in all_sensor_data_collectors:
        sensor_data = sensor.get_sensor_data()

        mq.publish_message( args.mqtt_topic_ds18b20_message, sensor_data.to_json())
        sensor_data.set_initial_values()
        # print("Device id " + sensor_data.get_sensor_info().get_device_data_file() + "; Temp (°C): " + str(sensor_data.get_temperature_c()))
  #time.sleep(1.0)


i=0

y=9

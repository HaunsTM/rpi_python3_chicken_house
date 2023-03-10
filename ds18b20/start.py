# -*- coding: utf-8 -*
import argparse
from ds18b20 import ds18b20
import sys, os
sys.path.insert(0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.mqtt_client_reporter import mqtt_client_reporter
del sys.path[0]

import RPi.GPIO as GPIO


parser = argparse.ArgumentParser(description = 'Usage of ds18b20-script')
parser.add_argument("--broker_address", default = "localhost", type = str, help = "broker address")
parser.add_argument("--mqtt_topic_message", default = "ds18b20_message", type = str, help = "mqtt topic to publish lidar data on")
parser.add_argument("--mqtt_topic_heart_beat_message", default="ds18b20_heartBeat", type = str, help = "mqtt topic to publish heart beat on")
parser.add_argument("--heart_beat_frequency_ms", default = 2 * 1000, type = int, help="the frequency (1/ms) at which heartbeats are sent")
parser.add_argument("--gpio_pull_up_resistors", default = "4", type = str, help = "GPIO of pull up resistors, GPIO-list separated by ,")

args = parser.parse_args()

gpio_pull_up_resistors = [int(n) for n in args.gpio_pull_up_resistors.split(",")]


set_pullup_mode_on_current_resistors = ds18b20.set_pullup_mode_on_current_resistors(gpio_pull_up_resistors)

all_temperature_sensors_infos = ds18b20.all_temperature_sensors_infos()

all_sensor_data_collectors = list(map(ds18b20,all_temperature_sensors_infos))

mqtt_client_reporter = mqtt_client_reporter(args.broker_address, args.mqtt_topic_heart_beat_message)

def beat_heart():    
    mqtt_client_reporter.send_heart_beat_message_if_it_is_time_to_do_so(args.heart_beat_frequency_ms, os.getpid())

def report_sensor_values():
    for sensor in all_sensor_data_collectors:
        sensor_data = sensor.get_sensor_data(os.getpid())

        mqtt_client_reporter.publish_message( args.mqtt_topic_message, sensor_data.to_json())
        sensor_data.set_initial_values()

def run():
    while True:
        report_sensor_values()
        beat_heart()

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt: # ctrl + c in terminal.    
        print("program interrupted by the user")
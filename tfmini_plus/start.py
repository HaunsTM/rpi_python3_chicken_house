# -*- coding: utf-8 -*
import argparse
from tfmini_plus import tfmini_plus

import sys, os
sys.path.insert(0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.mqtt_client_reporter import mqtt_client_reporter
del sys.path[0]

parser = argparse.ArgumentParser(description = 'Usage of LIDAR-script')
parser.add_argument("--broker_address", default = "localhost", type = str, help = "broker address")
parser.add_argument("--mqtt_topic_message", default = "LIDAR_message", type = str, help = "mqtt topic to publish lidar data on")
parser.add_argument("--mqtt_topic_heart_beat_message", default="LIDAR_heartBeat", type = str, help = "mqtt topic to publish heart beat on")
parser.add_argument("--heart_beat_frequency_ms", default = 2 * 1000, type = int, help="the frequency (1/ms) at which heartbeats are sent")

parser.add_argument("--tfmini_plus_port", default = "/dev/ttyAMA0", type = str, help = "port to connect to tf mini plus")
parser.add_argument("--tfmini_plus_baud_rate", default = 115200, type = int, help = "speed communicate with tf mini plus")

args = parser.parse_args()

tfmini_plus = tfmini_plus(args.tfmini_plus_port, args.tfmini_plus_baud_rate, os.getpid())

mqtt_client_reporter = mqtt_client_reporter(args.broker_address, args.mqtt_topic_heart_beat_message)

def beat_heart():    
    mqtt_client_reporter.send_heart_beat_message_if_it_is_time_to_do_so(args.heart_beat_frequency_ms, os.getpid())

def report_sensor_value():
    tfmini_plus.ensure_serial_is_open()
    if tfmini_plus.sensor_data_is_available():
        sensor_data = tfmini_plus.get_sensor_data()
        mqtt_client_reporter.publish_message(args.mqtt_topic_message, sensor_data.to_json())

def run():
    while True:
        report_sensor_value()
        beat_heart()

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt: # ctrl + c in terminal.
    
        tfmini_plus.close_serial()
        print("program interrupted by the user")



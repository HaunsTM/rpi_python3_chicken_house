# -*- coding: utf-8 -*
import argparse
from tfmini_plus import tfmini_plus
from datetime import datetime, timezone
import sys, os
sys.path.insert(0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.mqtt_client import mqtt_client
del sys.path[0]

parser = argparse.ArgumentParser(description = 'Usage of LIDAR-script')
parser.add_argument("--broker_address", default = "localhost", type = str, help = "broker address")
parser.add_argument("--mqtt_topic_lidar_message", default = "lidarMessage", type = str, help = "mqtt topic to publish lidar data on")
parser.add_argument("--mqtt_topic_heart_beat_message", default="heartBeat", type = str, help = "mqtt topic to publish heart beat on")
parser.add_argument("--heart_beat_frequency_ms", default = 2 * 1000, type = int, help="the frequency (1/ms) at which heartbeats are sent")

parser.add_argument("--tfmini_plus_port", default = "/dev/ttyAMA0", type = str, help = "port to connect to tf mini plus")
parser.add_argument("--tfmini_plus_baud_rate", default = 115200, type = int, help = "speed communicate with tf mini plus")

args = parser.parse_args()

tfmini_plus = tfmini_plus(args.tfmini_plus_port, args.tfmini_plus_baud_rate)

client = mqtt_client(args.broker_address, args.mqtt_topic_heart_beat_message)


last_reported_heart_beat_time = -1
next_time_heart_beat_time = -1

def beat_heart():
    global last_reported_heart_beat_time, next_time_heart_beat_time
    utc = datetime.now(timezone.utc).timestamp() * 1000

    if next_time_heart_beat_time < utc:
        last_reported_heart_beat_time = utc
        next_time_heart_beat_time = last_reported_heart_beat_time + args.heart_beat_frequency_ms
        client.publish_message(args.mqtt_topic_heart_beat_message, str(utc))

def report_sensor_value():
    tfmini_plus.ensure_serial_is_open()
    sensor_data = tfmini_plus.get_sensor_data()
    if tfmini_plus.sensor_data_is_available():
        client.publish_message(args.mqtt_topic_lidar_message, sensor_data.to_json())

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



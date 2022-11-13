# -*- coding: utf-8 -*
from ds18b20_data import ds18b20_data
from ds18b20_sensor_info import ds18b20_sensor_info
import os
import RPi.GPIO as GPIO

class ds18b20:

    def __init__( self, sensor_info: ds18b20_sensor_info):
        self._sensor_info: ds18b20_sensor_info = sensor_info

    @staticmethod
    def set_pullup_mode_on_current_resistors(gpio_resitors):
        for gpio in gpio_resitors:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @staticmethod
    def all_temperature_sensors_infos() -> list[ds18b20_sensor_info]:
        valid_sensor_infos = []
        all_w1_devices = os.listdir("/sys/bus/w1/devices/")
        for device_id in all_w1_devices:
            device_data_file = "/sys/bus/w1/devices/" + device_id + "/w1_slave"
            if os.path.isfile(device_data_file):
                sensor_infos = ds18b20_sensor_info(device_data_file)
                valid_sensor_infos.append(sensor_infos)
        return valid_sensor_infos    

    def get_sensor_data(self, pid: int) -> ds18b20_data:
        sensor_data = ds18b20_data(self._sensor_info, pid)

        device_data_file = sensor_data.get_sensor_info().get_device_data_file()
        try:
            f = open(device_data_file, "r")
            data = f.read()
            f.close()
            
            if "YES" in data:
                (discard, sep, reading) = data.partition(' t=')
                temperature_c = float(reading) / float(1000.0)
                sensor_data.set_temperature_c( temperature_c )
            else:
                error = 'No YES flag: bad data.'
                sensor_data.set_error( error )
        except Exception as e:
            error = 'Exception during file parsing: ' + str(e)
            sensor_data.set_error( error )

        return sensor_data
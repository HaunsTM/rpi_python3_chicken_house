# -*- coding: utf-8 -*
class ds18b20_sensor_info:

    def __init__(self, device_data_file):
    # def __init__(self, gpio_in_number, device_data_file):
        self._device_data_file = device_data_file

    def get_device_data_file(self):
        return self._device_data_file
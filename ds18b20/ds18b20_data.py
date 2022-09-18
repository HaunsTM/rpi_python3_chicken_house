import ds18b20_sensor_info
# -*- coding: utf-8 -*
class ds18b20_data:

    def __init__(self, sensor_info: ds18b20_sensor_info):
        self._sensor_info = sensor_info

        self._NO_ERROR = "NO ERROR"
        self._INVALID_TEMPETRATURE_C = -300

        self.set_initial_values()   

    def get_sensor_info(self) -> ds18b20_sensor_info:
        return self._sensor_info


    def get_error(self):
        return self._error

    def set_error(self, error):
        self._error = error


    def get_temperature_c(self) -> float:
        return self._temperature_c

    def set_temperature_c(self, temperature_c: float):
        self._temperature_c = temperature_c


    def set_initial_values(self):
        self._temperature_c = self._INVALID_TEMPETRATURE_C
        self._error = self._NO_ERROR

    def to_json(self):
        json = '{ "device_data_file":"' + str(self._sensor_info.get_device_data_file()) + '", "temperature_c":' + str(self._temperature_c) + ', "error":"' + str(self._error) + '"}'
        return json

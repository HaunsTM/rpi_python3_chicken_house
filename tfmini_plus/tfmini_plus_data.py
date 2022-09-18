# -*- coding: utf-8 -*
class tfmini_plus_data:

    def __init__(self):
        self._NO_DISTANCE_CM = -1
        self._NO_VALID_DATA = "NO VALID DATA"
        self._NO_ERROR = "NO ERROR"
        self._NO_STRENGTH = -1
        self._INVALID_TEMPETRATURE_C = -300

        self.set_initial_values()

    def get_distance_cm(self) -> float:
        return self._distance_cm

    def set_distance_cm(self, distance_cm: float):
        self._distance_cm = distance_cm

    def get_error(self) -> str:
        return self._error

    def set_error(self, error):
        self._error = error

    def get_strength(self) -> int:
        return self._strength

    def set_strength(self, strength: int):
        self._strength = strength

    def get_temperature_c(self) -> float:
        return self._temperature_c

    def set_temperature_c(self, temperature_c: float):
        self._temperature_c = temperature_c

    def set_initial_values(self):
        self._distance_cm = self._NO_DISTANCE_CM
        self._error = self._NO_VALID_DATA
        self._strength = self._NO_STRENGTH
        self._temperature_c = self._INVALID_TEMPETRATURE_C

    def set_values(self, distance_cm: float, strength: int, temperature_c: float):
        self._distance_cm = distance_cm
        self._strength = strength
        self._temperature_c = temperature_c
        self._error = self._NO_ERROR

    def to_json(self):
        json = '{"distance_cm":' + str(self._distance_cm) + ', "strength":' + str(self._strength) + ', "temperature_c":' + str(self._temperature_c) + ', "error":"' + str(self._error) + '"}'
        return json

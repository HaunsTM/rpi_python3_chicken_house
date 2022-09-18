# -*- coding: utf-8 -*
import serial
from tfmini_plus_data import tfmini_plus_data

class tfmini_plus:

    def __init__(self, port, baud_rate: int):
        self._port = port
        self._baud_rate = baud_rate
        self._serial = serial.Serial(port, baud_rate)
    
    def ensure_serial_is_closed(self):
        if self._serial != None and self._serial.isOpen() == True:
            self._serial.close()

    def ensure_serial_is_open(self):
        if self._serial.isOpen() == False:
            self._serial.open()

    def sensor_data_is_available(self) -> bool:
        counter = self._serial.in_waiting # count the number of bytes of the serial port

        return counter > 8

    # we define a new function that will get the data from LiDAR and publish it
    def get_sensor_data(self) -> tfmini_plus_data:
        counter = self._serial.in_waiting # count the number of bytes of the serial port
        sensor_data = tfmini_plus_data()

        if counter > 8:
            bytes_serial = self._serial.read(9)
            self._serial.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # this portion is for python3
                distance_cm = bytes_serial[2] + bytes_serial[3]*256 # multiplied by 256, because the binary data is shifted by 8 to the left (equivalent to "<< 8").                                              # Dist_L, could simply be added resulting in 16-bit data of Dist_Total.
                strength = bytes_serial[4] + bytes_serial[5]*256
                temperature_c = bytes_serial[6] + bytes_serial[7]*256
                temperature_c = (temperature_c/8) - 256
                sensor_data.set_values(distance_cm, strength, temperature_c)
                self._serial.reset_input_buffer()

            if bytes_serial[0] == "Y" and bytes_serial[1] == "Y":
                distL = int(bytes_serial[2].encode("hex"), 16)
                distH = int(bytes_serial[3].encode("hex"), 16)
                stL = int(bytes_serial[4].encode("hex"), 16)
                stH = int(bytes_serial[5].encode("hex"), 16)
                distance_cm = distL + distH*256
                strength = stL + stH*256
                tempL = int(bytes_serial[6].encode("hex"), 16)
                tempH = int(bytes_serial[7].encode("hex"), 16)
                temperature_c = tempL + tempH*256
                temperature_c = (temperature_c/8) - 256
                sensor_data.set_values(distance_cm, strength, temperature_c)
                self._serial.reset_input_buffer()

        return sensor_data

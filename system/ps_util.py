# -*- coding: utf-8 -*
from typing import List
from psax_data import psax_data
import subprocess
import re

class ps_util:

    def get_active_processes(self, value_delimiter: str) -> str:
        ax_parameters = ("%C" + value_delimiter + "%G" + value_delimiter + "%P" + value_delimiter + "%U" + value_delimiter + "%a" + value_delimiter + "%c" + value_delimiter + "%g" + value_delimiter + "%n" + value_delimiter + "%p" + value_delimiter + "%r" + value_delimiter + "%t" + value_delimiter + "%u" + value_delimiter + "%x" + value_delimiter + "%y" + value_delimiter + "%z")
        ax_command = "ps ax -o '{0}'".format(ax_parameters)

        output = subprocess.getoutput(ax_command)

        return output

    def get_active_processes_array(self, value_delimiter: str) -> list[str]:    
        row_delimiter = "\n"
        active_processes_array = self.get_active_processes(value_delimiter).split(row_delimiter)

        return active_processes_array

    def get_active_processes_json(self) -> str:
        value_delimiter = ";"
        active_processes_array = self.get_active_processes_array(value_delimiter)

        active_processes_json = "["

        first_data_row_index = 1
        start = first_data_row_index
        stop = len(active_processes_array)
        step = 1
        for i in range(start, stop, step):   # omit header row
            row = active_processes_array[i]
            parsed_row = psax_data(row, value_delimiter)
            active_processes_json += parsed_row.to_json()
            if i < stop - 1:
                active_processes_json += ","

        active_processes_json += "]"

        return active_processes_json
# -*- coding: utf-8 -*
from typing import List
from psax_data import psax_data
import subprocess



def get_active_processes(value_delimiter: str) -> str:
    ax_parameters = ("%C" + value_delimiter + "%G" + value_delimiter + "%P" + value_delimiter + "%U" + value_delimiter + "%a" + value_delimiter + "%c" + value_delimiter + "%g" + value_delimiter + "%n" + value_delimiter + "%p" + value_delimiter + "%r" + value_delimiter + "%t" + value_delimiter + "%u" + value_delimiter + "%x" + value_delimiter + "%y" + value_delimiter + "%z")
    ax_command = "ps ax -o '{0}'".format(ax_parameters)

    output = subprocess.getoutput(ax_command)

    return output

def get_active_processes_array(value_delimiter: str) -> list[str]:    
    row_delimiter = "\n"
    active_processes_array = get_active_processes(value_delimiter).split(row_delimiter)

    return active_processes_array

def get_active_processes_json() -> str:
    value_delimiter = ";"
    active_processes_array = get_active_processes_array(value_delimiter)

    active_processes_json = "["

    for i, row in enumerate(active_processes_array, start=1):   # omit header row
        parsed_row = psax_data(row, value_delimiter)
        active_processes_json += parsed_row.to_json()

    active_processes_json += "]"

    return active_processes_json

k = get_active_processes_json()

i=8
# -*- coding: utf-8 -*
import json

class psax_data:

    def __init__(self, data_row: str, delimiter: str):
        self._data_row = data_row
        self._delimiter = delimiter

    def get_pcpu(self) -> str:
        return self.get_element_by_index(0)

    def get_group(self) -> str:
        return self.get_element_by_index(1)

    def get_ppid(self) -> str:
        return self.get_element_by_index(2)

    def get_user(self) -> str:
        return self.get_element_by_index(3)

    def get_args(self) -> str:
        return self.get_element_by_index(4)

    def get_comm(self) -> str:
        return self.get_element_by_index(5)

    def get_rgroup(self) -> str:
        return self.get_element_by_index(6)

    def get_nice(self) -> str:
        return self.get_element_by_index(7)

    def get_pid(self) -> str:
        return self.get_element_by_index(8)

    def get_pgid(self) -> str:
        return  self.get_element_by_index(9)

    def get_etime(self) -> str:
        return self.get_element_by_index(10)

    def get_ruser(self) -> str:
        return self.get_element_by_index(11)

    def get_time(self) -> str:
        return self.get_element_by_index(12)

    def get_tty(self) -> str:
        return self.get_element_by_index(13)

    def get_vsz(self) -> str:
        return  self.get_element_by_index(14)
    
    def get_element_by_index(self, index: int) -> str:
        value = self._data_row.split(self._delimiter)[index].strip()
        return value
    
    def to_json(self) -> str:
        json_string = (
            '{"pcpu":' + json.dumps(self.get_pcpu()) + ',' +
            '"group":' + json.dumps(self.get_group()) + ',' +
            '"ppid":' + json.dumps((self.get_ppid() if self.get_ppid().isnumeric() else '"n/a"')) + ',' +
            '"user":' + json.dumps(self.get_user()) + ',' +
            '"args":' + json.dumps(self.get_args()) + ',' +
            '"comm":' + json.dumps(self.get_comm()) + ',' +
            '"rgroup":' + json.dumps(self.get_rgroup()) + ',' +
            '"nice":' + json.dumps((self.get_nice() if self.get_nice().isnumeric() else '"n/a"')) + ',' +
            '"pid":' + json.dumps((self.get_pid() if self.get_pid().isnumeric() else '"n/a"')) + ',' +
            '"pgid":' + json.dumps((self.get_pgid() if self.get_pgid().isnumeric() else '"n/a"')) + ',' +
            '"etime":' + json.dumps(self.get_etime()) + ',' +
            '"ruser":' + json.dumps(self.get_ruser()) + ',' +
            '"time":' + json.dumps(self.get_time()) + ',' +
            '"tty":' + json.dumps(self.get_tty()) + ',' +
            '"vsz":' + json.dumps((self.get_vsz() if self.get_vsz().isnumeric() else '"n/a"')) + '}')

        return json_string
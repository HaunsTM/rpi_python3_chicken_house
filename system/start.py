# -*- coding: utf-8 -*
import argparse
import sys
from ps_util import ps_util


parser = argparse.ArgumentParser(description = 'Usage of system-script')
parser.add_argument("--method", required = True, default = "NO METHOD", type = str, help = "name of method to invoke")
#parser.add_argument("--method",  default = "get_active_processes_json", type = str, help = "name of method to invoke")

args = parser.parse_args()


def get_active_processes_json() -> str:
    ps = ps_util()
    active_processes_json = ps.get_active_processes_json()
    
    sys.stdout.write(active_processes_json)
    sys.stdout.flush()
    
    sys.exit(0)

def no_defined_method_selected() -> str:
    print("Please select a valid method")

if __name__ == "__main__":
    try:
        if args.method == 'get_active_processes_json':
            get_active_processes_json()        
        else:
            no_defined_method_selected()
    except KeyboardInterrupt: # ctrl + c in terminal.
        sys.exit(1)
        print("program interrupted by the user")
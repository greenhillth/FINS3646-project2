""" Aux functions to verify the project2_main.py module

Simply run this module to verify that:

1. The project2/project2_main.py module can be found in the path

2. Any function defined inside `project2_main.py` (whose name does not start
   with and underscore) is one of the functions you need to complete.

3. There are no imports other than 0s, pandas, and tk_utils


Important: This function will not verify if you have completed the body of any
function. It simply ensures the module can be imported and examines that
module's namespace.

         
"""
import os

import pandas as pd

import toolkit_config as cfg
from project2 import project2_main as prj


def verify_ns():
    """ This function will verify that only valid names are defined in the
    global namespace of project2_main.py
    """
    valid_names = {
            'os',
            'pd',
            'np',
            'tk_utils',
            'read_dat',
            'str_to_float',
            'fmt_col_names',
            'read_ret_dat',
            'read_prc_dat',
            'mk_ret_df',
            'fmt_col_name',
            'fmt_ticker',
            }
            
    # Check the namespace of the `prj` module
    ns = {k:v for k, v in vars(prj).items() if not k.startswith('_')}

    invalid = {k:v for k, v in ns.items() if k not in valid_names}

    if len(invalid) > 0:
        err = [
            'Verification failed',
            'The following names are improperly defined in the project2_main.py module',
            ] + [f" - {x}" for x in invalid]
        raise Exception('\n'.join(err))
    else:
        print('Done')




if __name__ == "__main__":
    verify_ns()
    






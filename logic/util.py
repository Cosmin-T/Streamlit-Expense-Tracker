# util.py

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(SCRIPT_DIR, 'data.json')

def get_json_file_path():
    # Return the path to the JSON file
    return FILE_NAME
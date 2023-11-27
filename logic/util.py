# util.py

import os
from pathlib import Path

DETA_KEY = 'a0jtvvxnh2x_7Dxsy9FxkYMvoZjtxeCAvQFjJgh1adZ2'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(SCRIPT_DIR, 'data.json')
HASHED_FILE = os.path.join(SCRIPT_DIR, 'hashed_pw.pkl')
INSTALMENTS_PATH = os.path.join(SCRIPT_DIR, 'instalments.json')

def get_json_file_path():
    # Return the path to the JSON file
    return FILE_NAME
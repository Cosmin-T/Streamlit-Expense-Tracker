# util.py

import os
from pathlib import Path
from dotenv import load_dotenv, get_key
import os
import logging
import glob
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(SCRIPT_DIR, 'data.json')
HASHED_FILE = os.path.join(SCRIPT_DIR, 'hashed_pw.pkl')
INSTALMENTS_PATH = os.path.join(SCRIPT_DIR, 'instalments.json')
INSTALMENTS_DOWNLOAD = os.path.join(SCRIPT_DIR, 'instalments.csv')

def get_json_file_path() -> str:
    """
    Return the path to the JSON file containing the expense data.

    Returns:
        str: The path to the JSON file.
    """
    # Return the path to the JSON file
    return FILE_NAME


dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path, override=True)


HOST = os.getenv('HOST')
print(f'HOST IS: {HOST}')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')
KEY = os.getenv('KEY')
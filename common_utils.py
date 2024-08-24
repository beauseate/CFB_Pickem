"""
common_utils.py
"""

from configparser import ConfigParser
CONFIG_FILE = 'config.ini'


def get_config():
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config

def validate_number(num):
    while not num.isdigit():
       num = input("Please enter a valid number: ")
    return int(num)
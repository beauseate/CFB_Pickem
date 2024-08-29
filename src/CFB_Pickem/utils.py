"""
utils.py
"""
import datetime
from configparser import ConfigParser


CONFIG_FILE = 'config.ini'
CUR_YEAR = str(datetime.date.today().year)


def get_config():
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config

def get_sheet_service_account():
    return get_config().get('Sheet', 'service_account')

def get_sheet_name():
    return get_config().get('Sheet', 'name')

def validate_number(num):
    while not num.isdigit():
       num = input("Please enter a valid number: ")
    return int(num)

def get_year():
    year = CUR_YEAR
    ans = input(f"Would you like to enter a different year than {CUR_YEAR}? (y/n): ")
    while ans not in ('y', 'n'):
        print("Please select a valid option")
        ans = input(f"Would you like to enter a different year than {CUR_YEAR}? (y/n): ")
    if ans == 'y':
        year = input("Please enter the year: ")

    return validate_number(year)

def get_week():
    week = input("Enter the week of CFB: ")
    return validate_number(week)

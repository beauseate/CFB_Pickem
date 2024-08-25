"""
sheet_utils.py
"""
from common_utils import get_config


def get_service_account():
    return get_config().get('Sheet', 'service_account')

def get_name():
    return get_config().get('Sheet', 'name')

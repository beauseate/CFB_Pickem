"""
main.py
"""
import utils
from cfbd_api import CFBD_API
from cfb_pickem import CFBPickem

def main():
    auth = utils.get_sheet_service_account()
    sheet_name = utils.get_sheet_name()

    year = utils.get_year()
    week = utils.get_week()
    cfbd_api = CFBD_API(year, week)

    cfb_pickem = CFBPickem(auth, sheet_name, cfbd_api)

    cfb_pickem.update_this_weeks_spread()
    cfb_pickem.update_weeks_scores()
    
if __name__ == "__main__":
    try:
        main()
    except Exception as exception:
        raise SystemExit(f"Error: {exception}") from exception

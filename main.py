"""
main.py
"""
import datetime
import sheet_utils
import common_utils
from cfbd_api import CFBD_API
from schedule import Schedule
from individual_scoresheet import IndividualScoreSheet

CUR_YEAR = datetime.date.today().year

def main():
    ans = input(f"Would you like to enter a different year than {CUR_YEAR}? (y/n): ")
    while ans not in ('y', 'n'):
        print("Please select a valid option")
        ans = input(f"Would you like to enter a different year than {CUR_YEAR}? (y/n): ")
    if ans == 'y':
        year = input("Please enter the year: ")
        year = common_utils.validate_number(year)
    else:
        year = CUR_YEAR
    week = input("Enter the week of CFB: ")
    week = common_utils.validate_number(week)

    auth = sheet_utils.get_service_account()
    sheet_name = sheet_utils.get_name()
    cfbd_api = CFBD_API(year, week)

    schedule_sheet = Schedule(auth=auth, sheet_name=sheet_name, worksheet='Schedule', cfbd_api=cfbd_api)
    schedule_sheet.update_schedule_scores()

    individual_score_sheet = IndividualScoreSheet(auth=auth,
                                                  sheet_name=sheet_name,
                                                  worksheet='',
                                                  cfbd_api=cfbd_api,
                                                  total_score=0)
    individual_score_sheet.update_individual_scoreshet()
    print("Complete!")

if __name__ == "__main__":
    try:
        main()
    except Exception as exception:
        raise SystemExit(f"Error: {exception}") from exception

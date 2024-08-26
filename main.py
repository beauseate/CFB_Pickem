"""
main.py
"""
import datetime
import sheet_utils
import common_utils
from cfbd_api import CFBD_API
from schedule import Schedule
from sheet import Sheet
from individual_scoresheet import IndividualScoreSheet
from scoreboard import Scoreboard

CUR_YEAR = datetime.date.today().year

def main():
    scores_dict = {}
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

    schedule_sheet = Schedule(auth=auth, sheet_name=sheet_name, cfbd_api=cfbd_api)
    schedule_sheet.update_schedule()

    sheet = Sheet(auth=auth,  sheet_name=sheet_name)
    worksheets = sheet.spreadsheet.worksheets()

    # scoreboard = Scoreboard(auth=auth, sheet_name=sheet_name, cfbd_api=cfbd_api)
    for worksheet in worksheets:
        worksheet_name = worksheet.title
        if (worksheet_name == 'Schedule') or (worksheet_name == 'Scoreboard'):
            continue

        individual_score_sheet = IndividualScoreSheet(auth=auth,
                                                      sheet_name=sheet_name,
                                                      worksheet=worksheet_name,
                                                      cfbd_api=cfbd_api)
        individual_score_sheet.update_individual_scoreshet()
        weeks_score = individual_score_sheet.get_weeks_score()
        scores_dict[worksheet_name] = weeks_score
    # scoreboard.calculate_scoreboard(scores_dict)
    
    print("Complete!")

if __name__ == "__main__":
    try:
        main()
    except Exception as exception:
        raise SystemExit(f"Error: {exception}") from exception

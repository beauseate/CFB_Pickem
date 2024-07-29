"""
main.py
"""
import datetime
from cfbd_api import CFBD_API
from excel import Excel


spreadsheet = 'CFB_Data\\TestingSpreadsheet.xlsx'
sheet_name = 'Schedule'
CUR_YEAR = datetime.date.today().year

def validate_number(num):
    while not num.isdigit():
       num = input("Please enter a valid number: ")
    return num

def main():
    ans = input(f"Would you like to enter a different year than {CUR_YEAR}? (y/n): ")
    while ans not in ('y', 'n'):
        print("Please select a valid option")
        ans = input(f"Would you like to enter a different year than {CUR_YEAR}? (y/n): ")
    if ans == 'y':
        year = input("Please enter the year: ")
        year = validate_number(year)
    else:
        year = CUR_YEAR
    week = input("Enter the week of CFB: ")
    week = validate_number(week)

    year = int(year)
    week = int(week)

    cfbd_api = CFBD_API(year, week)
    excel = Excel(spreadsheet, sheet_name)
    print('Please wait while we update the scores...')
    print(excel.get_weeks_matchups(week=week))
    for matchup in excel.get_weeks_matchups(week=week):
        away_team = matchup['Away Team']
        home_team = matchup['Home Team']
        game_score = cfbd_api.get_game_score(away_team, home_team)
        excel.update_score(game_score, away_team, home_team)

    print('Scores updated!')

if __name__ == "__main__":
    try:
        main()
    except Exception as exception:
        raise SystemExit(f"Error: {exception}") from exception




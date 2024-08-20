import pandas as pd
import logging
import urllib3
import gspread
from gspread_dataframe import set_with_dataframe
from gspread_formatting import CellFormat, Color, format_cell_ranges, TextFormat
from oauth2client.service_account import ServiceAccountCredentials


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s"
)

class Sheet():

    def __init__(self, auth, sheet_name, subsheet='Schedule'):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(auth, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name)
        
        self.worksheet = sheet.worksheet(subsheet)
        records = self.worksheet.get_all_records()
        self.pandas_df = pd.DataFrame(records)
        self.log = logging.getLogger(__name__)
    
    def get_score_mask(self, away_team, home_team):
        return (self.pandas_df['Away Team'] == away_team) & (self.pandas_df['Home Team'] == home_team)
    
    def update_score(self, score, away_team, home_team):
        score_mask = self.get_score_mask(away_team, home_team)
        self.pandas_df.loc[score_mask, 'Home Points'] = score['home_points']
        self.pandas_df.loc[score_mask, 'Away Points'] = score['away_points']
    
    def get_weeks_matchups(self, week):
        weeks_matchups = self.pandas_df[self.pandas_df['Week'] == week]
        return [{'Away Team': row['Away Team'],
                 'Home Team': row['Home Team']}
                 for _, row in weeks_matchups.iterrows()]
    
    def highlight_winning_team(self):
        batch_update = []
        yellow_format = CellFormat(backgroundColor=Color(1.0, 1.0, 0.7), textFormat=TextFormat(bold=True))
        for i, (_, row) in enumerate(self.pandas_df.iterrows(), start=2):
            
            home_points = row['Home Points']
            away_points = row['Away Points']
            if home_points > away_points:
                batch_update.append((f'F{i}', yellow_format))
                batch_update.append((f'G{i}', yellow_format))
            elif home_points < away_points:
                batch_update.append((f'D{i}', yellow_format))
                batch_update.append((f'E{i}', yellow_format))
        
        format_cell_ranges(self.worksheet, batch_update)

    
    def save_sheet(self):
        set_with_dataframe(self.worksheet, self.pandas_df)

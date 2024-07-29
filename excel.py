import pandas as pd
import logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s"
)

class Excel():

    def __init__(self, spreadsheet, sheet_name):
        self.df = pd.read_excel(spreadsheet, sheet_name=sheet_name)
        self.path = spreadsheet
        self.sheet_name = sheet_name
        self.log = logging.getLogger(__name__)
    
    def get_score_mask(self, away_team, home_team):
        return (self.df['Away Team'] == away_team) & (self.df['Home Team'] == home_team)
    
    def update_score(self, score, away_team, home_team):
        score_mask = self.get_score_mask(away_team, home_team)
        self.df.loc[score_mask, 'Home Points'] = score['home_points']
        self.df.loc[score_mask, 'Away Points'] = score['away_points']
        self.save_excel()
    
    def get_weeks_matchups(self, week):
        weeks_matchups = self.df[self.df['Week'] == week]
        return [{'Away Team': row['Away Team'],
                 'Home Team': row['Home Team']}
                 for _, row in weeks_matchups.iterrows()]
    
    def save_excel(self):
        self.df.to_excel(self.path, sheet_name=self.sheet_name, index=False)

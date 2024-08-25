"""
score_sheet.py
"""
from sheet import Sheet

class ScoreSheet(Sheet):
    
    def __init__(self, auth, sheet_name, worksheet, cfbd_api):
        super().__init__(auth, sheet_name, worksheet)
        self.cfbd_api = cfbd_api
    
    def get_score_mask(self, away_team, home_team):
        return (self.pandas_df['Away Team'] == away_team) & \
               (self.pandas_df['Home Team'] == home_team) & \
               (self.pandas_df['Week'] == self.cfbd_api.week)

    def get_weeks_matchups(self):
        weeks_matchups = self.pandas_df[self.pandas_df['Week'] == self.cfbd_api.week]
        return [{'Away Team': row['Away Team'],
                 'Home Team': row['Home Team']}
                 for _, row in weeks_matchups.iterrows()]
    
    def get_game_score(self, matchup):
        away_team = matchup['Away Team']
        home_team = matchup['Home Team']
        return self.cfbd_api.get_game_score(away_team, home_team)
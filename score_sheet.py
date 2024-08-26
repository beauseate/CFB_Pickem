"""
score_sheet.py
"""
from sheet import Sheet

class ScoreSheet(Sheet):
    
    def __init__(self, auth, sheet_name, cfbd_api):
        super().__init__(auth, sheet_name)
        self.cfbd_api = cfbd_api
    
    def get_this_week_mask(self, away_team, home_team):
        return (self.pandas_df['Away Team'] == away_team) & \
               (self.pandas_df['Home Team'] == home_team) & \
               (self.pandas_df['Week'] == self.cfbd_api.week)

    def get_next_week_mask(self, away_team, home_team):
        week = self.cfbd_api.week + 1 if self.cfbd_api.week + 1 <= 14 else 14
        return (self.pandas_df['Away Team'] == away_team) & \
               (self.pandas_df['Home Team'] == home_team) & \
               (self.pandas_df['Week'] == week)

    def get_weeks_matchups(self):
        weeks_matchups = self.pandas_df[self.pandas_df['Week'] == self.cfbd_api.week]
        return [{'Away Team': row['Away Team'],
                 'Home Team': row['Home Team']}
                 for _, row in weeks_matchups.iterrows()]
    
    def get_next_weeks_matchups(self):
        week = self.cfbd_api.week + 1 if self.cfbd_api.week + 1 <= 14 else 14
        weeks_matchups = self.pandas_df[self.pandas_df['Week'] == week]
        return [{'Away Team': row['Away Team'],
                 'Home Team': row['Home Team']}
                 for _, row in weeks_matchups.iterrows()]
    
    def get_game_score(self, matchup):
        away_team = matchup['Away Team']
        home_team = matchup['Home Team']
        return self.cfbd_api.get_game_score(away_team, home_team)
    
    def get_this_week_game_spread(self, week, matchup):
        away_team = matchup['Away Team']
        home_team = matchup['Home Team']
        return self.cfbd_api.get_game_spread(week, away_team, home_team)
    
    def get_next_week_game_spread(self, week, matchup):
        away_team = matchup['Away Team']
        home_team = matchup['Home Team']
        return self.cfbd_api.get_game_spread(week, away_team, home_team)
    
    def update_pd_next_week_spread_frame(self, spread, matchup):
        spread_mask = self.get_next_week_mask(matchup['Away Team'], matchup['Home Team'])
        self.pandas_df.loc[spread_mask, 'Spread'] = spread
    
    def update_pd_this_week_spread_frame(self, spread, matchup):
        spread_mask = self.get_this_week_mask(matchup['Away Team'], matchup['Home Team'])
        self.pandas_df.loc[spread_mask, 'Spread'] = spread
    
    def update_next_weeks_spread(self):
        print("Updating next week's spread...")
        week = self.cfbd_api.week + 1 if self.cfbd_api.week + 1 <= 14 else 14
        for matchup in self.get_next_weeks_matchups():
            spread = self.get_next_week_game_spread(week, matchup)
            self.update_pd_next_week_spread_frame(spread, matchup)
    
    def update_this_weeks_spread(self):
        print("Updating this week's spread...")
        for matchup in self.get_weeks_matchups():
            spread = self.get_this_week_game_spread(self.cfbd_api.week, matchup)
            self.update_pd_this_week_spread_frame(spread, matchup)

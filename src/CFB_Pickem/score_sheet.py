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

    def get_this_weeks_matchups(self):
        print('Getting this weeks matchups...')
        weeks_matchups = self.pandas_df[self.pandas_df['Week'] == self.cfbd_api.week]
        return [{'Away Team': row['Away Team'],
                 'Home Team': row['Home Team']}
                 for _, row in weeks_matchups.iterrows()]
    
    def get_next_weeks_matchups(self):
        week = self.cfbd_api.week + 1
        if week >= 15:
            return []
        print('Getting next weeks matchups...')
        weeks_matchups = self.pandas_df[self.pandas_df['Week'] == week]
        return [{'Away Team': row['Away Team'],
                 'Home Team': row['Home Team']}
                 for _, row in weeks_matchups.iterrows()]
    
    def get_game_scores(self, matchups):
        print('Getting this weeks game scores...')
        return [self.cfbd_api.get_game_score(matchup['Away Team'], matchup['Home Team']) for matchup in matchups]
    
    def get_this_week_game_spread(self, matchups):
        print('Getting this weeks game spreads...')
        return [self.cfbd_api.get_game_spread(self.cfbd_api.week, matchup['Away Team'], matchup['Home Team']) for matchup in matchups]
    
    def get_next_week_game_spread(self, matchups):
        week = self.cfbd_api.week + 1
        if week >= 15:
            return []
        print('Getting next weeks game spreads...')
        return [self.cfbd_api.get_game_spread(week, matchup['Away Team'], matchup['Home Team']) for matchup in matchups]
    
    def update_pd_next_week_spread_frame(self, matchup, spread):
        spread_mask = self.get_next_week_mask(matchup['Away Team'], matchup['Home Team'])
        self.pandas_df.loc[spread_mask, 'Spread'] = spread
    
    def update_pd_this_week_spread_frame(self, spread, matchup):
        spread_mask = self.get_this_week_mask(matchup['Away Team'], matchup['Home Team'])
        self.pandas_df.loc[spread_mask, 'Spread'] = spread
    
    def update_next_weeks_spread(self, next_weeks_matchups, next_weeks_spreads):
        print('Updating next weeks spread...')
        for matchup, spread in zip(next_weeks_matchups, next_weeks_spreads):
            self.update_pd_next_week_spread_frame(matchup, spread)
    
    def update_this_weeks_spread(self):
        print("Updating this week's spread...")
        for matchup in self.get_this_weeks_matchups():
            spread = self.get_this_week_game_spread(self.cfbd_api.week, matchup)
            self.update_pd_this_week_spread_frame(spread, matchup)

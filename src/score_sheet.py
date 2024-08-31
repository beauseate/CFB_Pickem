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
    
    def update_next_weeks_spread(self, next_weeks_matchups, next_weeks_spreads):
        print('Updating next weeks spread...')
        for matchup, spread in zip(next_weeks_matchups, next_weeks_spreads):
            next_week_spread_mask = self.get_next_week_mask(matchup['Away Team'], matchup['Home Team'])
            self.pandas_df.loc[next_week_spread_mask, 'Spread'] = spread
    
    def update_this_weeks_spread(self, this_weeks_matchups, this_weeks_spreads):
        print("Updating this week's spread...")
        for matchup, spread in zip(this_weeks_matchups, this_weeks_spreads):
            this_week_spread_mask = self.get_this_week_mask(matchup['Away Team'], matchup['Home Team'])
            self.pandas_df.loc[this_week_spread_mask, 'Spread'] = spread
    
    def get_total_games_played(self, games_completed_this_week):
        number_of_games_completed_this_week = len(games_completed_this_week)
        total_games_up_to_this_week = self.cfbd_api.get_total_games_up_to_this_week()
        total_games_not_played = total_games_up_to_this_week - number_of_games_completed_this_week
        total_games_played = total_games_up_to_this_week - total_games_not_played
        return total_games_played

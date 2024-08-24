"""
schedule.py
"""
from sheet import Sheet
import pandas as pd
from gspread_dataframe import set_with_dataframe
from gspread_formatting import CellFormat, Color, format_cell_ranges, TextFormat

class Schedule(Sheet):
    
    def __init__(self, auth, sheet_name, cfbd_api):
        super().__init__(auth, sheet_name)
        self.cfbd_api = cfbd_api
        self.worksheet = self.sheet.worksheet('Schedule')

        records = self.worksheet.get_all_records()
        self.pandas_df = pd.DataFrame(records)

    def update_schedule(self):
        print('Please wait while we update the scores...')
        for matchup in self.get_weeks_matchups(week=self.cfbd_api.week):
            away_team = matchup['Away Team']
            home_team = matchup['Home Team']
            game_score = self.cfbd_api.get_game_score(away_team, home_team)
            self.update_score(game_score, away_team, home_team, self.cfbd_api.week)
        self.save_schedule_sheet()
        self.highlight_winning_team()
        print('Schedule updated!')

    def get_score_mask(self, away_team, home_team, week):
        return (self.pandas_df['Away Team'] == away_team) & \
               (self.pandas_df['Home Team'] == home_team) & \
               (self.pandas_df['Week'] == week)
    
    def update_score(self, score, away_team, home_team, week):
        score_mask = self.get_score_mask(away_team, home_team, week)
        self.pandas_df.loc[score_mask, 'Home Points'] = score['home_points']
        self.pandas_df.loc[score_mask, 'Away Points'] = score['away_points']
    
    def get_weeks_matchups(self, week):
        weeks_matchups = self.pandas_df[self.pandas_df['Week'] == week]
        print(weeks_matchups)
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
    
    def save_schedule_sheet(self):
        set_with_dataframe(self.worksheet, self.pandas_df)
"""
schedule.py
"""
from score_sheet import ScoreSheet
import pandas as pd
from gspread_dataframe import set_with_dataframe
from gspread_formatting import CellFormat, Color, format_cell_ranges, TextFormat

class Schedule(ScoreSheet):
    
    def __init__(self, auth, sheet_name, worksheet, cfbd_api):
        super().__init__(auth, sheet_name, worksheet, cfbd_api)
        records = self.worksheet.get_all_records(head=4)
        self.pandas_df = pd.DataFrame(records)

    def update_schedule_scores(self):
        print('Please wait while we update the schedule...')
        for matchup in self.get_weeks_matchups():
            game_score = self.get_game_score(matchup)
            self.update_pd_score_frame(game_score, matchup)
        self.set_schedule_sheet_scores()
        self.highlight_winning_teams()
        print('Schedule scores updated!')
    
    def update_pd_score_frame(self, game_score, matchup):
        score_mask = self.get_score_mask(matchup['Away Team'], matchup['Home Team'])
        self.pandas_df.loc[score_mask, 'Home Points'] = game_score['home_points']
        self.pandas_df.loc[score_mask, 'Away Points'] = game_score['away_points']
    
    def highlight_winning_teams(self):
        batch_update = []
        light_yellow_highlight = CellFormat(backgroundColor=Color(1.0, 1.0, 0.7), textFormat=TextFormat(bold=True))
        for i, (_, row) in enumerate(self.pandas_df.iterrows(), start=5):
            
            home_points = row['Home Points']
            away_points = row['Away Points']
            if home_points > away_points:
                batch_update.append((f'F{i}', light_yellow_highlight))
                batch_update.append((f'G{i}', light_yellow_highlight))
            elif home_points < away_points:
                batch_update.append((f'D{i}', light_yellow_highlight))
                batch_update.append((f'E{i}', light_yellow_highlight))
        
        format_cell_ranges(self.worksheet, batch_update)
    
    def set_schedule_sheet_scores(self):
        set_with_dataframe(self.worksheet, self.pandas_df, row=4, col=1)

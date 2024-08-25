"""
scoreboard.py
"""
import pandas as pd
from score_sheet import ScoreSheet
from gspread_formatting import CellFormat, Color, format_cell_ranges, TextFormat

class IndividualScoreSheet(ScoreSheet):

    def __init__(self, auth, sheet_name, worksheet, cfbd_api, total_score):
        super().__init__(auth, sheet_name, worksheet, cfbd_api)
        records = self.worksheet.get_all_records()
        self.pandas_df = pd.DataFrame(records)
        self.user_week_score = 0
        self.user_total_score = total_score
        self.batch_update = []

    def update_individual_scoreshet(self):
        print(f"Updating {self.worksheet.title}'s individual score...")
        for matchup in self.get_weeks_matchups():
            game_score = self.get_game_score(matchup)
            self.calc_user_week_score(game_score, matchup)
        self.do_batch_update()
        print(f"Finished updating {self.worksheet.title}'s individual score...")
  
    def calc_user_week_score(self, game_score, matchup):
        score_mask = self.get_score_mask(matchup['Away Team'], matchup['Home Team'])
        row = self.pandas_df.loc[score_mask]

        home_points = game_score['home_points']
        away_points = game_score['away_points']

        is_home_win = home_points > away_points
        is_away_win = home_points < away_points

        picked_home = row['Pick Home'].iloc[0] == 1
        picked_away = row['Pick Away'].iloc[0] == 1

        if (picked_home and picked_away) or (not picked_home and not picked_away):
            highlight_type = None

        elif is_home_win:
            if picked_home:
                self.user_week_score += 1
                highlight_type = 'Home_Win'
            else:
                highlight_type = 'Home_Loss'

        elif is_away_win:
            if picked_away:
                self.user_week_score += 1
                highlight_type = 'Away_Win'
            else:
                highlight_type = 'Away_Loss'

        self.highlight_score(row, highlight_type)
    
    def highlight_score(self, row, type):
        light_green_highlight = CellFormat(backgroundColor=Color(0.8, 1.0, 0.8), textFormat=TextFormat(bold=True))
        ligt_red_hightlight = CellFormat(backgroundColor=Color(1.0, 0.8, 0.8), textFormat=TextFormat(bold=True))

        index = row.index[0] + 2
        
        if type == 'Home_Win':
            self.batch_update.append((f'F{index}', light_green_highlight))
            self.batch_update.append((f'G{index}', light_green_highlight))
        elif type == 'Home_Loss':
            self.batch_update.append((f'C{index}', ligt_red_hightlight))
            self.batch_update.append((f'D{index}', ligt_red_hightlight))
        elif type == 'Away_Win':
            self.batch_update.append((f'C{index}', light_green_highlight))
            self.batch_update.append((f'D{index}', light_green_highlight))
        elif type == 'Away_Loss':
            self.batch_update.append((f'F{index}', ligt_red_hightlight))
            self.batch_update.append((f'G{index}', ligt_red_hightlight))
        elif not type:
            self.batch_update.append((f'C{index}', ligt_red_hightlight))
            self.batch_update.append((f'D{index}', ligt_red_hightlight))
            self.batch_update.append((f'F{index}', ligt_red_hightlight))
            self.batch_update.append((f'G{index}', ligt_red_hightlight))
    
    def do_batch_update(self):
        format_cell_ranges(self.worksheet, self.batch_update)

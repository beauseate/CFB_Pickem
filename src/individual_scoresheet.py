"""
individual_scoresheet.py
"""
import pandas as pd
from score_sheet import ScoreSheet
from gspread_dataframe import set_with_dataframe
from gspread_formatting import CellFormat, Color, format_cell_ranges, TextFormat


class IndividualScoreSheet(ScoreSheet):

    def __init__(self, auth, sheet_name, cfbd_api, worksheet):
        super().__init__(auth, sheet_name, cfbd_api)
        self.worksheet = self.spreadsheet.worksheet(worksheet)
        records = self.worksheet.get_all_records()
        self.pandas_df = pd.DataFrame(records)
        self.week_score = 0
        self.batch_update = []
    
    def get_weeks_score(self):
        return {f'Week {self.cfbd_api.week} Points': self.week_score}

    def update_individual_scoresheet(self, matchups, game_scores):
        print(f"Updating {self.worksheet.title}'s individual score...")
        self.calc_week_score(matchups, game_scores)

        self.save_individual_scoresheet()
        self.do_batch_update()
        print(f"Finished updating {self.worksheet.title}'s individual score!")
  
    def calc_week_score(self, matchups, game_scores):
        for matchup, game_score in zip(matchups, game_scores):
            if not game_score:
                continue
            score_mask = self.get_this_week_mask(matchup['Away Team'], matchup['Home Team'])
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
                    self.week_score += 1
                    highlight_type = 'Home_Win'
                else:
                    highlight_type = 'Home_Loss'

            elif is_away_win:
                if picked_away:
                    self.week_score += 1
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
    
    def save_individual_scoresheet(self):
        print(f"Saving {self.worksheet.title}'s worksheet...")
        set_with_dataframe(self.worksheet, self.pandas_df)

    def do_batch_update(self):
        format_cell_ranges(self.worksheet, self.batch_update)

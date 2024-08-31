"""
scoreboard.py
"""
from score_sheet import ScoreSheet
import pandas as pd
from gspread_dataframe import set_with_dataframe


class Scoreboard(ScoreSheet):

    def __init__(self, auth, sheet_name, cfbd_api, worksheet='Scoreboard'):
        super().__init__(auth, sheet_name, cfbd_api)
        self.worksheet = self.spreadsheet.worksheet(worksheet)
        values = self.worksheet.get_all_values()
        self.pandas_df = pd.DataFrame(values)

    def update_scoreboard(self, scores_dict, total_games_up_to_this_week):
        week = self.cfbd_api.week

        last_weeks_score = self.get_week_score_df(week - 1)
        this_weeks_score = self.get_week_score_df(week)
        this_weeks_score = self.add_week_score_to_scoreboard(this_weeks_score, scores_dict)
        if last_weeks_score.empty:
            this_weeks_score['Total Points'] = this_weeks_score[f'Week {week} Points']
        else:
            this_weeks_score = self.add_total_score_to_scoreboard(this_weeks_score, last_weeks_score)
        this_weeks_score = self.add_accuracy_score_to_scoreboard(this_weeks_score, total_games_up_to_this_week)
        self.set_score_sheet_scores(this_weeks_score)

    def add_week_score_to_scoreboard(self, weeks_score, scores_dict):
        for player, scores in scores_dict.items():
            if player in weeks_score['Players'].values:
                for week, score in scores.items():
                    weeks_score.loc[weeks_score['Players'] == player, week] = score
        return weeks_score

    def add_total_score_to_scoreboard(self, this_weeks_score, last_weeks_score):
        for index, row in this_weeks_score.iterrows():
            player = row['Players']

            if player in last_weeks_score['Players'].values:
                last_week_points = int(last_weeks_score.loc[last_weeks_score['Players'] == player, 'Total Points'].values[0])
                this_weeks_points = int(this_weeks_score.loc[this_weeks_score['Players'] == player, f'Week {self.cfbd_api.week} Points'].values[0])
                this_weeks_score.at[index, 'Total Points'] = this_weeks_points + last_week_points

        return this_weeks_score

    def add_accuracy_score_to_scoreboard(self, weeks_score, total_games_up_to_this_week):
        print(total_games_up_to_this_week)
        for index, row in weeks_score.iterrows():
            total_points = int(row[f'Total Points'])
            accuracy = '{:.2%}'.format(total_points / total_games_up_to_this_week)
            weeks_score.at[index, 'Total Accuracy'] = accuracy
        return weeks_score

    def set_score_sheet_scores(self, weeks_score):
        first_scoreboard_col = self.cfbd_api.week - 1
        cols = (first_scoreboard_col*4) + 2
        weeks_score = weeks_score.drop(weeks_score.columns[0], axis=1)
        set_with_dataframe(self.worksheet, weeks_score, row=5, col=cols)

    def get_week_score_df(self, week):
        week_row = 2
        weeks = self.pandas_df.iloc[week_row]
        players = self.pandas_df.iloc[4:, 0].reset_index(drop=True)
        week_score_df = pd.DataFrame()
        for i, col in enumerate(self.pandas_df.columns):
            if f'Week {week}' == str(weeks[col]):
                print(f"Processing Week: {weeks[col]}")
                week_data_columns = self.pandas_df.iloc[4:, i-1:i+3].reset_index(drop=True)
                rows_to_add = len(players) - len(week_data_columns)
                padding = pd.DataFrame(index=range(rows_to_add), columns=week_data_columns.columns)
                week_data_columns = pd.concat([week_data_columns, padding], ignore_index=True)

                week_score_df = pd.concat([players, week_data_columns], axis=1)
                week_score_df.columns = week_score_df.iloc[0]
                week_score_df = week_score_df.drop(week_score_df.index[0])
                week_score_df = week_score_df.reset_index(drop=True)
        
        return week_score_df

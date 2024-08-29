"""
cfb_pickem.py
"""
from schedule import Schedule
from individual_scoresheet import IndividualScoreSheet
from scoreboard import Scoreboard


class CFBPickem():
    def __init__(self, auth, sheet_name, cfbd_api):
        self._auth = auth
        self._sheet_name = sheet_name
        self._cfbd_api = cfbd_api

    @property
    def auth(self):
        return self._auth
    
    @property
    def sheet_name(self):
        return self._sheet_name
    
    @property
    def cfbd_api(self):
        return self._cfbd_api
    
    def get_schedule(self):
        return Schedule(auth=self.auth, sheet_name=self.sheet_name, cfbd_api=self.cfbd_api)
    
    def get_individual_scoresheet(self, worksheet_title):
        return IndividualScoreSheet(auth=self.auth,
                                    sheet_name=self.sheet_name,
                                    worksheet=worksheet_title,
                                    cfbd_api=self.cfbd_api)
    
    def get_scoreboard(self):
        return Scoreboard(auth=self.auth, sheet_name=self.sheet_name, cfbd_api=self.cfbd_api)
    
    def update_individual_scoresheets(self, worksheets, matchups, game_scores,
                                      next_weeks_matchups=None, next_weeks_spread=None):
        scores_dict = {}
        for worksheet in worksheets:
            if worksheet.title in ['Schedule', 'Scoreboard']:
                continue

            individual_score_sheet = self.get_individual_scoresheet(worksheet.title)
            individual_score_sheet.update_individual_scoresheet(matchups, game_scores)
            if next_weeks_matchups:
                individual_score_sheet.update_next_weeks_spread(next_weeks_matchups, next_weeks_spread)
            weeks_individual_score = individual_score_sheet.get_weeks_score()
            scores_dict[worksheet.title] = weeks_individual_score

        return scores_dict

    def update_weeks_scores(self):
        schedule = self.get_schedule()

        this_weeks_matchups = schedule.get_this_weeks_matchups()
        this_weeks_game_scores = schedule.get_game_scores(this_weeks_matchups)
        if next_weeks_matchups := schedule.get_next_weeks_matchups():
            next_weeks_spread = schedule.get_next_week_game_spread(next_weeks_matchups)
            schedule.update_next_weeks_spread(next_weeks_matchups, next_weeks_spread)
        else:
            next_weeks_spread = None
        schedule.update_schedule(this_weeks_matchups, this_weeks_game_scores)

        worksheets = schedule.spreadsheet.worksheets()
        scores_dict = self.update_individual_scoresheets(worksheets, this_weeks_matchups, this_weeks_game_scores,
                                                         next_weeks_matchups, next_weeks_spread)

        scoreboard = self.get_scoreboard()
        scoreboard.update_scoreboard(scores_dict)
        
        print("Updated weeks scores successfully!")

    def update_this_weeks_spread():
        raise NotImplementedError

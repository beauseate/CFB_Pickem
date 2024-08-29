"""
cfbs_api.py
"""
import cfbd
import logging
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s"
)



class CFBD_API():
    def __init__(self, year, week):
        self.log = logging.getLogger(__name__)
        configuration = cfbd.Configuration()
        key = open('apikey.txt')
        configuration.api_key['Authorization'] = key.read()
        configuration.api_key_prefix['Authorization'] = 'Bearer'
        
        self.games_api = cfbd.GamesApi(cfbd.ApiClient(configuration))
        self.betting_api = cfbd.BettingApi(cfbd.ApiClient(configuration))
        self.year = year
        self.week = week
    
    def get_number_of_games_up_to_week(self):
        total_games = 0
        for i in range(1, self.week+1):
            total_games += len(self.games_api.get_games(year=self.year, week=i, division='fbs'))

        return total_games

    def get_game_data(self, away_team, home_team):
        """
        Gets game data of Away @ Home team
        """
        return self.games_api.get_games(year=self.year,
                                        week=self.week,
                                        division='fbs',
                                        away=away_team,
                                        home=home_team)
    
    def get_game_score(self, away_team, home_team):
        game_data = self.get_game_data(away_team, home_team)
        return [{'home_points': attr.home_points, 'away_points': attr.away_points} for attr in game_data][0]
    
    def get_game_spread(self, week, away_team, home_team):
        lines = self.betting_api.get_lines(year=self.year, week=week, away=away_team, home=home_team)[0].lines
        if lines:
            return lines[0].formatted_spread
        return 'N/A'

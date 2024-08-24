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
        self.year = year
        self.week = week

    def get_cur_week_fbs_games(self, away_team='', home_team=''):
         return self.games_api.get_games(year=self.year,
                                         week=self.week,
                                         away=away_team,
                                         home=home_team
                                        )
    
    def get_game_data(self, away_team, home_team):
        """
        Gets gam data of Away @ Home team
        """
        return self.get_cur_week_fbs_games(away_team, home_team)
    
    def get_game_score(self, away_team, home_team):
        game_data = self.get_game_data(away_team, home_team)
        return [{'home_points': attr.home_points, 'away_points': attr.away_points} for attr in game_data][0]

    
    
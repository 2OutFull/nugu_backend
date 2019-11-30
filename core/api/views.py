import statsapi
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
id = {
        "Los Angeles Angels": 108,
        "Arizona Diamondbacks": 109,
        "Baltimore Orioles": 110,
        "Boston Red Sox": 111,
        "Chicago Cubs": 112,
        "Cincinnati Reds": 113,
        "Cleveland Indians": 114,
        "Colorado Rockies": 115,
        "Detroit Tigers": 116,
        "Houston Astros": 117,
        "Kansas City Royals": 118,
        "Los Angeles Dodgers": 119,
        "Washington Nationals": 120,
        "New York Mets": 121,
        "Oakland Athletics": 133,
        "Pittsburgh Pirates": 134,
        "San Diego Padres": 135,
        "Seattle Mariners": 136,
        "San Francisco Giants": 137,
        "St. Louis Cardinals": 138,
        "Tampa Bay Rays": 139,
        "Texas Rangers": 140,
        "Toronto Blue Jays": 141,
        "Minnesota Twins": 142,
        "Philadelphia Phillies": 143,
        "Atlanta Braves": 144,
        "Chicago White Sox": 145,
        "Miami Marlins": 146,
        "New York Yankees": 147,
        "Milwaukee Brewers": 158,
        "Shin-Soo Choo": 140,
        "Hyun-Jin Ryu": 110,
        "Jung Ho": 134,
        "Seunghwan": 115,
        "Ji-Man": 139,
}


class PlayerStats(APIView):
    permission_classes = [AllowAny]

    player_id = {
        "Shin-Soo Choo": 425783,
        "Hyun-Jin Ryu": 547943,
        "Jung Ho": 628356,
        "Seunghwan": 493200,
        "Ji-Man": 596847,
    }
    default_group = {
        "Shin-Soo Choo": "hitting",
        "Hyun-Jin Ryu": "pitching",
        "Jung Ho": "fielding",
        "Seunghwan": "pitching",
        "Ji-Man": "fielding",
    }

    def get(self, request, name):
        player = statsapi.player_stat_data(
            self.player_id[name], self.default_group[name], "season"
        )
        player = player["stats"][0]["stats"]
        return Response(player)

class Assigned_Scheduler(APIView):
    permission_classes = [AllowAny]

    def get(self, request, name, start_date, end_date):
        team_schedule = statsapi.schedule(
            start_date=start_date, end_date=end_date, team=id[name]
        )
        date_and_team = [[0] * 2 for i in range(len(team_schedule) - 1)]
        for schedule in range(0, len(team_schedule) - 1):
            date_and_team[schedule][0] = team_schedule[schedule]["game_date"]
            date_and_team[schedule][1] = team_schedule[schedule]["away_name"]
        return Response(date_and_team)

class Next_Game(APIView):
    permission_class = [AllowAny]

    def get(self, request, name):
        time = datetime.now()
        date_and_team = []
        default_start_date = time.strftime("%Y-%m-%d")
        default_end_date = (time + timedelta(days=365)).strftime("%Y-%m-%d")
        team_schedule = statsapi.schedule(
            start_date=default_start_date, end_date=default_end_date, team=id[name]
        )
        date_and_team.append(team_schedule[0]['game_date'])
        date_and_team.append(team_schedule[0]['away_name'])
        return Response(date_and_team)

class Scheduler(APIView):
    permission_classes = [AllowAny]

    def get(self, request, name):
        time = datetime.now()
        default_start_date = time.strftime("%Y-%m-%d")
        default_end_date = (time + timedelta(days=90)).strftime("%Y-%m-%d")
        team_schedule = statsapi.schedule(
            start_date=default_start_date, end_date=default_end_date, team=id[name]
        )
        date_and_team = [[0]*2 for i in range(len(team_schedule)-1)]
        for schedule in range(0, len(team_schedule) - 1):
            date_and_team[schedule][0] = team_schedule[schedule]["game_date"]
            date_and_team[schedule][1] = team_schedule[schedule]["away_name"]
        return Response(date_and_team)
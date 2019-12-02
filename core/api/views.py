import statsapi
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class PitcherStats(APIView):
    permission_classes = [AllowAny]

    player_id = {
        "Hyun-Jin Ryu": 547943,
        "Seunghwan": 493200,
    }
    default_group = {
        "Hyun-Jin Ryu": "pitching",
        "Seunghwan": "pitching",
    }

    def post(self, request):
        print("pitcher stat called!!**")
        print(request.data)
        name = request.data["pitcher"]
        stat = request.data["pitcher_stat"]
        player_stat = statsapi.player_stat_data(
            self.player_id[name], self.default_group[name], "season"
        )["stats"][0]["stats"][stat]
        return Response(player_stat)


class HitterStats(APIView):
    permission_classes = [AllowAny]

    player_id = {
        "Shin-Soo Choo": 425783,
        "Jung Ho": 628356,
        "Ji-Man": 596847,
    }
    default_group = {
        "Shin-Soo Choo": "hitting",
        "Jung Ho": "fielding",
        "Ji-Man": "fielding",
    }

    def post(self, request):
        name = request.data["hitter"]
        stat = request.data["hitter_stat"]
        player_stat = statsapi.player_stat_data(
            self.player_id[name], self.default_group[name], "season"
        )["stats"][0]["stats"][stat]
        return Response(player_stat)


class Scheduler(APIView):
    permission_classes = [AllowAny]
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

    def get(self, request, name, start_date, end_date):
        # 팀이름 받고 기간을 정해주면 그안에 있는거 다 뽑기
        team_schedule = statsapi.schedule(
            start_date=start_date, end_date=end_date, team=self.id[name]
        )
        dates = []
        for schedule in range(0, len(team_schedule) - 1):
            dates.append(team_schedule[schedule]["summary"])
        return Response(dates)

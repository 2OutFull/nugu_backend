import json

import statsapi
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class PitcherStats(APIView):
    permission_classes = [AllowAny]

    player_id = {
        "류현진": 547943,
        "오승환": 493200,
    }
    default_group = {
        "류현진": "pitching",
        "오승환": "pitching",
    }

    def post(self, request):
        data = request.data["action"]
        print(data)

        if data["actionName"] != "pitcher-stat":
            return Response({"message": "invalid request"})

        with open("configure_package/available_pitcher_stats.json") as pitcher_json:
            available_pitcher_stats = json.load(pitcher_json)
        request_stat = data["parameters"]["pitcher_stat"]["value"]
        pitcher = data["parameters"]["pitcher"]["value"]
        pitcher_stat = available_pitcher_stats[request_stat]

        return_pitcher_stat = statsapi.player_stat_data(
            self.player_id[pitcher], self.default_group[pitcher], "season"
        )["stats"][0]["stats"][pitcher_stat]

        response_builder = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "pitcher": pitcher,
                "pitcher_stat": request_stat,
                "return_pitcher_stat": return_pitcher_stat,
            },
        }
        return Response(response_builder)


class HitterStats(APIView):
    permission_classes = [AllowAny]

    player_id = {
        "추신수": 425783,
        "강정호": 628356,
        "최지만": 596847,
    }
    default_group = {
        "추신수": "hitting",
        "강정호": "fielding",
        "최지만": "fielding",
    }

    def post(self, request):
        data = request.data["action"]
        print(data)

        if data["actionName"] != "hitter-stat":
            return Response({"message": "invalid request"})

        with open("configure_package/available_hitter_stats.json") as hitter_json:
            available_hitter_stats = json.load(hitter_json)
        request_stat = data["parameters"]["hitter_stat"]["value"]
        hitter = data["parameters"]["hitter"]["value"]
        hitter_stat = available_hitter_stats[request_stat]

        return_hitter_stat = statsapi.player_stat_data(
            self.player_id[hitter], self.default_group[hitter], "season"
        )["stats"][0]["stats"][hitter_stat]

        response_builder = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "hitter": hitter,
                "hitter_stat": request_stat,
                "return_hitter_stat": return_hitter_stat,
            },
        }
        return Response(response_builder)


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

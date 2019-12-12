import json

import statsapi
from datetime import datetime, timedelta
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

class NextGame(APIView):
    permission_class = [AllowAny]

    def post(self, request):
        data = request.data["action"]
        if data["actionName"] != "nextgame":
            return Response({"message": "invalid request"})
        with open("configure_package/available_schedule.json") as schedule:
            available_schedule = json.load(schedule)
        request_team_id = data["parameters"]["teams"]["value"]
        team_id = available_schedule[request_team_id]
        time = datetime.now()
        date_and_team = []
        default_start_date = time.strftime("%Y-%m-%d")
        default_end_date = (time + timedelta(days=365)).strftime("%Y-%m-%d")
        team_schedule = statsapi.schedule(
            start_date=default_start_date, end_date=default_end_date, team=team_id
        )
        date_and_team.append(team_schedule[0]['game_date'])
        date_and_team.append(team_schedule[0]['away_name'])
        response_builder = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "our_team": request_team_id,
                "return_game_date": date_and_team[0],
                "return_away_name": date_and_team[1],
            },
        }
        return Response(response_builder)

class Scheduler(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data["action"]
        if data["actionName"] != "scheduler":
            return Response({"message": "invalid request"})
        with open("configure_package/available_schedule.json") as schedule:
            available_schedule = json.load(schedule)
        request_team_id = data["parameters"]["teams"]["value"]
        team_id = available_schedule[request_team_id]
        time = datetime.now()
        default_start_date = time.strftime("%Y-%m-%d")
        default_end_date = (time + timedelta(days=90)).strftime("%Y-%m-%d")
        team_schedule = statsapi.schedule(
            start_date=default_start_date, end_date=default_end_date, team=team_id
        )
        date_and_team = [[0]*2 for i in range(len(team_schedule)-1)]
        for schedule in range(0, 3):
            date_and_team[schedule][0] = team_schedule[schedule]["game_date"]
            date_and_team[schedule][1] = team_schedule[schedule]["away_name"]
        response_builder = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "our_team": request_team_id,
                "return_game_date1": date_and_team[0][0],
                "return_away_name1": date_and_team[0][1],
                "return_game_date2": date_and_team[1][0],
                "return_away_name2": date_and_team[1][1],
                "return_game_date3": date_and_team[2][0],
                "return_away_name3": date_and_team[2][1],
            },
        }
        return Response(response_builder)
import json
from datetime import datetime, timedelta

import requests
import statsapi
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class PlayerStats(APIView):
    permission_classes = [AllowAny]

    player_id = {
        "류현진": 547943,
        "오승환": 493200,
        "추신수": 425783,
        "강정호": 628356,
        "최지만": 596847,
    }
    default_group = {
        "류현진": "pitching",
        "오승환": "pitching",
        "추신수": "hitting",
        "강정호": "fielding",
        "최지만": "fielding",
    }

    def post(self, request):
        data = request.data["action"]

        last_url = request.get_full_path().split("/")[-1]
        if last_url == "pitcher-stat":
            position = "pitcher"
        else:
            position = "hitter"

        with open(f"configure_package/available_{position}_stats.json") as pitcher_json:
            available_pitcher_stats = json.load(pitcher_json)
        request_stat = data["parameters"][f"{position}_stat"]["value"]
        player = data["parameters"][position]["value"]

        player_stat = available_pitcher_stats[request_stat]

        return_stat = statsapi.player_stat_data(
            self.player_id[player], self.default_group[player], "season"
        )["stats"][0]["stats"][player_stat]
        if type(return_stat) is str:
            return_stat = float(return_stat)
        else:
            return_stat = str(return_stat) + "회"

        response_builder = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "pitcher": player,
                "pitcher_stat": request_stat,
                "return_pitcher_stat": return_stat,
            },
        }
        return Response(response_builder)


class NextGame(APIView):
    permission_class = [AllowAny]

    def post(self, request):
        data = request.data["action"]
        with open("configure_package/available_schedule.json") as schedule:
            available_schedule = json.load(schedule)
        request_team = data["parameters"]["team"]["value"]
        team_id = available_schedule[request_team]

        time = datetime.now()
        date_and_team = []
        default_start_date = time.strftime("%Y-%m-%d")
        default_end_date = (time + timedelta(days=365)).strftime("%Y-%m-%d")

        team_schedule = statsapi.schedule(
            start_date=default_start_date, end_date=default_end_date, team=team_id
        )
        date_and_team.append(team_schedule[0]["game_date"])
        date_and_team.append(team_schedule[0]["away_name"])
        response_builder = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "our_team": request_team,
                "return_game_date": date_and_team[0],
                "return_away_name": date_and_team[1],
            },
        }
        return Response(response_builder)


class Scheduler(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data["action"]
        request_team = data["parameters"]["team_name"]["value"]

        with open("configure_package/mlb_team_list.json") as mlb_team:
            mlb_team_list = json.load(mlb_team)
        if request_team in mlb_team_list:
            team_id = mlb_team_list[request_team]
            time = datetime.now()
            default_start_date = time.strftime("%Y-%m-%d")
            default_end_date = (time + timedelta(days=90)).strftime("%Y-%m-%d")
            team_schedule = statsapi.schedule(
                start_date=default_start_date, end_date=default_end_date, team=team_id
            )
            date_and_team = [[0] * 2 for i in range(len(team_schedule) - 1)]
            for schedule in range(0, 3):
                date_and_team[schedule][0] = team_schedule[schedule]["game_date"]
                date_and_team[schedule][1] = team_schedule[schedule]["away_name"]

            with open("configure_package/mlb_i18n_team_list.json") as mlb_i18n_team:
                away_team_list = json.load(mlb_i18n_team)

            response_builder = {
                "version": "2.0",
                "resultCode": "OK",
                "output": {
                    "our_team_name": request_team,
                    "return_game_date1": date_and_team[0][0],
                    "return_away_name1": away_team_list[date_and_team[0][1]],
                    "return_game_date2": date_and_team[1][0],
                    "return_away_name2": away_team_list[date_and_team[1][1]],
                    "return_game_date3": date_and_team[2][0],
                    "return_away_name3": away_team_list[date_and_team[2][1]],
                },
            }
        else:
            with open("configure_package/team_and_teamid.json") as other_team:
                other_team_list = json.load(other_team)
            team_id = other_team_list[request_team]

            other_team_schedule_url = (
                f"https://www.thesportsdb.com/api/v1/json/1/eventsnext.php?id={team_id}"
            )
            r = requests.get(other_team_schedule_url).text
            three_events = json.loads(r)["events"][2:5]

            response_builder = {
                "version": "2.0",
                "resultCode": "OK",
                "output": {
                    "our_team_name": request_team,
                    "return_game_date1": three_events[-1]["dateEvent"],
                    "return_away_name1": three_events[-1]["strAwayTeam"],
                    "return_game_date2": three_events[-2]["dateEvent"],
                    "return_away_name2": three_events[-2]["strAwayTeam"],
                    "return_game_date3": three_events[0]["dateEvent"],
                    "return_away_name3": three_events[0]["strAwayTeam"],
                },
            }

        return Response(response_builder)
class League_Schedule():
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data["action"]
        request_league = data["parameters"]["league_name"]["value"]
        with open("configure_package/available_league.json") as league_id:
            league_list = json.load(league_id)
        league_id = league_list(request_league)
        other_league_schedule_url = (
            f"https://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id={league_id}"
        )
        r = requests.get(other_league_schedule_url).text
        three_events = json.loads(r)["events"][2:5]
        response_builder = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "our_team_name": request_league,
                "return_game_date1": three_events[-1]["dateEvent"],
                "return_home_name1": three_events[-1]["strHomeTeam"],
                "return_away_name1": three_events[-1]["strAwayTeam"],
                "return_game_date2": three_events[-2]["dateEvent"],
                "return_home_name2": three_events[-2]["strHomeTeam"],
                "return_away_name2": three_events[-2]["strAwayTeam"],
            },
        }
        return Response(response_builder)


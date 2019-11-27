import datetime

import statsapi
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


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
            self.player_id[name], self.default_group[name], "career"
        )
        player = player["stats"][0]["stats"]
        return Response(player)


class Scheduler(APIView):
    permission_classes = [AllowAny]
    team_id = {
        "Texas Rangers": 140,
    }

    def get(self, request, name, period):
        # 팀이름 받고 기간을 정해주면 그안에 있는거 다 뽑기
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        team_schedule = statsapi.schedule(
            start_date=today_date, end_date=period, team=self.team_id[name]
        )
        dates = []
        for schedule in range(0, len(team_schedule) - 1):
            dates.append(team_schedule[schedule]["summary"])
        return Response(dates)

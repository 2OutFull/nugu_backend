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

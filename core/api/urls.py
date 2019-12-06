from django.urls import path

from core.api.views import PlayerStats, Scheduler, Assigned_Scheduler, Next_Game

urlpatterns = [
    path("player-stats/<str:name>/", PlayerStats.as_view()),
    path("scheduler", Scheduler.as_view()),
    path("assigned-scheduler", Assigned_Scheduler.as_view()),
    path("nextgame", Next_Game.as_view()),
]

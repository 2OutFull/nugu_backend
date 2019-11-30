from django.urls import path

from core.api.views import PlayerStats, Scheduler, Assigned_Scheduler, Next_Game

urlpatterns = [
    path("player-stats/<str:name>/", PlayerStats.as_view()),
    path("scheduler/<str:name>", Scheduler.as_view()),
    path("assigned-scheduler/<str:name>&<str:start_date>&<str:end_date>", Assigned_Scheduler.as_view()),
    path("nextgame/<str:name>", Next_Game.as_view()),
]

from django.urls import path

from core.api.views import PlayerStats, Scheduler, NextGame, LeagueSchedule

urlpatterns = [
    path("pitcher-stat", PlayerStats.as_view()),
    path("hitter-stat", PlayerStats.as_view()),
    path("schedule", Scheduler.as_view()),
    path("nextgame", NextGame.as_view()),
    path("league-schedule", LeagueSchedule.as_view()),
]

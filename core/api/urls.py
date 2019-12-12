from django.urls import path

from core.api.views import PitcherStats, HitterStats, Scheduler, NextGame,

urlpatterns = [
    path("pitcher-stat", PitcherStats.as_view()),
    path("hitter-stat", HitterStats.as_view()),
    path("scheduler", Scheduler.as_view()),
    path("nextgame", NextGame.as_view())
]

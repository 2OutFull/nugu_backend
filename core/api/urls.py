from django.urls import path

from core.api.views import PlayerStats, Scheduler, NextGame

urlpatterns = [
    path("pitcher-stat", PlayerStats.as_view()),
    path("hitter-stat", PlayerStats.as_view()),
    path("scheduler", Scheduler.as_view()),
    path("nextgame", NextGame.as_view())
]

from django.urls import path

from core.api.views import PitcherStats, HitterStats, Scheduler, Next_Game, Assigned_Scheduler

urlpatterns = [
    path("pitcher-stat", PitcherStats.as_view()),
    path("hitter-stat", HitterStats.as_view()),
    path("scheduler", Scheduler.as_view()),
    path("assigned-scheduler", Assigned_Scheduler.as_view()),
    path("nextgame", Next_Game.as_view())
]

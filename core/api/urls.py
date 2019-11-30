from django.urls import path

from core.api.views import PlayerStats, Scheduler

urlpatterns = [
    path("player-stats/<str:name>/", PlayerStats.as_view()),
    path("scheduler/<str:name>&<str:period>&<str:period2>/", Scheduler.as_view()),
]

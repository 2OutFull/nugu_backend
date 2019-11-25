from django.urls import path

from core.api.views import PlayerStats,scheduler
urlpatterns = [path("player-stats/<str:name>/", PlayerStats.as_view())]
urlpatterns = [path("scheduler/<str:name>&<str:period>/", scheduler.as_view())]
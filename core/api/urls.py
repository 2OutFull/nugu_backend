from django.urls import path

from core.api.views import PlayerStats

urlpatterns = [path("player-stats/<str:name>/", PlayerStats.as_view())]

from django.shortcuts import render
from .services import get_driver_standings
from django.utils import timezone

# Create your views here.
def index(request, season=None):
    standings = get_driver_standings()

    date_time_utc = timezone.now()
    if season is None:
        season = date_time_utc.year

    return render(request, "standings/index.html",{
        "standings":standings,
        "race":standings[0].race,
        "selected_season":season
    })

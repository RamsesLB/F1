from django.shortcuts import render
from .services import get_driver_standings, get_constructor_standings
from django.utils import timezone

# Create your views here.
def index(request, season=None):
    standings = get_driver_standings()
    constructor_standings = get_constructor_standings()

    date_time_utc = timezone.now()
    if season is None:
        season = date_time_utc.year

    user_timezone = request.COOKIES.get('user_timezone')

    return render(request, "standings/index.html",{
        "standings":standings,
        "constructor_standings":constructor_standings,
        "race":standings[0].race,
        "selected_season":season,
        "user_timezone":user_timezone
    })

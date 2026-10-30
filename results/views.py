from django.shortcuts import render
from .services import get_results
from .models import Result
from schedule.models import Race
from django.utils import timezone

# Create your views here.
def index(request, season=None):

    date_time_utc = timezone.now()
    if season is None:
        season = date_time_utc.year

    races = Race.objects.filter(
        season=season, 
        race_dateTime__lt=date_time_utc
    ).prefetch_related('results', 'results__driver').order_by("-race_dateTime")

    # Load to cache
    for race in races:
        dummy = get_results(race.season, race.round)

    user_timezone = request.COOKIES.get('user_timezone')

    return render(request, 'results/index.html',{
        "races":races,
        "selected_season":season,
        "user_timezone":user_timezone
    })


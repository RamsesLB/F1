from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from.services import get_f1_schedule, get_next_race
from results.services import get_results
import json

from .models import Circuit
from django.utils import timezone

# Create your views here.
def index(request, season=None):
    races = get_f1_schedule(season) 
    next_race = get_next_race()
    curr_year = timezone.now().year
    if season is not None:
        selected_season = season
    else:
        selected_season = curr_year
    season_list = [curr_year + 1, curr_year, curr_year - 1]

    # Reducir el largo de los nombres
    for race in races:
         race.name = race.name.replace("Grand Prix", "GP")
    
    # Get cookie
    user_timezone = request.COOKIES.get('user_timezone')

    return render(request, "schedule/index.html",{
        "races" :races,
        "next_race":next_race,
        "curr_year":curr_year,
        "selected_season":selected_season, 
        "season_list":season_list,
        "user_timezone":user_timezone
    })

def circuit(request, circuit_id):
    circuit = get_object_or_404(Circuit, id=circuit_id)
    season = request.GET.get("season", timezone.now().year)
    race = circuit.races.filter(season=season).first()
    results = None
    if race: results = get_results(race.season,race.round)

    return render(request, "schedule/circuit.html",{
        "circuit":circuit,
        "race":race,
        "results":results,
        "selected_season":race.season
    })

def manage_timezone_cookie(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get("action")
        time_zone = data.get("timezone")

        response = JsonResponse({"status":"success"})

        if action=="save" and time_zone:
            response.set_cookie("user_timezone", time_zone, max_age=31536000) # 1 year
        elif action=="delete":
            response.delete_cookie("user_timezone")

        print(response, "dentro de post",action,time_zone)
        return response

    return JsonResponse({"status":"error"})

def health_check(request):
    return JsonResponse({"status": "ok", "app": "F1 Schedule Awake"})
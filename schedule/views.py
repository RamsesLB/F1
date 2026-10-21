from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from.services import get_f1_schedule, get_next_race

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
    
    return render(request, "schedule/index.html",{
        "races" :races,
        "next_race":next_race,
        "curr_year":curr_year,
        "selected_season":selected_season, 
        "season_list":season_list
    })

def circuit(request, circuit_id):
    circuit = Circuit.objects.get(id=circuit_id)
    return render(request, "schedule/circuit.html",{
        "circuit":circuit
    })
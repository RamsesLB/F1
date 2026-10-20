from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from.services import get_f1_schedule, get_next_race

from .models import Circuit
from django.utils import timezone

# Create your views here.
def index(request):
    races = get_f1_schedule() 
    next_race = get_next_race()
    curr_year = timezone.now().year
    season_list = [curr_year + 1, curr_year, curr_year - 1]
    
    return render(request, "schedule/index.html",{
        "races" :races,
        "next_race":next_race,
        "curr_year":curr_year,
        "season_list":season_list
    })

def circuit(request, circuit_id):
    circuit = Circuit.objects.get(id=circuit_id)
    return render(request, "schedule/circuit.html",{
        "circuit":circuit
    })
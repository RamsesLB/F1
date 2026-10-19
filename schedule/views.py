from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from.services import get_f1_schedule, get_next_race

from .models import Circuit

# Create your views here.
def index(request):
    races = get_f1_schedule() 
    next_race = get_next_race()
    return render(request, "schedule/index.html",{
        "races" :races,
        "next_race":next_race
    })

def circuit(request, circuit_id):
    circuit = Circuit.objects.get(id=circuit_id)
    return render(request, "schedule/circuit.html",{
        "circuit":circuit
    })
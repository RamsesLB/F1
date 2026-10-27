from django.shortcuts import render
from .services import get_results

# Create your views here.
def index(request, season=None, round=None):
    results = get_results(season, round)
    if len(results)>0:
        race = results[0].race
    else: race = None

    print(results)
    return render(request, 'results/index.html',{
        "results":results,
        "race":race
    })
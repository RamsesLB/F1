from django.shortcuts import render
from .services import get_driver_standings

# Create your views here.
def index(request):
    standings = get_driver_standings()
  
    return render(request, "standings/index.html",{
        "standings":standings,
        "race":standings[0].race
    })

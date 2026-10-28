from django.urls import path
from . import views

urlpatterns = [
    path('<int:season>/', views.index, name="results_index")
    #path('<int:season>/<int:round>/', views.results, name = "results_season_round")
]
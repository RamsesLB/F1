from django.urls import path
from . import views

# app_name is needed for referencing names in htmls: 
# e.g.: <a href="{% url 'tasks:add' %}">Add a new task</a>
#app_name = "schedule"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:season>", views.index, name="season_index"),
    path("<str:circuit_id>/", views.circuit, name="circuit")
]
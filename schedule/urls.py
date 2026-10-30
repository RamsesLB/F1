from django.urls import path
from . import views

#app_name = "schedule"

urlpatterns = [
    path("", views.index, name="index"),
    path("health/", views.health_check, name="health_check"), # Endpoint que devuelve Json
    path("<int:season>", views.index, name="season_index"),
    path("circuit/<str:circuit_id>/", views.circuit, name="circuit"),
    path('set-timezone/', views.manage_timezone_cookie, name='manage_timezone')
]
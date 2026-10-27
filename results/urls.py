from django.urls import path
from . import views

urlpatterns = [
    path('<int:season>/<int:round>/', views.index, name = "results_index")
]
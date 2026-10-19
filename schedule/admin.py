from django.contrib import admin
from .models import Circuit, Race #

# Register your models here.
@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'city')
    search_fields = ('name',)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('season', 'round_number', 'name', 'circuit', 'race_dateTime')
    list_filter = ('season',)
    search_fields = ('name', 'circuit__name')
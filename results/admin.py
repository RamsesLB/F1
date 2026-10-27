from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Result

# Register your models here.
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('race', 'driver', 'position', 'points', 'grid','laps','status','time_string','time_millis',
                    'fastest_lap_rank', 'fastest_lap_number', 'fastest_lap_time')
    list_filter = ('race', 'driver')
    search_fields = ('race', 'driver')

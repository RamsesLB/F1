from django.contrib import admin
from .models import Driver, DriverStanding, Constructor

# Register your models here.
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'permanent_number', 'code', 'given_name', 'family_name', 'date_of_birth', 'nationality')
    list_filter = ('nationality',)
    search_fields = ('given_name',)

@admin.register(DriverStanding)
class DriverStandingAdmin(admin.ModelAdmin):
    list_display = ('race', 'driver', 'position', 'points', 'wins')
    list_filter = ('race',)
    search_fields = ('race', 'circuit__name')

@admin.register(Constructor)
class ConstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nationality')
    list_filter = ('nationality',)
    search_fields = ('name',)
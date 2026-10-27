from django.db import models
from schedule.models import Race
from standings.models import Driver

# Create your models here.
class Result(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="results")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="driver_results")

    position = models.IntegerField()
    points = models.FloatField()

    grid = models.IntegerField(null=True, blank=True)
    laps = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=150, null=True, blank=True)

    time_string = models.CharField(max_length=50, null=True, blank=True)
    time_millis = models.IntegerField(null=True, blank=True)

    fastest_lap_rank = models.IntegerField(null=True, blank=True)
    fastest_lap_number = models.IntegerField(null=True, blank=True)
    fastest_lap_time = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['race', 'driver'], name='unique_driver_race_result')
        ]
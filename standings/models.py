from django.db import models
from schedule.models import Race

# Create your models here.

class Driver(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    permanent_number = models.IntegerField(null=True, blank=True) 
    code = models.CharField(max_length=3, null=True, blank=True)
    given_name = models.CharField(max_length=150)
    family_name = models.CharField(max_length=150, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.given_name} {self.family_name}"

class Constructor(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    name = models.CharField(max_length=150)
    nationality = models.CharField(max_length=150, null=True, blank=True)

class DriverStanding(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="drivers_standings")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="standings")

    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE, related_name="constructor_standing", null=True, blank=True)
    position = models.IntegerField()
    points = models.FloatField()
    wins = models.IntegerField(null=True, blank=True)

    class Meta:
        # Un piloto solo tiene una entrada en una carrera
        constraints = [
            models.UniqueConstraint(fields=['race', 'driver'], name='unique_driver_race_standing')
        ]

    def __str__(self):
        return f"{self.driver.given_name} - {self.race.season} R{self.race.round} - P{self.position}"


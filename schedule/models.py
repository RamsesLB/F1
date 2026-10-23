from django.db import models
#from django_countries.fields import CountryField

# Create your models here.
class Circuit(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    name = models.CharField(max_length=150)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    # Map will save the circuit layout, sectors, corners
    map = models.ImageField(upload_to='circuits/', null=True, blank=True)

class Race(models.Model):
    season = models.CharField(max_length=150)
    round_number = models.IntegerField()
    name = models.CharField(max_length=150)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name="races")

    # Horarios (UTC)
    race_dateTime = models.DateTimeField()
    qualifying_dateTime = models.DateTimeField(null=True, blank=True)
    fp1_dateTime = models.DateTimeField(null=True, blank=True)
    fp2_dateTime = models.DateTimeField(null=True, blank=True)
    fp3_dateTime = models.DateTimeField(null=True, blank=True)

    SprintQualifying_dateTime = models.DateTimeField(null=True, blank=True)
    Sprint_dateTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Season {self.season}, Round {self.round_number}: {self.name}"
import requests
from django.core.cache import cache
from django.utils import timezone
from requests.exceptions import HTTPError, JSONDecodeError

from schedule.services import get_last_race
from schedule.models import Race
from standings.models import DriverStanding, Driver, Constructor
from .models import Result

def get_results(season, round):

    results = cache.get(f"results_{season}_R{round}")
    if results is not None:
        print("Results used from cache")
        return results

    #race = Race.objects.filter(season=season, round=round)
    #results = Result.objects.filter(race=race)

    race_obj = Race.objects.filter(season=season, round=round).first()
    if race_obj:
        results = Result.objects.filter(race=race_obj)
    else:
        results = Result.objects.none()

    if not results.exists():
        # Use the API
        if season is None:
            season = timezone.now().year
        if round is None:
            round = get_last_race().round

        try:
            response = requests.get(f"https://api.jolpi.ca/ergast/f1/{season}/{round}/results/?format=json")
            response.raise_for_status() # Arroja HTTPError, si ocurrió uno
            json_dict = response.json()
            results = json_dict["MRData"]["RaceTable"]["Races"][0]["Results"]
        except (HTTPError, JSONDecodeError, requests.RequestException, IndexError) as e:
            print(f"Race results may not exists yet. Error when reading API: {e}")
            return []
        
        for result in results:
            ##### Get or save driver data #####
            driver_obj, created = Driver.objects.get_or_create(
                id = result["Driver"]["driverId"],
                defaults={
                    "permanent_number" : result["Driver"]["permanentNumber"],
                    "code" : result["Driver"]["code"],
                    "given_name" : result["Driver"]["givenName"],
                    "family_name" : result["Driver"]["familyName"],
                    "date_of_birth" : result["Driver"]["dateOfBirth"],
                    "nationality" : result["Driver"]["nationality"]
                }
            )
            if created: print(f"Driver created: {driver_obj.id}: {driver_obj.given_name}")

            time_data = result.get("Time", {})
            fastest_lap = result.get("FastestLap", {})
            fastest_time_data = fastest_lap.get("Time", {})

            result_obj = Result.objects.get_or_create(
                race = race_obj,
                driver = driver_obj,

                position = result.get("position"),
                points = result.get("points"),
                grid = result.get("grid"),
                laps = result.get("laps"),
                status = result.get("status"),
            
                time_string = time_data.get("time"),
                time_millis = int(time_data["millis"]) if "millis" in time_data else None,
                fastest_lap_rank = int(fastest_lap["rank"]) if "rank" in fastest_lap else None,
                fastest_lap_number = int(fastest_lap["lap"]) if "lap" in fastest_lap else None,
                fastest_lap_time = fastest_time_data.get("time"),
            )

    results = Result.objects.filter(race=race_obj)

    if len(results)>0:
        # Guardar datos de BD o API en el caché
        # 86400 seg = 24 horas
        cache.set(f"results_{season}_R{round}", results, 86400)
        print("Cache set")
    else: 
        print("Nothing to save in BD, no standings found in API.")

    return results
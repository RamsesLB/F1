import requests
from django.core.cache import cache
from django.utils import timezone
from requests.exceptions import HTTPError, JSONDecodeError

from schedule.services import get_last_race
from schedule.models import Race
from .models import DriverStanding, Driver, Constructor, ConstructorStanding

def get_API_data(url, year=None):
    if year is None:
        year = timezone.now().year
    try:
        response = requests.get(url)
        response.raise_for_status() # Arroja HTTPError, si ocurrió uno
        json_dict = response.json()
        return json_dict
    
    except HTTPError as http_err:
        print(f"Error HTTP al consultar el año {year}: {http_err}")
        return [] 
    except JSONDecodeError:
        print(f"La API no devolvió un JSON válido para el año {year}.")
        return []
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")
        return []

def get_driver_standings(year=None):
    if year is None:
        year = timezone.now().year

    # Get last race and round
    date_time_utc = timezone.now()
    last_race = get_last_race(date_time_utc=date_time_utc)

    driver_standings = cache.get(f'driver_standings{year}_R{last_race.round}')
    if driver_standings is not None:
        print("Driver standings used from cache")
        return driver_standings

    # Get standings
    standings = DriverStanding.objects.filter(race = last_race)

    if not last_race:
        print(f"Could not get the last race of season {year}")
        return []
    
    if not standings.exists():
        json_dict = get_API_data(url=f"https://api.jolpi.ca/ergast/f1/{year}/driverstandings/?format=json",year=year)

        standing_list = json_dict["MRData"]["StandingsTable"]["StandingsLists"][0]
        season = standing_list["season"]
        API_round = standing_list["round"]
        driver_standings = standing_list["DriverStandings"]

        # If the new race just started, the API round will be different (-1) from the last_race round (current live race)
        # If this is the case we have to return the previous driver standing (the same API round, or bd)
        if API_round != last_race.round:
            # try cache, else bd
            cache_driver_standings = cache.get(f'driver_standings{year}_R{API_round}')
            if cache_driver_standings is not None:
                print(f"Driver standings used from cache, from previous race R{API_round}, not the last R{last_race.round}.")
                return cache_driver_standings 
            else:
                # Get from bd the previous race standings, not from the live race
                #last_race = Race.objects.filter(round=API_round).order_by('race_dateTime').last()
                last_race = get_last_race(round=API_round)
                

        for standing in driver_standings:

            ##### Get or save driver data #####
            driver, created = Driver.objects.get_or_create(
                id = standing["Driver"]["driverId"],
                defaults={
                    "permanent_number" : standing["Driver"]["permanentNumber"],
                    "code" : standing["Driver"]["code"],
                    "given_name" : standing["Driver"]["givenName"],
                    "family_name" : standing["Driver"]["familyName"],
                    "date_of_birth" : standing["Driver"]["dateOfBirth"],
                    "nationality" : standing["Driver"]["nationality"]
                }
            )
            if created: print(f"Driver created: {driver.id}: {driver.given_name}")

            ##### Get or save constructor data #####
            constructor, created = Constructor.objects.get_or_create(
                id = standing["Constructors"]["constructorId"],
                defaults={
                    "name":standing["Constructors"]["name"],
                    "nationality":standing["Constructors"]["nationality"]
                }
            )

            ##### Create DriverStanding #####
            driver_standing = DriverStanding.objects.get_or_create(
                race = last_race,
                driver = driver,
                constructor = constructor,
                defaults={
                    "position" : standing["position"],
                    "points" : standing["points"],
                    "wins" : standing["wins"],
                }
            )

    standings = DriverStanding.objects.filter(race = last_race)

    if len(standings)>0:
        # Guardar datos de BD o API en el caché
        # 86400 seg = 24 horas
        cache.set(f'driver_standings{year}_R{last_race.round}', standings, 86400)
        print("Cache set")
    else: 
        print("Nothing to save in BD, no standings found in API.")

    return standings


def get_constructor_standings(year=None):
    if year is None:
        year = timezone.now().year

    # Get last race and round
    date_time_utc = timezone.now()
    last_race = get_last_race(date_time_utc=date_time_utc)

    constructor_standings = cache.get(f'constructor_standings{year}_R{last_race.round}')
    if constructor_standings is not None:
        print("Constructor standings used from cache")
        return constructor_standings

    # Get standings from DB
    standings = ConstructorStanding.objects.filter(race = last_race)

    if not last_race:
        print(f"Could not get the last race of season {year}")
        return []
    
    if not standings.exists():
        json_dict = get_API_data(url=f"https://api.jolpi.ca/ergast/f1/{year}/constructorstandings/?format=json",year=year)

        standing_list = json_dict["MRData"]["StandingsTable"]["StandingsLists"][0]
        season = standing_list["season"]
        API_round = standing_list["round"]
        constructor_standings = standing_list["ConstructorStandings"]
        print(constructor_standings)
        # If the new race just started, the API round will be different (-1) from the last_race round (current live race)
        # If this is the case we have to return the previous driver standing (the same API round, or bd)
        if API_round != last_race.round:
            # try cache, else bd
            cache_constructor_standings = cache.get(f'constructor_standings{year}_R{API_round}')
            if cache_constructor_standings is not None:
                print(f"Constructor standings used from cache, from previous race R{API_round}, not the last R{last_race.round}.")
                return cache_constructor_standings 
            else:
                # Get from bd the previous race standings, not from the live race
                #last_race = Race.objects.filter(round=API_round).order_by('race_dateTime').last()
                last_race = get_last_race(round=API_round)
                

        for standing in constructor_standings:

            ##### Get or save the constructor data #####
            constructor, created = Constructor.objects.get_or_create(
                id = standing["Constructor"]["constructorId"],
                defaults={
                    "name" : standing["Constructor"]["name"],
                    "nationality" : standing["Constructor"]["nationality"]
                }
            )
            if created: print(f"Constructor created: {constructor.id}: {constructor.name}")

            ##### Create ConstructorStanding #####
            constructor_standing = ConstructorStanding.objects.get_or_create(
                race = last_race,
                constructor = constructor,
                defaults={
                    "position" : standing["position"],
                    "points" : standing["points"],
                    "wins" : standing["wins"],
                }
            )

    standings = ConstructorStanding.objects.filter(race = last_race)

    if len(standings)>0:
        # Guardar datos de BD o API en el caché
        # 86400 seg = 24 horas
        cache.set(f'constructor_standings{year}_R{last_race.round}', standings, 86400)
        print("Cache set")
    else: 
        print("Nothing to save in BD, no standings found in API.")

    return standings
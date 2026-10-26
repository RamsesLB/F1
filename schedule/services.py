# schedule/services.py
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from django.core.cache import cache
from django.utils import timezone

from .models import Race, Circuit
from django.db.models import Q
from cities_light.models import City, Country

from requests.exceptions import HTTPError, JSONDecodeError


def to_dateTime_UTC(item):
    if not item or not isinstance(item, dict):
        return None

    date_str = item.get('date')
    time_str = item.get('time', '00:00:00Z')

    # Concatenar "2026-03-01T15:00:00Z"
    date_time_str = f"{date_str}T{time_str}"
    
    # Str to datetime y UTC
    date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%SZ")
    date_time_utc = date_time_obj.replace(tzinfo=ZoneInfo("UTC"))

    return date_time_utc

def get_f1_schedule(year=None):
    # Argumento year es opcional, si no se indica obtiene el año actual
    if year is None:
        year = timezone.now().year
 
    # Obtener datos del caché. Pueden existir 3: f1_schedule{thisyear}, f1_schedule{thisyear-1} or f1_schedule{thisyear+1}
    schedule_data = cache.get(f'f1_schedule{year}')
    if schedule_data is not None:
        print("Data used from cache")
        return schedule_data

    # Si no está en caché, buscar en la BD las carreras del año indicado
    races = Race.objects.filter(season = year).order_by('round')

    if not races.exists():
        # Si tampoco está en BD, usar la API para poblar
        try:
            url = f"https://api.jolpi.ca/ergast/f1/{year}/races/?format=json"
            response = requests.get(url)
            response.raise_for_status() # Arroja HTTPError, si ocurrió uno
            json_dict = response.json()

        except HTTPError as http_err:
            print(f"Error HTTP al consultar el año {year}: {http_err}")
            return [] 
        except JSONDecodeError:
            print(f"La API no devolvió un JSON válido para el año {year}.")
            return []
        except requests.RequestException as e:
            print(f"Error de conexión: {e}")
            return []

        races_list = json_dict["MRData"]["RaceTable"]["Races"]

        for race_item in races_list:
            ##### API GET DATA #####
            race_season = race_item["season"]
            race_round = race_item["round"]
            race_name = race_item["raceName"]

            race_dateTime = to_dateTime_UTC(race_item) 
            qualy_dateTime = to_dateTime_UTC(race_item.get("Qualifying", None))
            fp1_dateTime = to_dateTime_UTC(race_item.get("FirstPractice", None))
            fp2_dateTime = to_dateTime_UTC(race_item.get("SecondPractice", None))
            fp3_dateTime = to_dateTime_UTC(race_item.get("ThirdPractice", None))
            sprint_dateTime = to_dateTime_UTC(race_item.get("Sprint", None))
            SprintQuali_dateTime = to_dateTime_UTC(race_item.get("SprintQualifying", None))

            circuit_data = race_item["Circuit"]
            circuit_id = circuit_data["circuitId"]
            circuit_name= circuit_data["circuitName"]
            circuit_locality= circuit_data["Location"]["locality"] 
            circuit_country= circuit_data["Location"]["country"]

            ###### COUNTRY ######
            # Mapper util cuando el nombre del país de la API no coincide con el nombre de la tabla Country cities_light
            API_COUNTRY_MAPPER = {
                'UK': 'United Kingdom',
            }
            # Mapper para localidades, no son ciudades por lo que no están en la tabla city de cities_light
            API_CITY_MAPPER = {
                'Monte Carlo': 'Monaco',
                'Silverstone': 'Northampton',
                'Marina Bay': 'Singapore',
            }

            # Normalizar el nombre si existe en el mapa, sino dejar el original
            search_name = API_COUNTRY_MAPPER.get(circuit_country, circuit_country)
            country = Country.objects.filter(
                Q(name__iexact=search_name) | Q(alternate_names__icontains=search_name)
            ).first()

            search_name = API_CITY_MAPPER.get(circuit_locality, circuit_locality)
            city = City.objects.filter(
                Q(name__iexact=search_name) | Q(alternate_names__icontains=search_name)
            ).first()

            #print(circuit_country, country, country.id, city, city.id)
            
            ##### CREATE DB OBJECTS #####
            ### CIRCUIT ###
            circuit, created = Circuit.objects.get_or_create(
                id = circuit_id,
                name = circuit_name,
                country = country,
                city = city
            )

            ### RACE ###
            race = Race.objects.create(
                season = race_season,
                round = race_round,
                name = race_name,
                circuit = circuit,
            
                # Horarios (UTC)
                race_dateTime = race_dateTime,
                qualifying_dateTime = qualy_dateTime,
                fp1_dateTime = fp1_dateTime,
                fp2_dateTime = fp2_dateTime,
                fp3_dateTime = fp3_dateTime,
            
                SprintQualifying_dateTime = SprintQuali_dateTime,
                Sprint_dateTime = sprint_dateTime
            )

        if len(races_list)>0: print("Races and circuits saved to DB")
        
    # Volver a obtener las carreras de BD
    #races = Race.objects.all().order_by('round_number')
    races = list(Race.objects.filter(season = year).order_by('round')) # para mejorar velocidad usamos list
    if len(races)>0:
        # Guardar datos de BD o API en el caché
        # 86400 seg = 24 horas
        cache.set(f'f1_schedule{year}', races, 86400)
        print("Cache set")
    else: 
        print("Nothing to save in BD, no races found in API.")
    
    return races

def get_next_race():
    date_time_utc = timezone.now()
    
    next_race = Race.objects.filter(race_dateTime__gt=date_time_utc).order_by('race_dateTime').first()
    return next_race

def get_last_race(date_time_utc=None, round=None):
    """
    date_time_utc has priority, if present it will be used, else, use round, else use timezone.now
    """
    if date_time_utc is not None:
        last_race = Race.objects.filter(race_dateTime__lt=date_time_utc).order_by('race_dateTime').last()
    elif round is not None: 
        last_race = Race.objects.filter(round=round).order_by('race_dateTime').last()
    else:
        date_time_utc = timezone.now()
        last_race = Race.objects.filter(race_dateTime__lt=date_time_utc).order_by('race_dateTime').last()
        
    return last_race
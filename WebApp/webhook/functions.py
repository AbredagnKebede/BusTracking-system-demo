
from posixpath import split
from .models import Buses,Shedule
from datetime import datetime
import pytz
from dashboard.models import Locations,Location_Order

TIME_ZONE = 'Africa/Addis_Ababa'


def time_calculater_for_js(time_of_data): 
    time_now_object = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
    time_now = str(time_now_object).split(":")
    time_data = str(time_of_data).split(":")
    if len(time_data) == 2 :
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])
    elif len(time_data)==3:
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])+int(time_data[2])
    total_seconds_now = 3600*int(time_now[0])+60*int(time_now[1])+int(time_now[2]) 
    time_difference = abs(total_seconds_data - total_seconds_now)
    
    return time_difference

def finding_nearest_shedule(bus_id):
    dict_of_shedule_times = {}
    list_of_values =[]
    list_of_values_sorted = []
    all_buses_with_route_number = Buses.objects.filter(bus_registration_number=bus_id)
    
    
    for bus in all_buses_with_route_number:
        bus_shedule = Shedule.objects.get(bus_id = bus)
        starting_to_destination = str(bus_shedule.starting_point_to_destination).split(',')
        for time in starting_to_destination:
            dict_of_shedule_times.update({time_calculater_for_js(time):f"{bus.bus_registration_number}/{time}/1"})
        destinaton_to_starting_point = str(bus_shedule.destinaton_to_starting_point).split(',')
        for time in destinaton_to_starting_point:
            dict_of_shedule_times.update({time_calculater_for_js(time):f"{bus.bus_registration_number}/{time}/0"})
    
    list_of_values = list(dict_of_shedule_times.keys())
    list_of_values_sorted = [int(x)  for x in list_of_values]
    list_of_values_sorted.sort()
  
    nearest_time_and_bus = dict_of_shedule_times[list_of_values_sorted[0]]
    differance = list_of_values_sorted[0]
    time_travel = nearest_time_and_bus.split("/")
    print("nearest sheduled time ",time_travel[1])
    return f"{nearest_time_and_bus}/{differance}"

# GPS-based location finding removed - now handled in views.py using bus stop names
    
   
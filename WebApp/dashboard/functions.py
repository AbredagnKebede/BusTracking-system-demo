
from time import localtime
from unicodedata import name
from webhook.views import time_calculater
from webhook.models import Buses,Shedule
from .models import Location_Order,Locations, Statics_Searching

def getextractlocation(starting_point,destination_point):
    """
    Simplified function that only handles bus stop names (no GPS coordinates).
    Users must select from predefined bus stops.
    """
    data_to_pass = {}
    startingpointtodestination = ''
    
    # Remove "My Location" option - only accept predefined bus stops
    if starting_point == "My Location" or destination_point == "My location" or starting_point == "My location" or destination_point == "My Location":
        raise ValueError("Please select a bus stop from the list. GPS location detection is not available.")
    
    # Both should be bus stop names
    try:
        starting_location = Locations.objects.get(name=starting_point)
        destination_location = Locations.objects.get(name=destination_point)
    except Locations.DoesNotExist:
        raise ValueError("Invalid bus stop selected. Please choose from the available bus stops.")
    
    route_number = int(starting_location.route_number)
    
    # Verify both stops are on the same route
    if starting_location.route_number != destination_location.route_number:
        raise ValueError("Starting point and destination must be on the same route.")
    
    locations_order_object = Location_Order.objects.get(route_number=route_number).list_of_locations.split(",")
    
    if starting_point not in locations_order_object or destination_point not in locations_order_object:
        raise ValueError("Selected stops are not valid for this route.")
    
    if(locations_order_object.index(starting_point) > locations_order_object.index(destination_point)):
        startingpointtodestination = False
    else:
        startingpointtodestination = True

    data_to_pass = {
        "destination_point": destination_point,
        "starting_point": starting_point,
        "userlocation": starting_point,
        "startingpointtodestination": startingpointtodestination,
        "route_number": route_number,
        "startcoordinates": "False",
        "endcoordinates": "False",
        "needdirections": False
    }
    
    return data_to_pass

    
    # location_order_object =Location_Order.objects.get(route_number=route_number)

    # for location in location_order_object:
    #     location_ordered_list.append(location.name)
def finding_nearest_shedule(route_number,startingpointtodestination):
    dict_of_shedule_times = {}
    list_of_values =[]
    list_of_values_sorted = []
    all_buses_with_route_number = Buses.objects.filter(route_number=route_number)
   
    if startingpointtodestination == True:
        for bus in all_buses_with_route_number:
            bus_shedule = Shedule.objects.get(bus_id = bus)
            starting_to_destination = str(bus_shedule.starting_point_to_destination).split(',')
            for time in starting_to_destination:
                dict_of_shedule_times.update({time_calculater(time):f"{bus.bus_registration_number}/{time}"})
        
        list_of_values = list(dict_of_shedule_times.keys())
        list_of_values_sorted = [int(x)  for x in list_of_values]
        list_of_values_sorted.sort()
        nearest_time_and_bus = dict_of_shedule_times[list_of_values_sorted[0]]

    elif startingpointtodestination == False:

        for bus in all_buses_with_route_number:
            bus_shedule = Shedule.objects.get(bus_id = bus)
            destinaton_to_starting_point = str(bus_shedule.destinaton_to_starting_point).split(',')
            for time in destinaton_to_starting_point:
                dict_of_shedule_times.update({time_calculater(time):f"{bus.bus_registration_number}/{time}"})
        
        list_of_values = list(dict_of_shedule_times.keys())
        list_of_values_sorted = [int(x)  for x in list_of_values]
        list_of_values_sorted.sort()
        nearest_time_and_bus = dict_of_shedule_times[list_of_values_sorted[0]]

    return nearest_time_and_bus



def finding_how_many_available_times(route_number,startingpointtodestination,key_id):
    dict_of_shedule_times = {}
    list_of_values =[]
    list_of_values_sorted = []
    available_shedules = {}
    all_buses_with_route_number = Buses.objects.filter(route_number=route_number)
    
    
    
    user_location = Statics_Searching.objects.get(key_id=key_id).starting_point

    if startingpointtodestination == True:
        for bus in all_buses_with_route_number:
            bus_shedule = Shedule.objects.get(bus_id = bus)
            starting_to_destination = str(bus_shedule.starting_point_to_destination).split(',')
            for time in starting_to_destination:
                dict_of_shedule_times.update({time_calculater(time):f"{bus.bus_registration_number}/{time}"})
        
        list_of_values = list(dict_of_shedule_times.keys())
        list_of_values_sorted = [int(x) for x in list_of_values]
        list_of_values_sorted.sort()
        
        for shedule in list_of_values_sorted:
            available_shedules.update({f"{list_of_values_sorted.index(shedule)}":f"{dict_of_shedule_times[shedule]}"})
        
    elif startingpointtodestination == False:
        for bus in all_buses_with_route_number:
            bus_shedule = Shedule.objects.get(bus_id = bus)
            destinaton_to_starting_point = str(bus_shedule.destinaton_to_starting_point).split(',')
            for time in destinaton_to_starting_point:
                dict_of_shedule_times.update({time_calculater(time):f"{bus.bus_registration_number}/{time}"})
        
        list_of_values = list(dict_of_shedule_times.keys())
        list_of_values_sorted = [int(x) for x in list_of_values]
        list_of_values_sorted.sort()
        
        for shedule in list_of_values_sorted:
            available_shedules.update({f"{list_of_values_sorted.index(shedule)}":f"{dict_of_shedule_times[shedule]}"})
    return available_shedules

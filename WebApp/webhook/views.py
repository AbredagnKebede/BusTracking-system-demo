from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Buses, Shedule,Active_buses, Turn_of_bus
import pytz,json
from datetime import datetime
import json
from .functions import finding_nearest_shedule
from django.core.exceptions import ObjectDoesNotExist
from dashboard.models import Infromations_related_to_a_tour,Locations, Statics_Searching, Location_Order

TIME_ZONE = 'Africa/Addis_Ababa'


def time_calculater(time_of_data): 
    time_now_object = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
    time_now = str(time_now_object).split(":")
    time_data = str(time_of_data).split(":")
    if len(time_data) == 2 :
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])
    elif len(time_data)==3:
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])+int(time_data[2])
    total_seconds_now = 3600*int(time_now[0])+60*int(time_now[1])+int(time_now[2]) 
    time_difference = total_seconds_data - total_seconds_now
    if time_difference < 0:
        time_difference = 86400 - total_seconds_now +total_seconds_data
    return time_difference


def time_calculater_for_js(time_of_data): 
    time_now_object = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
    time_now = str(time_now_object).split(":")
    time_data = str(time_of_data).split(":")
    if len(time_data) == 2 :
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])
    elif len(time_data)==3:
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])+int(time_data[2])
    total_seconds_now = 3600*int(time_now[0])+60*int(time_now[1])+int(time_now[2]) 
    time_difference = total_seconds_data - total_seconds_now
    
    return abs( time_difference)
def time_calculater_for_started(time_of_data): 
    time_now_object = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
    time_now = str(time_now_object).split(":")
    time_data = str(time_of_data).split(":")
    if len(time_data) == 2 :
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])
    elif len(time_data)==3:
        total_seconds_data = 3600*int(time_data[0])+60*int(time_data[1])+int(time_data[2])
    total_seconds_now = 3600*int(time_now[0])+60*int(time_now[1])+int(time_now[2]) 
    time_difference = total_seconds_data - total_seconds_now
    
    return  time_difference


def get_next_and_last_location(current_stop_name, route_number):
    """
    Simplified function to get next and last bus stops based on stop name and route.
    No GPS coordinates needed - just uses the route order.
    """
    try:
        locations_order_object = Location_Order.objects.get(route_number=route_number).list_of_locations.split(",")
        
        if current_stop_name not in locations_order_object:
            return {"next_location": "Unknown", "last_location": "Unknown", "Started": False}
        
        index = locations_order_object.index(current_stop_name)
        
        if index == 0:
            before_location = locations_order_object[0]
            next_location = locations_order_object[1] if len(locations_order_object) > 1 else locations_order_object[0]
        elif index == len(locations_order_object) - 1:
            next_location = locations_order_object[index]
            before_location = locations_order_object[index - 1]
        else:
            before_location = locations_order_object[index - 1]
            next_location = locations_order_object[index + 1]
        
        return {
            "next_location": next_location,
            "last_location": before_location,
            "Started": True
        }
    except Exception as e:
        print(f"Error getting location: {e}")
        return {"next_location": "Unknown", "last_location": "Unknown", "Started": False}
 


@csrf_exempt
def ActiveOrDisconnected(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bus_id = data['bus_id']
        tour_id = data['tour_id'][:-1]
        print("javascript data recieved :",bus_id)
    # informations_of_tour = Infromations_related_to_a_tour.objects.get(tour_id=tour_id)
    statics_of_tour = Statics_Searching.objects.get(pk=tour_id).starting_point
    relevent_bus = Buses.objects.get(bus_registration_number=bus_id)
    current_bus = Active_buses.objects.get(bus_id=relevent_bus)
    last_active_time = current_bus.active_time
    differance = time_calculater_for_js(last_active_time)
    if differance < 60 :
        time_for_live = f"{differance} Seconds ago"
    elif differance > 59 and differance < 3600 :
        time_for_live = f"{round(differance/60)} Minutes ago"
    elif differance > 3599 :
        time_for_live = f"{round(differance/3600)} Hours ago"
    print(time_for_live)
    render_data = {}
    
    if differance > 1200:
        current_bus.active = False
        current_bus.save()
        render_data['connected'] = "false"
    else:
        current_bus.active = True
        current_bus.save()
        render_data['connected'] = "true"
    current_details = Turn_of_bus.objects.filter(bus_id=relevent_bus).order_by('current_time')[0]
    started_difference = time_calculater_for_started(current_bus.starting_time)
    if started_difference > 0:
        render_data["started"] = "false"
        current_details.started = False
    else:
        render_data["started"] = "true"
        current_details.started = True
    

    print("Started or not",render_data["started"])
    # Simplified - no GPS distance calculation, just return location names
    render_data["times_ago"] = time_for_live
    render_data["last_location"] = current_details.last_location
    render_data["next_location"] = current_details.next_location
    render_data["current_longitude"] = 0  # Not used anymore
    render_data["current_altitude"] = 0    # Not used anymore
   
    render_data["bus_stand"] = statics_of_tour  # Just the stop name
    render_data["hours_free"] = 0  # Simplified - no distance calculation
    render_data["minutes_free"] = 0  # Simplified - no distance calculation
    current_details.save()
    print(render_data)
    
    return JsonResponse(render_data,headers={"access-control-allow-origin" : "*", 
"access-control-allow-credentials" : "true"})
    


@csrf_exempt
def iotdevice(request):
    """
    Simplified webhook that accepts bus stop name instead of GPS coordinates.
    Expected JSON: {"current_stop": "Bus Stop Name", "massage": "optional message"}
    Headers: id (bus_id), route (route_number), connected (true/false)
    """
    if request.method == 'POST':
        bus_id = request.headers.get("id", "")
        bus_route = request.headers.get("route", "")
        connected_status = request.headers.get("connected", "true")
        json_converted = json.load(request)
        
        # Get current bus stop name from JSON (instead of GPS coordinates)
        current_stop_name = json_converted.get("current_stop", "")
        
        if not current_stop_name:
            return HttpResponse("Error: 'current_stop' field required in JSON", status=400)
        
        print(f"My ID - {bus_id} | Current Stop - {current_stop_name} | message - '{json_converted.get('massage', '')}'")
        
        try:
            relevent_bus = Buses.objects.get(bus_registration_number=bus_id)
        except Buses.DoesNotExist:
            return HttpResponse(f"Error: Bus {bus_id} not found", status=404)
        
        activeordisconected = Active_buses.objects.get(bus_id=relevent_bus)
        activeordisconected.active = True
        activeordisconected.active_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
        
        details = finding_nearest_shedule(bus_id)
        registration_number, time, start_to_end, difference = str(details).split("/")
        activeordisconected.starting_time = time
        activeordisconected.save()
        
        # Get next and last locations based on current stop name
        try:
            route_number = int(bus_route) if bus_route else relevent_bus.route_number
        except (ValueError, AttributeError):
            route_number = relevent_bus.route_number
        
        data_about_locations = get_next_and_last_location(current_stop_name, route_number)
        
        try:
            current_turn = Turn_of_bus.objects.get(bus_id=relevent_bus)
        except ObjectDoesNotExist:
            current_turn = Turn_of_bus.objects.create(
                bus_id=relevent_bus,
                current_altitude=0,
                current_longitude=0,
                starting_time="00:00",
                next_location="none",
                last_location="None",
                started=False,
                current_time=datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S"),
            )
        
        current_turn.bus_id = relevent_bus
        current_turn.current_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
        current_turn.starting_time = activeordisconected.starting_time
        current_turn.next_location = data_about_locations["next_location"]
        current_turn.last_location = data_about_locations["last_location"]
        current_turn.started = data_about_locations["Started"]
        current_turn.save()

        return HttpResponse("Webhook received!")

    if request.method == "GET":
        bus_id = request.headers["id"]
        responce_for_time = ''
        relevent_bus = Buses.objects.get(bus_registration_number = bus_id)
        print(relevent_bus.id)
        bus_shedule = Shedule.objects.get(bus_id=relevent_bus)
        bus_destination_to_starting = str(bus_shedule.destinaton_to_starting_point).split(',')
        bus_starting_to_destination = str(bus_shedule.starting_point_to_destination).split(',')
        all_shedules = {}
        for times in bus_destination_to_starting:
            all_shedules.update({times : time_calculater(times)})
        for times in bus_starting_to_destination:
            all_shedules.update({times : time_calculater(times)})
        data_values =list(int(x) for x in all_shedules.values())
        data_values.sort()
        
        time_in_seconds = data_values[0]
        data_keys = list(all_shedules.keys())

        data_values = list(int(x) for x in all_shedules.values())
        data_to_send_server = data_keys[data_values.index(time_in_seconds)]
        print(bus_id,data_to_send_server)
        activeordisconected = Active_buses.objects.get(bus_id=relevent_bus)
        activeordisconected.active = True
        activeordisconected.active_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H:%M:%S")
        activeordisconected.starting_time = data_to_send_server
        activeordisconected.save()
        return HttpResponse(data_to_send_server)



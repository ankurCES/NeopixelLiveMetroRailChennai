import time
import datetime as dt
import threading
import json
import requests
import board
import neopixel
from datetime import datetime
from collections import Counter

pixels1 = neopixel.NeoPixel(board.D18, 55, brightness=1)

# ALL STATION CODES & HELPER FUNCTIONS
# STATION DATA

COLOR_CODES = {
  "rgb(0, 0, 255)": ["blue_on"],
  "rgb(0, 191, 255)": ["blue_rev"],
  "rgb(0, 255, 0)": ["green_on"],
  "rgb(50, 205, 50)": ["green_rev"],
  "rgb(135, 206, 250)": ["blue_on", "blue_rev"],
  "rgb(0, 255, 255)": ["blue_on", "green_on"],
  "rgb(64, 224, 208)": ["blue_on", "green_rev"],
  "rgb(127, 255, 212)": ["blue_rev", "green_on"],
  "rgb(0, 250, 154)": ["blue_rev", "green_rev"],
  "rgb(173, 255, 47)": ["green_on", "green_rev"],
  "rgb(255, 0, 255)": ["blue_on", "blue_rev", "green_on"],
  "rgb(138, 43, 226)": ["blue_on", "blue_rev", "green_rev"],
  "rgb(255, 255, 0)": ["blue_on", "green_on", "green_rev"],
  "rgb(255, 165, 0)": ["blue_rev", "green_on", "green_rev"],
  "rgb(255, 0, 0)": ["blue_on", "blue_rev", "green_on", "green_rev"]
}

BLUE_LINE_STATIONS = [
    {"name": "Chennai International Airport", "lat": 12.980826, "lon": 80.1642, "id": 117},
    {"name": "Meenambakkam", "lat": 12.987656, "lon": 80.176505, "id": 116},
    {"name": "Nanganallur Road", "lat": 12.999933, "lon": 80.193985, "id": 115},
    {"name": "Alandur", "lat": 13.004713, "lon": 80.20145, "id": 114},
    {"name": "Guindy", "lat": 13.00924, "lon": 80.213199, "id": 113},
    {"name": "Little Mount", "lat": 13.014712, "lon": 80.223993, "id": 112},
    {"name": "Saidapet", "lat": 13.023717, "lon": 80.228208, "id": 111},
    {"name": "Nandanam", "lat": 13.03139, "lon": 80.239969, "id": 110},
    {"name": "Teynampet", "lat": 13.037904, "lon": 80.247029, "id": 109},
    {"name": "AG-DMS", "lat": 13.044682, "lon": 80.248052, "id": 108},
    {"name": "Thousand Lights", "lat": 13.058198, "lon": 80.258056, "id": 107},
    {"name": "LIC", "lat": 13.064511, "lon": 80.266065, "id": 106},
    {"name": "Government Estate", "lat": 13.069557, "lon": 80.272842, "id": 105},
    {"name": "Chennai Central", "lat": 13.081426, "lon": 80.272887, "id": 104},
    {"name": "High Court", "lat": 13.087369, "lon": 80.285021, "id": 103},
    {"name": "Mannadi", "lat": 13.095177, "lon": 80.286164, "id": 102},
    {"name": "Washermenpet", "lat": 13.107064, "lon": 80.280528, "id": 101},
    {"name": "Theagaraya College", "lat": 13.116, "lon": 80.284, "id": 149},
    {"name": "Tondiarpet", "lat": 13.124, "lon": 80.289, "id": 148},
    {"name": "New Washermenpet", "lat": 13.13498, "lon": 80.29327, "id": 147},
    {"name": "Tollgate", "lat": 13.143, "lon": 80.296, "id": 146},
    {"name": "Kaladipet", "lat": 13.151, "lon": 80.299, "id": 145},
    {"name": "Tiruvottiyur Theradi", "lat": 13.15977258, "lon": 80.30244886, "id": 144},
    {"name": "Tiruvottiyur", "lat": 13.172, "lon": 80.305, "id": 143},
    {"name": "Wimco Nagar", "lat": 13.17915, "lon": 80.30767, "id": 142},
    {"name": "Wimco Nagar Depot", "lat": 13.1842985, "lon": 80.30909273, "id": 141}
]

GREEN_LINE_STATIONS = [
    {"name": "Chennai Central", "lat": 13.081426, "lon": 80.272887, "id": 104},
    {"name": "Egmore", "lat": 13.079059, "lon": 80.261098, "id": 202},
    {"name": "Nehru Park", "lat": 13.078625, "lon": 80.250855, "id": 203},
    {"name": "Kilpauk", "lat": 13.077508, "lon": 80.242867, "id": 204},
    {"name": "Pachaiyappa's College", "lat": 13.07557, "lon": 80.232347, "id": 205},
    {"name": "Shenoy Nagar", "lat": 13.078697, "lon": 80.225133, "id": 206},
    {"name": "Anna Nagar East", "lat": 13.084794, "lon": 80.21866, "id": 207},
    {"name": "Anna Nagar Tower", "lat": 13.084975, "lon": 80.208727, "id": 208},
    {"name": "Thirumangalam", "lat": 13.085259, "lon": 80.201575, "id": 209},
    {"name": "Koyambedu", "lat": 13.073708, "lon": 80.194869, "id": 210},
    {"name": "CMBT", "lat": 13.068568, "lon": 80.203882, "id": 211},
    {"name": "Arumbakkam", "lat": 13.062058, "lon": 80.211581, "id": 212},
    {"name": "Vadapalani", "lat": 13.050825, "lon": 80.212242, "id": 213},
    {"name": "Ashok Nagar", "lat": 13.035534, "lon": 80.21114, "id": 214},
    {"name": "Ekkattuthangal", "lat": 13.017044, "lon": 80.20594, "id": 215},
    {"name": "Alandur", "lat": 13.004713, "lon": 80.20145, "id": 114},
    {"name": "St. Thomas Mount", "lat": 12.995128, "lon": 80.19864, "id": 217}
]

LED_MAP = {
    "117": 0,
    "116": 1,
    "115": 2,
    "114": 3,
    "113": 4,
    "112": 5,
    "111": 6,
    "110": 7,
    "109": 8,
    "108": 9,
    "107": 10,
    "106": 11,
    "105": 12,
    "104": 13,
    "103": 14,
    "102": 15,
    "101": 16,
    "149": 17,
    "148": 18,
    "147": 19,
    "146": 20,
    "145": 21,
    "144": 22,
    "143": 23,
    "142": 24,
    "141": 25,
    "202": 27,
    "203": 28,
    "204": 29,
    "205": 30,
    "206": 31,
    "207": 32,
    "208": 33,
    "209": 34,
    "210": 35,
    "211": 36,
    "212": 37,
    "213": 38,
    "214": 39,
    "215": 40,
    "217": 41
}

def get_led_number(station_id):
    return LED_MAP.get(str(station_id), "LED_Unknown")

def get_color_codes(flag_check):
    for color, flags in COLOR_CODES.items():
        if Counter(flag_check) == Counter(flags):
            return color
    return "rgb(0, 0, 0)"

# GET METRO STATUS VIA API
def get_metro_status(from_station_id, to_station_code, travel_date, travel_time):
    url = "https://apiprod.chennaimetrorail.org/v4/api/TravelPlannerWithRoute/TravelPlanner"

    payload = json.dumps({
    "FromStationId": from_station_id,
    "ToStationCode": to_station_code,
    "strDate": travel_date,
    "strTime": travel_time,
    "SecretKey": "$GrtJyNgl^#*StH#QRit$kY"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        metro_status_data = response.json()
        train_timings = []
        for train in metro_status_data["timetable"]:
            train_timings.append(train['train_time'])
        return train_timings
    else:
        raise Exception(f"Failed to get metro status: {response.status_code} - {response.text}")
    
# LED CONTROLLER HELPER FUNCTIONS
def rgb_string_to_tuple(rgb_str):
    """Converts an RGB color string (e.g., '255,0,0' or '(255, 0, 0)') to a tuple."""
    rgb_str = rgb_str.replace("rgb", "")
    # Remove parentheses if present and split by comma
    cleaned_str = rgb_str.strip('()')
    rgb_values = [int(x.strip()) for x in cleaned_str.split(',')]
    new_rgb_values = [rgb_values[1], rgb_values[0], rgb_values[2]]  # Convert RGB to GRB
    return tuple(new_rgb_values)

def startup_sequence():
    # Placeholder for startup LED sequence
    print("Starting up... Cycling through LED colors.")
    for p in range(26):
        pixels1[p] = (0, 0, 255)
        time.sleep(0.5)
    for p in range(27,42):
        pixels1[p] = (255, 0, 0)
        time.sleep(0.5)
    time.sleep(1)
    pixels1.fill((0, 0, 0))

def set_led_color(station_id, color_code):
    # Placeholder for setting the LED color for the station
    led_number = get_led_number(station_id)
    rgb_tuple_code = rgb_string_to_tuple(color_code)
    pixels1[led_number] = rgb_tuple_code
    # Use rgb_tuple_code as needed to set the LED color in neopixel

    print(f"Setting LED color Station Id {station_id} for LED {led_number} to {color_code}")

# MAIN SCRIPT

ROUTE_DATA = {}


def make_request_t(from_station_id, to_station_code, flag, retry_wait_time=5):
    train_time = 0
    try:
        current_time = datetime.now()
        time_delta = dt.timedelta(minutes=5)
        future_time = current_time + time_delta
        travel_date = future_time.strftime("%Y-%m-%d")
        travel_time = future_time.strftime("%H:%M")
        train_timings = get_metro_status(from_station_id, to_station_code, travel_date, travel_time)
        route ={
            "from": from_station_id,
            "direction": flag
        }
        for train_time in train_timings:
            if train_time in ROUTE_DATA.keys():
                if str(from_station_id) in ROUTE_DATA[train_time].keys():
                    ROUTE_DATA[train_time][str(from_station_id)].append(flag)
                else:
                    ROUTE_DATA[train_time][str(from_station_id)] = [flag]
            else:
                ROUTE_DATA[train_time] = {}
                ROUTE_DATA[train_time][str(from_station_id)] = [flag]
    except Exception as e:
        print(f"An error occurred: {e}...Retrying in {retry_wait_time} seconds")
        time.sleep(retry_wait_time)
        next_retry_time = retry_wait_time*(0.1)+retry_wait_time
        make_request_t(from_station_id, to_station_code, flag, retry_wait_time=next_retry_time)

def create_route_list():
    blue_stations = BLUE_LINE_STATIONS
    blue_station_pairs = [(blue_stations[i]['id'], blue_stations[i+1]['id']) for i in range(len(blue_stations)-1)]

    green_stations = GREEN_LINE_STATIONS
    green_station_pairs = [(green_stations[i]['id'], green_stations[i+1]['id']) for i in range(len(green_stations)-1)]
    return blue_station_pairs, green_station_pairs


def set_route_alarm(train_time, route):
    # Placeholder for setting an alarm for the route
    alarm_time = datetime.strptime(train_time, "%H:%M:%S").time()
    print(f"⏰ : {alarm_time}")
    while True:
        # Get the current time
        now = datetime.now().time()
        
        # Check if it's time for the train
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute and now.second >= alarm_time.second:
            for from_station_id, color_code in route.items():
                set_led_color(from_station_id, color_code)
        elif now.hour > alarm_time.hour or (now.hour == alarm_time.hour and now.minute > alarm_time.minute) or (now.hour == alarm_time.hour and now.minute == alarm_time.minute and now.second - alarm_time.second > 30):
            for from_station_id, color_code in route.items():
                set_led_color(from_station_id, "rgb(0, 0, 0)")
            break
        
        # Wait for one second before checking again
        time.sleep(1)

if __name__ == "__main__":
    start_time = time.time()

    # Cycle through LED colors to indicate startup
    print("<--------- Starting Metro Live Status Application --------->")
    startup_sequence()

    # Init the ROUTE_DATA
    blue_station_pairs, green_station_pairs = create_route_list()
    
    
    # Main Thread to get the route timings
    route_threads = []

    for from_station_id, to_station_code in blue_station_pairs:
        route_thread = threading.Thread(target=make_request_t, args=(from_station_id, to_station_code, 'blue_on'))
        route_threads.append(route_thread)
        route_thread.start()
    
    for from_station_id, to_station_code in blue_station_pairs:
        route_thread = threading.Thread(target=make_request_t, args=(to_station_code, from_station_id, 'blue_rev'))
        route_threads.append(route_thread)
        route_thread.start()
    
    for from_station_id, to_station_code in green_station_pairs:
        route_thread = threading.Thread(target=make_request_t, args=(from_station_id, to_station_code, 'green_on'))
        route_threads.append(route_thread)
        route_thread.start()
    
    for from_station_id, to_station_code in green_station_pairs:
        route_thread = threading.Thread(target=make_request_t, args=(to_station_code, from_station_id, 'green_rev'))
        route_threads.append(route_thread)
        route_thread.start()
    
    for route_thread in route_threads:
        route_thread.join() # This line blocks until the thread is finished
    

    for train_time, routes in ROUTE_DATA.items():
        for from_station_id, flags in routes.items():
            color_code = get_color_codes(flags)
            ROUTE_DATA[train_time][from_station_id] = color_code


    end_time = time.time()
    print(f"<--------- Route data retrieved in {end_time - start_time:.2f} seconds ---------> \n {json.dumps(ROUTE_DATA)}")

    print(f"<--------- Setting Timed LED Triggers --------->")

    # Set alarms for each train time in ROUTE_DATA

    alarm_threads = []
    for train_time, routes in ROUTE_DATA.items():
        alarm_thread = threading.Thread(target=set_route_alarm, args=(train_time+':00', routes))
        alarm_threads.append(alarm_thread)
        alarm_thread.start()
    
    for alarm_thread in alarm_threads:
        alarm_thread.join()
    
    print(f"<--------- Timed LED Triggers Set Successfully --------->")
    # Final execution time
    end_time = time.time()
    print(f"<--------- Execution completed in {end_time - start_time:.2f} seconds --------->")

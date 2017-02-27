import requests
import sys

LYFT_KEY = 'YOUR KEY HERE'
LYFT_URL = 'https://api.lyft.com/v1/cost'
UBER_KEY = 'YOUR KEY HERE'
UBER_URL = 'https://api.uber.com/v1.2/estimates/price'

'''

    Compare Route Functions

'''

def compare(start_lat, start_lng, end_lat, end_lng):
    # Create params for API requests to Lyft and Uber
    lyft_params = {
        'start_lat':start_lat,
        'start_lng':start_lng,
        'end_lat':end_lat,
        'end_lng':end_lng
    }
    lyft_headers = {
        'Authorization':'bearer ' + LYFT_KEY
    }
    uber_params = {
        'start_latitude':start_lat,
        'start_longitude':start_lng,
        'end_latitude':end_lat,
        'end_longitude':end_lng
    }
    uber_headers = {
        'Authorization':'Token ' + UBER_KEY
    }

    # Do API Requests to Lyft and Uber
    lyft_request = requests.get(LYFT_URL, params=lyft_params, headers=lyft_headers)
    uber_request = requests.get(UBER_URL, params=uber_params, headers=uber_headers)

    # Check if both requests were succesful
    if lyft_request.status_code != 200 or uber_request.status_code != 200:
        return {'success':False}

    # Get estimates from both requests
    lyft_cost_estimates = lyft_request.json()['cost_estimates']
    uber_cost_estimates = uber_request.json()['prices']

    # Check to see what is cheaper and send it back to the user
    lyft_cost = sys.maxint
    uber_cost = sys.maxint

    for estimate in lyft_cost_estimates:
        lyft_cost = min(lyft_cost, (estimate['estimated_cost_cents_min']/100))
        if estimate['ride_type'] == 'lyft':
            break

    for estimate in uber_cost_estimates:
        uber_cost = min(uber_cost, estimate['low_estimate'])
        if estimate['display_name'] == 'uberX':
            break

    if lyft_cost > uber_cost:
        # Uber is cheaper
        return {'success':True, 'winner':'uber', 'cost':uber_cost}

    return {'success':True, 'winner':'lyft', 'cost':lyft_cost}

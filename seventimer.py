import urllib.parse, urllib.request, urllib.error, json

# Accepts the following parameters:
#      - lat (float degrees): Latitude.
#        Optional. Default 47.653457 for Rainier Vista.
#      - lon (float degrees): Longitude.
#        Optional. Default -122.307550 for Rainier Vista.
# Other parameters:
#      - ac (0|2|7 km): Altitude correction.
#        Optional. Default 0.
#      - unit (metric|british): Metric or Imperial (British).
#        Optional. Default metric.
#      - tzshift (0|1|-1): Timezone adjustment.
#        Optional. Default 0.
def safe_get(lat = 47.653457, lon = -122.307550):
    args = {"lat":lat, "lon":lon, "product":"astro", "output":"json"}


    base_url = "http://www.7timer.info/bin/api.pl"
    url = base_url + "?" + urllib.parse.urlencode(args)

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode()
    except urllib.error.HTTPError as e:
        print("Error from server. Error code: ", e.code)
        return None
    except urllib.error.URLError as e:
        print("Failed to reach server. Reason: ", e.reason)
        return None
    return json.loads(data)

# import pprint
# Extracts and returns select fields from the API JSON output.
def get(latlon, hours):
    data_loaded = safe_get(latlon[0], latlon[1])
    # pprint.pprint(data_loaded)

    hours_data = []
    for hour in hours:
        data_extracted = dict.fromkeys(["cloudcover", "prec_type", "transparency"])
        for key in data_extracted:
            data_extracted[key] = data_loaded["dataseries"][int(hour/3-1)][key]
        data_extracted["hour"] = hour
        hours_data.append(data_extracted)
    # pprint.pprint(hours_data)
    return hours_data

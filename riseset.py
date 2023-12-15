import urllib.parse, urllib.request, urllib.error, json

# Accepts the following parameters:
#      - lat (float degrees): Latitude.
#        Optional. Default 47.653457 for Rainier Vista.
#      - lng (float degrees): Longitude.
#        Optional. Default -122.307550 for Rainier Vista.
#      - date (string YYYY-MM-DD): Also accepts other absolute and relative date formats.
#        Default current date.
# Other parameters:
#      - formatted (0|1): For formatted times.
#        Default 1.
#      - callback (string): Callback function name for JSONP response.
#      - tzId (string): Timezone identifier.
def safe_get(lat = 47.653457, lng = -122.307550, date = None, tzId = None):
    args = {"lat":lat, "lng":lng, "date":date, "tzId":tzId}
    if (date == None): args.pop("date")
    if (tzId == None): args.pop("tzId")
    base_url = "https://api.sunrise-sunset.org/json"
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
def extract(latlng, day, tzId):
    if day == 0:
        data_loaded = safe_get(latlng[0], latlng[1], None, tzId)
    else:
        data_loaded = safe_get(latlng[0], latlng[1], "+"+str(day)+" days", tzId)
    if data_loaded["status"] == "UKNOWN_ERROR":
        print("Failed to reach server")
    # pprint.pprint(data_loaded)

    data_extracted = dict.fromkeys(["sunrise", "sunset", "nautical_twilight_begin", "nautical_twilight_end"])
    for key in data_extracted:
        data_extracted[key] = data_loaded["results"][key]
    data_extracted["day"] = day
    return data_extracted

def get(latlng, days, tzId):
    days_data = []
    for day in days:
        days_data.append(extract(latlng, day, tzId))
    # pprint.pprint(days_data)
    return days_data

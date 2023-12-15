import riseset, seventimer

# day0 and hour0 are the time of init

all_days = [0, 1, 2]
all_hours = [3, 24, 48, 72]

locations_data =   {"San Francisco": {"coords":(37.7749, -122.4194), "tzId":"America/Los_Angeles"}, 
                    "Seattle"      : {"coords":(47.6061, -122.3328), "tzId":"America/Los_Angeles"}, 
                    "Paris"        : {"coords":(48.8566,    2.3522), "tzId":"Europe/Paris"}, 
                    "Kyiv"         : {"coords":(50.4504,   30.5245), "tzId":"Europe/Kyiv"}, 
                    "Beijing"      : {"coords":(39.9042,  116.4074), "tzId":"Asia/Shanghai"}, 
                    "Seoul"        : {"coords":(37.5519,  126.9918), "tzId":"Asia/Seoul"}}

import pprint
def get(locations, days, hours):
    pprint.pprint(locations)
    for location in locations.keys():
        locations[location]["name"] = location
        coords = locations[location]["coords"]
        tzId = locations[location]["tzId"]
        locations[location]["days"] = riseset.get(coords, days, tzId)
        locations[location]["hours"] = seventimer.get(coords, hours)
    pprint.pprint(locations)
    return locations

if __name__ == "__main__":
    pprint.pprint(get(locations_data, all_days, all_hours))

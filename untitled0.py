#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 08:15:52 2019

@author: john
"""

#!/usr/bin/env python2
import time
import datetime
from opensky_api import OpenSkyApi
minlat = 51.25
maxlat = 51.75
minlong = 0.5
maxlong = 1.75
#for gb3ngi
#minlat = 52
#maxlat = 54
#minlong = 3
#maxlong = 5
bbox =[minlat,maxlat,minlong,maxlong]
api = OpenSkyApi()
s = api.get_states(0,None,None,bbox)
mylist = s.states
biglist = []
for plane in mylist:
    planedict = {}
    planedict["baro_altitude"] = plane.baro_altitude
    planedict["plane.callsign"] = plane.callsign  
    planedict["plane.geo_altitude"] = plane.geo_altitude
    planedict["heading"] = plane.heading
    planedict["icao24"] = plane.icao24
    planedict["last_contact"] = plane.last_contact
    planedict['latitude'] = plane.latitude
    planedict['longitude'] = plane.longitude
    planedict['on_ground'] = plane.on_ground
    planedict['origin_country'] = plane.origin_country
    planedict['position_source'] = plane.position_source
    planedict['sensors'] = plane.sensors
    planedict['spi'] = plane.spi
    planedict['squawk'] = plane.squawk
    planedict['time_position'] = plane.time_position
    planedict['velocity'] = plane.velocity
    planedict['vertical_rate'] = plane.vertical_rate
    planedict['snr'] = 0.0
    biglist.append(planedict)
#for item in biglist:
#    print(item)
    print("last contact data " + str(planedict["last_contact"]) + " " + str(time.gmtime(planedict["last_contact"])) + " at " + str(datetime.datetime.now()))

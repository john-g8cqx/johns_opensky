#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:37:39 2019
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You need copy of the GNU General Public License
    along with this program.  See <https://www.gnu.org/licenses/>.

@author: john G8CQX
"""

from opensky_api import OpenSkyApi
import math
import json
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def unpack_statevector(plane):
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
    return(planedict)

longscale = 0.6184 #cos(52) gives relative size of a degree of longitude to latitude where we are
mylat = 51.854
mylong = -2.042
gb3vhflat = 51.313
gb3vhflong = 0.375
gb3ngilat = 55.063
gb3ngilong = -6.208
middle_lat = (mylat + gb3vhflat)/2
middle_long =(mylong + gb3vhflong)/2
print("middle latitude " + str(middle_lat))
print("middle longitude " + str(middle_long))
vrange = 69*math.cos(middle_long)*(mylong - gb3vhflong)
hrange = 69*(mylat - gb3vhflat)
mymidrange = (math.sqrt(math.pow(vrange,2)+ math.pow(hrange,2)))/2 
midrange_vis_height = 1000*(math.sqrt(math.pow(6371,2) + math.pow(mymidrange,2)) - 6371)
print("midrange is " + str(mymidrange) + " height limit is above " + str(midrange_vis_height) + " meters")       
#total box side is 1 degree latitude or about 43.7 miles
maxlat = middle_lat + 0.5
minlat = middle_lat - 0.5
maxlong = middle_long + (longscale/2)
minlong = middle_long - (longscale/2)
bbox =[minlat,maxlat,minlong,maxlong]
print(bbox)
api = OpenSkyApi()
snrplane = []
CHUNKSIZE = 480000# fixed chunk size 10 sec
DECIMATION = 10
fs = CHUNKSIZE
# initialize portaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=CHUNKSIZE)
diff = 0.0
while True:
    data = stream.read(CHUNKSIZE)
    x = np.frombuffer(data, dtype=np.int16)
    x =x.astype(float)
    x = signal.decimate(x,DECIMATION)
    narrf = []
    narrp = []
    f,p = signal.periodogram(x,CHUNKSIZE//(DECIMATION*10))
    p = 10*np.log10(p)
    for j in range(len(f)):
        if 4e2 < f[j] <1e3:
            narrf.append(f[j])
            narrp.append(p[j])
    max = np.amax(narrp)
    av = np.mean(narrp)
    for j in range(len(narrp)):
        if max - narrp[j]:
            maxfreq = narrf[j]
    diff = max-av
    print("maximum " + str(max) + "at freq " + str(maxfreq) + " and mean" + str(av) + " diff " + str(diff))
    plt.plot(narrf,narrp)
    plt.show()
    notgotit = True
    while notgotit:
        try:
            s = api.get_states(0,None,None,bbox)
            notgotit = False
        except:
            print("api statevector fetch a=gain")
            pass
        if not s:
            print ("no planes")
        else:
            print(str(len(s.states)) + " planes")
            for plane in s.states:
                newplane = unpack_statevector(plane)
                newplane['snr'] = diff
                with open('/home/john/snrplanes.json', 'a') as json_file:  
                   json.dump(newplane, json_file)
#                print ()
#                print(newplane)
                    
##close stream
stream.stop_stream()
stream.close()
p.terminate()



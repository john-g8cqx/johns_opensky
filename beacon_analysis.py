#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:28:32 2019

@author: john
"""
import json
import matplotlib.pyplot as plt
import itertools
import operator
import time
import matplotlib.pyplot as plt
import tilemapbase
import math

###first plot a basemap####
tilemapbase.init(create=True)

longscale = 0.6184 #cos(52) gives relative size of a degree of longitude to latitude where we are
mylat = 51.854
mylong = -2.042
gb3vhflat = 51.313
gb3vhflong = 0.375
gb3ngilat = 55.063
gb3ngilong = -6.208
#select the right beacon
middle_lat = (mylat + gb3ngilat)/2
middle_long =(mylong + gb3ngilong)/2
print("middle latitude " + str(middle_lat))
print("middle longitude " + str(middle_long))
#select the right beacon
vrange = 69*math.cos(middle_long)*(mylong - gb3ngilong)
hrange = 69*(mylat - gb3ngilat)
mymidrange = (math.sqrt(math.pow(vrange,2)+ math.pow(hrange,2)))/2 
midrange_vis_height = 1000*(math.sqrt(math.pow(6371,2) + math.pow(mymidrange,2)) - 6371)
print("midrange is " + str(mymidrange) + " height limit is above " + str(midrange_vis_height) + " meters")       
#total box side is 1 degree latitude or about 43.7 miles
maxlat = middle_lat + 1
minlat = middle_lat - 1
maxlong = middle_long + (longscale)
minlong = middle_long - (longscale)
bbox =[minlat,maxlat,minlong,maxlong]
print(bbox)


def sortbyicao24(mydata):
    return(sorted(mydata, key=operator.itemgetter('icao24')))
 
path = "/home/john/johns_opensky/gb3ngi_snrplanes.json"
with open(path,"r") as datafile:
    mydata = json.load(datafile)
snrs = list(map(lambda x: x['snr'],mydata))
plt.hist(snrs)
plt.show()
with open(path,"r") as datafile:
    mydata = json.load(datafile)
newlist = []
selection =sortbyicao24(mydata)
for key, group in itertools.groupby(selection, key=lambda x:x['icao24']):
    thislist = list(group)
    for sighting in thislist:
        obsdict = {}
        try:
            if (sighting['snr'] > 20.0) and (float(sighting['plane.geo_altitude']) > midrange_vis_height):
                obsdict = {'icao24':sighting['icao24'],'latitude':sighting['latitude'],
                       'longitude':sighting['longitude'],'last_contact':sighting['last_contact']}
                newlist.append(obsdict)
        except TypeError:
            print('record type issue')
#print(newlist)
##    print(' from ' + time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(tamydalist[0]['last_contact'])),end = '')
#    print(' to ' + time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(mydatalist[-1]['last_contact'])))
# Define the `extent` of basemap


extent = tilemapbase.Extent.from_lonlat(minlong,maxlong,minlat,maxlat)
extent = extent.to_aspect(1.0)
fig, ax = plt.subplots(figsize=(10,10))

plotter = tilemapbase.Plotter(extent, tilemapbase.tiles.build_OSM(), width=600)
plotter.plot(ax)
plotter.plot(plt.axes())
for planeobservation in newlist:
    x,y = tilemapbase.project(planeobservation['longitude'],planeobservation['latitude'])
    print('x ' + str(x) + ' y ' + str(y))
    plt.plot(x,y, "ro-")
plt.show

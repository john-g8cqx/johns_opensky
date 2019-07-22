#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:15:22 2019

@author: john
"""

import matplotlib.pyplot as plt
import tilemapbase
import math

tilemapbase.init(create=True)

longscale = 0.6184 #cos(52) gives relative size of a degree of longitude to latitude where we are
mylat = 51.854
mylong = -2.042
gb3vhflat = 51.313
gb3vhflong = 0.375
gb3ngilat = 55.063
gb3ngilong = -6.208
#select the right beacon
middle_lat = (mylat + gb3vhflat)/2
middle_long =(mylong + gb3vhflong)/2
print("middle latitude " + str(middle_lat))
print("middle longitude " + str(middle_long))
#select the right beacon
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

# Define the `extent`


extent = tilemapbase.Extent.from_lonlat(minlong,maxlong,minlat,maxlat)
extent = extent.to_aspect(1.0)
ig, ax = plt.subplots(figsize=(10,10))

plotter = tilemapbase.Plotter(extent, tilemapbase.tiles.build_OSM(), width=600)
plotter.plot(ax)


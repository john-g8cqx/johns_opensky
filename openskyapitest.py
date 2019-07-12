#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 19:44:04 2019
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

@author: john-G8CQX
"""
from opensky_api import OpenSkyApi
#minlat = 51.25
#maxlat = 51.75
#minlong = 0.5
#maxlong = 1.75
#for gb3ngi
minlat = 52
maxlat = 54
minlong = 3
maxlong = 5
bbox =[minlat,maxlat,minlong,maxlong]
api = OpenSkyApi()
s = api.get_states(0,None,None,bbox)
mylist = s.states
newresults = []
for l in mylist:
    newlist = []
    newlist = [0.0,l]
    newresults.append(newlist)
print(newresults)

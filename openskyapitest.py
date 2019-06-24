#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 19:44:04 2019

@author: john
"""
minlat = 51.25
maxlat = 51.75
minlong = 0.5
maxlong = 1.75
bbox =[minlat,maxlat,minlong,maxlong]
from opensky_api import OpenSkyApi
api = OpenSkyApi()
s = api.get_states(0,None,None,bbox)
for state in s.states:
    print(state)

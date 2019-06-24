#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 19:44:04 2019

@author: john
"""

from opensky_api import OpenSkyApi
api = OpenSkyApi()
s = api.get_states()
print(s)

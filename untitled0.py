#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 19:08:36 2019

@author: john
"""

import math

free_space_imp = 377.0
imax = 1.5e-3
mu_0 = 1.257e-6
radius = 1.0
rin = 3.0
area = 2*math.pi*math.pow(radius,2)
for frequency in range(1,30):
    wu_oa = 2.0*math.pi*frequency
    power_density = free_space_imp*(imax*math.pow((3+wu_oa)/wu_oa,2))
    print("at freq " + str(frequency) + " max safe power density is " + str(power_density) + 
          " and v/m is " + str(math.sqrt(free_space_imp*power_density)))
    
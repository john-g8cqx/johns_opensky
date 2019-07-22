#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:28:32 2019

@author: john
"""
import json
import matplotlib.pyplot as plt


path = "/home/john/johns_opensky/gb3ngi_snrplanes.json"
with open(path,"r") as datafile:
    mydata = json.load(datafile)
snrs = list(map(lambda x: x['snr'],mydata))
plt.hist(snrs)
plt.show()
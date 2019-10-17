#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 13:44:45 2019

@author: john
"""
import json
import matplotlib.pyplot as plt

path = "/home/john/gb3vhf16oct17oct.json"
with open(path,"r") as datafile:
    mydata = json.load(datafile)
snrs = list(map(lambda x: x['snr'],mydata))
plt.plot(snrs)
plt.show()

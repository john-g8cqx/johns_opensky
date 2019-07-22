#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:28:32 2019

@author: john
"""
import json
import re

listdics = []
path = "/home/john/johns_opensky/gb3ngi_snrplanes.json"
with open(path,"r") as datafile:
    mydata = datafile.read()
for result in re.findall('{(.*?)}',mydata, re.S):
    stuff = "{" + result + "}"
    planedict = json.loads(stuff)
    print(planedict)
    listdics.append(planedict)
with open(path,'w') as outputfile:
    json.dump(listdics,outputfile)
print("file overwritten")
#print(list3data)
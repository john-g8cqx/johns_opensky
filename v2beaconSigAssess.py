#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 16:26:59 2019

@author: john
"""

#10  ''' tracking number of times it prints'''
from threading import Timer, Thread, Event
from datetime import datetime
from opensky_api import OpenSkyApi
import math
import json
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import traceback
import threading
CHUNKSIZE = 480000# fixed chunk size 10 sec
DECIMATION = 1
fs = CHUNKSIZE
p = pyaudio.PyAudio()

signal_observation_list =[]
# initialize portaudio
stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=CHUNKSIZE)
 
class perpetualTimer():

    def __init__(self, duration, hFunction):
        self.duration = duration
        self.hFunction = hFunction
        self.thread = Timer(self.duration, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.duration, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()
     
def timcheck():
    timp = time.time() 
    tempo = datetime.fromtimestamp(timp)
#    h = tempo.hour
#    m = tempo.minute
    s = tempo.second
    return(s)
            

def do_stuff():
    while timcheck()%10  != 0:
        pass
    ts = time.time()
    tempo = datetime.fromtimestamp(ts)
    h,m,s = tempo.hour, tempo.minute, tempo.second
    max,maxfreq,av,diff = getsigs(stream,CHUNKSIZE,DECIMATION)
    print(f"{h}:{m}:{s}" + " maximum " + str(max) + "at freq " + str(maxfreq) + " and mean " + str(av) + " diff " + str(diff))
    sigobs = {}
    sigobs={'hour':h,'minute':m,'second':s,'snr':diff,'frequency':maxfreq}
#    signal_observation_list.append(sigobs)
    with open('/home/john/beaconsnrobs.json', 'a+') as json_file:  
        json.dump(sigobs, json_file)

def getsigs(stream,CHUNKSIZE,DECIMATION):
    data = stream.read(CHUNKSIZE,DECIMATION)
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
        if max == narrp[j]:
            maxfreq = narrf[j]
    diff = max-av
#    plt.plot(narrf,narrp)
#    plt.show()
    return(max,maxfreq,av,diff)

def every(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc()
      # in production code you might want to have this instead of course:
      # logger.exception("Problem while executing repetitive task.")
    # skip tasks if we are behind schedule:
    next_time += (time.time() - next_time) // delay * delay + delay


threading.Thread(target=lambda: every(10, do_stuff)).start()

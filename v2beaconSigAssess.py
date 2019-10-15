#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 16:26:59 2019

@author: john
"""

#10  ''' tracking number of times it prints'''
from datetime import datetime
import json
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import traceback
import threading
MULTIPLE = 6
CHUNKSIZE = 480000*MULTIPLE# fixed chunk size 10 sec*MULTIPLE
DECIMATION = 1
fs = CHUNKSIZE/(10*DECIMATION*MULTIPLE)
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
    while timcheck()  != 0:
        pass
    ts = time.time()
    tempo = datetime.fromtimestamp(ts)
    h,m,s = tempo.hour, tempo.minute, tempo.second
    max,maxfreq,av,diff,freqs = getsigs(stream,CHUNKSIZE,DECIMATION)
    print(f"{h}:{m}:{s}" + " maximum " + str(max) + "at freq " + str(maxfreq) + " and mean " + str(av) + " diff " + str(diff))
    print('frequencies ' + str(freqs))
    sigobs = {}
    sigobs={'hour':h,'minute':m,'second':s,'snr':diff,'frequency':maxfreq,'observed freqs':freqs}
    signal_observation_list.append(sigobs)
    with open('/home/john/beaconsnrobs.json', 'w') as json_file:  
        json.dump(signal_observation_list, json_file)

def getsigs(stream,CHUNKSIZE,DECIMATION):
    data = stream.read(CHUNKSIZE,DECIMATION)
    x = np.frombuffer(data, dtype=np.int16)
    x =x.astype(float)
    x = signal.decimate(x,DECIMATION)
    narrf = []
    narrp = []
    f,p = signal.periodogram(x,fs)
    p = 10*np.log10(p)
    for j in range(len(f)):
        if 4e2 < f[j] <1e3:
            narrf.append(f[j])
            narrp.append(p[j])
    max = np.amax(narrp)
    av = np.mean(narrp)
    peaks = np.argpartition(narrp,-8)[-8:]
    peaks.sort()
    peaks = peaks[::-1]
#    print("peaks " + str(peaks) )
    filtpeaks = [peaks[0]]
    for index in range(len(peaks)-1):
        if (peaks[index+1] + 50) < (peaks[index]):
            filtpeaks.append(peaks[index+1])        
    freqs = []
    for peak in filtpeaks:
        freqs.append(narrf[peak])
#    print("filtered frequency peaks indexes are " + str(filtpeaks) + " whose frequencies are " + str(freqs))
    for j in range(len(narrp)):
        if max == narrp[j]:
            maxfreq = narrf[j]
#            print("max freq index really is " + str(j))
    diff = max-av
#    plt.plot(narrf,narrp)
#    plt.show()
    return(max,maxfreq,av,diff,freqs)

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


threading.Thread(target=lambda: every(60, do_stuff)).start()

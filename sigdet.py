#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 18:13:51 2019
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
calculate power spectrum by fft of autocorrelation function
"""
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



CHUNKSIZE = 480000# fixed chunk size 10 sec
DECIMATION = 10
fs = CHUNKSIZE
# initialize portaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=CHUNKSIZE)

# do this as long as you want fresh samples
while True:
    
    data = stream.read(CHUNKSIZE)

    x = np.frombuffer(data, dtype=np.int16)
    x =x.astype(float)
    x = signal.decimate(x,DECIMATION)
    f,p = signal.periodogram(x,CHUNKSIZE//(DECIMATION*10))
    p = 10*np.log10(p)
    max = np.amax(p)
    av = np.mean(p)
    diff = max-av
    print("maximum " + str(max) + " and mean" + str(av) + " diff " + str(diff))
    plt.plot(f,p)
    plt.show()
# close stream
stream.stop_stream()
stream.close()
p.terminate()
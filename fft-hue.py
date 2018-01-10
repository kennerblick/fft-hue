#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pyaudio
import numpy as np
import requests
import time

LOW_BRI = 0
MAX_BRI = 254
MAX_HUE = 65534
max_peak = 1
min_peak = 1000
result = 0
chunk = 1024 #2**12
rate = 44100
fft_selection_filter = 12
hue_cycle_speed = 500
activation_threshold = 150000
run_time = 600 #in sec
user_id = 'your_user_id'
hue_bridge_ip = 'your_ip_bridge_ipv4_address'
previous_peak = 0
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,
              frames_per_buffer=chunk, input_device_index=2)

previous_bri = LOW_BRI
for i_data_blocks in range(run_time*rate/chunk):
    try:
        data = np.fromstring(stream.read(chunk, exception_on_overflow = False),dtype=np.int16)
        peak=int(np.average(np.abs(data))*2)
        if peak < min_peak:
            min_peak = peak
        if peak > max_peak:
            max_peak = peak
        peak = peak - min_peak
        if peak > 256:
            peak = 256
        peak_factor = (max_peak-min_peak+1)/256
        if peak_factor < 0.1:
            peak_factor = 0.1
        print("max, min, factor: " + str(max_peak) + ", " + str(min_peak) + ", " + str(peak_factor))
        peak = int(peak/peak_factor)
        bars="#"*int(200*peak/chunk)
        print("%04d %05d %s"%(i_data_blocks,peak,bars))
        fft = np.fft.fft(data)
        bri = int(np.absolute(np.average(fft[0:fft_selection_filter])))
        print("bri: " + str(bri))
        hue = str((i_data_blocks*hue_cycle_speed)%MAX_HUE)
        result = np.append(result, data)
        w = np.fft.fft(result)
        freqs = np.abs((np.fft.fftfreq(len(w))*44100))
        print("freqs: " + str(freqs))
        if peak != previous_peak:
            #r_1 = requests.put('http://' + hue_bridge_ip + '/api/' + user_id +'/lights/2/state',data='{"bri": ' + str(peak) +', "transitiontime" : 1, "hue": ' + hue +'}')
            r_2 = requests.put('http://' + hue_bridge_ip + '/api/' + user_id +'/lights/17/state',data='{"bri": ' + str(peak) +', "transitiontime" : 1, "hue": ' + hue +'}')

        previous_peak = peak
        max_peak = max_peak -10
        min_peak = min_peak +10
    except IOError:
        print "FAIL"
        stream.stop_stream()
stream.stop_stream()
stream.close()
p.terminate()

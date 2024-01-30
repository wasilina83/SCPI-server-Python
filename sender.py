#!/usr/bin/env python3

import numpy as np
import math
from matplotlib import pyplot as plt
import redpitaya_scpi as scpi

def send_waveform_to_red_pitaya(x, y):
    IP = '169.254.6.100'
    rp_s = scpi.scpi(IP)
    wave_form = 'arbitrary'
    freq = 10000
    ampl=1
    
    
    waveform_ch_10 = []
    waveform_ch_20 = []

    for n in x:
        waveform_ch_10.append(f"{n:.5f}")
    waveform_ch_1 = ", ".join(map(str, waveform_ch_10))

    for n in y:
        waveform_ch_20.append(f"{n:.5f}")
    waveform_ch_2 = ", ".join(map(str, waveform_ch_20))


    rp_s.tx_txt('GEN:RST')

    rp_s.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
    rp_s.tx_txt('SOUR2:FUNC ' + str(wave_form).upper())

    rp_s.tx_txt('SOUR1:TRAC:DATA:DATA ' + waveform_ch_1)
    rp_s.tx_txt('SOUR2:TRAC:DATA:DATA ' + waveform_ch_2)

    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
    rp_s.tx_txt('SOUR2:FREQ:FIX ' + str(freq))

    rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))
    rp_s.tx_txt('SOUR2:VOLT ' + str(ampl))

    rp_s.tx_txt('OUTPUT:STATE ON')
    rp_s.tx_txt('SOUR:TRIG:INT')

    rp_s.close()

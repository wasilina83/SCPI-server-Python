#!/usr/bin/env python3

import numpy as np
import math
from matplotlib import pyplot as plt
import redpitaya_scpi as scpi

IP = '169.254.6.100'
rp_s = scpi.scpi(IP)

wave_form = 'arbitrary'
freq = 10000
ampl = 1

N = 16384               # Number of samples
t = np.linspace(0, 1, N)*2*math.pi

x = np.sin(t) + 1/3*np.sin(3*t)
y = 1/2*np.sin(t) + 1/4*np.sin(4*t)

plt.plot(t, x, t, y)
plt.title('Custom waveform')
plt.show()


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

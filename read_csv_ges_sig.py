import numpy as np
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import genfromtxt
import sys
sys.path.insert(0, r'autopulse\Code\DataMaker')
from SignalGenerator import signal_functions, noise_beta, generate_signal, add_noise_to_signal
from SignalGenerator import *


class SignalGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Generator GUI")

        # Red Pitaya IP und Verbindung
        self.IP = '169.254.6.100'
        self.rp_s = scpi.scpi(self.IP)

        # GUI-Elemente
        self.create_gui()

    def create_gui(self):
        # Labels und Entry-Felder für die Parameter
        ttk.Label(self.root, text="Amplitude:").grid(row=0, column=0)
        self.amplitude_entry = ttk.Entry(self.root)
        self.amplitude_entry.grid(row=0, column=1)

        ttk.Label(self.root, text="Frequency:").grid(row=1, column=0)
        self.frequency_entry = ttk.Entry(self.root)
        self.frequency_entry.grid(row=1, column=1)

        ttk.Label(self.root, text="Offset:").grid(row=2, column=0)
        self.offset_entry = ttk.Entry(self.root)
        self.offset_entry.grid(row=2, column=1)

        ttk.Label(self.root, text="Phase Shift:").grid(row=3, column=0)
        self.phase_shift_entry = ttk.Entry(self.root)
        self.phase_shift_entry.grid(row=3, column=1)

        
        ttk.Label(self.root, text="Noise-Typ Name:").grid(row=4, column=0)
        self.noise_type_entry = tk.StringVar()
        self.noise_type_combobox = ttk.Combobox(self.root, textvariable=self.noise_type_entry, values=list(noise_beta.keys()))
        self.noise_type_combobox.grid(row=4, column=1)
        self.noise_type_combobox.set("Rot")  # Setzen Sie den Standardwert

        ttk.Label(self.root, text="Noise Weight:").grid(row=5, column=0)
        self.noise_weight_entry = ttk.Entry(self.root)
        self.noise_weight_entry.grid(row=5, column=1)

        # Dropdown-Menü für Signalnamen
        ttk.Label(self.root, text="Signal Name:").grid(row=6, column=0)
        self.signal_name_var = tk.StringVar()
        self.signal_name_combobox = ttk.Combobox(self.root, textvariable=self.signal_name_var, values=list(signal_functions.keys()))
        self.signal_name_combobox.grid(row=6, column=1)
        self.signal_name_combobox.set("Ansauglufttemperatur")  # Setzen Sie den Standardwert
        

        # Button zum Aktualisieren des Signals
        ttk.Button(self.root, text="Update Signal", command=self.update_signal).grid(row=7, column=0, columnspan=2)

        # Matplotlib-Figure für die Anzeige des Signals
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2)
        
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


    def update_signal(self):
        # Holen Sie die eingegebenen Werte aus den Entry-Feldern
        duration = 6
        amplitude = float(self.amplitude_entry.get())
        frequency = float(self.frequency_entry.get())
        offset = float(self.offset_entry.get())
        phase_shift = float(self.phase_shift_entry.get())
        noise_type = self.noise_type_entry.get()
        noise_weight = float(self.noise_weight_entry.get())

        # Holen Sie den ausgewählten Signalnamen aus dem Dropdown-Menü
        signal_name = self.signal_name_var.get()

        # Generieren Sie das Signal und fügen Sie das Rauschen hinzu
        t, x = generate_signal(signal_name, duration, amplitude, frequency, offset, phase_shift)
        t, y = add_noise_to_signal(t, x, noise_type, noise_weight)
        send_waveform_to_red_pitaya(x, y)

        # Plotten Sie das Signal auf der Matplotlib-Figur
        self.ax.clear()
        self.ax.plot(t, x, label='Ohne Rauschen')
        self.ax.plot(t, y, label='mit Rauschen')
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalGeneratorApp(root)
    root.mainloop()
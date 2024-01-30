import numpy as np
from numpy import genfromtxt
import math
from matplotlib import pyplot as plt
import redpitaya_scpi as scpi
import sys
sys.path.insert(0, r'autopulse\Code\DataMaker')
from SignalGenerator import signal_functions, noise_beta, generate_signal, add_noise_to_signal
from SignalGenerator import *
from sender import send_waveform_to_red_pitaya

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        ttk.Label(self.root, text="Duration:").grid(row=0, column=0)
        self.duration_entry = ttk.Entry(self.root)
        self.duration_entry.grid(row=0, column=1)

        ttk.Label(self.root, text="Amplitude:").grid(row=1, column=0)
        self.amplitude_entry = ttk.Entry(self.root)
        self.amplitude_entry.grid(row=1, column=1)

        ttk.Label(self.root, text="Frequency:").grid(row=2, column=0)
        self.frequency_entry = ttk.Entry(self.root)
        self.frequency_entry.grid(row=2, column=1)

        ttk.Label(self.root, text="Offset:").grid(row=3, column=0)
        self.offset_entry = ttk.Entry(self.root)
        self.offset_entry.grid(row=3, column=1)

        ttk.Label(self.root, text="Phase Shift:").grid(row=4, column=0)
        self.phase_shift_entry = ttk.Entry(self.root)
        self.phase_shift_entry.grid(row=4, column=1)

        ttk.Label(self.root, text="Noise Type:").grid(row=5, column=0)
        self.noise_type_entry = ttk.Entry(self.root)
        self.noise_type_entry.grid(row=5, column=1)

        ttk.Label(self.root, text="Noise Weight:").grid(row=6, column=0)
        self.noise_weight_entry = ttk.Entry(self.root)
        self.noise_weight_entry.grid(row=6, column=1)

        # Dropdown-Menü für Signalnamen
        ttk.Label(self.root, text="Signal Name:").grid(row=7, column=0)
        self.signal_name_var = tk.StringVar()
        self.signal_name_combobox = ttk.Combobox(self.root, textvariable=self.signal_name_var, values=list(signal_functions.keys()))
        self.signal_name_combobox.grid(row=7, column=1)
        self.signal_name_combobox.set("Ansauglufttemperatur")  # Setzen Sie den Standardwert

        # Button zum Aktualisieren des Signals
        ttk.Button(self.root, text="Update Signal", command=self.update_signal).grid(row=8, column=0, columnspan=2)

        # Matplotlib-Figure für die Anzeige des Signals
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2)

    def update_signal(self):
        # Holen Sie die eingegebenen Werte aus den Entry-Feldern
        duration = float(self.duration_entry.get())
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
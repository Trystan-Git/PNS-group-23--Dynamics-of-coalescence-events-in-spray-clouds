import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import pandas as pd
from lmfit import models
import csv

file_path = r"C:\Users\thijm\Documents\Video_droplets\nttm\50000fps_64micron_1mlperminute_1_vel_size2.csv"
scaling_fac = 3.85e-6

# Initialize your lists first so Python knows they exist
speed_px_per_s = []
r_area_px = []
r_vol_px = []
track_len = []
cx_mean_px = []
cy_mean_px = []

with open(file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    # 1. Grabs the first row as a list of headers
    column_headers = next(reader)

    # 2. Loop through the READER, not the file. 
    # 'row' is already automatically split into a list of strings by the commas!
    for row in reader:
        # Convert data to float and append to lists
        speed_px_per_s.append(float(row[0]))
        r_area_px.append(float(row[1]))
        r_vol_px.append(float(row[2]))
        track_len.append(float(row[3]))
        cx_mean_px.append(float(row[4]))
        cy_mean_px.append(float(row[5]))

print("Columns:", column_headers)

speed_m_per_sec= np.array(speed_px_per_s) * scaling_fac

speed_tot = np.average(speed_m_per_sec)

print(speed_tot)

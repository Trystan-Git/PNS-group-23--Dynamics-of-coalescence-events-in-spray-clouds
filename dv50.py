import math
import matplotlib.pyplot as plt
import numpy as np 

#alle parameter waardes (dus hoogte/flowrate etc)
parameter = []

#Alle lijsten met dv50 per hoogte/flowrate/whatever
dv50 = [
    [],
    [],
    [],
    [],
    [],
]

#scatterplot maken
for parameter, dv50 in zip(parameter, dv50):
    for waarde in dv50:
        plt.scatter(parameter, waarde, color = "blue")

#plotten
plt.xlabel("Parameter")
plt.ylabel("Dv50")
plt.show()

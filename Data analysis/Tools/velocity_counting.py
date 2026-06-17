import matplotlib.pyplot as plt
import numpy as np

#Lijsten met frames die het kost voor druppels om een bepaalde pixel-afstand af te leggen:

#bestand 100fps:
frames_tot_aankomst_50fps = np.array([
    27, 25, 28, 28, 26, 30, 27, 27, 25, 26, 26, 27, 28, 27, 
    25, 27, 29, 28, 25, 25, 27, 28, 27, 27, 27, 27, 27, 28, 
    26, 29, 27, 25, 27, 30, 27, 30, 26, 26, 27, 26, 26, 26, 
    28, 29, 26, 28, 27, 27, 28, 28, 27, 28, 26, 25, 26, 27
])
#bestand 50fps:
frames_tot_aankomst_100fps = np.array([
    25, 24, 25, 25, 24, 25, 25, 24, 24, 24, 24, 24, 24, 24, 
    24, 25, 24, 24, 24, 25, 24, 24, 25, 25, 26, 25, 24, 25, 
    24, 25, 24, 24, 25, 24, 25, 24, 24, 24, 24, 25, 24, 23, 
    25
])

#snelheid berekenen (de teller getallen zijn van te voren berekend, wetende dat 1 pixel = 3.912 * 10**-6 m, het aantal fps van het bestand en de pixel-afstand)
snelheid_50fps = 125.5752 / frames_tot_aankomst_50fps
snelheid_100fps = 424.452 / frames_tot_aankomst_100fps

#iedere snelheid, gemiddelde snelheid en standaarddeviatie printen:
print(snelheid_50fps)
print(snelheid_100fps)

print(np.mean(snelheid_50fps))
print(np.mean(snelheid_100fps))

print(np.std(snelheid_50fps))
print(np.std(snelheid_100fps))

import matplotlib.pyplot as plt
import numpy as np

#parameter invullen (hoogte of flowrate of wat dan ook)
parameter = [5, 10, 15, 20, 25, 30]

#waarde invullen (in dit geval d[4][3], kan ook iets anders zijn)
d43 = [
    [215.250701904, 207.690261841, 210.522613525],
    [246.732009888, 254.487854004, 491.828399658],
    [271.026489258, 265.640197754, 259.53717041],
    [303.691589355, 305.189880371, 314.244476318],
    [318.642669678, 341.954376221, 338.040924072],
    [361.928710938, 356.186828613, 360.57220459]
]

#de fout op iedere waarde hier in de lijsten zetten
d43_fout = [
    [35.1771659851, 45.2812614441, 32.5582427979],
    [31.3087768555, 34.9372062683, 83.3335037231],
    [29.908706665, 33.8166351318, 29.2559127808],
    [41.075302124, 40.7919464111, 40.9451980591],
    [44.2761497498, 44.4484901428, 43.842792511],
    [42.9053230286, 42.3033676147, 44.9048728943],
]

#Iedere meting met eigen foutbalk plotten
for p, waardes, fouten in zip(parameter, d43, d43_fout):
    for waarde, fout in zip(waardes, fouten):
        plt.errorbar(
            p,
            waarde,
            yerr=fout,
            fmt='o',
            color='blue',
            ecolor='black',
            capsize=5
        )

#Alle meetpunten verzamelen
x = []
y = []

for p, waardes in zip(parameter, d43):
    for waarde in waardes:
        x.append(p)
        y.append(waarde)

#Lineaire fit
coefs = np.polyfit(x, y, 1)
fit = np.poly1d(coefs)

#x-waarden voor de fitlijn
x_fit = np.linspace(0, max(parameter), 100)
y_fit = fit(x_fit)

plt.title("Height of spray vs droplet diameter")
plt.xlabel("Height (cm)")
plt.ylabel("Diameter D[4][3] (µm)")
plt.plot(x_fit, y_fit, color="red", label="Lineaire fit")
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.grid()
plt.show()

#fit vergelijking
print(f"y = {coefs[0]:.3f} x + {coefs[1]:.3f}")
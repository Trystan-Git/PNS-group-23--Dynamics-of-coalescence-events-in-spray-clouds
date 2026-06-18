import matplotlib.pyplot as plt
import numpy as np 

#parameter invullen (hoogte of flowrate of wat dan ook)
parameter = []

#waarde invullen (in dit geval d[4][3], kan ook iets anders zijn)
d43 = [
    [],
    [],
    [],
    [],
    [],
    [],
    [215.250701904, 207.690261841, 210.522613525],
    [246.732009888, 254.487854004, 491.828399658],
    [271.026489258, 265.640197754, 259.53717041],
    [303.691589355, 305.189880371, 314.244476318],
    [318.642669678, 341.954376221, 338.040924072],
    [361.928710938, 356.186828613, 360.57220459],
]

#de fout op iedere waarde hier in de lijsten zetten
d43_fout = [
    [],
    [],
    [],
    [],
    [],
    [],
    [35.1771659851, 45.2812614441, 32.5582427979],
    [31.3087768555, 34.9372062683, 83.3335037231],
    [29.908706665, 33.8166351318, 29.2559127808],
    [41.075302124, 40.7919464111, 40.9451980591],
    [44.2761497498, 44.4484901428, 43.842792511],
    [42.9053230286, 42.3033676147, 44.9048728943],
]

#hier berekent de code het gemiddelde per waarde en de foutbalken van die gemiddeldes (dus niet iets in die lijsten zetten)
gemiddelde_d43 = []
foutbalken = []

for waardes, fouten in zip(d43, d43_fout):
    gemiddelde = np.mean(waardes)
    fout_op_gemiddelde = np.sqrt(np.sum(np.array(fouten)**2)) / len(fouten)

    gemiddelde_d43.append(gemiddelde)
    foutbalken.append(fout_op_gemiddelde)

#alle losse meetpunten plotten
for p, waardes_bij_p in zip(parameter, d43):
    for waarde in waardes_bij_p:
        plt.scatter(p, waarde, color="blue")

#gemiddelde met foutbalken plotten
plt.errorbar(
    parameter,
    gemiddelde_d43,
    yerr=foutbalken,
    fmt="o",
    color="black",
    ecolor="black",
    capsize=5,
    label="Gemiddelde d43"
)

#labels
plt.title("Hoogte tot spray vs gemiddelde diameter")
plt.xlabel("Hoogte (cm)")
plt.ylabel("Gemiddelde diameter d43 (µm)")
plt.ylim(bottom=0)
plt.legend()
plt.show()

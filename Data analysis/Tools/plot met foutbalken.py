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
]

#de fout op iedere waarde hier in de lijsten zetten
d43_fout = [
    [],
    [],
    [],
    [],
    [],
    [],
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

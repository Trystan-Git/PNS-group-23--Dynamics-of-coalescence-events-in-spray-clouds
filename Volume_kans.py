import sys
print(sys.executable)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm

#DEZE CODE GAAT UIT VAN EEN LOGNORMALE VERDELING VAN DE DRUPPELS.

#Bestand inlezen

file = "5juntest.txt"

data = pd.read_csv(
    file,
    na_values=["", "---"],
    encoding="latin1"
)

print("Eerste regels:")
print(data.head())

print("\nEerste 40 kolommen:")
print(data.columns[:40])


#Relevante kolommen kiezen

spray = data[[
    "T",
    "Ts",
    "Sequence",
    "Trans(Value)",
    "Dv(10)(Value)",
    "Dv(50)(Value)",
    "Dv(90)(Value)",
    "D[4][3](Value)",
    "D[3][2](Value)",
    "Cv(Value)",
    "Span(Value)",
    "%V < 10µ(Value)",
    "%V < 100µ(Value)"
]].copy()

#kolommen hernoemen

spray = spray.rename(columns={
    "Trans(Value)": "Transmission",
    "Dv(10)(Value)": "Dv10",
    "Dv(50)(Value)": "Dv50",
    "Dv(90)(Value)": "Dv90",
    "D[4][3](Value)": "D43",
    "D[3][2](Value)": "D32",
    "Cv(Value)": "Cv",
    "Span(Value)": "Span",
    "%V < 10µ(Value)": "V_less_10um_percent",
    "%V < 100µ(Value)": "V_less_100um_percent"
})

#Diameter naar volume omzetten

spray["V10"] = np.pi / 6 * spray["Dv10"]**3
spray["V50"] = np.pi / 6 * spray["Dv50"]**3
spray["V90"] = np.pi / 6 * spray["Dv90"]**3
spray["V43"] = np.pi / 6 * spray["D43"]**3



#Grensvolume kiezen om druppelvolumes mee te vergelijken

# Vul hier de echte nozzle-diameter in µm in (vermenigvuldigd door drie)
D_nozzle = 3 *210

V_nozzle = np.pi / 6 * D_nozzle**3
V_grens = 2 * V_nozzle

D_grens = (6 * V_grens / np.pi)**(1/3)

print("\nNozzle diameter:", D_nozzle, "µm")
print("Nozzle volume:", V_nozzle, "µm³")
print("Grensvolume:", V_grens, "µm³")
print("Grensdiameter:", D_grens, "µm")

#Logaritmisch model maken (en met z10 en z90 kijken hoe breed de verdeling is)

z10 = norm.ppf(0.10)
z90 = norm.ppf(0.90)

spray["mu_logD"] = np.log(spray["Dv50"])
spray["sigma_logD"] = (np.log(spray["Dv90"]) - np.log(spray["Dv10"])) / (z90 - z10)

#Kans dat V > V_grens berekenen

spray["P_larger_than_grens"] = 1 - lognorm.cdf(D_grens, s=spray["sigma_logD"], scale=np.exp(spray["mu_logD"]))

gemiddelde_kans = spray["P_larger_than_grens"].mean()

print("\nGemiddelde kans op V > V_grens:")
print(gemiddelde_kans)

#Plotjes

plt.plot(spray["Ts"], spray["P_larger_than_grens"])
plt.xlabel("Tijd binnen meting, Ts")
plt.ylabel("P(V > V_grens)")
plt.title("Geschatte kans op druppels groter dan grensvolume")
plt.grid(True)
plt.show()

plt.plot(spray["Ts"], spray["Dv50"])
plt.xlabel("Tijd binnen meting, Ts")
plt.ylabel("Dv50 (µm)")
plt.title("Mediane druppeldiameter door de tijd")
plt.grid(True)
plt.show()

#Opslaan resultaten

spray.to_csv("spray_analyse_resultaten.csv", index=False)

print("\nResultaten opgeslagen als spray_analyse_resultaten.csv")


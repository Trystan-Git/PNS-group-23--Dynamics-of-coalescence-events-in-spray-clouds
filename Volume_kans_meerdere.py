#DIT IS WEER DE LOGNORMALE CODE MAAR DAN VOOR MEERDERE BESTANDEN.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm
from pathlib import Path

#Map waarin je .txt-bestanden staan 
data_map = Path("1750_210") 

#Alle .txt-bestanden in de map zoeken 
bestanden = sorted(data_map.glob("*.txt"))

# Vul hier de grensdiameter in
D_grens = 420

print("Grensdiameter D_grens =", D_grens, "µm")

#Functie voor één bestand

def analyseer_bestand(bestand):
    print(f"Bezig met: {bestand.name}")

    data = pd.read_csv(
        bestand,
        na_values=["", "---"],
        encoding="latin1"
    )

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
        "Span(Value)"
    ]].copy()

    spray = spray.rename(columns={
        "Trans(Value)": "Transmission",
        "Dv(10)(Value)": "Dv10",
        "Dv(50)(Value)": "Dv50",
        "Dv(90)(Value)": "Dv90",
        "D[4][3](Value)": "D43",
        "D[3][2](Value)": "D32",
        "Cv(Value)": "Cv",
        "Span(Value)": "Span"
    })

    #Numeriek maken
    numerieke_kolommen = [
        "Ts", "Sequence", "Transmission",
        "Dv10", "Dv50", "Dv90", "D43", "D32", "Cv", "Span"
    ]

    for col in numerieke_kolommen:
        spray[col] = pd.to_numeric(spray[col], errors="coerce")

    #Ongeldige rijen verwijderen
    spray = spray.dropna(subset=["Ts", "Dv10", "Dv50", "Dv90"])
    spray = spray[(spray["Dv10"] > 0) & (spray["Dv50"] > 0) & (spray["Dv90"] > 0)].copy()

    if len(spray) == 0:
        raise ValueError(f"Geen geldige data over in bestand: {bestand.name}")

    #Relatieve tijd maken voor plots
    spray["tijd_s"] = spray["Ts"] - spray["Ts"].iloc[0]
    spray["tijd_ms"] = spray["tijd_s"] * 1000

    #Logaritmisch maken

    z10 = norm.ppf(0.10)
    z90 = norm.ppf(0.90)

    spray["mu_logD"] = np.log(spray["Dv50"])
    spray["sigma_logD"] = (np.log(spray["Dv90"]) - np.log(spray["Dv10"])) / (z90 - z10)

    #Kans dat diameter groter is dan D_grens
    spray["P_D_groter_dan_grens"] = 1 - lognorm.cdf(D_grens, s=spray["sigma_logD"], scale=np.exp(spray["mu_logD"]))

    # Extra info toevoegen
    spray["bestand"] = bestand.name
    spray["D_grens"] = D_grens

    return spray

#Alle bestanden analyseren

alle_resultaten = []

for bestand in bestanden:
    try:
        resultaat = analyseer_bestand(bestand)
        alle_resultaten.append(resultaat)
    except Exception as e:
        print(f"Fout bij bestand {bestand.name}: {e}")

resultaten = pd.concat(alle_resultaten, ignore_index=True)

#Samenvatting per bestand

samenvatting = resultaten.groupby("bestand").agg(
    aantal_records=("P_D_groter_dan_grens", "count"),
    gemiddelde_kans=("P_D_groter_dan_grens", "mean"),
    min_kans=("P_D_groter_dan_grens", "min"),
    max_kans=("P_D_groter_dan_grens", "max"),
    gemiddelde_Dv10=("Dv10", "mean"),
    gemiddelde_Dv50=("Dv50", "mean"),
    gemiddelde_Dv90=("Dv90", "mean"),
    gemiddelde_D43=("D43", "mean"),
    #gemiddelde_Span=("Span", "mean"),
    #gemiddelde_Transmission=("Transmission", "mean")
).reset_index()

print("\n--- Samenvatting per bestand ---")
print(samenvatting)

#Gemiddelde Dv50 over alle bestanden samen
gemiddelde_Dv50_folder = samenvatting["gemiddelde_Dv50"].mean()

print("\n--- Gemiddelde Dv50 voor deze folder ---")
print(f"Gemiddelde Dv50 over alle bestanden = {gemiddelde_Dv50_folder:.2f} µm")

#Lijst met gemiddelde Dv50 per bestand
lijst_Dv50 = samenvatting["gemiddelde_Dv50"].tolist()

print("\n--- Dv50 lijst per bestand ---")
print("Dv50 =", lijst_Dv50)

#gemiddelde kans over alle bestanden samen

gemiddelde_kans_totaal = resultaten["P_D_groter_dan_grens"].mean()
print(f"Gemiddelde P(D > {D_grens} µm) over alles = {gemiddelde_kans_totaal:.4f}")

#Resultaten opslaan

resultaten.to_csv("lognormaal_diameter_kans_alle_bestanden.csv", index=False)
samenvatting.to_csv("lognormaal_diameter_kans_samenvatting.csv", index=False)

print("\nOpgeslagen:")
print("- lognormaal_diameter_kans_alle_bestanden.csv")
print("- lognormaal_diameter_kans_samenvatting.csv")

#gemiddelde kans per bestand plot

plt.bar(samenvatting["bestand"], samenvatting["gemiddelde_kans"])
plt.xlabel("Bestand")
plt.ylabel(f"Gemiddelde P(D > {D_grens} µm)")
plt.title(f"Gemiddelde kans per bestand voor D > {D_grens} µm")
plt.xticks(rotation=45, ha="right")
plt.grid(True, axis="y")
plt.tight_layout()
plt.show()
import folium
import numpy as np

ventes["map_color"] = pd.qcut(
    ventes["valeur_fonciere"], [0, 0.8, 1], labels=["lightblue", "red"]
)
ventes["icon"] = np.where(ventes["type_local"] == "Maison", "home", "")
ventes["num_voie_clean"] = np.where(
    ventes["numero_voie"].isnull(), "", ventes["numero_voie"]
)
ventes["text"] = ventes.apply(
    lambda s: "Adresse: {num} {voie} <br>Vente en {annee} <br>Prix {prix:.0f} €".format(
        num=s["num_voie_clean"],
        voie=s["voie"],
        annee=s["date_mutation"].split("-")[0],
        prix=s["valeur_fonciere"],
    ),
    axis=1,
)

center = ventes[["lat", "lon"]].mean().values.tolist()
sw = ventes[["lat", "lon"]].min().values.tolist()
ne = ventes[["lat", "lon"]].max().values.tolist()

m = folium.Map(location=center, tiles="OpenStreetMap")

# I can add marker one by one on the map
for i in range(0, len(ventes)):
    folium.Marker(
        [ventes.iloc[i]["lat"], ventes.iloc[i]["lon"]],
        popup=ventes.iloc[i]["text"],
        icon=folium.Icon(
            color=ventes.iloc[i]["map_color"], icon=ventes.iloc[i]["icon"]
        ),
    ).add_to(m)

m.fit_bounds([sw, ne])

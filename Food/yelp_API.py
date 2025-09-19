import requests
import pandas as pd
import time

API_KEY = "-1QD5AKvLDLywVP1yPxw1vxZu8xmWhUz7hjkEfN8nrldAuIS1Ql3sLtlXfsVTFGmdSlDm6XMKm3k-0yAgKY99LUtmv-Xlicx38aWXnFRFo-IJItFyjfT_mgoDRzNaHYx"
ENDPOINT = "https://api.yelp.com/v3/businesses/search"
headers = {"Authorization": f"Bearer {API_KEY}"}

all_restaurants = []

# Paris = arrondissements 75001 à 75020
arrondissements = [f"750{str(i).zfill(2)}" for i in range(1, 21)]

for arr in arrondissements:
    print(f"Récupération des restos de l'arrondissement {arr}...")
    for offset in range(0, 150, 50):  # max 1000 résultats par arrondissement
        params = {
            "term": "restaurant",
            "location": arr + " Paris",
            "limit": 50,
            "offset": offset
        }
        response = requests.get(ENDPOINT, headers=headers, params=params)
        print(response.status_code)
        data = response.json()
        businesses = data.get("businesses", [])
        if not businesses:
            print("  Aucun résultat trouvé.")
            break  # plus de résultats dans cet arrondissement
        all_restaurants.extend(businesses)
        time.sleep(0.5)  # éviter de spammer l'API

# Convertir en DataFrame
restaurants_data = pd.DataFrame([
    {
        "nom": b["name"],
        "note": b["rating"],
        "prix": b.get("price", "N/A"),
        "categories": ", ".join([c["title"] for c in b["categories"]]),
        "adresse": " ".join(b["location"]["display_address"]),
        "latitude": b["coordinates"]["latitude"],
        "longitude": b["coordinates"]["longitude"]
    }
    for b in all_restaurants
])
restaurants_data.drop_duplicates(subset=["nom"], inplace=True)
print(f"{len(restaurants_data)} restaurants récupérés au total")
restaurants_data.to_csv("restaurants_paris_complet.csv", index=False, encoding="utf-8")
import requests
import pandas as pd
import time

API_KEY = "-1QD5AKvLDLywVP1yPxw1vxZu8xmWhUz7hjkEfN8nrldAuIS1Ql3sLtlXfsVTFGmdSlDm6XMKm3k-0yAgKY99LUtmv-Xlicx38aWXnFRFo-IJItFyjfT_mgoDRzNaHYx"
ENDPOINT = "https://api.yelp.com/v3/businesses/search"

headers = {"Authorization": f"Bearer {API_KEY}"}

all_restaurants = []

# Exemple : Paris (peut remplacer par "Lyon", "Marseille", etc.)
location = "Paris"

for offset in range(0, 190, 50):  # Yelp max = 1000 résultats
    params = {
        "term": "restaurant",
        "location": location,
        "limit": 50,
        "offset": offset
    }
    response = requests.get(ENDPOINT, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        businesses = data.get("businesses", [])
        if not businesses:
            break  # plus de résultats
        all_restaurants.extend(businesses)
    else:
        print("Erreur:", response.status_code, response.text)
        break

    time.sleep(0.5)  # éviter de spammer l’API

# Convertir en DataFrame
restaurants_data = []
for biz in all_restaurants:
    restaurants_data.append({
        "nom": biz["name"],
        "note": biz["rating"],
        "prix": biz.get("price", "N/A"),
        "categories": ", ".join([c["title"] for c in biz["categories"]]),
        "adresse": " ".join(biz["location"]["display_address"]),
        "latitude": biz["coordinates"]["latitude"],
        "longitude": biz["coordinates"]["longitude"]
    })

df = pd.DataFrame(restaurants_data)

# Sauvegarde locale
df.to_csv("restaurants_paris.csv", index=False, encoding="utf-8")
print(f"{len(df)} restaurants sauvegardés dans restaurants_paris.csv")
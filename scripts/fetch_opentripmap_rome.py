import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENTRIPMAP_API_KEY")

if not API_KEY:
    raise ValueError("OPENTRIPMAP_API_KEY .env dosyasında bulunamadı.")

ROME_LAT = 41.9028
ROME_LON = 12.4964
RADIUS = 8000
LIMIT = 100

BASE_URL = "https://api.opentripmap.com/0.1/en/places/radius"


def fetch_rome_places():
    params = {
    "radius": RADIUS,
    "lon": ROME_LON,
    "lat": ROME_LAT,
    "limit": 500,
    "format": "json",
    "apikey": API_KEY,
    "rate": 3,
    "kinds": "interesting_places,historic,architecture,museums,cultural,religion,natural"
}

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    return response.json()


def normalize_places(places):
    rows = []

    for place in places:
        point = place.get("point", {})

        rows.append({
    "source_opentripmap_id": place.get("xid"),
    "location_name": place.get("name"),
    "normalized_name": str(place.get("name", "")).lower().strip(),
    "city": "Rome",
    "country": "Italy",
    "category_raw": place.get("kinds"),
    "latitude": point.get("lat"),
    "longitude": point.get("lon"),
    "opentripmap_rate": place.get("rate"),
    "popularity_score": place.get("rate"),
    "source_wikidata_id": place.get("wikidata"),
    "source_osm_id": place.get("osm"),
    "data_source": "OpenTripMap"
})

    return pd.DataFrame(rows)


def main():
    places = fetch_rome_places()
    df = normalize_places(places)

    df = df[df["location_name"].notna()]
    df = df[df["location_name"].str.strip() != ""]

    output_path = "datasets/raw/rome/opentripmap_rome_raw.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"{len(df)} lokasyon çekildi.")
    print(f"Dosya oluşturuldu: {output_path}")
    print(df.head(10))


if __name__ == "__main__":
    main()
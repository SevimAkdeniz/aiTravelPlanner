import os
import re
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from rapidfuzz import fuzz

load_dotenv()

API_KEY = os.getenv("OPENTRIPMAP_API_KEY")

INPUT_PATH = "datasets/master/rome_master_dataset_v1_enriched.csv"
OUTPUT_CSV_PATH = "datasets/master/rome_master_dataset_v1_enriched_by_name.csv"
OUTPUT_XLSX_PATH = "datasets/master/rome_master_dataset_v1_enriched_by_name.xlsx"

ROME_LAT = 41.9028
ROME_LON = 12.4964
RADIUS = 20000

AUTOSUGGEST_URL = "https://api.opentripmap.com/0.1/en/places/autosuggest"

ALIASES = {
    "Palatine Hill": ["Palatine Hill", "Palatino", "Palatine"],
    "Pantheon": ["Pantheon", "Pantheon Rome"],
    "Piazza Navona": ["Piazza Navona"],
    "Vatican Museums": ["Vatican Museums", "Musei Vaticani"],
    "St. Peter's Basilica": ["St. Peter's Basilica", "Saint Peter's Basilica", "Basilica di San Pietro"],
    "Sistine Chapel": ["Sistine Chapel", "Cappella Sistina"],
    "Castel Sant'Angelo": ["Castel Sant'Angelo", "Mausoleum of Hadrian"],
    "Capitoline Museums": ["Capitoline Museums", "Musei Capitolini"],
    "Campo de' Fiori": ["Campo de' Fiori", "Campo de Fiori"],
    "Trastevere": ["Trastevere"],
    "Piazza del Popolo": ["Piazza del Popolo"],
    "Baths of Caracalla": ["Baths of Caracalla", "Terme di Caracalla"],
    "Circus Maximus": ["Circus Maximus", "Circo Massimo"],
    "Ara Pacis": ["Ara Pacis", "Museo dell'Ara Pacis", "Museum of the Ara Pacis"],
    "MAXXI Museum": ["MAXXI", "MAXXI Museum", "Museo nazionale delle arti del XXI secolo"],
    "Janiculum Hill": ["Janiculum Hill", "Gianicolo", "Janiculum"],
    "Orange Garden": ["Orange Garden", "Giardino degli Aranci", "Parco Savello"],
    "Mouth of Truth": ["Mouth of Truth", "Bocca della Verità", "Bocca della Verita"],
    "Tiber Island": ["Tiber Island", "Isola Tiberina"],
    "Appian Way": ["Appian Way", "Via Appia Antica"],
    "Catacombs of San Callisto": ["Catacombs of San Callisto", "Catacombe di San Callisto"],
    "Basilica of Saint John Lateran": [
        "Basilica of Saint John Lateran",
        "Archbasilica of Saint John Lateran",
        "San Giovanni in Laterano",
        "Basilica di San Giovanni in Laterano",
    ],
        "Domus Aurea": ["Domus Aurea"],
    "Basilica of Saint Paul Outside the Walls": [
        "Basilica of Saint Paul Outside the Walls",
        "Basilica di San Paolo fuori le Mura",
        "San Paolo fuori le Mura",
    ],
    "Pincian Hill": ["Pincian Hill", "Pincio"],
    "Piazza della Rotonda": ["Piazza della Rotonda"],
    "Largo di Torre Argentina": ["Largo di Torre Argentina", "Torre Argentina"],
}


def normalize_name(value):
    if pd.isna(value):
        return ""

    value = str(value).lower().strip()
    value = value.replace("’", "'")
    value = value.replace("`", "'")
    value = value.replace("´", "'")
    value = value.replace(".", "")
    value = re.sub(r"\(.*?\)", "", value)
    value = re.sub(r"[^a-z0-9\s']", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def search_opentripmap(name):
    params = {
        "name": name,
        "radius": RADIUS,
        "lon": ROME_LON,
        "lat": ROME_LAT,
        "limit": 10,
        "format": "json",
        "apikey": API_KEY,
    }

    response = requests.get(AUTOSUGGEST_URL, params=params)
    response.raise_for_status()
    return response.json()


def choose_best_result(location_name, results):
    best = None
    best_score = 0

    target = normalize_name(location_name)

    for item in results:
        item_name = normalize_name(item.get("name", ""))

        if not item_name:
            continue

        score = fuzz.token_sort_ratio(target, item_name)

        if score > best_score:
            best_score = score
            best = item

    return best, best_score


def update_row_from_otm(row, item, score):
    point = item.get("point", {})

    row["source_opentripmap_id"] = item.get("xid", "")
    row["source_osm_id"] = item.get("osm", "")
    row["source_wikidata_id"] = item.get("wikidata", "")
    row["latitude"] = point.get("lat", "")
    row["longitude"] = point.get("lon", "")
    row["category_raw"] = item.get("kinds", "")
    row["opentripmap_rate"] = item.get("rate", "")
    row["popularity_score"] = item.get("rate", "")
    row["data_source"] = "OpenTripMap"
    row["opentripmap_match_name"] = item.get("name", "")
    row["opentripmap_match_score"] = score

    if score >= 95:
        row["opentripmap_match_status"] = "strong_match"
    elif score >= 80:
        row["opentripmap_match_status"] = "possible_match"
    else:
        row["opentripmap_match_status"] = "not_matched"

    return row


def main():
    if not API_KEY:
        raise ValueError("OPENTRIPMAP_API_KEY .env içinde yok.")

    df = pd.read_csv(INPUT_PATH)

    updated_rows = []

    for _, row in df.iterrows():
        row = row.copy()
        location_name = row["location_name"]
        current_status = row.get("opentripmap_match_status", "")

        # Strong match ise dokunma
        if current_status == "strong_match":
            updated_rows.append(row)
            continue

        # Yanlış possible matchleri temizle
        row["source_opentripmap_id"] = ""
        row["source_osm_id"] = ""
        row["source_wikidata_id"] = ""
        row["category_raw"] = ""
        row["opentripmap_rate"] = ""
        row["popularity_score"] = ""
        row["data_source"] = ""
        row["opentripmap_match_status"] = "not_matched"

        search_terms = ALIASES.get(location_name, [location_name])

        best_item = None
        best_score = 0

        for term in search_terms:
            try:
                results = search_opentripmap(term)
                item, score = choose_best_result(term, results)

                if item and score > best_score:
                    best_item = item
                    best_score = score

                time.sleep(0.2)

            except Exception as e:
                print(f"Hata: {location_name} / {term} -> {e}")

        if best_item and best_score >= 80:
            row = update_row_from_otm(row, best_item, best_score)

        updated_rows.append(row)

    out_df = pd.DataFrame(updated_rows)

    out_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8-sig")
    out_df.to_excel(OUTPUT_XLSX_PATH, index=False)

    print("İsim bazlı OpenTripMap araması tamamlandı.")
    print(f"CSV çıktı: {OUTPUT_CSV_PATH}")
    print(f"Excel çıktı: {OUTPUT_XLSX_PATH}")

    print("\nKontrol tablosu:")
    print(
        out_df[
            [
                "location_name",
                "opentripmap_match_name",
                "opentripmap_match_score",
                "opentripmap_match_status",
                "source_opentripmap_id",
                "source_wikidata_id",
            ]
        ].to_string(index=False)
    )

    print("\nÖzet:")
    print(out_df["opentripmap_match_status"].value_counts())


if __name__ == "__main__":
    main()
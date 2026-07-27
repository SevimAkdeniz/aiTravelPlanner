import os
import pandas as pd


OUTPUT_PATH = "datasets/master/rome_master_dataset_v1_locations_placed.csv"


ROME_LOCATIONS = [
    "Colosseum",
    "Roman Forum",
    "Palatine Hill",
    "Pantheon",
    "Trevi Fountain",
    "Spanish Steps",
    "Piazza Navona",
    "Vatican Museums",
    "St. Peter's Basilica",
    "Sistine Chapel",
    "Castel Sant'Angelo",
    "Villa Borghese",
    "Borghese Gallery",
    "Capitoline Museums",
    "Altare della Patria",
    "Campo de' Fiori",
    "Trastevere",
    "Piazza Venezia",
    "Piazza del Popolo",
    "Basilica of Saint Mary Major",
    "Baths of Caracalla",
    "Circus Maximus",
    "Trajan's Market",
    "Ara Pacis",
    "Doria Pamphilj Gallery",
    "MAXXI Museum",
    "National Roman Museum",
    "Piazza Barberini",
    "Quirinal Palace",
    "Janiculum Hill",
    "Orange Garden",
    "Mouth of Truth",
    "Tiber Island",
    "Appian Way",
    "Catacombs of San Callisto",
    "Basilica of Saint John Lateran",
    "Basilica of Saint Paul Outside the Walls",
    "Pincian Hill",
"Domus Aurea",    "Largo di Torre Argentina",
]


def normalize_name(name):
    return (
        name.lower()
        .replace(".", "")
        .replace("'", "")
        .replace("’", "")
        .strip()
    )


def main():
    rows = []

    for index, name in enumerate(ROME_LOCATIONS, start=1):
        rows.append({
            "location_id": index,
            "location_name": name,
            "normalized_name": normalize_name(name),
            "city": "Rome",
            "country": "Italy",
        })

    df = pd.DataFrame(rows)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("40 lokasyonluk master başlangıç dosyası oluşturuldu.")
    print(f"Dosya yolu: {OUTPUT_PATH}")
    print(f"Toplam lokasyon: {len(df)}")
    print(df)


if __name__ == "__main__":
    main()
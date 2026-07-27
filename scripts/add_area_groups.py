import os
import pandas as pd


INPUT_PATH = "datasets/master/rome_location_scores_sample.csv"

OUTPUT_CSV_PATH = "datasets/master/rome_location_scores_with_area.csv"
OUTPUT_XLSX_PATH = "datasets/master/rome_location_scores_with_area.xlsx"


AREA_GROUPS = {
    # Vatican / nehir hattı
    "St. Peter's Basilica": "vatican_area",
    "Vatican Museums": "vatican_area",
    "Sistine Chapel": "vatican_area",
    "Castel Sant'Angelo": "vatican_area",

    # Antik Roma hattı
    "Colosseum": "ancient_rome",
    "Roman Forum": "ancient_rome",
    "Palatine Hill": "ancient_rome",
    "Circus Maximus": "ancient_rome",
    "Baths of Caracalla": "ancient_rome",
    "Domus Aurea": "ancient_rome",
    "Trajan's Market": "ancient_rome",
    "Altare della Patria": "ancient_rome",
    "Largo di Torre Argentina": "ancient_rome",

    # Tarihi merkez
    "Pantheon": "historic_center",
    "Trevi Fountain": "historic_center",
    "Spanish Steps": "historic_center",
    "Piazza Navona": "historic_center",
    "Campo de' Fiori": "historic_center",
    "Piazza Venezia": "historic_center",
    "Piazza Barberini": "historic_center",
    "Piazza del Popolo": "historic_center",
    "Pincian Hill": "historic_center",
    "Piazza della Rotonda": "historic_center",

    # Trastevere / güneybatı
    "Trastevere": "trastevere_area",
    "Tiber Island": "trastevere_area",
    "Mouth of Truth": "trastevere_area",
    "Orange Garden": "trastevere_area",
    "Janiculum Hill": "trastevere_area",

    # Müze / kuzey
    "Villa Borghese": "borghese_north",
    "Borghese Gallery": "borghese_north",
    "MAXXI Museum": "borghese_north",

    # Bazilikalar / dış rota
    "Basilica of Saint Mary Major": "basilica_route",
    "Basilica of Saint John Lateran": "basilica_route",
    "Basilica of Saint Paul Outside the Walls": "basilica_route",

    # Şehir dışı / özel rota
    "Appian Way": "appian_way_area",
    "Catacombs of San Callisto": "appian_way_area",

    # Müze / merkez
    "Capitoline Museums": "ancient_rome",
    "Ara Pacis": "historic_center",
    "Doria Pamphilj Gallery": "historic_center",
    "National Roman Museum": "basilica_route",
    "Quirinal Palace": "historic_center",
}


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    df["area_group"] = df["location_name"].map(AREA_GROUPS).fillna("other")

    df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8-sig")
    df.to_excel(OUTPUT_XLSX_PATH, index=False)

    print("Area group kolonları eklendi.")
    print(f"CSV çıktı: {OUTPUT_CSV_PATH}")
    print(f"Excel çıktı: {OUTPUT_XLSX_PATH}")

    print("\nArea group özeti:")
    print(df["area_group"].value_counts())

    print("\nKontrol:")
    print(
        df[
            [
                "location_name",
                "category",
                "area_group",
                "suitability_score",
                "average_visit_duration_min",
            ]
        ].sort_values(["area_group", "suitability_score"], ascending=[True, False]).to_string(index=False)
    )


if __name__ == "__main__":
    main()
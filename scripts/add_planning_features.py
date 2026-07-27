import os
import pandas as pd


INPUT_PATH = "datasets/master/rome_master_dataset_v1_final.csv"

OUTPUT_CSV_PATH = "datasets/master/rome_master_dataset_v1_planning_ready.csv"
OUTPUT_XLSX_PATH = "datasets/master/rome_master_dataset_v1_planning_ready.xlsx"


DEFAULT_VALUES = {
    "category": "sightseeing",
    "sub_category": "",
    "description": "",
    "indoor_outdoor": "outdoor",
    "average_visit_duration_min": 90,
    "min_visit_duration_min": 45,
    "max_visit_duration_min": 120,
    "recommended_visit_time": "any",
    "reservation_required": False,
    "is_family_friendly": True,
    "opening_hours_raw": "",
    "opening_time": "",
    "closing_time": "",
    "open_days": "Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    "closed_days": "",
    "is_open_24h": False,
    "entry_fee_adult": 0,
    "entry_fee_student": 0,
    "currency": "EUR",
    "is_free": True,
    "budget_level": "free",
    "google_rating": "",
    "google_review_count": "",
    "tourist_importance_score": 7,
    "history_score": 5,
    "museum_score": 0,
    "art_score": 3,
    "architecture_score": 5,
    "photography_score": 6,
    "nature_score": 0,
    "gastronomy_score": 0,
    "shopping_score": 0,
    "religious_score": 0,
    "public_transport_score": 7,
    "walking_difficulty_score": 4,
    "weather_sensitivity": "medium",
    "good_for_rainy_weather": False,
    "good_for_hot_weather": True,
}


LOCATION_FEATURES = {
    "Colosseum": {
        "category": "historic",
        "sub_category": "amphitheatre",
        "indoor_outdoor": "outdoor",
        "average_visit_duration_min": 120,
        "entry_fee_adult": 18,
        "is_free": False,
        "budget_level": "medium",
        "reservation_required": True,
        "tourist_importance_score": 10,
        "history_score": 10,
        "architecture_score": 10,
        "photography_score": 10,
        "walking_difficulty_score": 6,
    },
    "Roman Forum": {
        "category": "historic",
        "sub_category": "archaeological_site",
        "indoor_outdoor": "outdoor",
        "average_visit_duration_min": 120,
        "entry_fee_adult": 18,
        "is_free": False,
        "budget_level": "medium",
        "tourist_importance_score": 10,
        "history_score": 10,
        "architecture_score": 8,
        "photography_score": 9,
        "walking_difficulty_score": 7,
    },
    "Palatine Hill": {
        "category": "historic",
        "sub_category": "archaeological_site",
        "indoor_outdoor": "outdoor",
        "average_visit_duration_min": 90,
        "entry_fee_adult": 18,
        "is_free": False,
        "budget_level": "medium",
        "tourist_importance_score": 9,
        "history_score": 10,
        "nature_score": 5,
        "photography_score": 8,
        "walking_difficulty_score": 7,
    },
    "Pantheon": {
        "category": "historic",
        "sub_category": "temple_church",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 45,
        "entry_fee_adult": 5,
        "is_free": False,
        "budget_level": "low",
        "tourist_importance_score": 10,
        "history_score": 9,
        "architecture_score": 10,
        "religious_score": 6,
        "photography_score": 9,
        "good_for_rainy_weather": True,
    },
    "Trevi Fountain": {
        "category": "landmark",
        "sub_category": "fountain",
        "indoor_outdoor": "outdoor",
        "average_visit_duration_min": 30,
        "entry_fee_adult": 0,
        "is_free": True,
        "budget_level": "free",
        "tourist_importance_score": 10,
        "architecture_score": 8,
        "photography_score": 10,
    },
    "Spanish Steps": {
        "category": "landmark",
        "sub_category": "stairs_square",
        "indoor_outdoor": "outdoor",
        "average_visit_duration_min": 45,
        "tourist_importance_score": 9,
        "architecture_score": 7,
        "photography_score": 9,
        "shopping_score": 7,
    },
    "Piazza Navona": {
        "category": "square",
        "sub_category": "historic_square",
        "indoor_outdoor": "outdoor",
        "average_visit_duration_min": 60,
        "tourist_importance_score": 10,
        "architecture_score": 9,
        "photography_score": 10,
        "gastronomy_score": 6,
    },
    "Vatican Museums": {
        "category": "museum",
        "sub_category": "art_museum",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 180,
        "entry_fee_adult": 20,
        "is_free": False,
        "budget_level": "medium",
        "reservation_required": True,
        "tourist_importance_score": 10,
        "museum_score": 10,
        "art_score": 10,
        "history_score": 8,
        "good_for_rainy_weather": True,
    },
    "St. Peter's Basilica": {
        "category": "religious",
        "sub_category": "basilica",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 90,
        "entry_fee_adult": 0,
        "is_free": True,
        "budget_level": "free",
        "tourist_importance_score": 10,
        "religious_score": 10,
        "architecture_score": 10,
        "history_score": 9,
        "photography_score": 9,
        "good_for_rainy_weather": True,
    },
    "Sistine Chapel": {
        "category": "religious",
        "sub_category": "chapel_art",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 45,
        "entry_fee_adult": 20,
        "is_free": False,
        "budget_level": "medium",
        "reservation_required": True,
        "tourist_importance_score": 10,
        "art_score": 10,
        "religious_score": 9,
        "museum_score": 8,
        "good_for_rainy_weather": True,
    },
    "Castel Sant'Angelo": {
        "category": "historic",
        "sub_category": "castle_museum",
        "indoor_outdoor": "mixed",
        "average_visit_duration_min": 90,
        "entry_fee_adult": 15,
        "is_free": False,
        "budget_level": "medium",
        "tourist_importance_score": 9,
        "history_score": 9,
        "museum_score": 6,
        "architecture_score": 8,
        "photography_score": 9,
    },
    "Villa Borghese": {
        "category": "park",
        "sub_category": "urban_park",
        "indoor_outdoor": "outdoor",
        "average_visit_duration_min": 90,
        "tourist_importance_score": 8,
        "nature_score": 10,
        "photography_score": 8,
        "is_free": True,
        "budget_level": "free",
    },
    "Borghese Gallery": {
        "category": "museum",
        "sub_category": "art_gallery",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 120,
        "entry_fee_adult": 15,
        "is_free": False,
        "budget_level": "medium",
        "reservation_required": True,
        "tourist_importance_score": 9,
        "museum_score": 10,
        "art_score": 10,
        "good_for_rainy_weather": True,
    },
    "Capitoline Museums": {
        "category": "museum",
        "sub_category": "history_art_museum",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 120,
        "entry_fee_adult": 16,
        "is_free": False,
        "budget_level": "medium",
        "tourist_importance_score": 8,
        "museum_score": 9,
        "art_score": 8,
        "history_score": 9,
        "good_for_rainy_weather": True,
    },
    "Altare della Patria": {
        "category": "monument",
        "sub_category": "national_monument",
        "indoor_outdoor": "outdoor",
        "average_visit_duration_min": 60,
        "tourist_importance_score": 9,
        "history_score": 8,
        "architecture_score": 9,
        "photography_score": 10,
    },
    "Campo de' Fiori": {
        "category": "square",
        "sub_category": "market_square",
        "average_visit_duration_min": 45,
        "tourist_importance_score": 7,
        "gastronomy_score": 8,
        "shopping_score": 6,
        "photography_score": 7,
    },
    "Trastevere": {
        "category": "district",
        "sub_category": "historic_neighbourhood",
        "average_visit_duration_min": 120,
        "recommended_visit_time": "evening",
        "tourist_importance_score": 9,
        "gastronomy_score": 10,
        "photography_score": 8,
        "history_score": 7,
    },
    "Piazza Venezia": {
        "category": "square",
        "sub_category": "central_square",
        "average_visit_duration_min": 45,
        "tourist_importance_score": 8,
        "architecture_score": 8,
        "photography_score": 8,
    },
    "Piazza del Popolo": {
        "category": "square",
        "sub_category": "historic_square",
        "average_visit_duration_min": 60,
        "tourist_importance_score": 8,
        "architecture_score": 8,
        "photography_score": 9,
    },
    "Basilica of Saint Mary Major": {
        "category": "religious",
        "sub_category": "basilica",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 60,
        "tourist_importance_score": 8,
        "religious_score": 10,
        "architecture_score": 9,
        "history_score": 8,
        "good_for_rainy_weather": True,
    },
    "Baths of Caracalla": {
        "category": "historic",
        "sub_category": "archaeological_site",
        "average_visit_duration_min": 90,
        "entry_fee_adult": 8,
        "is_free": False,
        "budget_level": "low",
        "tourist_importance_score": 8,
        "history_score": 9,
        "architecture_score": 8,
        "photography_score": 8,
    },
    "Circus Maximus": {
        "category": "historic",
        "sub_category": "ancient_stadium",
        "average_visit_duration_min": 45,
        "tourist_importance_score": 7,
        "history_score": 8,
        "photography_score": 7,
    },
    "Trajan's Market": {
        "category": "historic",
        "sub_category": "archaeological_museum",
        "average_visit_duration_min": 90,
        "entry_fee_adult": 15,
        "is_free": False,
        "budget_level": "medium",
        "tourist_importance_score": 8,
        "history_score": 9,
        "museum_score": 7,
        "architecture_score": 8,
    },
    "Ara Pacis": {
        "category": "museum",
        "sub_category": "historic_monument_museum",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 60,
        "entry_fee_adult": 10,
        "is_free": False,
        "budget_level": "low",
        "tourist_importance_score": 7,
        "history_score": 8,
        "museum_score": 7,
        "art_score": 7,
        "good_for_rainy_weather": True,
    },
    "Doria Pamphilj Gallery": {
        "category": "museum",
        "sub_category": "art_gallery",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 90,
        "entry_fee_adult": 16,
        "is_free": False,
        "budget_level": "medium",
        "tourist_importance_score": 7,
        "museum_score": 8,
        "art_score": 9,
        "good_for_rainy_weather": True,
    },
    "MAXXI Museum": {
        "category": "museum",
        "sub_category": "modern_art_museum",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 90,
        "entry_fee_adult": 12,
        "is_free": False,
        "budget_level": "medium",
        "tourist_importance_score": 7,
        "museum_score": 8,
        "art_score": 8,
        "architecture_score": 8,
        "good_for_rainy_weather": True,
    },
    "National Roman Museum": {
        "category": "museum",
        "sub_category": "archaeology_museum",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 120,
        "entry_fee_adult": 12,
        "is_free": False,
        "budget_level": "medium",
        "tourist_importance_score": 8,
        "museum_score": 9,
        "history_score": 9,
        "good_for_rainy_weather": True,
    },
    "Piazza Barberini": {
        "category": "square",
        "sub_category": "historic_square_fountain",
        "average_visit_duration_min": 30,
        "tourist_importance_score": 6,
        "architecture_score": 7,
        "photography_score": 7,
    },
    "Quirinal Palace": {
        "category": "palace",
        "sub_category": "government_palace",
        "average_visit_duration_min": 45,
        "tourist_importance_score": 7,
        "history_score": 7,
        "architecture_score": 8,
        "photography_score": 7,
    },
    "Janiculum Hill": {
        "category": "viewpoint",
        "sub_category": "hill_viewpoint",
        "average_visit_duration_min": 60,
        "recommended_visit_time": "sunset",
        "tourist_importance_score": 7,
        "nature_score": 6,
        "photography_score": 9,
        "walking_difficulty_score": 7,
    },
    "Orange Garden": {
        "category": "park",
        "sub_category": "viewpoint_garden",
        "average_visit_duration_min": 45,
        "recommended_visit_time": "sunset",
        "tourist_importance_score": 7,
        "nature_score": 8,
        "photography_score": 9,
    },
    "Mouth of Truth": {
        "category": "landmark",
        "sub_category": "historic_sculpture",
        "average_visit_duration_min": 30,
        "tourist_importance_score": 7,
        "history_score": 6,
        "photography_score": 8,
    },
    "Tiber Island": {
        "category": "landmark",
        "sub_category": "island",
        "average_visit_duration_min": 45,
        "tourist_importance_score": 6,
        "history_score": 6,
        "photography_score": 7,
    },
    "Appian Way": {
        "category": "historic",
        "sub_category": "ancient_road",
        "average_visit_duration_min": 120,
        "tourist_importance_score": 8,
        "history_score": 10,
        "nature_score": 6,
        "photography_score": 8,
        "walking_difficulty_score": 8,
    },
    "Catacombs of San Callisto": {
        "category": "historic",
        "sub_category": "catacombs",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 60,
        "entry_fee_adult": 10,
        "is_free": False,
        "budget_level": "low",
        "tourist_importance_score": 7,
        "history_score": 9,
        "religious_score": 7,
        "good_for_rainy_weather": True,
    },
    "Basilica of Saint John Lateran": {
        "category": "religious",
        "sub_category": "basilica",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 60,
        "tourist_importance_score": 8,
        "religious_score": 10,
        "architecture_score": 9,
        "history_score": 8,
        "good_for_rainy_weather": True,
    },
    "Basilica of Saint Paul Outside the Walls": {
        "category": "religious",
        "sub_category": "basilica",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 60,
        "tourist_importance_score": 7,
        "religious_score": 10,
        "architecture_score": 8,
        "history_score": 8,
        "good_for_rainy_weather": True,
    },
    "Pincian Hill": {
        "category": "viewpoint",
        "sub_category": "hill_viewpoint",
        "average_visit_duration_min": 45,
        "recommended_visit_time": "sunset",
        "tourist_importance_score": 7,
        "nature_score": 6,
        "photography_score": 9,
    },
    "Domus Aurea": {
        "category": "historic",
        "sub_category": "archaeological_site",
        "indoor_outdoor": "indoor",
        "average_visit_duration_min": 90,
        "entry_fee_adult": 16,
        "is_free": False,
        "budget_level": "medium",
        "reservation_required": True,
        "tourist_importance_score": 8,
        "history_score": 9,
        "architecture_score": 8,
        "museum_score": 5,
        "good_for_rainy_weather": True,
    },
    "Largo di Torre Argentina": {
        "category": "historic",
        "sub_category": "archaeological_square",
        "average_visit_duration_min": 45,
        "tourist_importance_score": 7,
        "history_score": 8,
        "photography_score": 7,
    },
}


def apply_default_values(df):
    for column, value in DEFAULT_VALUES.items():
        if column not in df.columns:
            df[column] = value
        else:
            df[column] = df[column].fillna(value)

    return df


def apply_location_features(df):
    for location_name, features in LOCATION_FEATURES.items():
        mask = df["location_name"] == location_name

        if not mask.any():
            print(f"Uyarı: {location_name} bulunamadı.")
            continue

        for column, value in features.items():
            df.loc[mask, column] = value

    return df


def calculate_budget_level(row):
    fee = row.get("entry_fee_adult", 0)

    try:
        fee = float(fee)
    except:
        fee = 0

    if fee == 0:
        return "free"
    elif fee <= 10:
        return "low"
    elif fee <= 25:
        return "medium"
    else:
        return "high"


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    df = apply_default_values(df)
    df = apply_location_features(df)

    df["budget_level"] = df.apply(calculate_budget_level, axis=1)
    df["is_free"] = df["entry_fee_adult"].apply(lambda x: float(x) == 0 if str(x).strip() != "" else True)

    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)

    df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8-sig")
    df.to_excel(OUTPUT_XLSX_PATH, index=False)

    print("Planlama kolonları eklendi.")
    print(f"CSV çıktı: {OUTPUT_CSV_PATH}")
    print(f"Excel çıktı: {OUTPUT_XLSX_PATH}")
    print(f"Toplam kolon: {len(df.columns)}")
    print(f"Toplam lokasyon: {len(df)}")

    print("\nKontrol:")
    print(
        df[
            [
                "location_name",
                "category",
                "sub_category",
                "average_visit_duration_min",
                "entry_fee_adult",
                "budget_level",
                "tourist_importance_score",
                "history_score",
                "museum_score",
                "art_score",
                "architecture_score",
                "photography_score",
                "nature_score",
                "gastronomy_score",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
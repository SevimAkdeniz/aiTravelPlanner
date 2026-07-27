import os
import pandas as pd


INPUT_PATH = "datasets/master/rome_master_dataset_v1_planning_ready_with_confidence.csv"

OUTPUT_CSV_PATH = "datasets/master/rome_location_scores_sample.csv"
OUTPUT_XLSX_PATH = "datasets/master/rome_location_scores_sample.xlsx"


USER_PROFILES = {
    "history_architecture_user": {
        "interests": ["history", "architecture", "photography"],
        "budget_level": "medium",
        "tempo": "normal",
        "preferred_visit_time": "any",
        "rainy_weather": False,
        "hot_weather": False,
        "max_entry_fee": 25,
    },

    "art_museum_user": {
        "interests": ["museum", "art", "architecture"],
        "budget_level": "medium",
        "tempo": "slow",
        "preferred_visit_time": "any",
        "rainy_weather": True,
        "hot_weather": False,
        "max_entry_fee": 25,
    },

    "food_evening_user": {
        "interests": ["gastronomy", "photography"],
        "budget_level": "low",
        "tempo": "normal",
        "preferred_visit_time": "evening",
        "rainy_weather": False,
        "hot_weather": False,
        "max_entry_fee": 10,
    },

    "nature_slow_user": {
        "interests": ["nature", "photography"],
        "budget_level": "low",
        "tempo": "slow",
        "preferred_visit_time": "sunset",
        "rainy_weather": False,
        "hot_weather": False,
        "max_entry_fee": 10,
    },

    "low_budget_fast_user": {
        "interests": ["history", "photography"],
        "budget_level": "free",
        "tempo": "fast",
        "preferred_visit_time": "any",
        "rainy_weather": False,
        "hot_weather": False,
        "max_entry_fee": 0,
    },
}


INTEREST_COLUMNS = {
    "history": "history_score",
    "museum": "museum_score",
    "art": "art_score",
    "architecture": "architecture_score",
    "photography": "photography_score",
    "nature": "nature_score",
    "gastronomy": "gastronomy_score",
    "shopping": "shopping_score",
    "religious": "religious_score",
}


BUDGET_LEVEL_SCORE = {
    "free": 100,
    "low": 90,
    "medium": 75,
    "high": 45,
}


def safe_float(value, default=0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except:
        return default


def calculate_interest_match(row, user_profile):
    interests = user_profile.get("interests", [])

    if not interests:
        return 50

    scores = []

    for interest in interests:
        column = INTEREST_COLUMNS.get(interest)

        if column and column in row:
            scores.append(safe_float(row[column]))

    if not scores:
        return 50

    # 0-10 arası skoru 0-100'e çeviriyoruz
    return (sum(scores) / len(scores)) * 10


def calculate_budget_match(row, user_profile):
    entry_fee = safe_float(row.get("entry_fee_adult", 0))
    max_entry_fee = safe_float(user_profile.get("max_entry_fee", 999))

    if entry_fee > max_entry_fee:
        return 20

    budget_level = str(row.get("budget_level", "medium")).lower()

    return BUDGET_LEVEL_SCORE.get(budget_level, 60)


def calculate_time_match(row, user_profile):
    preferred_time = str(user_profile.get("preferred_visit_time", "any")).lower()
    recommended_time = str(row.get("recommended_visit_time", "any")).lower()

    if preferred_time == "any":
        return 80

    if recommended_time == "any":
        return 70

    if preferred_time == recommended_time:
        return 100

    return 50


def calculate_tempo_match(row, user_profile):
    tempo = str(user_profile.get("tempo", "normal")).lower()
    duration = safe_float(row.get("average_visit_duration_min", 90))

    if tempo == "slow":
        if duration <= 60:
            return 90
        elif duration <= 120:
            return 75
        else:
            return 55

    if tempo == "normal":
        if duration <= 45:
            return 75
        elif duration <= 120:
            return 90
        else:
            return 65

    if tempo == "fast":
        if duration <= 60:
            return 95
        elif duration <= 120:
            return 70
        else:
            return 45

    return 70


def calculate_weather_match(row, user_profile):
    rainy_weather = user_profile.get("rainy_weather", False)
    hot_weather = user_profile.get("hot_weather", False)

    good_for_rainy = str(row.get("good_for_rainy_weather", False)).lower() in ["true", "1", "yes"]
    good_for_hot = str(row.get("good_for_hot_weather", False)).lower() in ["true", "1", "yes"]

    indoor_outdoor = str(row.get("indoor_outdoor", "")).lower()

    if rainy_weather:
        if good_for_rainy or indoor_outdoor == "indoor":
            return 100
        elif indoor_outdoor == "mixed":
            return 75
        else:
            return 40

    if hot_weather:
        if good_for_hot or indoor_outdoor == "indoor":
            return 90
        elif indoor_outdoor == "mixed":
            return 75
        else:
            return 55

    return 80


def calculate_importance_score(row):
    importance = safe_float(row.get("tourist_importance_score", 7))

    return importance * 10


def calculate_suitability_score(row, user_profile):
    interest_match = calculate_interest_match(row, user_profile)
    budget_match = calculate_budget_match(row, user_profile)
    time_match = calculate_time_match(row, user_profile)
    tempo_match = calculate_tempo_match(row, user_profile)
    weather_match = calculate_weather_match(row, user_profile)
    importance_score = calculate_importance_score(row)

    final_score = (
    interest_match * 0.35
    + importance_score * 0.25
    + budget_match * 0.15
    + time_match * 0.10
    + tempo_match * 0.10
    + weather_match * 0.05
)

    return {
        "interest_match_score": round(interest_match, 2),
        "budget_match_score": round(budget_match, 2),
        "time_match_score": round(time_match, 2),
        "tempo_match_score": round(tempo_match, 2),
        "weather_match_score": round(weather_match, 2),
        "importance_match_score": round(importance_score, 2),
        "suitability_score": round(final_score, 2),
    }


def generate_recommendation_reason(row):
    reasons = []

    category = row.get("category", "")
    sub_category = row.get("sub_category", "")
    location_name = row.get("location_name", "")

    if safe_float(row.get("history_score", 0)) >= 8:
        reasons.append("tarih ilgisine uygun")

    if safe_float(row.get("architecture_score", 0)) >= 8:
        reasons.append("mimari açıdan güçlü")

    if safe_float(row.get("photography_score", 0)) >= 8:
        reasons.append("fotoğraf çekimi için uygun")

    if safe_float(row.get("museum_score", 0)) >= 8:
        reasons.append("müze ve sanat ilgisine uygun")

    if safe_float(row.get("gastronomy_score", 0)) >= 8:
        reasons.append("yeme-içme ve atmosfer açısından güçlü")

    if not reasons:
        reasons.append(f"{category} / {sub_category} türünde uygun bir lokasyon")

    return f"{location_name}, " + ", ".join(reasons) + " olduğu için önerildi."

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    all_profile_results = []

    for profile_name, user_profile in USER_PROFILES.items():
        score_rows = []

        for _, row in df.iterrows():
            row = row.copy()

            scores = calculate_suitability_score(row, user_profile)

            for column, value in scores.items():
                row[column] = value

            row["user_profile_name"] = profile_name
            row["recommendation_reason"] = generate_recommendation_reason(row)

            score_rows.append(row)

        scored_df = pd.DataFrame(score_rows)

        scored_df = scored_df.sort_values(
            by="suitability_score",
            ascending=False
        )

        profile_csv_path = f"datasets/master/rome_location_scores_{profile_name}.csv"
        profile_xlsx_path = f"datasets/master/rome_location_scores_{profile_name}.xlsx"

        scored_df.to_csv(profile_csv_path, index=False, encoding="utf-8-sig")
        scored_df.to_excel(profile_xlsx_path, index=False)

        top_10 = scored_df.head(10).copy()
        all_profile_results.append(top_10)

        print("\n" + "=" * 80)
        print(f"Kullanıcı profili: {profile_name}")
        print(user_profile)
        print("\nEn uygun 10 lokasyon:")
        print(
            top_10[
                [
                    "location_name",
                    "category",
                    "average_visit_duration_min",
                    "entry_fee_adult",
                    "budget_level",
                    "interest_match_score",
                    "budget_match_score",
                    "importance_match_score",
                    "suitability_score",
                    "recommendation_reason",
                ]
            ].to_string(index=False)
        )

        print(f"\nCSV çıktı: {profile_csv_path}")
        print(f"Excel çıktı: {profile_xlsx_path}")

    comparison_df = pd.concat(all_profile_results, ignore_index=True)

    comparison_csv_path = "datasets/master/rome_location_scores_profile_comparison.csv"
    comparison_xlsx_path = "datasets/master/rome_location_scores_profile_comparison.xlsx"

    comparison_df.to_csv(comparison_csv_path, index=False, encoding="utf-8-sig")
    comparison_df.to_excel(comparison_xlsx_path, index=False)

    print("\n" + "=" * 80)
    print("Tüm profil karşılaştırma dosyası oluşturuldu.")
    print(f"CSV çıktı: {comparison_csv_path}")
    print(f"Excel çıktı: {comparison_xlsx_path}")
if __name__ == "__main__":
    main()
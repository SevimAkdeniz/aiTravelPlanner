from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "datasets/master/"
    "rome_master_dataset_v1_planning_ready_with_confidence.csv"
)

OUTPUT_PATH = Path(
    "datasets/processed/"
    "rome_locations_ml_ready.csv"
)


IDENTIFIER_COLUMNS = [
    "location_id",
    "location_name",
]

NUMERIC_COLUMNS = [
    "latitude",
    "longitude",
    "opentripmap_match_score",
    "opentripmap_rate",
    "popularity_score",
    "average_visit_duration_min",
    "min_visit_duration_min",
    "max_visit_duration_min",
    "entry_fee_adult",
    "entry_fee_student",
    "tourist_importance_score",
    "history_score",
    "museum_score",
    "art_score",
    "architecture_score",
    "photography_score",
    "nature_score",
    "gastronomy_score",
    "shopping_score",
    "religious_score",
    "public_transport_score",
    "walking_difficulty_score",
]

BOOLEAN_COLUMNS = [
    "reservation_required",
    "is_family_friendly",
    "is_open_24h",
    "is_free",
    "good_for_rainy_weather",
    "good_for_hot_weather",
    "needs_verification",
]

CATEGORICAL_COLUMNS = [
    "category",
    "sub_category",
    "indoor_outdoor",
    "recommended_visit_time",
    "budget_level",
    "weather_sensitivity",
    "data_confidence_level",
]


def validate_columns(df: pd.DataFrame) -> None:
    required_columns = (
        IDENTIFIER_COLUMNS
        + NUMERIC_COLUMNS
        + BOOLEAN_COLUMNS
        + CATEGORICAL_COLUMNS
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Veri setinde eksik sütunlar bulundu: "
            + ", ".join(missing_columns)
        )


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    for column in NUMERIC_COLUMNS:
        result[column] = pd.to_numeric(
            result[column],
            errors="coerce",
        )

        median_value = result[column].median()

        if pd.isna(median_value):
            median_value = 0

        result[column] = result[column].fillna(median_value)

    return result


def clean_boolean_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    true_values = {
        True,
        1,
        "1",
        "true",
        "True",
        "TRUE",
        "yes",
        "Yes",
        "YES",
    }

    for column in BOOLEAN_COLUMNS:
        result[column] = result[column].apply(
            lambda value: 1 if value in true_values else 0
        )

    return result


def clean_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    for column in CATEGORICAL_COLUMNS:
        result[column] = (
            result[column]
            .fillna("unknown")
            .astype(str)
            .str.strip()
            .str.lower()
        )

        result.loc[
            result[column].isin(["", "nan", "none"]),
            column,
        ] = "unknown"

    return result


def remove_unused_columns(df: pd.DataFrame) -> pd.DataFrame:
    selected_columns = (
        IDENTIFIER_COLUMNS
        + NUMERIC_COLUMNS
        + BOOLEAN_COLUMNS
        + CATEGORICAL_COLUMNS
    )

    return df[selected_columns].copy()


def preprocess_locations(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)

    processed_df = remove_unused_columns(df)
    processed_df = clean_numeric_columns(processed_df)
    processed_df = clean_boolean_columns(processed_df)
    processed_df = clean_categorical_columns(processed_df)

    processed_df = processed_df.drop_duplicates(
        subset=["location_id"],
        keep="first",
    )

    processed_df = processed_df.sort_values(
        by="location_id",
    ).reset_index(drop=True)

    return processed_df


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Girdi dosyası bulunamadı: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    print(f"Ham veri boyutu: {df.shape}")

    processed_df = preprocess_locations(df)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    processed_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"İşlenmiş veri boyutu: {processed_df.shape}")
    print(f"Çıktı dosyası: {OUTPUT_PATH}")

    print("\nEksik değer sayıları:")
    missing_values = processed_df.isna().sum()
    print(missing_values[missing_values > 0])

    print("\nKullanılan sütunlar:")
    for column in processed_df.columns:
        print(f"- {column}")


if __name__ == "__main__":
    main()
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from src.feature_engineering import build_feature_dataframe

MODEL_PATH = Path(
    "models/location_recommender_v2.joblib"
)

LOCATIONS_PATH = Path(
    "datasets/processed/rome_locations_ml_ready.csv"
)

FEATURE_COLUMNS_PATH = Path(
    "models/feature_columns.json"
)

OUTPUT_PATH = Path(
    "reports/latest_recommendations.csv"
)


DEFAULT_USER_PROFILE = {
    "history_interest": 9,
    "museum_interest": 7,
    "art_interest": 6,
    "architecture_interest": 9,
    "photography_interest": 8,
    "nature_interest": 3,
    "gastronomy_interest": 5,
    "shopping_interest": 2,
    "religious_interest": 4,
    "budget_level": "medium",
    "max_entry_fee": 25,
    "tempo": "normal",
    "preferred_visit_time": "any",
    "rainy_weather": False,
    "hot_weather": False,
    "family_friendly_required": False,
    "free_place_preference": 5,
}


def validate_files() -> None:
    required_files = [
        MODEL_PATH,
        LOCATIONS_PATH,
        FEATURE_COLUMNS_PATH,
    ]

    missing_files = [
        str(path)
        for path in required_files
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Eksik dosyalar:\n- "
            + "\n- ".join(missing_files)
        )


def load_expected_features() -> list[str]:
    with FEATURE_COLUMNS_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        payload = json.load(file)

    expected_features = payload.get(
        "input_features",
        [],
    )

    if not expected_features:
        raise ValueError(
            "Model özellik listesi bulunamadı."
        )

    return expected_features


def prepare_model_features(
    feature_df: pd.DataFrame,
    expected_features: list[str],
) -> pd.DataFrame:
    result = feature_df.copy()

    for column in expected_features:
        if column not in result.columns:
            result[column] = np.nan

    extra_columns = [
        column
        for column in result.columns
        if column not in expected_features
    ]

    if extra_columns:
        result = result.drop(
            columns=extra_columns
        )

    result = result[
        expected_features
    ]

    return result


def generate_recommendation_reason(
    row: pd.Series,
    user_profile: dict[str, Any],
) -> str:
    reasons: list[str] = []

    interest_pairs = [
        (
            "history_interest",
            "history_score",
            "tarih ilginizle yüksek uyumlu",
        ),
        (
            "museum_interest",
            "museum_score",
            "müze tercihinize uygun",
        ),
        (
            "art_interest",
            "art_score",
            "sanat ilginizle eşleşiyor",
        ),
        (
            "architecture_interest",
            "architecture_score",
            "mimari ilginizle yüksek uyumlu",
        ),
        (
            "photography_interest",
            "photography_score",
            "fotoğraf çekimi için uygun",
        ),
        (
            "nature_interest",
            "nature_score",
            "doğa ilginizle eşleşiyor",
        ),
        (
            "gastronomy_interest",
            "gastronomy_score",
            "gastronomi tercihinize uygun",
        ),
        (
            "shopping_interest",
            "shopping_score",
            "alışveriş ilginizle eşleşiyor",
        ),
        (
            "religious_interest",
            "religious_score",
            "dini ve kültürel yapı ilginize uygun",
        ),
    ]

    for (
        user_interest_column,
        location_score_column,
        message,
    ) in interest_pairs:
        user_interest = float(
            user_profile.get(
                user_interest_column,
                0,
            )
        )

        location_score = float(
            row.get(
                location_score_column,
                0,
            )
        )

        if (
            user_interest >= 7
            and location_score >= 7
        ):
            reasons.append(message)

    if int(row.get("is_affordable", 0)) == 1:
        reasons.append(
            "belirlediğiniz giriş ücreti sınırına uygun"
        )

    if float(
        row.get(
            "tempo_duration_match",
            0,
        )
    ) >= 75:
        reasons.append(
            "gezi temponuzla uyumlu"
        )

    if int(
        row.get(
            "flexible_visit_time_match",
            0,
        )
    ) == 1:
        reasons.append(
            "tercih ettiğiniz ziyaret zamanına uygun"
        )

    if int(
        row.get(
            "family_requirement_match",
            0,
        )
    ) == 1 and bool(
        user_profile.get(
            "family_friendly_required",
            False,
        )
    ):
        reasons.append(
            "aile dostu mekân şartınızı karşılıyor"
        )

    if not reasons:
        reasons.append(
            "genel tercihlerinizle dengeli bir uyum sağlıyor"
        )

    return "; ".join(reasons[:4]).capitalize() + "."


def predict_recommendations(
    user_profile: dict[str, Any],
    top_n: int = 10,
) -> pd.DataFrame:
    validate_files()

    locations_df = pd.read_csv(
        LOCATIONS_PATH
    )

    model = joblib.load(
        MODEL_PATH
    )

    expected_features = (
        load_expected_features()
    )

    feature_df = build_feature_dataframe(
        locations_df,
        user_profile,
    )

    model_features = prepare_model_features(
        feature_df,
        expected_features,
    )

    predictions = model.predict(
        model_features
    )

    predictions = np.clip(
        predictions,
        0,
        100,
    )

    result_df = feature_df.copy()

    result_df[
        "predicted_suitability_score"
    ] = np.round(
        predictions,
        2,
    )

    result_df[
        "recommendation_reason"
    ] = result_df.apply(
        lambda row: generate_recommendation_reason(
            row,
            user_profile,
        ),
        axis=1,
    )

    result_df = result_df.sort_values(
        by="predicted_suitability_score",
        ascending=False,
    ).reset_index(drop=True)

    result_df.insert(
        0,
        "recommendation_rank",
        range(
            1,
            len(result_df) + 1,
        ),
    )

    output_columns = [
        "recommendation_rank",
        "location_id",
        "location_name",
        "category",
        "sub_category",
        "latitude",
        "longitude",
        "indoor_outdoor",
        "predicted_suitability_score",
        "entry_fee_adult",
        "budget_level",
        "average_visit_duration_min",
        "min_visit_duration_min",
        "max_visit_duration_min",
        "recommended_visit_time",
        "reservation_required",
        "is_family_friendly",
        "is_free",
        "public_transport_score",
        "walking_difficulty_score",
        "weighted_interest_match",
        "tempo_duration_match",
        "is_affordable",
        "recommendation_reason",
    ]


    return result_df[
        output_columns
    ].head(top_n)


def main() -> None:
    recommendations_df = (
        predict_recommendations(
            DEFAULT_USER_PROFILE,
            top_n=10,
        )
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    recommendations_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("=" * 100)
    print("KULLANICI PROFİLİ")
    print("=" * 100)

    for key, value in (
        DEFAULT_USER_PROFILE.items()
    ):
        print(f"{key}: {value}")

    print("\n" + "=" * 100)
    print("EN UYGUN 10 ROMA LOKASYONU")
    print("=" * 100)

    display_columns = [
        "recommendation_rank",
        "location_name",
        "predicted_suitability_score",
        "entry_fee_adult",
        "average_visit_duration_min",
        "recommendation_reason",
    ]

    print(
        recommendations_df[
            display_columns
        ].to_string(
            index=False
        )
    )

    print(
        f"\nÇıktı dosyası: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
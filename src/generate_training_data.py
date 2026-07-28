from __future__ import annotations

import random
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from feature_engineering import (
    INTEREST_COLUMNS,
    build_feature_dataframe,
)


INPUT_PATH = Path(
    "datasets/processed/rome_locations_ml_ready.csv"
)

OUTPUT_PATH = Path(
    "datasets/training/rome_user_location_training.csv"
)

PROFILE_OUTPUT_PATH = Path(
    "datasets/training/synthetic_user_profiles.csv"
)

RANDOM_SEED = 42
PROFILE_COUNT = 1000


BUDGET_CONFIG = {
    "free": {
        "max_fee_range": (0, 0),
        "free_preference_range": (8, 10),
    },
    "low": {
        "max_fee_range": (5, 15),
        "free_preference_range": (6, 10),
    },
    "medium": {
        "max_fee_range": (15, 35),
        "free_preference_range": (3, 8),
    },
    "high": {
        "max_fee_range": (35, 100),
        "free_preference_range": (0, 6),
    },
}


TEMPO_VALUES = [
    "fast",
    "normal",
    "slow",
]

VISIT_TIME_VALUES = [
    "any",
    "morning",
    "afternoon",
    "evening",
    "sunset",
    "night",
]


def set_random_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def generate_interest_values() -> dict[str, int]:
    interests: dict[str, int] = {}

    interest_names = list(INTEREST_COLUMNS.keys())

    primary_interest_count = random.randint(1, 3)

    primary_interests = random.sample(
        interest_names,
        primary_interest_count,
    )

    for interest in interest_names:
        if interest in primary_interests:
            interests[f"{interest}_interest"] = (
                random.randint(7, 10)
            )
        else:
            interests[f"{interest}_interest"] = (
                random.randint(0, 6)
            )

    return interests


def generate_budget_preferences() -> dict[str, Any]:
    budget_level = random.choices(
        population=[
            "free",
            "low",
            "medium",
            "high",
        ],
        weights=[
            0.10,
            0.30,
            0.45,
            0.15,
        ],
        k=1,
    )[0]

    config = BUDGET_CONFIG[budget_level]

    min_fee, max_fee = config["max_fee_range"]
    min_free_pref, max_free_pref = (
        config["free_preference_range"]
    )

    max_entry_fee = random.randint(
        min_fee,
        max_fee,
    )

    free_place_preference = random.randint(
        min_free_pref,
        max_free_pref,
    )

    return {
        "budget_level": budget_level,
        "max_entry_fee": max_entry_fee,
        "free_place_preference": (
            free_place_preference
        ),
    }


def generate_weather_preferences() -> dict[str, bool]:
    rainy_weather = random.random() < 0.20
    hot_weather = random.random() < 0.30

    return {
        "rainy_weather": rainy_weather,
        "hot_weather": hot_weather,
    }


def generate_user_profile(
    profile_id: int,
) -> dict[str, Any]:
    profile: dict[str, Any] = {
        "user_profile_id": profile_id,
    }

    profile.update(
        generate_interest_values()
    )

    profile.update(
        generate_budget_preferences()
    )

    profile.update(
        generate_weather_preferences()
    )

    profile.update(
        {
            "tempo": random.choices(
                population=TEMPO_VALUES,
                weights=[
                    0.25,
                    0.50,
                    0.25,
                ],
                k=1,
            )[0],
            "preferred_visit_time": (
                random.choices(
                    population=VISIT_TIME_VALUES,
                    weights=[
                        0.35,
                        0.15,
                        0.15,
                        0.15,
                        0.12,
                        0.08,
                    ],
                    k=1,
                )[0]
            ),
            "family_friendly_required": (
                random.random() < 0.25
            ),
        }
    )

    return profile


def calculate_interest_target(
    row: pd.Series,
) -> float:
    interest_names = list(
        INTEREST_COLUMNS.keys()
    )

    user_interests = []
    location_scores = []

    for interest in interest_names:
        user_value = float(
            row.get(
                f"user_{interest}_interest",
                0,
            )
        )

        location_value = float(
            row.get(
                INTEREST_COLUMNS[interest],
                0,
            )
        )

        user_interests.append(
            user_value
        )

        location_scores.append(
            location_value
        )

    user_array = np.asarray(
        user_interests,
        dtype=float,
    )

    location_array = np.asarray(
        location_scores,
        dtype=float,
    )

    preference_total = float(
        user_array.sum()
    )

    if preference_total <= 0:
        return 50.0

    weighted_average = float(
        np.sum(
            user_array * location_array
        )
        / preference_total
    )

    dominant_indices = np.argsort(
        user_array
    )[::-1][:3]

    dominant_user_values = (
        user_array[
            dominant_indices
        ]
    )

    dominant_location_values = (
        location_array[
            dominant_indices
        ]
    )

    dominant_weight_total = float(
        dominant_user_values.sum()
    )

    if dominant_weight_total > 0:
        dominant_match = float(
            np.sum(
                dominant_user_values
                * dominant_location_values
            )
            / dominant_weight_total
        )
    else:
        dominant_match = weighted_average

    low_interest_indices = np.where(
        user_array <= 2
    )[0]

    low_interest_mismatch = 0.0

    if len(low_interest_indices) > 0:
        low_interest_location_scores = (
            location_array[
                low_interest_indices
            ]
        )

        low_interest_mismatch = float(
            np.mean(
                np.maximum(
                    low_interest_location_scores
                    - 7,
                    0,
                )
            )
        )

    final_interest_score = (
        dominant_match * 0.65
        + weighted_average * 0.35
    ) * 10

    final_interest_score -= (
        low_interest_mismatch * 2.5
    )

    return float(
        np.clip(
            final_interest_score,
            0,
            100,
        )
    )

def calculate_importance_target(
    row: pd.Series,
) -> float:
    importance = float(
        row.get(
            "tourist_importance_score",
            0,
        )
    )

    popularity = float(
        row.get(
            "popularity_score",
            0,
        )
    )

    opentipmap_rate = float(
        row.get(
            "opentripmap_rate",
            0,
        )
    )

    importance_score = (
        importance * 7
        + popularity * 2
        + opentipmap_rate
    )

    return float(
        np.clip(
            importance_score,
            0,
            100,
        )
    )


def calculate_budget_target(
    row: pd.Series,
) -> float:
    is_affordable = int(
        row.get(
            "is_affordable",
            0,
        )
    )

    affordability_ratio = float(
        row.get(
            "affordability_ratio",
            0,
        )
    )

    free_preference_match = float(
        row.get(
            "free_preference_match",
            0,
        )
    )

    if is_affordable == 0:
        return 15.0

    budget_score = (
        affordability_ratio * 70
        + free_preference_match * 3
    )

    return float(
        np.clip(
            budget_score,
            0,
            100,
        )
    )


def calculate_tempo_target(
    row: pd.Series,
) -> float:
    tempo_match = float(
        row.get(
            "tempo_duration_match",
            0,
        )
    )

    walking_difficulty = float(
        row.get(
            "walking_difficulty_score",
            5,
        )
    )

    user_tempo = str(
        row.get(
            "user_tempo",
            "normal",
        )
    ).lower()

    walking_adjustment = 0.0

    if user_tempo == "fast":
        walking_adjustment = (
            walking_difficulty - 5
        ) * 1.5

    elif user_tempo == "slow":
        walking_adjustment = (
            5 - walking_difficulty
        ) * 2.0

    adjusted_score = (
        tempo_match
        + walking_adjustment
    )

    return float(
        np.clip(
            adjusted_score,
            0,
            100,
        )
    )


def calculate_time_target(
    row: pd.Series,
) -> float:
    exact_match = int(
        row.get(
            "exact_visit_time_match",
            0,
        )
    )

    flexible_match = int(
        row.get(
            "flexible_visit_time_match",
            0,
        )
    )

    if exact_match == 1:
        return 100.0

    if flexible_match == 1:
        return 80.0

    return 45.0


def calculate_weather_target(
    row: pd.Series,
) -> float:
    rainy_match = int(
        row.get(
            "rainy_weather_match",
            1,
        )
    )

    hot_match = int(
        row.get(
            "hot_weather_match",
            1,
        )
    )

    user_rainy_weather = int(
        row.get(
            "user_rainy_weather",
            0,
        )
    )

    user_hot_weather = int(
        row.get(
            "user_hot_weather",
            0,
        )
    )

    weather_requirements = 0
    weather_matches = 0

    if user_rainy_weather == 1:
        weather_requirements += 1
        weather_matches += rainy_match

    if user_hot_weather == 1:
        weather_requirements += 1
        weather_matches += hot_match

    if weather_requirements == 0:
        return 80.0

    return float(
        weather_matches
        / weather_requirements
        * 100
    )


def calculate_family_target(
    row: pd.Series,
) -> float:
    family_required = int(
        row.get(
            "user_family_friendly_required",
            0,
        )
    )

    if family_required == 0:
        return 80.0

    walking_difficulty = float(
        row.get(
            "walking_difficulty_score",
            5,
        )
    )

    visit_duration = float(
        row.get(
            "average_visit_duration_min",
            90,
        )
    )

    nature_score = float(
        row.get(
            "nature_score",
            0,
        )
    )

    family_friendly = int(
        row.get(
            "is_family_friendly",
            1,
        )
    )

    walking_score = float(
        np.clip(
            110
            - walking_difficulty * 10,
            20,
            100,
        )
    )

    if visit_duration <= 60:
        duration_score = 100.0
    elif visit_duration <= 90:
        duration_score = 85.0
    elif visit_duration <= 120:
        duration_score = 65.0
    else:
        duration_score = 40.0

    nature_bonus = min(
        nature_score * 2,
        15,
    )

    family_score = (
        walking_score * 0.45
        + duration_score * 0.40
        + family_friendly * 15
        + nature_bonus
    )

    return float(
        np.clip(
            family_score,
            0,
            100,
        )
    )
def calculate_data_quality_adjustment(
    row: pd.Series,
) -> float:
    confidence_level = str(
        row.get(
            "data_confidence_level",
            "medium",
        )
    ).lower()

    needs_verification = int(
        row.get(
            "needs_verification",
            0,
        )
    )

    confidence_adjustments = {
        "high": 2.0,
        "medium": 0.0,
        "low": -4.0,
    }

    adjustment = confidence_adjustments.get(
        confidence_level,
        0.0,
    )

    if needs_verification == 1:
        adjustment -= 1.0

    return adjustment


def calculate_target_score(
    row: pd.Series,
) -> dict[str, float]:
    interest_score = calculate_interest_target(
        row
    )

    importance_score = (
        calculate_importance_target(
            row
        )
    )

    budget_score = calculate_budget_target(
        row
    )

    tempo_score = calculate_tempo_target(
        row
    )

    time_score = calculate_time_target(
        row
    )

    weather_score = calculate_weather_target(
        row
    )

    family_score = calculate_family_target(
        row
    )

    final_score = (
    interest_score * 0.45
    + importance_score * 0.12
    + budget_score * 0.15
    + tempo_score * 0.10
    + time_score * 0.07
    + weather_score * 0.06
    + family_score * 0.05
)

    final_score += (
        calculate_data_quality_adjustment(
            row
        )
    )

    noise = np.random.normal(
        loc=0.0,
        scale=1.5,
    )

    final_score += noise

    final_score = float(
        np.clip(
            final_score,
            0,
            100,
        )
    )

    return {
        "target_interest_score": round(
            interest_score,
            4,
        ),
        "target_importance_score": round(
            importance_score,
            4,
        ),
        "target_budget_score": round(
            budget_score,
            4,
        ),
        "target_tempo_score": round(
            tempo_score,
            4,
        ),
        "target_time_score": round(
            time_score,
            4,
        ),
        "target_weather_score": round(
            weather_score,
            4,
        ),
        "target_family_score": round(
            family_score,
            4,
        ),
        "suitability_score": round(
            final_score,
            4,
        ),
    }


def generate_training_rows(
    locations_df: pd.DataFrame,
    profiles: list[dict[str, Any]],
) -> pd.DataFrame:
    all_training_frames = []

    for index, profile in enumerate(
        profiles,
        start=1,
    ):
        profile_id = profile[
            "user_profile_id"
        ]

        model_profile = {
            key: value
            for key, value in profile.items()
            if key != "user_profile_id"
        }

        feature_df = build_feature_dataframe(
            locations_df,
            model_profile,
        )

        feature_df.insert(
            0,
            "user_profile_id",
            profile_id,
        )

        target_rows = feature_df.apply(
            calculate_target_score,
            axis=1,
            result_type="expand",
        )

        training_df = pd.concat(
            [
                feature_df,
                target_rows,
            ],
            axis=1,
        )

        all_training_frames.append(
            training_df
        )

        if (
            index % 100 == 0
            or index == len(profiles)
        ):
            print(
                f"İşlenen profil: "
                f"{index}/{len(profiles)}"
            )

    return pd.concat(
        all_training_frames,
        ignore_index=True,
    )


def validate_training_dataset(
    training_df: pd.DataFrame,
) -> None:
    if training_df.empty:
        raise ValueError(
            "Eğitim veri seti boş oluşturuldu."
        )

    if training_df[
        "suitability_score"
    ].isna().any():
        raise ValueError(
            "Hedef puanlarda eksik değer var."
        )

    invalid_scores = training_df[
        ~training_df[
            "suitability_score"
        ].between(
            0,
            100,
        )
    ]

    if not invalid_scores.empty:
        raise ValueError(
            "0-100 aralığı dışında "
            "hedef puan bulundu."
        )


def main() -> None:
    set_random_seed(
        RANDOM_SEED
    )

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Girdi dosyası bulunamadı: "
            f"{INPUT_PATH}"
        )

    locations_df = pd.read_csv(
        INPUT_PATH
    )

    print(
        f"Lokasyon veri boyutu: "
        f"{locations_df.shape}"
    )

    profiles = [
        generate_user_profile(
            profile_id
        )
        for profile_id in range(
            1,
            PROFILE_COUNT + 1,
        )
    ]

    profiles_df = pd.DataFrame(
        profiles
    )

    PROFILE_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    profiles_df.to_csv(
        PROFILE_OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print(
        f"Sentetik kullanıcı profili: "
        f"{len(profiles_df)}"
    )

    training_df = (
        generate_training_rows(
            locations_df,
            profiles,
        )
    )

    validate_training_dataset(
        training_df
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    training_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("\nEğitim veri seti oluşturuldu.")
    print(
        f"Boyut: {training_df.shape}"
    )
    print(
        f"Çıktı: {OUTPUT_PATH}"
    )
    print(
        f"Profil çıktısı: "
        f"{PROFILE_OUTPUT_PATH}"
    )

    print("\nHedef puan özeti:")
    print(
        training_df[
            "suitability_score"
        ].describe()
    )

    print("\nİlk 10 örnek:")
    print(
        training_df[
            [
                "user_profile_id",
                "location_name",
                "weighted_interest_match",
                "is_affordable",
                "tempo_duration_match",
                "suitability_score",
            ]
        ]
        .head(10)
        .to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()
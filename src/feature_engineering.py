from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


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


USER_INTEREST_COLUMNS = {
    "history": "user_history_interest",
    "museum": "user_museum_interest",
    "art": "user_art_interest",
    "architecture": "user_architecture_interest",
    "photography": "user_photography_interest",
    "nature": "user_nature_interest",
    "gastronomy": "user_gastronomy_interest",
    "shopping": "user_shopping_interest",
    "religious": "user_religious_interest",
}


TEMPO_DURATION_TARGETS = {
    "fast": 45,
    "normal": 90,
    "slow": 150,
}


BUDGET_MAX_FEES = {
    "free": 0,
    "low": 10,
    "medium": 25,
    "high": 100,
}


VALID_BUDGET_LEVELS = set(BUDGET_MAX_FEES.keys())
VALID_TEMPOS = set(TEMPO_DURATION_TARGETS.keys())

VALID_VISIT_TIMES = {
    "any",
    "morning",
    "afternoon",
    "evening",
    "sunset",
    "night",
}


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default

        return float(value)
    except (TypeError, ValueError):
        return default


def safe_bool(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)

    normalized_value = str(value).strip().lower()

    return int(
        normalized_value
        in {
            "true",
            "1",
            "yes",
            "evet",
        }
    )


def normalize_text(value: Any, default: str = "unknown") -> str:
    if value is None or pd.isna(value):
        return default

    normalized_value = str(value).strip().lower()

    if normalized_value in {"", "nan", "none"}:
        return default

    return normalized_value


def clip_interest(value: Any) -> float:
    numeric_value = safe_float(value, default=0.0)

    return float(np.clip(numeric_value, 0, 10))


def normalize_user_profile(
    user_profile: dict[str, Any],
) -> dict[str, Any]:
    normalized_profile: dict[str, Any] = {}

    for interest, user_column in USER_INTEREST_COLUMNS.items():
        fallback_value = 0

        interests = user_profile.get("interests", [])

        if isinstance(interests, list) and interest in interests:
            fallback_value = 8

        normalized_profile[user_column] = clip_interest(
            user_profile.get(
                user_column,
                user_profile.get(
                    f"{interest}_interest",
                    fallback_value,
                ),
            )
        )

    budget_level = normalize_text(
        user_profile.get("budget_level", "medium")
    )

    if budget_level not in VALID_BUDGET_LEVELS:
        budget_level = "medium"

    tempo = normalize_text(
        user_profile.get("tempo", "normal")
    )

    if tempo not in VALID_TEMPOS:
        tempo = "normal"

    preferred_visit_time = normalize_text(
        user_profile.get(
            "preferred_visit_time",
            "any",
        )
    )

    if preferred_visit_time not in VALID_VISIT_TIMES:
        preferred_visit_time = "any"

    default_max_fee = BUDGET_MAX_FEES[budget_level]

    normalized_profile.update(
        {
            "user_budget_level": budget_level,
            "user_tempo": tempo,
            "user_preferred_visit_time": preferred_visit_time,
            "user_max_entry_fee": max(
                0,
                safe_float(
                    user_profile.get(
                        "max_entry_fee",
                        default_max_fee,
                    ),
                    default=float(default_max_fee),
                ),
            ),
            "user_rainy_weather": safe_bool(
                user_profile.get(
                    "rainy_weather",
                    False,
                )
            ),
            "user_hot_weather": safe_bool(
                user_profile.get(
                    "hot_weather",
                    False,
                )
            ),
            "user_family_friendly_required": safe_bool(
                user_profile.get(
                    "family_friendly_required",
                    False,
                )
            ),
            "user_free_place_preference": clip_interest(
                user_profile.get(
                    "free_place_preference",
                    5,
                )
            ),
        }
    )

    return normalized_profile


def calculate_interest_features(
    location_row: pd.Series,
    normalized_profile: dict[str, Any],
) -> dict[str, float]:
    features: dict[str, float] = {}

    weighted_match_total = 0.0
    preference_total = 0.0

    location_interest_total = 0.0
    location_interest_count = 0

    for interest, location_column in INTEREST_COLUMNS.items():
        user_column = USER_INTEREST_COLUMNS[interest]

        user_interest = clip_interest(
            normalized_profile[user_column]
        )

        location_interest = clip_interest(
            location_row.get(
                location_column,
                0,
            )
        )

        absolute_difference = abs(
            user_interest - location_interest
        )

        similarity_score = max(
            0.0,
            10.0 - absolute_difference,
        )

        interaction_score = (
            user_interest * location_interest
        ) / 10.0

        features[f"{interest}_absolute_difference"] = round(
            absolute_difference,
            4,
        )

        features[f"{interest}_similarity"] = round(
            similarity_score,
            4,
        )

        features[f"{interest}_interaction"] = round(
            interaction_score,
            4,
        )

        weighted_match_total += (
            location_interest * user_interest
        )

        preference_total += user_interest

        location_interest_total += location_interest
        location_interest_count += 1

    if preference_total > 0:
        weighted_interest_match = (
            weighted_match_total / preference_total
        )
    else:
        weighted_interest_match = (
            location_interest_total
            / max(location_interest_count, 1)
        )

    features["weighted_interest_match"] = round(
        weighted_interest_match,
        4,
    )

    features["user_interest_total"] = round(
        preference_total,
        4,
    )

    features["location_interest_average"] = round(
        location_interest_total
        / max(location_interest_count, 1),
        4,
    )

    return features


def calculate_budget_features(
    location_row: pd.Series,
    normalized_profile: dict[str, Any],
) -> dict[str, float | int]:
    entry_fee = max(
        0.0,
        safe_float(
            location_row.get(
                "entry_fee_adult",
                0,
            )
        ),
    )

    max_entry_fee = max(
        0.0,
        safe_float(
            normalized_profile.get(
                "user_max_entry_fee",
                0,
            )
        ),
    )

    fee_difference = max_entry_fee - entry_fee
    is_affordable = int(entry_fee <= max_entry_fee)

    if max_entry_fee == 0:
        affordability_ratio = (
            1.0 if entry_fee == 0 else 0.0
        )
    else:
        affordability_ratio = min(
            1.0,
            max_entry_fee / max(entry_fee, 1.0),
        )

    location_is_free = safe_bool(
        location_row.get(
            "is_free",
            False,
        )
    )

    free_preference = safe_float(
        normalized_profile.get(
            "user_free_place_preference",
            5,
        )
    )

    free_preference_match = (
        free_preference
        if location_is_free
        else 10.0 - free_preference
    )

    return {
        "entry_fee_difference": round(
            fee_difference,
            4,
        ),
        "is_affordable": is_affordable,
        "affordability_ratio": round(
            affordability_ratio,
            4,
        ),
        "free_preference_match": round(
            free_preference_match,
            4,
        ),
    }


def calculate_tempo_features(
    location_row: pd.Series,
    normalized_profile: dict[str, Any],
) -> dict[str, float]:
    tempo = normalize_text(
        normalized_profile.get(
            "user_tempo",
            "normal",
        )
    )

    target_duration = TEMPO_DURATION_TARGETS.get(
        tempo,
        TEMPO_DURATION_TARGETS["normal"],
    )

    location_duration = max(
        0.0,
        safe_float(
            location_row.get(
                "average_visit_duration_min",
                90,
            ),
            default=90.0,
        ),
    )

    duration_difference = abs(
        location_duration - target_duration
    )

    tempo_match = max(
        0.0,
        100.0 - (
            duration_difference
            / max(target_duration, 1)
            * 100.0
        ),
    )

    return {
        "tempo_target_duration": float(
            target_duration
        ),
        "duration_difference": round(
            duration_difference,
            4,
        ),
        "tempo_duration_match": round(
            tempo_match,
            4,
        ),
    }


def calculate_visit_time_features(
    location_row: pd.Series,
    normalized_profile: dict[str, Any],
) -> dict[str, int]:
    preferred_time = normalize_text(
        normalized_profile.get(
            "user_preferred_visit_time",
            "any",
        )
    )

    recommended_time = normalize_text(
        location_row.get(
            "recommended_visit_time",
            "any",
        )
    )

    exact_time_match = int(
        preferred_time == recommended_time
    )

    flexible_time_match = int(
        preferred_time == "any"
        or recommended_time == "any"
        or exact_time_match == 1
    )

    return {
        "exact_visit_time_match": exact_time_match,
        "flexible_visit_time_match": flexible_time_match,
    }


def calculate_weather_features(
    location_row: pd.Series,
    normalized_profile: dict[str, Any],
) -> dict[str, int]:
    rainy_weather = safe_bool(
        normalized_profile.get(
            "user_rainy_weather",
            False,
        )
    )

    hot_weather = safe_bool(
        normalized_profile.get(
            "user_hot_weather",
            False,
        )
    )

    good_for_rainy = safe_bool(
        location_row.get(
            "good_for_rainy_weather",
            False,
        )
    )

    good_for_hot = safe_bool(
        location_row.get(
            "good_for_hot_weather",
            False,
        )
    )

    indoor_outdoor = normalize_text(
        location_row.get(
            "indoor_outdoor",
            "unknown",
        )
    )

    rainy_weather_match = int(
        rainy_weather == 0
        or good_for_rainy == 1
        or indoor_outdoor == "indoor"
    )

    hot_weather_match = int(
        hot_weather == 0
        or good_for_hot == 1
        or indoor_outdoor == "indoor"
    )

    return {
        "rainy_weather_match": rainy_weather_match,
        "hot_weather_match": hot_weather_match,
    }


def calculate_family_features(
    location_row: pd.Series,
    normalized_profile: dict[str, Any],
) -> dict[str, int]:
    family_required = safe_bool(
        normalized_profile.get(
            "user_family_friendly_required",
            False,
        )
    )

    location_family_friendly = safe_bool(
        location_row.get(
            "is_family_friendly",
            False,
        )
    )

    family_requirement_match = int(
        family_required == 0
        or location_family_friendly == 1
    )

    return {
        "family_requirement_match": (
            family_requirement_match
        ),
    }


def build_user_location_features(
    location_row: pd.Series,
    user_profile: dict[str, Any],
) -> dict[str, Any]:
    normalized_profile = normalize_user_profile(
        user_profile
    )

    features: dict[str, Any] = {
        "location_id": int(
            location_row["location_id"]
        ),
        "location_name": str(
            location_row["location_name"]
        ),
    }

    for column in location_row.index:
        if column not in {
            "location_id",
            "location_name",
        }:
            features[column] = location_row[column]

    features.update(normalized_profile)

    features.update(
        calculate_interest_features(
            location_row,
            normalized_profile,
        )
    )

    features.update(
        calculate_budget_features(
            location_row,
            normalized_profile,
        )
    )

    features.update(
        calculate_tempo_features(
            location_row,
            normalized_profile,
        )
    )

    features.update(
        calculate_visit_time_features(
            location_row,
            normalized_profile,
        )
    )

    features.update(
        calculate_weather_features(
            location_row,
            normalized_profile,
        )
    )

    features.update(
        calculate_family_features(
            location_row,
            normalized_profile,
        )
    )

    return features


def build_feature_dataframe(
    locations_df: pd.DataFrame,
    user_profile: dict[str, Any],
) -> pd.DataFrame:
    feature_rows = []

    for _, location_row in locations_df.iterrows():
        feature_rows.append(
            build_user_location_features(
                location_row,
                user_profile,
            )
        )

    return pd.DataFrame(feature_rows)
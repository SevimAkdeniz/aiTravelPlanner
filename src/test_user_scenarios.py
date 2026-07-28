from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any

import pandas as pd

from predict import predict_recommendations


REPORTS_DIR = Path("reports")

SCENARIO_RESULTS_PATH = (
    REPORTS_DIR / "user_scenario_recommendations.csv"
)

SCENARIO_SUMMARY_PATH = (
    REPORTS_DIR / "user_scenario_summary.csv"
)

PROFILE_SIMILARITY_PATH = (
    REPORTS_DIR / "profile_top10_similarity.csv"
)

PROFILE_SIMILARITY_MATRIX_PATH = (
    REPORTS_DIR / "profile_similarity_matrix.csv"
)

SCENARIO_REPORT_PATH = (
    REPORTS_DIR / "user_scenario_report.json"
)


USER_SCENARIOS: dict[str, dict[str, Any]] = {
    "history_architecture": {
        "history_interest": 10,
        "museum_interest": 5,
        "art_interest": 4,
        "architecture_interest": 10,
        "photography_interest": 8,
        "nature_interest": 2,
        "gastronomy_interest": 2,
        "shopping_interest": 1,
        "religious_interest": 5,
        "budget_level": "medium",
        "max_entry_fee": 25,
        "tempo": "normal",
        "preferred_visit_time": "any",
        "rainy_weather": False,
        "hot_weather": False,
        "family_friendly_required": False,
        "free_place_preference": 4,
    },

    "museum_art": {
        "history_interest": 5,
        "museum_interest": 10,
        "art_interest": 10,
        "architecture_interest": 7,
        "photography_interest": 5,
        "nature_interest": 1,
        "gastronomy_interest": 1,
        "shopping_interest": 2,
        "religious_interest": 4,
        "budget_level": "high",
        "max_entry_fee": 50,
        "tempo": "slow",
        "preferred_visit_time": "morning",
        "rainy_weather": True,
        "hot_weather": False,
        "family_friendly_required": False,
        "free_place_preference": 2,
    },

    "nature_photography": {
        "history_interest": 2,
        "museum_interest": 1,
        "art_interest": 3,
        "architecture_interest": 3,
        "photography_interest": 10,
        "nature_interest": 10,
        "gastronomy_interest": 2,
        "shopping_interest": 1,
        "religious_interest": 1,
        "budget_level": "low",
        "max_entry_fee": 10,
        "tempo": "slow",
        "preferred_visit_time": "sunset",
        "rainy_weather": False,
        "hot_weather": False,
        "family_friendly_required": False,
        "free_place_preference": 8,
    },

    "gastronomy_evening": {
        "history_interest": 1,
        "museum_interest": 1,
        "art_interest": 2,
        "architecture_interest": 3,
        "photography_interest": 7,
        "nature_interest": 2,
        "gastronomy_interest": 10,
        "shopping_interest": 5,
        "religious_interest": 1,
        "budget_level": "medium",
        "max_entry_fee": 20,
        "tempo": "normal",
        "preferred_visit_time": "evening",
        "rainy_weather": False,
        "hot_weather": False,
        "family_friendly_required": False,
        "free_place_preference": 5,
    },

    "free_low_budget": {
        "history_interest": 7,
        "museum_interest": 3,
        "art_interest": 4,
        "architecture_interest": 7,
        "photography_interest": 8,
        "nature_interest": 5,
        "gastronomy_interest": 3,
        "shopping_interest": 1,
        "religious_interest": 4,
        "budget_level": "free",
        "max_entry_fee": 0,
        "tempo": "normal",
        "preferred_visit_time": "any",
        "rainy_weather": False,
        "hot_weather": False,
        "family_friendly_required": False,
        "free_place_preference": 10,
    },

    "family_with_children": {
        "history_interest": 5,
        "museum_interest": 5,
        "art_interest": 4,
        "architecture_interest": 5,
        "photography_interest": 6,
        "nature_interest": 8,
        "gastronomy_interest": 4,
        "shopping_interest": 3,
        "religious_interest": 2,
        "budget_level": "medium",
        "max_entry_fee": 30,
        "tempo": "slow",
        "preferred_visit_time": "morning",
        "rainy_weather": False,
        "hot_weather": False,
        "family_friendly_required": True,
        "free_place_preference": 6,
    },

    "fast_first_time_visitor": {
        "history_interest": 9,
        "museum_interest": 4,
        "art_interest": 4,
        "architecture_interest": 9,
        "photography_interest": 9,
        "nature_interest": 3,
        "gastronomy_interest": 3,
        "shopping_interest": 2,
        "religious_interest": 4,
        "budget_level": "medium",
        "max_entry_fee": 30,
        "tempo": "fast",
        "preferred_visit_time": "any",
        "rainy_weather": False,
        "hot_weather": False,
        "family_friendly_required": False,
        "free_place_preference": 5,
    },

    "slow_relaxed_traveler": {
        "history_interest": 5,
        "museum_interest": 7,
        "art_interest": 7,
        "architecture_interest": 5,
        "photography_interest": 6,
        "nature_interest": 7,
        "gastronomy_interest": 5,
        "shopping_interest": 2,
        "religious_interest": 3,
        "budget_level": "medium",
        "max_entry_fee": 25,
        "tempo": "slow",
        "preferred_visit_time": "afternoon",
        "rainy_weather": False,
        "hot_weather": False,
        "family_friendly_required": False,
        "free_place_preference": 5,
    },

    "rainy_weather": {
        "history_interest": 5,
        "museum_interest": 9,
        "art_interest": 8,
        "architecture_interest": 6,
        "photography_interest": 3,
        "nature_interest": 1,
        "gastronomy_interest": 3,
        "shopping_interest": 3,
        "religious_interest": 4,
        "budget_level": "medium",
        "max_entry_fee": 30,
        "tempo": "normal",
        "preferred_visit_time": "any",
        "rainy_weather": True,
        "hot_weather": False,
        "family_friendly_required": False,
        "free_place_preference": 4,
    },

    "shopping_city_life": {
        "history_interest": 2,
        "museum_interest": 2,
        "art_interest": 4,
        "architecture_interest": 5,
        "photography_interest": 7,
        "nature_interest": 1,
        "gastronomy_interest": 7,
        "shopping_interest": 10,
        "religious_interest": 1,
        "budget_level": "high",
        "max_entry_fee": 60,
        "tempo": "normal",
        "preferred_visit_time": "evening",
        "rainy_weather": False,
        "hot_weather": False,
        "family_friendly_required": False,
        "free_place_preference": 1,
    },
}


def calculate_category_distribution(
    recommendations_df: pd.DataFrame,
) -> str:
    category_counts = (
        recommendations_df["category"]
        .value_counts()
        .to_dict()
    )

    return ", ".join(
        f"{category}: {count}"
        for category, count in category_counts.items()
    )


def build_scenario_summary(
    profile_name: str,
    recommendations_df: pd.DataFrame,
) -> dict[str, Any]:
    free_location_count = int(
        (
            recommendations_df["entry_fee_adult"] == 0
        ).sum()
    )

    affordable_location_count = int(
        recommendations_df["is_affordable"].sum()
    )

    top_location = str(
        recommendations_df.iloc[0]["location_name"]
    )

    top_score = float(
        recommendations_df.iloc[0][
            "predicted_suitability_score"
        ]
    )

    return {
        "profile_name": profile_name,
        "top_location": top_location,
        "top_score": round(top_score, 2),
        "average_top10_score": round(
            float(
                recommendations_df[
                    "predicted_suitability_score"
                ].mean()
            ),
            2,
        ),
        "minimum_top10_score": round(
            float(
                recommendations_df[
                    "predicted_suitability_score"
                ].min()
            ),
            2,
        ),
        "maximum_top10_score": round(
            float(
                recommendations_df[
                    "predicted_suitability_score"
                ].max()
            ),
            2,
        ),
        "free_location_count": free_location_count,
        "affordable_location_count": (
            affordable_location_count
        ),
        "average_entry_fee": round(
            float(
                recommendations_df[
                    "entry_fee_adult"
                ].mean()
            ),
            2,
        ),
        "average_visit_duration": round(
            float(
                recommendations_df[
                    "average_visit_duration_min"
                ].mean()
            ),
            2,
        ),
        "category_distribution": (
            calculate_category_distribution(
                recommendations_df
            )
        ),
    }


def calculate_top_k_similarity(
    first_df: pd.DataFrame,
    second_df: pd.DataFrame,
    top_k: int = 10,
) -> dict[str, Any]:
    first_locations = set(
        first_df.head(top_k)[
            "location_id"
        ].tolist()
    )

    second_locations = set(
        second_df.head(top_k)[
            "location_id"
        ].tolist()
    )

    shared_locations = (
        first_locations.intersection(
            second_locations
        )
    )

    union_locations = (
        first_locations.union(
            second_locations
        )
    )

    overlap_ratio = (
        len(shared_locations) / top_k
    )

    jaccard_similarity = (
        len(shared_locations)
        / len(union_locations)
        if union_locations
        else 0
    )

    return {
        "shared_location_count": len(
            shared_locations
        ),
        "top10_overlap_ratio": round(
            overlap_ratio,
            4,
        ),
        "jaccard_similarity": round(
            jaccard_similarity,
            4,
        ),
    }


def create_similarity_matrix(
    scenario_results: dict[
        str,
        pd.DataFrame,
    ],
) -> pd.DataFrame:
    profile_names = list(
        scenario_results.keys()
    )

    matrix_data = []

    for first_profile in profile_names:
        row = {
            "profile_name": first_profile,
        }

        for second_profile in profile_names:
            if first_profile == second_profile:
                similarity = 1.0
            else:
                similarity_result = (
                    calculate_top_k_similarity(
                        scenario_results[
                            first_profile
                        ],
                        scenario_results[
                            second_profile
                        ],
                    )
                )

                similarity = (
                    similarity_result[
                        "top10_overlap_ratio"
                    ]
                )

            row[second_profile] = similarity

        matrix_data.append(row)

    return pd.DataFrame(matrix_data)


def main() -> None:
    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    scenario_results: dict[
        str,
        pd.DataFrame,
    ] = {}

    all_recommendation_frames = []
    summary_rows = []

    print("=" * 100)
    print("KULLANICI SENARYOSU TESTLERİ")
    print("=" * 100)

    for profile_name, user_profile in (
        USER_SCENARIOS.items()
    ):
        recommendations_df = (
            predict_recommendations(
                user_profile=user_profile,
                top_n=10,
            )
        )

        recommendations_df.insert(
            0,
            "profile_name",
            profile_name,
        )

        scenario_results[
            profile_name
        ] = recommendations_df.copy()

        all_recommendation_frames.append(
            recommendations_df
        )

        summary = build_scenario_summary(
            profile_name,
            recommendations_df,
        )

        summary_rows.append(summary)

        print("\n" + "-" * 100)
        print(f"PROFİL: {profile_name}")
        print("-" * 100)

        print(
            recommendations_df[
                [
                    "recommendation_rank",
                    "location_name",
                    "category",
                    "predicted_suitability_score",
                    "entry_fee_adult",
                ]
            ].to_string(
                index=False
            )
        )

        print(
            "\nÖzet:"
            f"\n- Birinci öneri: "
            f"{summary['top_location']}"
            f"\n- Birinci öneri puanı: "
            f"{summary['top_score']}"
            f"\n- Ortalama Top 10 puanı: "
            f"{summary['average_top10_score']}"
            f"\n- Ücretsiz lokasyon: "
            f"{summary['free_location_count']}"
            f"\n- Ortalama giriş ücreti: "
            f"{summary['average_entry_fee']} EUR"
        )

    all_recommendations_df = pd.concat(
        all_recommendation_frames,
        ignore_index=True,
    )

    summary_df = pd.DataFrame(
        summary_rows
    )

    similarity_rows = []

    for (
        first_profile,
        second_profile,
    ) in combinations(
        USER_SCENARIOS.keys(),
        2,
    ):
        similarity = (
            calculate_top_k_similarity(
                scenario_results[
                    first_profile
                ],
                scenario_results[
                    second_profile
                ],
            )
        )

        similarity_rows.append(
            {
                "first_profile": (
                    first_profile
                ),
                "second_profile": (
                    second_profile
                ),
                **similarity,
            }
        )

    similarity_df = pd.DataFrame(
        similarity_rows
    )

    similarity_matrix_df = (
        create_similarity_matrix(
            scenario_results
        )
    )

    all_recommendations_df.to_csv(
        SCENARIO_RESULTS_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    summary_df.to_csv(
        SCENARIO_SUMMARY_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    similarity_df.to_csv(
        PROFILE_SIMILARITY_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    similarity_matrix_df.to_csv(
        PROFILE_SIMILARITY_MATRIX_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    average_similarity = round(
        float(
            similarity_df[
                "top10_overlap_ratio"
            ].mean()
        ),
        4,
    )

    minimum_similarity_row = (
        similarity_df.sort_values(
            by="top10_overlap_ratio",
            ascending=True,
        ).iloc[0]
    )

    maximum_similarity_row = (
        similarity_df.sort_values(
            by="top10_overlap_ratio",
            ascending=False,
        ).iloc[0]
    )

    unique_top_locations = (
        summary_df[
            "top_location"
        ].nunique()
    )

    report_payload = {
        "scenario_count": len(
            USER_SCENARIOS
        ),
        "top_n": 10,
        "unique_top_location_count": int(
            unique_top_locations
        ),
        "average_profile_similarity": (
            average_similarity
        ),
        "most_different_profiles": {
            "first_profile": str(
                minimum_similarity_row[
                    "first_profile"
                ]
            ),
            "second_profile": str(
                minimum_similarity_row[
                    "second_profile"
                ]
            ),
            "top10_overlap_ratio": float(
                minimum_similarity_row[
                    "top10_overlap_ratio"
                ]
            ),
        },
        "most_similar_profiles": {
            "first_profile": str(
                maximum_similarity_row[
                    "first_profile"
                ]
            ),
            "second_profile": str(
                maximum_similarity_row[
                    "second_profile"
                ]
            ),
            "top10_overlap_ratio": float(
                maximum_similarity_row[
                    "top10_overlap_ratio"
                ]
            ),
        },
        "scenario_summaries": (
            summary_df.to_dict(
                orient="records"
            )
        ),
    }

    with SCENARIO_REPORT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report_payload,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print("\n" + "=" * 100)
    print("GENEL KİŞİSELLEŞTİRME SONUCU")
    print("=" * 100)

    print(
        f"Test edilen profil: "
        f"{len(USER_SCENARIOS)}"
    )

    print(
        f"Farklı birinci öneri sayısı: "
        f"{unique_top_locations}"
    )

    print(
        f"Ortalama Top-10 profil benzerliği: "
        f"{average_similarity:.4f}"
    )

    print(
        "En farklı profiller: "
        f"{minimum_similarity_row['first_profile']} "
        "ve "
        f"{minimum_similarity_row['second_profile']} "
        f"({minimum_similarity_row['top10_overlap_ratio']:.4f})"
    )

    print(
        "En benzer profiller: "
        f"{maximum_similarity_row['first_profile']} "
        "ve "
        f"{maximum_similarity_row['second_profile']} "
        f"({maximum_similarity_row['top10_overlap_ratio']:.4f})"
    )

    print("\nProfil özetleri:")

    print(
        summary_df[
            [
                "profile_name",
                "top_location",
                "top_score",
                "average_top10_score",
                "free_location_count",
                "average_entry_fee",
            ]
        ].to_string(
            index=False
        )
    )

    print("\nOluşturulan dosyalar:")
    print(f"- {SCENARIO_RESULTS_PATH}")
    print(f"- {SCENARIO_SUMMARY_PATH}")
    print(f"- {PROFILE_SIMILARITY_PATH}")
    print(f"- {PROFILE_SIMILARITY_MATRIX_PATH}")
    print(f"- {SCENARIO_REPORT_PATH}")


if __name__ == "__main__":
    main()
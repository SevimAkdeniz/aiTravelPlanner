from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

import create_itinerary as itinerary_module
from predict import predict_recommendations


REPORTS_DIR = Path("reports/itinerary_scenarios")

SUMMARY_CSV_PATH = (
    REPORTS_DIR / "itinerary_scenario_summary.csv"
)

SUMMARY_JSON_PATH = (
    REPORTS_DIR / "itinerary_scenario_summary.json"
)

ALL_PLANS_PATH = (
    REPORTS_DIR / "all_itinerary_scenarios.csv"
)


SCENARIOS: dict[str, dict[str, Any]] = {
    "history_architecture": {
        "user_profile": {
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
        "trip": {
            "trip_days": 3,
            "start_time": "09:30",
            "end_time": "18:30",
            "lunch_start": "12:30",
            "lunch_break_min": 60,
            "maximum_total_entry_fee": 120,
            "minimum_suitability_score": 55,
            "max_locations_per_day": 5,
        },
    },

    "free_low_budget": {
        "user_profile": {
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
        "trip": {
            "trip_days": 3,
            "start_time": "09:30",
            "end_time": "18:00",
            "lunch_start": "12:30",
            "lunch_break_min": 60,
            "maximum_total_entry_fee": 0,
            "minimum_suitability_score": 50,
            "max_locations_per_day": 5,
        },
    },

    "nature_photography": {
        "user_profile": {
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
        "trip": {
            "trip_days": 2,
            "start_time": "10:00",
            "end_time": "19:30",
            "lunch_start": "13:00",
            "lunch_break_min": 75,
            "maximum_total_entry_fee": 30,
            "minimum_suitability_score": 50,
            "max_locations_per_day": 4,
        },
    },

    "gastronomy_evening": {
        "user_profile": {
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
        "trip": {
            "trip_days": 2,
            "start_time": "11:00",
            "end_time": "21:00",
            "lunch_start": "14:00",
            "lunch_break_min": 75,
            "maximum_total_entry_fee": 50,
            "minimum_suitability_score": 50,
            "max_locations_per_day": 5,
        },
    },

    "family_with_children": {
        "user_profile": {
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
        "trip": {
            "trip_days": 3,
            "start_time": "09:30",
            "end_time": "17:30",
            "lunch_start": "12:30",
            "lunch_break_min": 90,
            "maximum_total_entry_fee": 100,
            "minimum_suitability_score": 50,
            "max_locations_per_day": 3,
        },
    },

    "fast_first_time_visitor": {
        "user_profile": {
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
        "trip": {
            "trip_days": 2,
            "start_time": "08:30",
            "end_time": "20:00",
            "lunch_start": "13:00",
            "lunch_break_min": 45,
            "maximum_total_entry_fee": 100,
            "minimum_suitability_score": 50,
            "max_locations_per_day": 6,
        },
    },
}


DEFAULT_TRIP_SETTINGS = {
    "city": "Rome",
    "route_distance_factor": 1.25,
    "walking_speed_kmh": 4.5,
    "minimum_travel_buffer_min": 10,
    "start_latitude": None,
    "start_longitude": None,
}


def configure_trip(
    trip_settings: dict[str, Any],
) -> None:
    configured_trip = {
        **DEFAULT_TRIP_SETTINGS,
        **trip_settings,
    }

    itinerary_module.USER_TRIP.clear()
    itinerary_module.USER_TRIP.update(
        configured_trip
    )


def build_summary(
    scenario_name: str,
    itinerary_df: pd.DataFrame,
    skipped_df: pd.DataFrame,
    trip_settings: dict[str, Any],
) -> dict[str, Any]:
    if itinerary_df.empty:
        return {
            "scenario_name": scenario_name,
            "trip_days": trip_settings["trip_days"],
            "planned_day_count": 0,
            "planned_location_count": 0,
            "total_entry_fee": 0,
            "total_route_km": 0,
            "average_suitability_score": 0,
            "skipped_location_count": len(skipped_df),
            "first_location": "",
            "last_location": "",
        }

    location_rows = itinerary_df[
        itinerary_df["item_type"] == "location"
    ].copy()

    return {
        "scenario_name": scenario_name,
        "trip_days": trip_settings["trip_days"],
        "planned_day_count": int(
            location_rows["day"].nunique()
        ),
        "planned_location_count": int(
            len(location_rows)
        ),
        "total_entry_fee": round(
            float(
                location_rows[
                    "entry_fee_adult"
                ].sum()
            ),
            2,
        ),
        "maximum_total_entry_fee": (
            trip_settings[
                "maximum_total_entry_fee"
            ]
        ),
        "total_route_km": round(
            float(
                location_rows[
                    "distance_from_previous_km"
                ].sum()
            ),
            2,
        ),
        "total_travel_minutes": int(
            location_rows[
                "travel_from_previous_min"
            ].sum()
        ),
        "average_suitability_score": round(
            float(
                location_rows[
                    "predicted_suitability_score"
                ].mean()
            ),
            2,
        ),
        "skipped_location_count": int(
            len(skipped_df)
        ),
        "first_location": str(
            location_rows.iloc[0][
                "location_name"
            ]
        ),
        "last_location": str(
            location_rows.iloc[-1][
                "location_name"
            ]
        ),
    }


def validate_scenario(
    summary: dict[str, Any],
) -> list[str]:
    warnings = []

    if (
        summary["total_entry_fee"]
        > summary["maximum_total_entry_fee"]
    ):
        warnings.append(
            "Toplam giriş ücreti bütçeyi aşıyor."
        )

    if (
        summary["planned_day_count"]
        > summary["trip_days"]
    ):
        warnings.append(
            "Planlanan gün sayısı seyahat gününü aşıyor."
        )

    if summary["planned_location_count"] == 0:
        warnings.append(
            "Hiç lokasyon planlanamadı."
        )

    if (
        summary["planned_day_count"]
        < summary["trip_days"]
    ):
        warnings.append(
            "Seyahatin tüm günleri doldurulamadı."
        )

    return warnings


def main() -> None:
    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary_rows = []
    all_plan_frames = []
    json_results = []

    print("=" * 110)
    print("V2 PLANLAMA SENARYOSU TESTLERİ")
    print("=" * 110)

    for scenario_name, scenario in (
        SCENARIOS.items()
    ):
        user_profile = scenario[
            "user_profile"
        ]

        trip_settings = scenario[
            "trip"
        ]

        configure_trip(
            trip_settings
        )

        recommendations_df = (
            predict_recommendations(
                user_profile=user_profile,
                top_n=40,
            )
        )

        candidates_df = (
            itinerary_module.filter_candidates(
                recommendations_df
            )
        )

        itinerary_df, skipped_df = (
            itinerary_module.create_itinerary(
                candidates_df
            )
        )

        scenario_directory = (
            REPORTS_DIR / scenario_name
        )

        scenario_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        itinerary_output_path = (
            scenario_directory
            / "itinerary.csv"
        )

        itinerary_excel_path = (
            scenario_directory
            / "itinerary.xlsx"
        )

        skipped_output_path = (
            scenario_directory
            / "skipped.csv"
        )

        itinerary_df.to_csv(
            itinerary_output_path,
            index=False,
            encoding="utf-8-sig",
        )

        itinerary_df.to_excel(
            itinerary_excel_path,
            index=False,
        )

        skipped_df.to_csv(
            skipped_output_path,
            index=False,
            encoding="utf-8-sig",
        )

        if not itinerary_df.empty:
            scenario_plan_df = (
                itinerary_df.copy()
            )

            scenario_plan_df.insert(
                0,
                "scenario_name",
                scenario_name,
            )

            all_plan_frames.append(
                scenario_plan_df
            )

        summary = build_summary(
            scenario_name,
            itinerary_df,
            skipped_df,
            trip_settings,
        )

        warnings = validate_scenario(
            summary
        )

        summary["warning_count"] = len(
            warnings
        )

        summary["warnings"] = (
            " | ".join(warnings)
        )

        summary_rows.append(summary)

        json_results.append(
            {
                "scenario_name": (
                    scenario_name
                ),
                "user_profile": (
                    user_profile
                ),
                "trip_settings": (
                    {
                        **DEFAULT_TRIP_SETTINGS,
                        **trip_settings,
                    }
                ),
                "summary": summary,
                "warnings": warnings,
            }
        )

        print("\n" + "-" * 110)
        print(
            f"SENARYO: {scenario_name}"
        )
        print("-" * 110)

        if itinerary_df.empty:
            print(
                "Plan oluşturulamadı."
            )

            continue

        print(
            itinerary_df[
                [
                    "day",
                    "order",
                    "start_time",
                    "end_time",
                    "location_name",
                    "category",
                    "entry_fee_adult",
                    "predicted_suitability_score",
                ]
            ].to_string(
                index=False
            )
        )

        print("\nÖzet:")

        print(
            f"- Gün: "
            f"{summary['planned_day_count']}"
            f"/{summary['trip_days']}"
        )

        print(
            f"- Lokasyon: "
            f"{summary['planned_location_count']}"
        )

        print(
            f"- Giriş ücreti: "
            f"{summary['total_entry_fee']:.2f}"
            f"/{summary['maximum_total_entry_fee']:.2f} EUR"
        )

        print(
            f"- Yaklaşık rota: "
            f"{summary['total_route_km']:.2f} km"
        )

        print(
            f"- Ortalama uygunluk: "
            f"{summary['average_suitability_score']:.2f}"
        )

        if warnings:
            print(
                "- Uyarılar: "
                + " | ".join(warnings)
            )
        else:
            print(
                "- Uyarı: yok"
            )

    summary_df = pd.DataFrame(
        summary_rows
    )

    summary_df.to_csv(
        SUMMARY_CSV_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    if all_plan_frames:
        all_plans_df = pd.concat(
            all_plan_frames,
            ignore_index=True,
        )

        all_plans_df.to_csv(
            ALL_PLANS_PATH,
            index=False,
            encoding="utf-8-sig",
        )

    with SUMMARY_JSON_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            {
                "scenario_count": len(
                    SCENARIOS
                ),
                "results": json_results,
            },
            file,
            ensure_ascii=False,
            indent=2,
        )

    print("\n" + "=" * 110)
    print("GENEL PLANLAMA TEST SONUCU")
    print("=" * 110)

    print(
        summary_df[
            [
                "scenario_name",
                "trip_days",
                "planned_day_count",
                "planned_location_count",
                "total_entry_fee",
                "maximum_total_entry_fee",
                "total_route_km",
                "average_suitability_score",
                "warning_count",
            ]
        ].to_string(
            index=False
        )
    )

    successful_scenarios = int(
        (
            summary_df["warning_count"]
            == 0
        ).sum()
    )

    print(
        "\nBaşarılı senaryo: "
        f"{successful_scenarios}"
        f"/{len(SCENARIOS)}"
    )

    print("\nOluşturulan dosyalar:")
    print(f"- {SUMMARY_CSV_PATH}")
    print(f"- {SUMMARY_JSON_PATH}")
    print(f"- {ALL_PLANS_PATH}")
    print(
        f"- {REPORTS_DIR}\\<senaryo>\\itinerary.csv"
    )
    print(
        f"- {REPORTS_DIR}\\<senaryo>\\itinerary.xlsx"
    )
    print(
        f"- {REPORTS_DIR}\\<senaryo>\\skipped.csv"
    )


if __name__ == "__main__":
    main()
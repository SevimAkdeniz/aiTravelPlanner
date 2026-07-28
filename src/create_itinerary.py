from __future__ import annotations

import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from predict import predict_recommendations


OUTPUT_CSV_PATH = Path(
    "reports/latest_itinerary.csv"
)

OUTPUT_XLSX_PATH = Path(
    "reports/latest_itinerary.xlsx"
)


USER_PROFILE: dict[str, Any] = {
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


USER_TRIP: dict[str, Any] = {
    "city": "Rome",
    "trip_days": 3,

    "start_time": "09:30",
    "end_time": "18:30",

    "lunch_start": "12:30",
    "lunch_break_min": 60,

    "maximum_total_entry_fee": 120,
    "minimum_suitability_score": 55,

    "max_locations_per_day": 5,

    # Kuş uçuşu mesafeyi yaklaşık yürüyüş
    # mesafesine çevirmek için kullanılan katsayı.
    "route_distance_factor": 1.25,

    # Ortalama şehir içi yürüyüş hızı.
    "walking_speed_kmh": 4.5,

    # Her ulaşımın üzerine eklenen hazırlık/geçiş payı.
    "minimum_travel_buffer_min": 10,

    # İlk gün başlangıç noktası verilmezse
    # en yüksek puanlı lokasyonla başlanır.
    "start_latitude": None,
    "start_longitude": None,
}


def safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        if pd.isna(value):
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


def parse_time(
    time_text: str,
) -> datetime:
    return datetime.strptime(
        time_text,
        "%H:%M",
    )


def format_time(
    value: datetime,
) -> str:
    return value.strftime("%H:%M")


def calculate_distance_km(
    latitude_1: float,
    longitude_1: float,
    latitude_2: float,
    longitude_2: float,
) -> float:
    """
    İki koordinat arasındaki kuş uçuşu mesafeyi
    Haversine formülüyle hesaplar.
    """

    latitude_1 = math.radians(
        safe_float(latitude_1)
    )

    longitude_1 = math.radians(
        safe_float(longitude_1)
    )

    latitude_2 = math.radians(
        safe_float(latitude_2)
    )

    longitude_2 = math.radians(
        safe_float(longitude_2)
    )

    earth_radius_km = 6371.0

    latitude_difference = (
        latitude_2 - latitude_1
    )

    longitude_difference = (
        longitude_2 - longitude_1
    )

    haversine_value = (
        math.sin(
            latitude_difference / 2
        ) ** 2
        + math.cos(latitude_1)
        * math.cos(latitude_2)
        * math.sin(
            longitude_difference / 2
        ) ** 2
    )

    central_angle = 2 * math.atan2(
        math.sqrt(haversine_value),
        math.sqrt(
            max(
                0.0,
                1 - haversine_value,
            )
        ),
    )

    return earth_radius_km * central_angle


def calculate_route_distance_km(
    distance_km: float,
) -> float:
    """
    Kuş uçuşu mesafeyi yaklaşık gerçek rota
    mesafesine dönüştürür.
    """

    route_factor = safe_float(
        USER_TRIP.get(
            "route_distance_factor",
            1.25,
        ),
        default=1.25,
    )

    return max(
        0.0,
        distance_km * route_factor,
    )


def calculate_travel_minutes(
    distance_km: float,
) -> int:
    walking_speed = max(
        1.0,
        safe_float(
            USER_TRIP.get(
                "walking_speed_kmh",
                4.5,
            ),
            default=4.5,
        ),
    )

    minimum_buffer = max(
        0,
        int(
            safe_float(
                USER_TRIP.get(
                    "minimum_travel_buffer_min",
                    10,
                )
            )
        ),
    )

    route_distance = (
        calculate_route_distance_km(
            distance_km
        )
    )

    walking_minutes = (
        route_distance
        / walking_speed
        * 60
    )

    return max(
        minimum_buffer,
        int(
            round(
                walking_minutes
                + minimum_buffer
            )
        ),
    )


def calculate_location_priority(
    row: pd.Series,
) -> float:
    suitability_score = safe_float(
        row.get(
            "predicted_suitability_score",
            0,
        )
    )

    interest_match = safe_float(
        row.get(
            "weighted_interest_match",
            0,
        )
    ) * 10

    tempo_match = safe_float(
        row.get(
            "tempo_duration_match",
            0,
        )
    )

    affordability_bonus = (
        5.0
        if int(
            safe_float(
                row.get(
                    "is_affordable",
                    0,
                )
            )
        ) == 1
        else -10.0
    )

    return (
        suitability_score * 0.70
        + interest_match * 0.15
        + tempo_match * 0.10
        + affordability_bonus
    )


def filter_candidates(
    recommendations_df: pd.DataFrame,
) -> pd.DataFrame:
    result = recommendations_df.copy()

    minimum_score = safe_float(
        USER_TRIP.get(
            "minimum_suitability_score",
            0,
        )
    )

    result = result[
        result[
            "predicted_suitability_score"
        ] >= minimum_score
    ].copy()

    result["planning_priority"] = (
        result.apply(
            calculate_location_priority,
            axis=1,
        )
    )

    result = result.sort_values(
        by=[
            "planning_priority",
            "predicted_suitability_score",
        ],
        ascending=[
            False,
            False,
        ],
    ).reset_index(drop=True)

    return result


def choose_day_start_location(
    remaining_df: pd.DataFrame,
    previous_day_last_location: dict[str, Any] | None,
) -> pd.Series:
    if remaining_df.empty:
        raise ValueError(
            "Başlangıç lokasyonu seçilecek aday yok."
        )

    configured_latitude = USER_TRIP.get(
        "start_latitude"
    )

    configured_longitude = USER_TRIP.get(
        "start_longitude"
    )

    if (
        previous_day_last_location is not None
        and configured_latitude is None
        and configured_longitude is None
    ):
        return remaining_df.sort_values(
            by="planning_priority",
            ascending=False,
        ).iloc[0]

    if (
        configured_latitude is None
        or configured_longitude is None
    ):
        return remaining_df.sort_values(
            by="planning_priority",
            ascending=False,
        ).iloc[0]

    scored_candidates = remaining_df.copy()

    scored_candidates[
        "distance_from_start"
    ] = scored_candidates.apply(
        lambda row: calculate_distance_km(
            configured_latitude,
            configured_longitude,
            row["latitude"],
            row["longitude"],
        ),
        axis=1,
    )

    scored_candidates[
        "start_selection_score"
    ] = (
        scored_candidates[
            "planning_priority"
        ]
        - scored_candidates[
            "distance_from_start"
        ] * 4
    )

    return scored_candidates.sort_values(
        by="start_selection_score",
        ascending=False,
    ).iloc[0]


def choose_next_location(
    current_location: dict[str, Any],
    remaining_df: pd.DataFrame,
    current_total_fee: float,
) -> tuple[pd.Series | None, float, int]:
    if remaining_df.empty:
        return None, 0.0, 0

    maximum_total_fee = safe_float(
        USER_TRIP.get(
            "maximum_total_entry_fee",
            float("inf"),
        ),
        default=float("inf"),
    )

    candidate_rows = []

    for index, row in remaining_df.iterrows():
        entry_fee = safe_float(
            row.get(
                "entry_fee_adult",
                0,
            )
        )

        if (
            current_total_fee + entry_fee
            > maximum_total_fee
        ):
            continue

        distance_km = calculate_distance_km(
            current_location["latitude"],
            current_location["longitude"],
            row["latitude"],
            row["longitude"],
        )

        travel_minutes = (
            calculate_travel_minutes(
                distance_km
            )
        )

        route_score = (
            safe_float(
                row.get(
                    "planning_priority",
                    0,
                )
            )
            - distance_km * 5
            - travel_minutes * 0.08
        )

        candidate_rows.append(
            {
                "index": index,
                "distance_km": distance_km,
                "travel_minutes": (
                    travel_minutes
                ),
                "route_score": route_score,
            }
        )

    if not candidate_rows:
        return None, 0.0, 0

    best_candidate = max(
        candidate_rows,
        key=lambda item: item[
            "route_score"
        ],
    )

    selected_row = remaining_df.loc[
        best_candidate["index"]
    ]

    return (
        selected_row,
        float(
            best_candidate[
                "distance_km"
            ]
        ),
        int(
            best_candidate[
                "travel_minutes"
            ]
        ),
    )


def add_lunch_break(
    rows: list[dict[str, Any]],
    day_number: int,
    order_number: int,
    current_time: datetime,
) -> tuple[datetime, int]:
    lunch_duration = int(
        USER_TRIP["lunch_break_min"]
    )

    lunch_end = (
        current_time
        + timedelta(
            minutes=lunch_duration
        )
    )

    rows.append(
        {
            "day": day_number,
            "order": order_number,
            "item_type": "break",
            "start_time": format_time(
                current_time
            ),
            "end_time": format_time(
                lunch_end
            ),
            "location_name": "Lunch Break",
            "category": "break",
            "duration_min": lunch_duration,
            "travel_from_previous_min": 0,
            "distance_from_previous_km": 0,
            "entry_fee_adult": 0,
            "predicted_suitability_score": "",
            "recommendation_reason": (
                "Gün ortasında dinlenme "
                "ve yemek molası."
            ),
        }
    )

    return lunch_end, order_number + 1


def create_itinerary(
    candidates_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    trip_days = int(
        USER_TRIP["trip_days"]
    )

    maximum_locations_per_day = int(
        USER_TRIP[
            "max_locations_per_day"
        ]
    )

    start_time = parse_time(
        USER_TRIP["start_time"]
    )

    end_time = parse_time(
        USER_TRIP["end_time"]
    )

    lunch_start_reference = parse_time(
        USER_TRIP["lunch_start"]
    )

    remaining_df = (
        candidates_df.copy()
        .reset_index(drop=True)
    )

    itinerary_rows: list[
        dict[str, Any]
    ] = []

    skipped_rows: list[
        dict[str, Any]
    ] = []

    total_entry_fee = 0.0

    previous_day_last_location = None

    for day_number in range(
        1,
        trip_days + 1,
    ):
        if remaining_df.empty:
            break

        current_time = start_time
        lunch_added = False
        order_number = 1
        visited_location_count = 0

        start_location = (
            choose_day_start_location(
                remaining_df,
                None,
            )
        )
        current_location = None
        next_location = start_location
        distance_km = 0.0
        travel_minutes = 0

        while (
            next_location is not None
            and visited_location_count
            < maximum_locations_per_day
        ):
            location = next_location.copy()

            duration_min = max(
                15,
                int(
                    safe_float(
                        location.get(
                            "average_visit_duration_min",
                            90,
                        ),
                        default=90,
                    )
                ),
            )

            entry_fee = max(
                0.0,
                safe_float(
                    location.get(
                        "entry_fee_adult",
                        0,
                    )
                ),
            )

            maximum_total_fee = safe_float(
                USER_TRIP.get(
                    "maximum_total_entry_fee",
                    float("inf"),
                ),
                default=float("inf"),
            )

            if (
                total_entry_fee + entry_fee
                > maximum_total_fee
            ):
                skipped_rows.append(
                    {
                        "location_name": (
                            location[
                                "location_name"
                            ]
                        ),
                        "reason": (
                            "Toplam giriş ücreti "
                            "bütçesini aşıyor."
                        ),
                    }
                )

                remaining_df = remaining_df[
                    remaining_df["location_id"]
                    != location["location_id"]
                ].reset_index(drop=True)

                if current_location is None:
                    if remaining_df.empty:
                        break

                    next_location = (
                        choose_day_start_location(
                            remaining_df,
                            previous_day_last_location,
                        )
                    )

                    distance_km = 0.0
                    travel_minutes = 0

                else:
                    (
                        next_location,
                        distance_km,
                        travel_minutes,
                    ) = choose_next_location(
                        current_location,
                        remaining_df,
                        total_entry_fee,
                    )

                continue

            arrival_time = (
                current_time
                + timedelta(
                    minutes=travel_minutes
                )
            )

            lunch_reference = arrival_time.replace(
                hour=lunch_start_reference.hour,
                minute=lunch_start_reference.minute,
            )

            if (
                not lunch_added
                and arrival_time
                >= lunch_reference
            ):
                current_time, order_number = (
                    add_lunch_break(
                        itinerary_rows,
                        day_number,
                        order_number,
                        current_time,
                    )
                )

                lunch_added = True

                arrival_time = (
                    current_time
                    + timedelta(
                        minutes=travel_minutes
                    )
                )

            visit_start = arrival_time

            visit_end = (
                visit_start
                + timedelta(
                    minutes=duration_min
                )
            )

            if visit_end > end_time:
                # Lokasyon yalnızca mevcut güne sığmadı.
                # Sonraki gün tekrar değerlendirilebilmesi için
                # remaining_df listesinden çıkarmıyoruz.
                break
            itinerary_rows.append(
                {
                    "day": day_number,
                    "order": order_number,
                    "item_type": "location",
                    "start_time": format_time(
                        visit_start
                    ),
                    "end_time": format_time(
                        visit_end
                    ),
                    "location_id": int(
                        location[
                            "location_id"
                        ]
                    ),
                    "location_name": (
                        location[
                            "location_name"
                        ]
                    ),
                    "category": location[
                        "category"
                    ],
                    "duration_min": duration_min,
                    "travel_from_previous_min": (
                        travel_minutes
                    ),
                    "distance_from_previous_km": round(
                        calculate_route_distance_km(
                            distance_km
                        ),
                        2,
                    ),
                    "entry_fee_adult": entry_fee,
                    "predicted_suitability_score": (
                        location[
                            "predicted_suitability_score"
                        ]
                    ),
                    "latitude": location[
                        "latitude"
                    ],
                    "longitude": location[
                        "longitude"
                    ],
                    "reservation_required": (
                        location[
                            "reservation_required"
                        ]
                    ),
                    "recommendation_reason": (
                        location[
                            "recommendation_reason"
                        ]
                    ),
                }
            )

            total_entry_fee += entry_fee

            visited_location_count += 1
            order_number += 1

            current_time = visit_end

            current_location = (
                location.to_dict()
            )

            previous_day_last_location = (
                current_location
            )

            remaining_df = remaining_df[
                remaining_df["location_id"]
                != location["location_id"]
            ].reset_index(drop=True)

            (
                next_location,
                distance_km,
                travel_minutes,
            ) = choose_next_location(
                current_location,
                remaining_df,
                total_entry_fee,
            )

        if (
            not lunch_added
            and current_time < end_time
            and visited_location_count > 0
        ):
            lunch_reference = current_time.replace(
                hour=lunch_start_reference.hour,
                minute=lunch_start_reference.minute,
            )

            if current_time >= lunch_reference:
                add_lunch_break(
                    itinerary_rows,
                    day_number,
                    order_number,
                    current_time,
                )

    itinerary_df = pd.DataFrame(
        itinerary_rows
    )

    skipped_df = pd.DataFrame(
        skipped_rows
    )

    return itinerary_df, skipped_df


def print_plan_summary(
    itinerary_df: pd.DataFrame,
) -> None:
    if itinerary_df.empty:
        print(
            "Uygun bir gezi planı "
            "oluşturulamadı."
        )

        return

    location_rows = itinerary_df[
        itinerary_df["item_type"]
        == "location"
    ]

    print("\n" + "=" * 110)
    print("V2 KİŞİSELLEŞTİRİLMİŞ ROMA PLANI")
    print("=" * 110)

    print(
        itinerary_df[
            [
                "day",
                "order",
                "start_time",
                "end_time",
                "location_name",
                "category",
                "duration_min",
                "travel_from_previous_min",
                "distance_from_previous_km",
                "entry_fee_adult",
                "predicted_suitability_score",
            ]
        ].to_string(
            index=False
        )
    )

    print("\nPlan özeti:")

    print(
        "- Planlanan lokasyon: "
        f"{len(location_rows)}"
    )

    print(
        "- Toplam giriş ücreti: "
        f"{location_rows['entry_fee_adult'].sum():.2f} EUR"
    )

    print(
        "- Toplam yaklaşık rota: "
        f"{location_rows['distance_from_previous_km'].sum():.2f} km"
    )

    print(
        "- Ortalama uygunluk puanı: "
        f"{location_rows['predicted_suitability_score'].mean():.2f}"
    )

    print("\nGün bazlı özet:")

    for day_number, day_df in (
        location_rows.groupby("day")
    ):
        print(
            f"- {day_number}. gün: "
            f"{len(day_df)} lokasyon, "
            f"{day_df['entry_fee_adult'].sum():.2f} EUR, "
            f"{day_df['distance_from_previous_km'].sum():.2f} km"
        )


def main() -> None:
    recommendations_df = (
        predict_recommendations(
            user_profile=USER_PROFILE,
            top_n=40,
        )
    )

    candidates_df = filter_candidates(
        recommendations_df
    )

    if candidates_df.empty:
        raise ValueError(
            "Kullanıcı tercihlerine ve minimum "
            "puana uygun lokasyon bulunamadı."
        )

    itinerary_df, skipped_df = (
        create_itinerary(
            candidates_df
        )
    )

    OUTPUT_CSV_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    itinerary_df.to_csv(
        OUTPUT_CSV_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    itinerary_df.to_excel(
        OUTPUT_XLSX_PATH,
        index=False,
    )

    skipped_output_path = (
        OUTPUT_CSV_PATH.parent
        / "latest_itinerary_skipped.csv"
    )

    skipped_df.to_csv(
        skipped_output_path,
        index=False,
        encoding="utf-8-sig",
    )

    print_plan_summary(
        itinerary_df
    )

    print("\nOluşturulan dosyalar:")
    print(f"- {OUTPUT_CSV_PATH}")
    print(f"- {OUTPUT_XLSX_PATH}")
    print(f"- {skipped_output_path}")

    print(
        "\nNot: Açılış-kapanış saatleri "
        "mevcut veri setinde dolu olmadığı için "
        "bu sürümde gerçek saat kontrolü yapılmadı."
    )


if __name__ == "__main__":
    main()
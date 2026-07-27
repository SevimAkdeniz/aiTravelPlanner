import os
import math
import pandas as pd
from datetime import datetime, timedelta


INPUT_PATH = "datasets/master/rome_location_scores_with_area.csv"
OUTPUT_CSV_PATH = "datasets/master/rome_sample_itinerary.csv"
OUTPUT_XLSX_PATH = "datasets/master/rome_sample_itinerary.xlsx"


USER_TRIP = {
    "city": "Rome",
    "trip_days": 3,
    "start_time": "09:30",
    "end_time": "18:30",
    "lunch_break_min": 60,
    "travel_buffer_min": 25,
    "max_locations_per_day": 5,
    "min_suitability_score": 70,
    "include_special_routes": False,
}


def safe_float(value, default=0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except:
        return default


def parse_time(time_text):
    return datetime.strptime(time_text, "%H:%M")


def format_time(dt):
    return dt.strftime("%H:%M")


def calculate_distance_km(lat1, lon1, lat2, lon2):
    """
    Basit haversine mesafe hesabı.
    Gerçek rota değil, kuş uçuşu yaklaşık mesafe.
    """

    lat1 = math.radians(safe_float(lat1))
    lon1 = math.radians(safe_float(lon1))
    lat2 = math.radians(safe_float(lat2))
    lon2 = math.radians(safe_float(lon2))

    earth_radius_km = 6371

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_km * c

def sort_by_route_rules(day_number, day_locations):
    """
    Bazı günler için manuel rota sırası uygular.
    Eğer manuel sırada olmayan lokasyon varsa sona ekler.
    """

    manual_order = {
        1: [
            "Vatican Museums",
            "Sistine Chapel",
            "St. Peter's Basilica",
            "Castel Sant'Angelo",
        ],
        2: [
            "Colosseum",
            "Roman Forum",
            "Palatine Hill",
            "Altare della Patria",
        ],
        3: [
            "Pantheon",
            "Piazza Navona",
            "Trevi Fountain",
            "Spanish Steps",
            "Piazza del Popolo",
            "Trastevere",
        ],
    }

    route_order = manual_order.get(day_number)

    if not route_order:
        return sort_by_nearest_neighbor(day_locations)

    ordered = []
    remaining = day_locations.copy()

    for location_name in route_order:
        match = next(
            (item for item in remaining if item.get("location_name") == location_name),
            None
        )

        if match:
            ordered.append(match)
            remaining.remove(match)

    remaining = sorted(
        remaining,
        key=lambda x: safe_float(x.get("suitability_score", 0)),
        reverse=True
    )

    ordered.extend(remaining)

    return ordered
def select_locations(df, trip_days, max_locations_per_day):
    selected = df[
        df["suitability_score"] >= USER_TRIP["min_suitability_score"]
    ].copy()

    if not USER_TRIP.get("include_special_routes", False):
        selected = selected[
            selected["area_group"] != "appian_way_area"
        ].copy()

    selected = selected.sort_values(
        by="suitability_score",
        ascending=False
    )

    return selected
def distribute_locations_to_days(selected_df, trip_days):
    """
    Gün bazlı bölge seçimi.
    Her gün kendi bölgesinden en iyi lokasyonları alır.
    Böylece Vatikan günü boş kalmaz.
    """

    day_plan_groups = {
        1: ["vatican_area"],
        2: ["ancient_rome", "basilica_route"],
        3: ["historic_center", "trastevere_area", "borghese_north"],
    }

    days = {day: [] for day in range(1, trip_days + 1)}
    used_locations = set()

    for day in range(1, trip_days + 1):
        groups = day_plan_groups.get(day, [])

        day_candidates = selected_df[
            selected_df["area_group"].isin(groups)
        ].copy()

        day_candidates = day_candidates[
            ~day_candidates["location_name"].isin(used_locations)
        ]

        day_candidates = day_candidates.sort_values(
            by="suitability_score",
            ascending=False
        )

        day_candidates = day_candidates.head(USER_TRIP["max_locations_per_day"])

        day_rows = day_candidates.to_dict("records")

        days[day] = day_rows

        for row in day_rows:
            used_locations.add(row["location_name"])


            # Day 2 için Palatine Hill antik Roma rotasında önemli.
    # Eğer seçilmediyse ve veri setinde varsa, daha düşük öncelikli bir item yerine ekle.
    day_2_names = [item.get("location_name") for item in days.get(2, [])]

    if "Palatine Hill" not in day_2_names:
        palatine_row = selected_df[selected_df["location_name"] == "Palatine Hill"]

        if not palatine_row.empty:
            palatine_item = palatine_row.iloc[0].to_dict()

            if len(days[2]) >= USER_TRIP["max_locations_per_day"]:
                days[2] = days[2][:-1]

            days[2].append(palatine_item)

    return days
def create_day_schedule(day_number, locations):
    start_dt = parse_time(USER_TRIP["start_time"])
    end_dt = parse_time(USER_TRIP["end_time"])

    current_time = start_dt
    lunch_added = False

    rows = []

    ordered_locations = sort_by_route_rules(day_number, locations)

    order_no = 1

    for location in ordered_locations:
        duration_min = int(safe_float(location.get("average_visit_duration_min", 90)))

        # Öğle arası: 12:30 civarında bir kere ekle
        if not lunch_added and current_time.hour >= 12:
            lunch_start = current_time
            lunch_end = lunch_start + timedelta(minutes=USER_TRIP["lunch_break_min"])

            rows.append({
                "day": day_number,
                "order": order_no,
                "start_time": format_time(lunch_start),
                "end_time": format_time(lunch_end),
                "location_name": "Lunch Break",
                "category": "break",
                "duration_min": USER_TRIP["lunch_break_min"],
                "entry_fee_adult": 0,
                "suitability_score": "",
                "latitude": "",
                "longitude": "",
                "recommendation_reason": "Gün ortasında dinlenme ve yemek molası.",
            })

            current_time = lunch_end
            order_no += 1
            lunch_added = True

        visit_start = current_time
        visit_end = visit_start + timedelta(minutes=duration_min)

        if visit_end > end_dt:
            continue

        rows.append({
            "day": day_number,
            "order": order_no,
            "start_time": format_time(visit_start),
            "end_time": format_time(visit_end),
            "location_name": location.get("location_name"),
            "category": location.get("category"),
            "duration_min": duration_min,
            "entry_fee_adult": location.get("entry_fee_adult"),
            "budget_level": location.get("budget_level"),
            "suitability_score": location.get("suitability_score"),
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "recommendation_reason": location.get("recommendation_reason"),
        })

        current_time = visit_end + timedelta(minutes=USER_TRIP["travel_buffer_min"])
        order_no += 1

    return rows


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    selected_df = select_locations(
        df,
        USER_TRIP["trip_days"],
        USER_TRIP["max_locations_per_day"]
    )

    days = distribute_locations_to_days(
        selected_df,
        USER_TRIP["trip_days"]
    )

    itinerary_rows = []

    for day_number, locations in days.items():
        day_rows = create_day_schedule(day_number, locations)
        itinerary_rows.extend(day_rows)

    itinerary_df = pd.DataFrame(itinerary_rows)

    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)

    itinerary_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8-sig")
    itinerary_df.to_excel(OUTPUT_XLSX_PATH, index=False)

    print("Örnek gezi planı oluşturuldu.")
    print(f"CSV çıktı: {OUTPUT_CSV_PATH}")
    print(f"Excel çıktı: {OUTPUT_XLSX_PATH}")

    print("\nKullanıcı seyahat bilgisi:")
    print(USER_TRIP)

    print("\nGünlük plan:")
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
                "suitability_score",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
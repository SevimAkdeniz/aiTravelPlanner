from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


GASTRONOMY_PROFILE = {
    "history_interest": 2,
    "museum_interest": 1,
    "art_interest": 2,
    "architecture_interest": 3,
    "photography_interest": 8,
    "nature_interest": 2,
    "gastronomy_interest": 10,
    "shopping_interest": 6,
    "religious_interest": 1,
    "budget_level": "medium",
    "max_entry_fee": 20,
    "tempo": "normal",
    "preferred_visit_time": "evening",
    "rainy_weather": False,
    "hot_weather": False,
    "family_friendly_required": False,
    "free_place_preference": 5,
}


HISTORY_PROFILE = {
    "history_interest": 9,
    "museum_interest": 6,
    "art_interest": 5,
    "architecture_interest": 9,
    "photography_interest": 8,
    "nature_interest": 3,
    "gastronomy_interest": 4,
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


TRIP_SETTINGS = {
    "city": "Rome",
    "trip_days": 3,
    "start_time": "09:30",
    "end_time": "18:30",
    "lunch_start": "12:30",
    "lunch_break_min": 60,
    "maximum_total_entry_fee": 120,
    "minimum_suitability_score": 55,
    "max_locations_per_day": 5,
    "route_distance_factor": 1.25,
    "walking_speed_kmh": 4.5,
    "minimum_travel_buffer_min": 10,
    "start_latitude": None,
    "start_longitude": None,
}


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == (
        "AI Travel Planner API çalışıyor."
    )

    assert body["version"] == "2.0.0"
    assert body["docs"] == "/docs"


def test_health_endpoint() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "healthy"
    assert body["model"] == "location_recommender_v2"
    assert body["city"] == "Rome"


def test_recommendations_endpoint() -> None:
    response = client.post(
        "/api/recommendations",
        json={
            "user_profile": GASTRONOMY_PROFILE,
            "top_n": 5,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["city"] == "Rome"
    assert body["recommendation_count"] == 5
    assert len(body["recommendations"]) == 5

    recommendations = body["recommendations"]

    expected_top_locations = {
        "Trastevere",
        "Piazza Navona",
        "Campo de' Fiori",
    }

    returned_locations = {
        item["location_name"]
        for item in recommendations[:3]
    }

    assert returned_locations == expected_top_locations

    scores = [
        item["predicted_suitability_score"]
        for item in recommendations
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )

    for item in recommendations:
        assert 0 <= (
            item["predicted_suitability_score"]
        ) <= 100

        assert item["recommendation_reason"]
        assert item["location_id"] > 0


def test_recommendations_top_n_validation() -> None:
    response = client.post(
        "/api/recommendations",
        json={
            "user_profile": GASTRONOMY_PROFILE,
            "top_n": 50,
        },
    )

    assert response.status_code == 422


def test_recommendations_interest_validation() -> None:
    invalid_profile = {
        **GASTRONOMY_PROFILE,
        "gastronomy_interest": 15,
    }

    response = client.post(
        "/api/recommendations",
        json={
            "user_profile": invalid_profile,
            "top_n": 5,
        },
    )

    assert response.status_code == 422


def test_itinerary_endpoint() -> None:
    response = client.post(
        "/api/itineraries",
        json={
            "user_profile": HISTORY_PROFILE,
            "trip": TRIP_SETTINGS,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["city"] == "Rome"

    summary = body["summary"]

    assert summary["planned_day_count"] == 3
    assert summary["planned_location_count"] > 0

    assert (
        summary["total_entry_fee"]
        <= summary["maximum_total_entry_fee"]
    )

    assert summary[
        "average_suitability_score"
    ] >= 55

    day_summaries = body["day_summaries"]

    assert len(day_summaries) == 3

    itinerary = body["itinerary"]

    assert len(itinerary) > 0

    location_items = [
        item
        for item in itinerary
        if item["item_type"] == "location"
    ]

    break_items = [
        item
        for item in itinerary
        if item["item_type"] == "break"
    ]

    assert len(location_items) == (
        summary["planned_location_count"]
    )

    assert len(break_items) >= 1

    planned_days = {
        item["day"]
        for item in location_items
    }

    assert planned_days == {1, 2, 3}

    for item in location_items:
        assert item["start_time"]
        assert item["end_time"]

        assert (
            item["predicted_suitability_score"]
            >= 55
        )

        assert item["entry_fee_adult"] >= 0


def test_zero_budget_itinerary() -> None:
    free_profile = {
        **HISTORY_PROFILE,
        "budget_level": "free",
        "max_entry_fee": 0,
        "free_place_preference": 10,
    }

    free_trip = {
        **TRIP_SETTINGS,
        "maximum_total_entry_fee": 0,
        "minimum_suitability_score": 45,
    }

    response = client.post(
        "/api/itineraries",
        json={
            "user_profile": free_profile,
            "trip": free_trip,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["summary"]["total_entry_fee"] == 0

    location_items = [
        item
        for item in body["itinerary"]
        if item["item_type"] == "location"
    ]

    assert location_items

    for item in location_items:
        assert item["entry_fee_adult"] == 0


def test_invalid_trip_time_format() -> None:
    invalid_trip = {
        **TRIP_SETTINGS,
        "start_time": "9:30",
    }

    response = client.post(
        "/api/itineraries",
        json={
            "user_profile": HISTORY_PROFILE,
            "trip": invalid_trip,
        },
    )

    assert response.status_code == 422


def test_invalid_trip_days() -> None:
    invalid_trip = {
        **TRIP_SETTINGS,
        "trip_days": 0,
    }

    response = client.post(
        "/api/itineraries",
        json={
            "user_profile": HISTORY_PROFILE,
            "trip": invalid_trip,
        },
    )

    assert response.status_code == 422
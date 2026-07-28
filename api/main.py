from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src import create_itinerary as itinerary_module
from src.predict import predict_recommendations


app = FastAPI(
    title="AI Travel Planner API",
    description=(
        "Kullanıcı tercihlerine göre Roma lokasyonları önerir "
        "ve kişiselleştirilmiş saatlik gezi planı oluşturur."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserProfileRequest(BaseModel):
    history_interest: int = Field(
        default=5,
        ge=0,
        le=10,
    )
    museum_interest: int = Field(
        default=5,
        ge=0,
        le=10,
    )
    art_interest: int = Field(
        default=5,
        ge=0,
        le=10,
    )
    architecture_interest: int = Field(
        default=5,
        ge=0,
        le=10,
    )
    photography_interest: int = Field(
        default=5,
        ge=0,
        le=10,
    )
    nature_interest: int = Field(
        default=5,
        ge=0,
        le=10,
    )
    gastronomy_interest: int = Field(
        default=5,
        ge=0,
        le=10,
    )
    shopping_interest: int = Field(
        default=5,
        ge=0,
        le=10,
    )
    religious_interest: int = Field(
        default=5,
        ge=0,
        le=10,
    )

    budget_level: Literal[
        "free",
        "low",
        "medium",
        "high",
    ] = "medium"

    max_entry_fee: float = Field(
        default=25,
        ge=0,
    )

    tempo: Literal[
        "fast",
        "normal",
        "slow",
    ] = "normal"

    preferred_visit_time: Literal[
        "any",
        "morning",
        "afternoon",
        "evening",
        "sunset",
        "night",
    ] = "any"

    rainy_weather: bool = False
    hot_weather: bool = False
    family_friendly_required: bool = False

    free_place_preference: int = Field(
        default=5,
        ge=0,
        le=10,
    )


class RecommendationRequest(BaseModel):
    user_profile: UserProfileRequest

    top_n: int = Field(
        default=10,
        ge=1,
        le=40,
    )


class TripSettingsRequest(BaseModel):
    city: str = "Rome"

    trip_days: int = Field(
        default=3,
        ge=1,
        le=14,
    )

    start_time: str = Field(
        default="09:30",
        pattern=r"^\d{2}:\d{2}$",
    )

    end_time: str = Field(
        default="18:30",
        pattern=r"^\d{2}:\d{2}$",
    )

    lunch_start: str = Field(
        default="12:30",
        pattern=r"^\d{2}:\d{2}$",
    )

    lunch_break_min: int = Field(
        default=60,
        ge=0,
        le=180,
    )

    maximum_total_entry_fee: float = Field(
        default=120,
        ge=0,
    )

    minimum_suitability_score: float = Field(
        default=50,
        ge=0,
        le=100,
    )

    max_locations_per_day: int = Field(
        default=5,
        ge=1,
        le=10,
    )

    route_distance_factor: float = Field(
        default=1.25,
        ge=1,
        le=3,
    )

    walking_speed_kmh: float = Field(
        default=4.5,
        gt=0,
        le=15,
    )

    minimum_travel_buffer_min: int = Field(
        default=10,
        ge=0,
        le=120,
    )

    start_latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90,
    )

    start_longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180,
    )


class ItineraryRequest(BaseModel):
    user_profile: UserProfileRequest
    trip: TripSettingsRequest


def dataframe_records(
    dataframe: pd.DataFrame,
) -> list[dict[str, Any]]:
    if dataframe.empty:
        return []

    cleaned_df = dataframe.copy()

    cleaned_df = cleaned_df.where(
        pd.notna(cleaned_df),
        None,
    )

    return cleaned_df.to_dict(
        orient="records"
    )


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "AI Travel Planner API çalışıyor.",
        "version": "2.0.0",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "model": "location_recommender_v2",
        "city": "Rome",
    }


@app.post("/api/recommendations")
def create_recommendations(
    request: RecommendationRequest,
) -> dict[str, Any]:
    try:
        user_profile = (
            request.user_profile.model_dump()
        )

        recommendations_df = (
            predict_recommendations(
                user_profile=user_profile,
                top_n=request.top_n,
            )
        )

        return {
            "city": "Rome",
            "recommendation_count": len(
                recommendations_df
            ),
            "user_profile": user_profile,
            "recommendations": dataframe_records(
                recommendations_df
            ),
        }

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Öneriler oluşturulurken "
                f"bir hata meydana geldi: {error}"
            ),
        ) from error


@app.post("/api/itineraries")
def create_personalized_itinerary(
    request: ItineraryRequest,
) -> dict[str, Any]:
    original_trip_settings = deepcopy(
        itinerary_module.USER_TRIP
    )

    try:
        user_profile = (
            request.user_profile.model_dump()
        )

        trip_settings = (
            request.trip.model_dump()
        )

        itinerary_module.USER_TRIP.clear()
        itinerary_module.USER_TRIP.update(
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

        if candidates_df.empty:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Verilen tercihlere uygun "
                    "planlanabilir lokasyon bulunamadı."
                ),
            )

        itinerary_df, skipped_df = (
            itinerary_module.create_itinerary(
                candidates_df
            )
        )

        if itinerary_df.empty:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Süre ve bütçe şartlarıyla "
                    "bir gezi planı oluşturulamadı."
                ),
            )

        location_rows = itinerary_df[
            itinerary_df["item_type"]
            == "location"
        ].copy()

        day_summaries = []

        for day_number, day_df in (
            location_rows.groupby("day")
        ):
            day_summaries.append(
                {
                    "day": int(day_number),
                    "location_count": int(
                        len(day_df)
                    ),
                    "entry_fee_total": round(
                        float(
                            day_df[
                                "entry_fee_adult"
                            ].sum()
                        ),
                        2,
                    ),
                    "route_distance_km": round(
                        float(
                            day_df[
                                "distance_from_previous_km"
                            ].sum()
                        ),
                        2,
                    ),
                    "travel_minutes": int(
                        day_df[
                            "travel_from_previous_min"
                        ].sum()
                    ),
                    "average_suitability_score": round(
                        float(
                            day_df[
                                "predicted_suitability_score"
                            ].mean()
                        ),
                        2,
                    ),
                }
            )

        summary = {
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
            "total_route_distance_km": round(
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
        }

        return {
            "city": trip_settings["city"],
            "user_profile": user_profile,
            "trip_settings": trip_settings,
            "summary": summary,
            "day_summaries": day_summaries,
            "itinerary": dataframe_records(
                itinerary_df
            ),
            "skipped_locations": (
                dataframe_records(
                    skipped_df
                )
            ),
            "limitations": [
                (
                    "Açılış ve kapanış saatleri "
                    "henüz doğrulanmış veriyle "
                    "kontrol edilmemektedir."
                ),
                (
                    "Ulaşım süreleri gerçek yol "
                    "servisi yerine yaklaşık "
                    "mesafe hesabıyla üretilmektedir."
                ),
            ],
        }

    except HTTPException:
        raise

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Gezi planı oluşturulurken "
                f"bir hata meydana geldi: {error}"
            ),
        ) from error

    finally:
        itinerary_module.USER_TRIP.clear()
        itinerary_module.USER_TRIP.update(
            original_trip_settings
        )
"use client";

import { FormEvent, useState } from "react";

type PlannerMode = "recommendation" | "itinerary" | null;

type Recommendation = {
  recommendation_rank: number;
  location_id: number;
  location_name: string;
  category: string;
  sub_category: string;
  predicted_suitability_score: number;
  entry_fee_adult: number;
  average_visit_duration_min: number;
  recommended_visit_time: string;
  recommendation_reason: string;
};

type ItineraryItem = {
  day: number;
  order: number;
  item_type: "location" | "break";
  start_time: string;
  end_time: string;
  location_id: number | null;
  location_name: string;
  category: string;
  duration_min: number;
  travel_from_previous_min: number;
  distance_from_previous_km: number;
  entry_fee_adult: number;
  predicted_suitability_score: number | string;
  reservation_required: number | null;
  recommendation_reason: string;
};

type ItinerarySummary = {
  planned_day_count: number;
  planned_location_count: number;
  total_entry_fee: number;
  maximum_total_entry_fee: number;
  total_route_distance_km: number;
  total_travel_minutes: number;
  average_suitability_score: number;
};

type DaySummary = {
  day: number;
  location_count: number;
  entry_fee_total: number;
  route_distance_km: number;
  travel_minutes: number;
  average_suitability_score: number;
};

type UserProfile = {
  history_interest: number;
  museum_interest: number;
  art_interest: number;
  architecture_interest: number;
  photography_interest: number;
  nature_interest: number;
  gastronomy_interest: number;
  shopping_interest: number;
  religious_interest: number;
  budget_level: "free" | "low" | "medium" | "high";
  max_entry_fee: number;
  tempo: "slow" | "normal" | "fast";
  preferred_visit_time: "morning" | "afternoon" | "evening" | "any";
  rainy_weather: boolean;
  hot_weather: boolean;
  family_friendly_required: boolean;
  free_place_preference: number;
};

type TripSettings = {
  city: "Rome";
  trip_days: number;
  start_time: string;
  end_time: string;
  lunch_start: string;
  lunch_break_min: number;
  maximum_total_entry_fee: number;
  minimum_suitability_score: number;
  max_locations_per_day: number;
  route_distance_factor: number;
  walking_speed_kmh: number;
  minimum_travel_buffer_min: number;
  start_latitude: number | null;
  start_longitude: number | null;
};

const initialProfile: UserProfile = {
  history_interest: 5,
  museum_interest: 5,
  art_interest: 5,
  architecture_interest: 5,
  photography_interest: 5,
  nature_interest: 5,
  gastronomy_interest: 5,
  shopping_interest: 5,
  religious_interest: 5,
  budget_level: "medium",
  max_entry_fee: 25,
  tempo: "normal",
  preferred_visit_time: "any",
  rainy_weather: false,
  hot_weather: false,
  family_friendly_required: false,
  free_place_preference: 5,
};

const initialTrip: TripSettings = {
  city: "Rome",
  trip_days: 3,
  start_time: "09:30",
  end_time: "18:30",
  lunch_start: "12:30",
  lunch_break_min: 60,
  maximum_total_entry_fee: 120,
  minimum_suitability_score: 55,
  max_locations_per_day: 5,
  route_distance_factor: 1.25,
  walking_speed_kmh: 4.5,
  minimum_travel_buffer_min: 10,
  start_latitude: null,
  start_longitude: null,
};

const interestFields = [
  ["history_interest", "Tarih"],
  ["museum_interest", "Müze"],
  ["art_interest", "Sanat"],
  ["architecture_interest", "Mimari"],
  ["photography_interest", "Fotoğrafçılık"],
  ["nature_interest", "Doğa"],
  ["gastronomy_interest", "Gastronomi"],
  ["shopping_interest", "Alışveriş"],
  ["religious_interest", "Dini yapılar"],
] as const;

export default function Home() {
  const [mode, setMode] = useState<PlannerMode>(null);

  const [profile, setProfile] = useState<UserProfile>(initialProfile);
  const [trip, setTrip] = useState<TripSettings>(initialTrip);
  const [topN, setTopN] = useState(5);

  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [itinerary, setItinerary] = useState<ItineraryItem[]>([]);
  const [summary, setSummary] = useState<ItinerarySummary | null>(null);
  const [daySummaries, setDaySummaries] = useState<DaySummary[]>([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const apiUrl =
    process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  const updateProfile = <K extends keyof UserProfile>(
    key: K,
    value: UserProfile[K],
  ) => {
    setProfile((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const updateTrip = <K extends keyof TripSettings>(
    key: K,
    value: TripSettings[K],
  ) => {
    setTrip((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const resetResults = () => {
    setRecommendations([]);
    setItinerary([]);
    setSummary(null);
    setDaySummaries([]);
    setError("");
  };

  const changeMode = () => {
    setMode(null);
    resetResults();
  };

  const getRecommendations = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setLoading(true);
    setError("");
    setRecommendations([]);

    try {
      const response = await fetch(`${apiUrl}/api/recommendations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_profile: profile,
          top_n: topN,
        }),
      });

      if (!response.ok) {
        throw new Error(`API hatası: ${response.status}`);
      }

      const data = await response.json();

      setRecommendations(data.recommendations || []);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Öneriler alınırken bir hata oluştu.",
      );
    } finally {
      setLoading(false);
    }
  };

  const createItinerary = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setLoading(true);
    setError("");
    setItinerary([]);
    setSummary(null);
    setDaySummaries([]);

    try {
      const response = await fetch(`${apiUrl}/api/itineraries`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_profile: profile,
          trip,
        }),
      });

      if (!response.ok) {
        throw new Error(`API hatası: ${response.status}`);
      }

      const data = await response.json();

      setItinerary(data.itinerary || []);
      setSummary(data.summary || null);
      setDaySummaries(data.day_summaries || []);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Gezi planı oluşturulurken bir hata oluştu.",
      );
    } finally {
      setLoading(false);
    }
  };

  const days = Array.from(
    new Set(
      itinerary
        .filter((item) => item.item_type === "location")
        .map((item) => item.day),
    ),
  );

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 md:px-8">
      <div className="mx-auto max-w-6xl">
        <header className="mb-10 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-blue-600">
            Rome AI Travel Planner
          </p>

          <h1 className="mt-3 text-4xl font-bold text-slate-950 md:text-5xl">
            Roma seyahatini kişiselleştir
          </h1>

          <p className="mx-auto mt-4 max-w-2xl text-slate-600">
            Sana uygun lokasyonları keşfet veya yapay zekâ destekli günlük gezi
            planı oluştur.
          </p>
        </header>

        {mode === null && (
          <section className="mx-auto max-w-4xl">
            <h2 className="mb-6 text-center text-2xl font-bold text-slate-900">
              Ne yapmak istiyorsun?
            </h2>

            <div className="grid gap-5 md:grid-cols-2">
              <button
                type="button"
                onClick={() => setMode("recommendation")}
                className="rounded-3xl border border-slate-200 bg-white p-8 text-left shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
              >
                <div className="text-4xl">✨</div>

                <h3 className="mt-5 text-2xl font-bold text-slate-950">
                  Sadece Öneri Al
                </h3>

                <p className="mt-3 leading-7 text-slate-600">
                  İlgi alanlarına ve bütçene göre Roma&apos;da sana en uygun
                  yerleri keşfet.
                </p>

                <span className="mt-6 inline-block font-semibold text-blue-600">
                  Önerileri keşfet →
                </span>
              </button>

              <button
                type="button"
                onClick={() => setMode("itinerary")}
                className="rounded-3xl border border-slate-200 bg-white p-8 text-left shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
              >
                <div className="text-4xl">🗺️</div>

                <h3 className="mt-5 text-2xl font-bold text-slate-950">
                  Gezi Planı Oluştur
                </h3>

                <p className="mt-3 leading-7 text-slate-600">
                  Tercihlerine göre gün gün ve saat saat kişiselleştirilmiş Roma
                  rotası oluştur.
                </p>

                <span className="mt-6 inline-block font-semibold text-emerald-600">
                  Plan oluşturmaya başla →
                </span>
              </button>
            </div>
          </section>
        )}

        {mode !== null && (
          <>
            <button
              type="button"
              onClick={changeMode}
              className="mb-6 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            >
              ← Seçimi değiştir
            </button>

            {error && (
              <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
                {error}
              </div>
            )}

            <div className="grid gap-8 lg:grid-cols-[430px_1fr]">
              <form
                onSubmit={
                  mode === "recommendation"
                    ? getRecommendations
                    : createItinerary
                }
                className="h-fit rounded-2xl bg-white p-6 shadow-sm"
              >
                <h2 className="text-xl font-bold text-slate-950">
                  Seyahat tercihlerin
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  İlgi seviyelerini 0 ile 10 arasında belirle.
                </p>

                <div className="mt-6 space-y-5">
                  {interestFields.map(([key, label]) => (
                    <label key={key} className="block">
                      <div className="mb-2 flex justify-between">
                        <span className="text-sm font-medium text-slate-700">
                          {label}
                        </span>

                        <span className="rounded-md bg-blue-50 px-2 py-1 text-sm font-bold text-blue-700">
                          {profile[key]}
                        </span>
                      </div>

                      <input
                        type="range"
                        min="0"
                        max="10"
                        step="1"
                        value={profile[key]}
                        onChange={(e) =>
                          updateProfile(key, Number(e.target.value))
                        }
                        className="w-full cursor-pointer accent-blue-600"
                      />
                    </label>
                  ))}
                </div>

                <div className="mt-8 space-y-4 border-t border-slate-200 pt-6">
                  <h3 className="font-bold text-slate-950">
                    Genel tercihler
                  </h3>

                  <label className="block">
                    <span className="mb-2 block text-sm font-medium text-slate-700">
                      Bütçe seviyesi
                    </span>

                    <select
                      value={profile.budget_level}
                      onChange={(e) =>
                        updateProfile(
                          "budget_level",
                          e.target.value as UserProfile["budget_level"],
                        )
                      }
                      className="w-full rounded-lg border border-slate-300 bg-white p-3"
                    >
                      <option value="free">Ücretsiz</option>
                      <option value="low">Düşük bütçe</option>
                      <option value="medium">Orta bütçe</option>
                      <option value="high">Yüksek bütçe</option>
                    </select>
                  </label>

                  <label className="block">
                    <span className="mb-2 block text-sm font-medium text-slate-700">
                      Maksimum tek giriş ücreti (€)
                    </span>

                    <input
                      type="number"
                      min="0"
                      value={profile.max_entry_fee}
                      onChange={(e) =>
                        updateProfile(
                          "max_entry_fee",
                          Number(e.target.value),
                        )
                      }
                      className="w-full rounded-lg border border-slate-300 p-3"
                    />
                  </label>

                  <label className="block">
                    <span className="mb-2 block text-sm font-medium text-slate-700">
                      Gezi temposu
                    </span>

                    <select
                      value={profile.tempo}
                      onChange={(e) =>
                        updateProfile(
                          "tempo",
                          e.target.value as UserProfile["tempo"],
                        )
                      }
                      className="w-full rounded-lg border border-slate-300 bg-white p-3"
                    >
                      <option value="slow">Yavaş ve rahat</option>
                      <option value="normal">Normal</option>
                      <option value="fast">Hızlı</option>
                    </select>
                  </label>

                  <label className="block">
                    <span className="mb-2 block text-sm font-medium text-slate-700">
                      Tercih edilen ziyaret zamanı
                    </span>

                    <select
                      value={profile.preferred_visit_time}
                      onChange={(e) =>
                        updateProfile(
                          "preferred_visit_time",
                          e.target
                            .value as UserProfile["preferred_visit_time"],
                        )
                      }
                      className="w-full rounded-lg border border-slate-300 bg-white p-3"
                    >
                      <option value="any">Fark etmez</option>
                      <option value="morning">Sabah</option>
                      <option value="afternoon">Öğleden sonra</option>
                      <option value="evening">Akşam</option>
                    </select>
                  </label>

                  {mode === "recommendation" && (
                    <label className="block">
                      <span className="mb-2 block text-sm font-medium text-slate-700">
                        Öneri sayısı
                      </span>

                      <select
                        value={topN}
                        onChange={(e) => setTopN(Number(e.target.value))}
                        className="w-full rounded-lg border border-slate-300 bg-white p-3"
                      >
                        <option value={3}>3 öneri</option>
                        <option value={5}>5 öneri</option>
                        <option value={10}>10 öneri</option>
                        <option value={15}>15 öneri</option>
                      </select>
                    </label>
                  )}
                </div>

                <div className="mt-6 space-y-3">
                  <label className="flex items-center gap-3 rounded-lg border border-slate-200 p-3">
                    <input
                      type="checkbox"
                      checked={profile.rainy_weather}
                      onChange={(e) =>
                        updateProfile("rainy_weather", e.target.checked)
                      }
                    />
                    <span className="text-sm text-slate-700">
                      Yağmurlu hava koşullarını dikkate al
                    </span>
                  </label>

                  <label className="flex items-center gap-3 rounded-lg border border-slate-200 p-3">
                    <input
                      type="checkbox"
                      checked={profile.hot_weather}
                      onChange={(e) =>
                        updateProfile("hot_weather", e.target.checked)
                      }
                    />
                    <span className="text-sm text-slate-700">
                      Sıcak hava koşullarını dikkate al
                    </span>
                  </label>

                  <label className="flex items-center gap-3 rounded-lg border border-slate-200 p-3">
                    <input
                      type="checkbox"
                      checked={profile.family_friendly_required}
                      onChange={(e) =>
                        updateProfile(
                          "family_friendly_required",
                          e.target.checked,
                        )
                      }
                    />
                    <span className="text-sm text-slate-700">
                      Aile dostu yerleri önceliklendir
                    </span>
                  </label>
                </div>

                {mode === "itinerary" && (
                  <div className="mt-8 space-y-4 border-t border-slate-200 pt-6">
                    <h3 className="font-bold text-slate-950">
                      Gezi planı ayarları
                    </h3>

                    <label className="block">
                      <span className="mb-2 block text-sm font-medium">
                        Kaç gün?
                      </span>

                      <input
                        type="number"
                        min="1"
                        max="7"
                        value={trip.trip_days}
                        onChange={(e) =>
                          updateTrip("trip_days", Number(e.target.value))
                        }
                        className="w-full rounded-lg border border-slate-300 p-3"
                      />
                    </label>

                    <div className="grid grid-cols-2 gap-3">
                      <label>
                        <span className="mb-2 block text-sm font-medium">
                          Başlangıç
                        </span>

                        <input
                          type="time"
                          value={trip.start_time}
                          onChange={(e) =>
                            updateTrip("start_time", e.target.value)
                          }
                          className="w-full rounded-lg border border-slate-300 p-3"
                        />
                      </label>

                      <label>
                        <span className="mb-2 block text-sm font-medium">
                          Bitiş
                        </span>

                        <input
                          type="time"
                          value={trip.end_time}
                          onChange={(e) =>
                            updateTrip("end_time", e.target.value)
                          }
                          className="w-full rounded-lg border border-slate-300 p-3"
                        />
                      </label>
                    </div>

                    <label className="block">
                      <span className="mb-2 block text-sm font-medium">
                        Öğle molası başlangıcı
                      </span>

                      <input
                        type="time"
                        value={trip.lunch_start}
                        onChange={(e) =>
                          updateTrip("lunch_start", e.target.value)
                        }
                        className="w-full rounded-lg border border-slate-300 p-3"
                      />
                    </label>

                    <label className="block">
                      <span className="mb-2 block text-sm font-medium">
                        Öğle molası süresi
                      </span>

                      <select
                        value={trip.lunch_break_min}
                        onChange={(e) =>
                          updateTrip(
                            "lunch_break_min",
                            Number(e.target.value),
                          )
                        }
                        className="w-full rounded-lg border border-slate-300 bg-white p-3"
                      >
                        <option value={30}>30 dakika</option>
                        <option value={45}>45 dakika</option>
                        <option value={60}>60 dakika</option>
                        <option value={90}>90 dakika</option>
                      </select>
                    </label>

                    <label className="block">
                      <span className="mb-2 block text-sm font-medium">
                        Toplam giriş bütçesi (€)
                      </span>

                      <input
                        type="number"
                        min="0"
                        value={trip.maximum_total_entry_fee}
                        onChange={(e) =>
                          updateTrip(
                            "maximum_total_entry_fee",
                            Number(e.target.value),
                          )
                        }
                        className="w-full rounded-lg border border-slate-300 p-3"
                      />
                    </label>

                    <label className="block">
                      <span className="mb-2 block text-sm font-medium">
                        Günlük maksimum lokasyon
                      </span>

                      <select
                        value={trip.max_locations_per_day}
                        onChange={(e) =>
                          updateTrip(
                            "max_locations_per_day",
                            Number(e.target.value),
                          )
                        }
                        className="w-full rounded-lg border border-slate-300 bg-white p-3"
                      >
                        <option value={3}>3 lokasyon</option>
                        <option value={4}>4 lokasyon</option>
                        <option value={5}>5 lokasyon</option>
                        <option value={6}>6 lokasyon</option>
                      </select>
                    </label>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className={`mt-8 w-full rounded-xl px-5 py-3 font-semibold text-white transition disabled:opacity-60 ${
                    mode === "recommendation"
                      ? "bg-blue-600 hover:bg-blue-700"
                      : "bg-emerald-600 hover:bg-emerald-700"
                  }`}
                >
                  {loading
                    ? "Hazırlanıyor..."
                    : mode === "recommendation"
                      ? "Önerileri oluştur"
                      : "Gezi planı oluştur"}
                </button>
              </form>

              <section>
                {mode === "recommendation" && (
                  <>
                    <h2 className="text-2xl font-bold text-slate-950">
                      Sana özel öneriler
                    </h2>

                    {recommendations.length === 0 && !loading && (
                      <div className="mt-4 rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">
                        Tercihlerini belirleyip önerilerini oluştur.
                      </div>
                    )}

                    <div className="mt-4 space-y-4">
                      {recommendations.map((item) => (
                        <article
                          key={item.location_id}
                          className="rounded-2xl bg-white p-6 shadow-sm"
                        >
                          <div className="flex flex-wrap justify-between gap-4">
                            <div>
                              <span className="font-bold text-blue-600">
                                #{item.recommendation_rank}
                              </span>

                              <h3 className="mt-1 text-2xl font-bold text-slate-950">
                                {item.location_name}
                              </h3>

                              <p className="mt-1 text-sm text-slate-500">
                                {item.category} · {item.sub_category}
                              </p>
                            </div>

                            <div className="rounded-xl bg-emerald-100 px-4 py-3 text-center">
                              <p className="text-xs font-semibold text-emerald-700">
                                Uygunluk
                              </p>

                              <p className="text-2xl font-bold text-emerald-800">
                                {item.predicted_suitability_score}
                              </p>
                            </div>
                          </div>

                          <p className="mt-5 leading-7 text-slate-700">
                            {item.recommendation_reason}
                          </p>

                          <div className="mt-5 flex flex-wrap gap-3 text-sm">
                            <span className="rounded-lg bg-slate-100 px-3 py-2">
                              {item.entry_fee_adult === 0
                                ? "Ücretsiz"
                                : `${item.entry_fee_adult} €`}
                            </span>

                            <span className="rounded-lg bg-slate-100 px-3 py-2">
                              {item.average_visit_duration_min} dk
                            </span>

                            <span className="rounded-lg bg-slate-100 px-3 py-2">
                              {item.recommended_visit_time}
                            </span>
                          </div>
                        </article>
                      ))}
                    </div>
                  </>
                )}

                {mode === "itinerary" && (
                  <>
                    <h2 className="text-2xl font-bold text-slate-950">
                      Kişisel gezi planın
                    </h2>

                    {!summary && !loading && (
                      <div className="mt-4 rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">
                        Tercihlerini ve gezi ayarlarını belirleyip planını
                        oluştur.
                      </div>
                    )}

                    {summary && (
                      <>
                        <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                          <div className="rounded-xl bg-white p-4 shadow-sm">
                            <p className="text-sm text-slate-500">Gün</p>
                            <p className="mt-1 text-2xl font-bold">
                              {summary.planned_day_count}
                            </p>
                          </div>

                          <div className="rounded-xl bg-white p-4 shadow-sm">
                            <p className="text-sm text-slate-500">Lokasyon</p>
                            <p className="mt-1 text-2xl font-bold">
                              {summary.planned_location_count}
                            </p>
                          </div>

                          <div className="rounded-xl bg-white p-4 shadow-sm">
                            <p className="text-sm text-slate-500">
                              Toplam ücret
                            </p>
                            <p className="mt-1 text-2xl font-bold">
                              {summary.total_entry_fee} €
                            </p>
                          </div>

                          <div className="rounded-xl bg-white p-4 shadow-sm">
                            <p className="text-sm text-slate-500">
                              Rota mesafesi
                            </p>
                            <p className="mt-1 text-2xl font-bold">
                              {summary.total_route_distance_km} km
                            </p>
                          </div>
                        </div>

                        <div className="mt-6 space-y-6">
                          {days.map((day) => {
                            const daySummary = daySummaries.find(
                              (item) => item.day === day,
                            );

                            return (
                              <article
                                key={day}
                                className="rounded-2xl bg-white p-6 shadow-sm"
                              >
                                <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
                                  <h3 className="text-2xl font-bold text-slate-950">
                                    {day}. Gün
                                  </h3>

                                  {daySummary && (
                                    <p className="text-sm text-slate-500">
                                      {daySummary.location_count} lokasyon ·{" "}
                                      {daySummary.entry_fee_total} € ·{" "}
                                      {daySummary.route_distance_km} km
                                    </p>
                                  )}
                                </div>

                                <div className="space-y-3">
                                  {itinerary
                                    .filter((item) => item.day === day)
                                    .map((item) => (
                                      <div
                                        key={`${item.day}-${item.order}`}
                                        className={`rounded-xl border p-4 ${
                                          item.item_type === "break"
                                            ? "border-amber-200 bg-amber-50"
                                            : "border-slate-200 bg-slate-50"
                                        }`}
                                      >
                                        <div className="flex flex-wrap items-start justify-between gap-4">
                                          <div>
                                            <p className="text-sm font-semibold text-slate-500">
                                              {item.start_time} –{" "}
                                              {item.end_time}
                                            </p>

                                            <h4 className="mt-1 text-lg font-bold text-slate-950">
                                              {item.item_type === "break"
                                                ? "☕ "
                                                : ""}
                                              {item.location_name}
                                            </h4>
                                          </div>

                                          {item.item_type === "location" && (
                                            <span className="rounded-lg bg-blue-100 px-3 py-1 text-sm font-bold text-blue-700">
                                              {
                                                item.predicted_suitability_score
                                              }
                                            </span>
                                          )}
                                        </div>

                                        {item.item_type === "location" && (
                                          <>
                                            <p className="mt-3 text-sm text-slate-600">
                                              {item.duration_min} dk ziyaret
                                              {item.travel_from_previous_min >
                                                0 &&
                                                ` · ${item.travel_from_previous_min} dk ulaşım`}
                                              {item.entry_fee_adult === 0
                                                ? " · Ücretsiz"
                                                : ` · ${item.entry_fee_adult} €`}
                                            </p>

                                            <p className="mt-3 text-sm leading-6 text-slate-700">
                                              {item.recommendation_reason}
                                            </p>
                                          </>
                                        )}
                                      </div>
                                    ))}
                                </div>
                              </article>
                            );
                          })}
                        </div>
                      </>
                    )}
                  </>
                )}
              </section>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
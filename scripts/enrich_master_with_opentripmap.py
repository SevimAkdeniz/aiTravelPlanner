import os
import re
import pandas as pd
from rapidfuzz import process, fuzz


MASTER_PATH = "datasets/master/rome_master_dataset_v1_locations_placed.csv"
OPENTRIPMAP_PATH = "datasets/raw/rome/opentripmap_rome_raw.csv"

OUTPUT_CSV_PATH = "datasets/master/rome_master_dataset_v1_enriched.csv"
OUTPUT_XLSX_PATH = "datasets/master/rome_master_dataset_v1_enriched.xlsx"


MANUAL_ALIASES = {
    "altare della patria": [
        "monument to vittorio emanuele ii",
        "monumento a vittorio emanuele ii",
    ],
    "borghese gallery": [
        "galleria borghese",
    ],
    "doria pamphilj gallery": [
        "palazzo doria pamphilj",
        "galleria doria pamphilj",
    ],
    "trajan's market": [
        "mercati di traiano",
        "trajan's market",
    ],
    "basilica of saint mary major": [
        "basilica of saint mary major",
        "basilica di santa maria maggiore",
        "santa maria maggiore",
    ],
    "national roman museum": [
        "museo nazionale romano",
        "museum of the baths of diocletian",
        "palazzo massimo alle terme",
    ],
    "piazza venezia": [
        "piazza venezia",
        "palazzo venezia",
    ],
    "piazza barberini": [
        "piazza barberini",
        "fontana del tritone",
        "triton fountain",
    ],
    "spanish steps": [
        "spanish steps",
    ],
    "villa borghese": [
        "villa borghese",
        "villa borghese pinciana",
    ],
    "trevi fountain": [
        "trevi fountain",
        "fontana di trevi",
    ],
    "st peter's basilica": [
        "st peter's basilica",
        "saint peter's basilica",
        "basilica di san pietro",
    ],
    "castel sant'angelo": [
        "castel sant'angelo",
        "castle sant'angelo",
        "mausoleum of hadrian",
    ],
    "capitoline museums": [
        "capitoline museums",
        "musei capitolini",
    ],
    "bath of caracalla": [
        "baths of caracalla",
        "terme di caracalla",
    ],
    "baths of caracalla": [
        "baths of caracalla",
        "terme di caracalla",
    ],
    "circus maximus": [
        "circus maximus",
        "circo massimo",
    ],
    "ara pacis": [
        "ara pacis",
        "museum of the ara pacis",
        "museo dell'ara pacis",
    ],
    "maxxi museum": [
        "maxxi",
        "maxxi museum",
        "museo nazionale delle arti del xxi secolo",
    ],
    "janiculum hill": [
        "janiculum",
        "janiculum hill",
        "gianicolo",
    ],
    "orange garden": [
        "orange garden",
        "giardino degli aranci",
        "parco savello",
    ],
    "mouth of truth": [
        "mouth of truth",
        "bocca della verita",
    ],
    "tiber island": [
        "tiber island",
        "isola tiberina",
    ],
    "appian way": [
        "appian way",
        "via appia antica",
    ],
    "catacombs of san callisto": [
        "catacombs of san callisto",
        "catacombe di san callisto",
    ],
    "basilica of saint john lateran": [
        "basilica of saint john lateran",
        "archbasilica of saint john lateran",
        "san giovanni in laterano",
    ],
    "basilica of saint paul outside the walls": [
        "basilica of saint paul outside the walls",
        "basilica di san paolo fuori le mura",
        "san paolo fuori le mura",
    ],
    "pincian hill": [
        "pincian hill",
        "pincio",
    ],
    "piazza della rotonda": [
        "piazza della rotonda",
    ],
    "largo di torre argentina": [
        "largo di torre argentina",
        "torre argentina",
    ],
}


def normalize_name(value):
    if pd.isna(value):
        return ""

    value = str(value).lower().strip()
    value = value.replace("’", "'")
    value = value.replace("`", "'")
    value = value.replace("´", "'")
    value = value.replace(".", "")
    value = re.sub(r"\(.*?\)", "", value)
    value = re.sub(r"[^a-z0-9\s']", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def find_best_match(master_name, otm_df):
    normalized_master = normalize_name(master_name)

    search_terms = [normalized_master]

    if normalized_master in MANUAL_ALIASES:
        search_terms.extend(MANUAL_ALIASES[normalized_master])

    search_terms = [normalize_name(x) for x in search_terms]

    best_row = None
    best_score = 0
    best_match_name = None

    # 1. Önce exact match dene
    for term in search_terms:
        exact_matches = otm_df[otm_df["otm_match_name"] == term]

        if not exact_matches.empty:
            exact_matches = exact_matches.copy()
            exact_matches["rate_num"] = pd.to_numeric(
                exact_matches["opentripmap_rate"],
                errors="coerce"
            ).fillna(0)

            exact_matches["is_relation"] = exact_matches["source_osm_id"].astype(str).str.startswith("relation/").astype(int)

            exact_matches = exact_matches.sort_values(
                by=["is_relation", "rate_num"],
                ascending=[False, False]
            )

            best_row = exact_matches.iloc[0]
            best_score = 100
            best_match_name = best_row["otm_match_name"]
            return best_row, best_match_name, best_score

    # 2. Exact yoksa fuzzy match dene
    otm_names = otm_df["otm_match_name"].dropna().unique().tolist()

    for term in search_terms:
        result = process.extractOne(
            term,
            otm_names,
            scorer=fuzz.token_sort_ratio
        )

        if result:
            matched_name, score, _ = result

            if score > best_score:
                candidates = otm_df[otm_df["otm_match_name"] == matched_name].copy()

                candidates["rate_num"] = pd.to_numeric(
                    candidates["opentripmap_rate"],
                    errors="coerce"
                ).fillna(0)

                candidates["is_relation"] = candidates["source_osm_id"].astype(str).str.startswith("relation/").astype(int)

                candidates = candidates.sort_values(
                    by=["is_relation", "rate_num"],
                    ascending=[False, False]
                )

                best_row = candidates.iloc[0]
                best_score = score
                best_match_name = matched_name

    return best_row, best_match_name, best_score


def main():
    if not os.path.exists(MASTER_PATH):
        raise FileNotFoundError(f"Master dosyası bulunamadı: {MASTER_PATH}")

    if not os.path.exists(OPENTRIPMAP_PATH):
        raise FileNotFoundError(f"OpenTripMap dosyası bulunamadı: {OPENTRIPMAP_PATH}")

    master_df = pd.read_csv(MASTER_PATH)
    otm_df = pd.read_csv(OPENTRIPMAP_PATH)

    otm_df["otm_match_name"] = otm_df["location_name"].apply(normalize_name)
    otm_df = otm_df[otm_df["otm_match_name"] != ""].copy()

    enriched_rows = []

    for _, row in master_df.iterrows():
        row = row.copy()
        master_name = row.get("location_name", "")

        match_row, matched_name, score = find_best_match(master_name, otm_df)

        row["opentripmap_match_name"] = matched_name
        row["opentripmap_match_score"] = score

        if match_row is not None and score >= 80:
            row["source_opentripmap_id"] = match_row.get("source_opentripmap_id")
            row["source_osm_id"] = match_row.get("source_osm_id")
            row["source_wikidata_id"] = match_row.get("source_wikidata_id")
            row["latitude"] = match_row.get("latitude")
            row["longitude"] = match_row.get("longitude")
            row["category_raw"] = match_row.get("category_raw")
            row["opentripmap_rate"] = match_row.get("opentripmap_rate")
            row["popularity_score"] = match_row.get("popularity_score")
            row["data_source"] = "OpenTripMap"

            if score >= 95:
                row["opentripmap_match_status"] = "strong_match"
            else:
                row["opentripmap_match_status"] = "possible_match"
        else:
            row["source_opentripmap_id"] = ""
            row["source_osm_id"] = ""
            row["source_wikidata_id"] = ""
            row["category_raw"] = ""
            row["opentripmap_rate"] = ""
            row["popularity_score"] = ""
            row["data_source"] = ""
            row["opentripmap_match_status"] = "not_matched"

        enriched_rows.append(row)

    enriched_df = pd.DataFrame(enriched_rows)

    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)

    enriched_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8-sig")
    enriched_df.to_excel(OUTPUT_XLSX_PATH, index=False)

    total = len(enriched_df)
    strong = len(enriched_df[enriched_df["opentripmap_match_status"] == "strong_match"])
    possible = len(enriched_df[enriched_df["opentripmap_match_status"] == "possible_match"])
    not_matched = len(enriched_df[enriched_df["opentripmap_match_status"] == "not_matched"])

    print("Eşleştirme tamamlandı.")
    print(f"Toplam lokasyon: {total}")
    print(f"Güçlü eşleşme: {strong}")
    print(f"Olası eşleşme: {possible}")
    print(f"Eşleşmeyen: {not_matched}")
    print(f"CSV çıktı: {OUTPUT_CSV_PATH}")
    print(f"Excel çıktı: {OUTPUT_XLSX_PATH}")

    print("\nKontrol tablosu:")
    print(
        enriched_df[
            [
                "location_name",
                "opentripmap_match_name",
                "opentripmap_match_score",
                "opentripmap_match_status",
                "source_opentripmap_id",
                "source_wikidata_id",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
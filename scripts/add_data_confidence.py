import os
import pandas as pd


INPUT_PATH = "datasets/master/rome_master_dataset_v1_planning_ready.csv"

OUTPUT_CSV_PATH = "datasets/master/rome_master_dataset_v1_planning_ready_with_confidence.csv"
OUTPUT_XLSX_PATH = "datasets/master/rome_master_dataset_v1_planning_ready_with_confidence.xlsx"


def determine_identity_source(row):
    data_source = str(row.get("data_source", "")).lower()

    if "opentripmap" in data_source:
        return "OpenTripMap"
    elif "wikidata" in data_source:
        return "Wikidata, Manual"
    else:
        return "Manual"


def determine_confidence_level(row):
    match_status = str(row.get("opentripmap_match_status", "")).lower()

    if match_status == "strong_match":
        return "high"
    elif match_status == "possible_match":
        return "medium"
    elif match_status == "manual_match":
        return "medium"
    else:
        return "low"


def determine_needs_verification(row):
    return True


def determine_verification_note(row):
    notes = []

    data_source = str(row.get("data_source", "")).lower()
    match_status = str(row.get("opentripmap_match_status", "")).lower()

    if "opentripmap" in data_source:
        notes.append("Identity and coordinates are sourced from OpenTripMap.")
    elif "wikidata" in data_source:
        notes.append("Identity and coordinates are manually completed using Wikidata.")
    else:
        notes.append("Identity source requires verification.")

    if match_status == "possible_match":
        notes.append("OpenTripMap match should be manually reviewed.")

    notes.append("Entry fee, visit duration, opening hours and interest scores are V1 draft planning features.")
    notes.append("These fields should be verified with official websites, Google Places API or user feedback in later versions.")

    return " ".join(notes)


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    df["location_identity_source"] = df.apply(determine_identity_source, axis=1)

    df["coordinate_source"] = df["location_identity_source"]

    df["planning_feature_source"] = "rule_based_v1_draft"

    df["fee_data_source"] = "draft_manual_needs_official_verification"

    df["opening_hours_source"] = "not_collected_yet"

    df["interest_scores_source"] = "rule_based_feature_engineering_v1"

    df["google_rating_source"] = "not_collected_yet"

    df["data_confidence_level"] = df.apply(determine_confidence_level, axis=1)

    df["needs_verification"] = df.apply(determine_needs_verification, axis=1)

    df["verification_note"] = df.apply(determine_verification_note, axis=1)

    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)

    df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8-sig")
    df.to_excel(OUTPUT_XLSX_PATH, index=False)

    print("Veri güven / kaynak kolonları eklendi.")
    print(f"CSV çıktı: {OUTPUT_CSV_PATH}")
    print(f"Excel çıktı: {OUTPUT_XLSX_PATH}")
    print(f"Toplam kolon: {len(df.columns)}")
    print(f"Toplam lokasyon: {len(df)}")

    print("\nGüven seviyesi özeti:")
    print(df["data_confidence_level"].value_counts())

    print("\nKaynak özeti:")
    print(df["location_identity_source"].value_counts())

    print("\nKontrol:")
    print(
        df[
            [
                "location_name",
                "opentripmap_match_status",
                "location_identity_source",
                "planning_feature_source",
                "fee_data_source",
                "interest_scores_source",
                "data_confidence_level",
                "needs_verification",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
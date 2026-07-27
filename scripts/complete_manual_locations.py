import os
import pandas as pd


INPUT_PATH = "datasets/master/rome_master_dataset_v1_enriched_by_name.csv"

OUTPUT_CSV_PATH = "datasets/master/rome_master_dataset_v1_final.csv"
OUTPUT_XLSX_PATH = "datasets/master/rome_master_dataset_v1_final.xlsx"


MANUAL_DATA = {
    "Piazza Navona": {
        "source_opentripmap_id": "",
        "source_osm_id": "",
        "source_wikidata_id": "Q463400",
        "latitude": 41.8989816,
        "longitude": 12.4731439,
        "category_raw": "historic,architecture,cultural,urban_environment,squares",
        "opentripmap_rate": "",
        "popularity_score": "",
        "data_source": "Wikidata, Manual",
        "opentripmap_match_name": "Manual: Piazza Navona",
        "opentripmap_match_score": 100,
        "opentripmap_match_status": "manual_match",
    },

    "Campo de' Fiori": {
        "source_opentripmap_id": "",
        "source_osm_id": "",
        "source_wikidata_id": "Q28303",
        "latitude": 41.8956638,
        "longitude": 12.4720465,
        "category_raw": "historic,cultural,urban_environment,squares,marketplace",
        "opentripmap_rate": "",
        "popularity_score": "",
        "data_source": "Wikidata, Manual",
        "opentripmap_match_name": "Manual: Campo de' Fiori",
        "opentripmap_match_score": 100,
        "opentripmap_match_status": "manual_match",
    },

    "Trastevere": {
        "source_opentripmap_id": "",
        "source_osm_id": "",
        "source_wikidata_id": "Q914255",
        "latitude": 41.887222,
        "longitude": 12.465556,
        "category_raw": "historic,cultural,urban_environment,districts,neighbourhood",
        "opentripmap_rate": "",
        "popularity_score": "",
        "data_source": "Wikidata, Manual",
        "opentripmap_match_name": "Manual: Trastevere",
        "opentripmap_match_score": 100,
        "opentripmap_match_status": "manual_match",
    },

    "Piazza del Popolo": {
        "source_opentripmap_id": "",
        "source_osm_id": "",
        "source_wikidata_id": "Q824997",
        "latitude": 41.910711,
        "longitude": 12.476319,
        "category_raw": "historic,architecture,cultural,urban_environment,squares",
        "opentripmap_rate": "",
        "popularity_score": "",
        "data_source": "Wikidata, Manual",
        "opentripmap_match_name": "Manual: Piazza del Popolo",
        "opentripmap_match_score": 100,
        "opentripmap_match_status": "manual_match",
    },

    "Appian Way": {
        "source_opentripmap_id": "",
        "source_osm_id": "",
        "source_wikidata_id": "Q189417",
        "latitude": 41.866944,
        "longitude": 12.532500,
        "category_raw": "historic,archaeology,cultural,roads,heritage",
        "opentripmap_rate": "",
        "popularity_score": "",
        "data_source": "Wikidata, Manual",
        "opentripmap_match_name": "Manual: Appian Way",
        "opentripmap_match_score": 100,
        "opentripmap_match_status": "manual_match",
    },
}


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    for location_name, manual_values in MANUAL_DATA.items():
        mask = df["location_name"] == location_name

        if not mask.any():
            print(f"Uyarı: {location_name} master dosyada bulunamadı.")
            continue

        for column, value in manual_values.items():
            df.loc[mask, column] = value

        print(f"Manuel tamamlandı: {location_name}")

    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)

    df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8-sig")
    df.to_excel(OUTPUT_XLSX_PATH, index=False)

    print("\nFinal dataset oluşturuldu.")
    print(f"CSV çıktı: {OUTPUT_CSV_PATH}")
    print(f"Excel çıktı: {OUTPUT_XLSX_PATH}")

    print("\nÖzet:")
    print(df["opentripmap_match_status"].value_counts())

    print("\nKontrol tablosu:")
    print(
        df[
            [
                "location_name",
                "opentripmap_match_name",
                "opentripmap_match_status",
                "source_wikidata_id",
                "latitude",
                "longitude",
                "data_source",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
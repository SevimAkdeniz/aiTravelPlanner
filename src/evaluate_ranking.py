from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


RANDOM_SEED = 42
TEST_SIZE = 0.20

INPUT_PATH = Path(
    "datasets/training/"
    "rome_user_location_training.csv"
)

MODEL_PATH = Path(
    "models/location_recommender_v2.joblib"
)

REPORTS_DIR = Path("reports")

RANKING_REPORT_PATH = (
    REPORTS_DIR / "ranking_metrics.json"
)

USER_RANKING_PATH = (
    REPORTS_DIR / "user_ranking_results.csv"
)

TOP_RECOMMENDATIONS_PATH = (
    REPORTS_DIR / "sample_top_recommendations.csv"
)


TARGET_COLUMN = "suitability_score"
GROUP_COLUMN = "user_profile_id"


TARGET_COMPONENT_COLUMNS = [
    "target_interest_score",
    "target_importance_score",
    "target_budget_score",
    "target_tempo_score",
    "target_time_score",
    "target_weather_score",
    "target_family_score",
]


NON_FEATURE_COLUMNS = [
    TARGET_COLUMN,
    GROUP_COLUMN,
    "location_name",
]


def load_data() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Eğitim veri seti bulunamadı: {INPUT_PATH}"
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model dosyası bulunamadı: {MODEL_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    if df.empty:
        raise ValueError(
            "Eğitim veri seti boş."
        )

    return df


def prepare_features(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    drop_columns = (
        NON_FEATURE_COLUMNS
        + TARGET_COMPONENT_COLUMNS
    )

    existing_drop_columns = [
        column
        for column in drop_columns
        if column in df.columns
    ]

    X = df.drop(
        columns=existing_drop_columns
    ).copy()

    y = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce",
    )

    groups = df[GROUP_COLUMN].copy()

    return X, y, groups


def get_test_indices(
    X: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series,
) -> np.ndarray:
    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
    )

    _, test_indices = next(
        splitter.split(
            X,
            y,
            groups=groups,
        )
    )

    return test_indices


def dcg_at_k(
    relevances: np.ndarray,
    k: int,
) -> float:
    relevances = np.asarray(
        relevances,
        dtype=float,
    )[:k]

    if len(relevances) == 0:
        return 0.0

    discounts = np.log2(
        np.arange(
            2,
            len(relevances) + 2,
        )
    )

    return float(
        np.sum(
            relevances / discounts
        )
    )


def ndcg_at_k(
    actual_scores: np.ndarray,
    predicted_order: np.ndarray,
    k: int,
) -> float:
    actual_scores = np.asarray(
        actual_scores,
        dtype=float,
    )

    predicted_relevances = (
        actual_scores[
            predicted_order
        ][:k]
    )

    ideal_order = np.argsort(
        actual_scores
    )[::-1]

    ideal_relevances = (
        actual_scores[
            ideal_order
        ][:k]
    )

    actual_dcg = dcg_at_k(
        predicted_relevances,
        k,
    )

    ideal_dcg = dcg_at_k(
        ideal_relevances,
        k,
    )

    if ideal_dcg == 0:
        return 0.0

    return actual_dcg / ideal_dcg


def top_k_overlap(
    actual_scores: np.ndarray,
    predicted_scores: np.ndarray,
    k: int,
) -> float:
    actual_top_k = set(
        np.argsort(
            actual_scores
        )[::-1][:k]
    )

    predicted_top_k = set(
        np.argsort(
            predicted_scores
        )[::-1][:k]
    )

    overlap_count = len(
        actual_top_k.intersection(
            predicted_top_k
        )
    )

    return overlap_count / k


def reciprocal_rank(
    actual_scores: np.ndarray,
    predicted_scores: np.ndarray,
) -> float:
    actual_best_index = int(
        np.argmax(
            actual_scores
        )
    )

    predicted_order = np.argsort(
        predicted_scores
    )[::-1]

    positions = np.where(
        predicted_order == actual_best_index
    )[0]

    if len(positions) == 0:
        return 0.0

    rank = int(
        positions[0]
    ) + 1

    return 1.0 / rank


def evaluate_user_group(
    user_df: pd.DataFrame,
) -> dict[str, float | int]:
    actual_scores = user_df[
        "actual_score"
    ].to_numpy()

    predicted_scores = user_df[
        "predicted_score"
    ].to_numpy()

    predicted_order = np.argsort(
        predicted_scores
    )[::-1]

    return {
        "user_profile_id": int(
            user_df[
                GROUP_COLUMN
            ].iloc[0]
        ),
        "top_1_correct": int(
            np.argmax(actual_scores)
            == np.argmax(predicted_scores)
        ),
        "top_3_overlap": round(
            top_k_overlap(
                actual_scores,
                predicted_scores,
                3,
            ),
            6,
        ),
        "top_5_overlap": round(
            top_k_overlap(
                actual_scores,
                predicted_scores,
                5,
            ),
            6,
        ),
        "top_10_overlap": round(
            top_k_overlap(
                actual_scores,
                predicted_scores,
                10,
            ),
            6,
        ),
        "ndcg_at_5": round(
            ndcg_at_k(
                actual_scores,
                predicted_order,
                5,
            ),
            6,
        ),
        "ndcg_at_10": round(
            ndcg_at_k(
                actual_scores,
                predicted_order,
                10,
            ),
            6,
        ),
        "reciprocal_rank": round(
            reciprocal_rank(
                actual_scores,
                predicted_scores,
            ),
            6,
        ),
    }


def create_sample_recommendations(
    prediction_df: pd.DataFrame,
    user_count: int = 5,
    top_k: int = 10,
) -> pd.DataFrame:
    sample_user_ids = (
        prediction_df[
            GROUP_COLUMN
        ]
        .drop_duplicates()
        .head(user_count)
        .tolist()
    )

    sample_frames = []

    for user_id in sample_user_ids:
        user_df = prediction_df[
            prediction_df[
                GROUP_COLUMN
            ] == user_id
        ].copy()

        user_df = user_df.sort_values(
            by="predicted_score",
            ascending=False,
        ).head(top_k)

        user_df.insert(
            1,
            "predicted_rank",
            range(
                1,
                len(user_df) + 1,
            ),
        )

        actual_sorted = (
            prediction_df[
                prediction_df[
                    GROUP_COLUMN
                ] == user_id
            ]
            .sort_values(
                by="actual_score",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        actual_rank_map = {
            int(location_id): rank
            for rank, location_id in enumerate(
                actual_sorted[
                    "location_id"
                ].tolist(),
                start=1,
            )
        }

        user_df[
            "actual_rank"
        ] = user_df[
            "location_id"
        ].map(
            actual_rank_map
        )

        sample_frames.append(
            user_df
        )

    return pd.concat(
        sample_frames,
        ignore_index=True,
    )


def main() -> None:
    df = load_data()

    X, y, groups = prepare_features(
        df
    )

    test_indices = get_test_indices(
        X,
        y,
        groups,
    )

    X_test = X.iloc[
        test_indices
    ].reset_index(drop=True)

    test_metadata = df.iloc[
        test_indices
    ][
        [
            GROUP_COLUMN,
            "location_id",
            "location_name",
            TARGET_COLUMN,
        ]
    ].reset_index(drop=True)

    model = joblib.load(
        MODEL_PATH
    )

    predictions = model.predict(
        X_test
    )

    predictions = np.clip(
        predictions,
        0,
        100,
    )

    prediction_df = test_metadata.rename(
        columns={
            TARGET_COLUMN: "actual_score",
        }
    )

    prediction_df[
        "predicted_score"
    ] = np.round(
        predictions,
        6,
    )

    prediction_df[
        "absolute_error"
    ] = np.round(
        np.abs(
            prediction_df[
                "actual_score"
            ]
            - prediction_df[
                "predicted_score"
            ]
        ),
        6,
    )

    user_results = []

    for _, user_df in prediction_df.groupby(
        GROUP_COLUMN
    ):
        user_results.append(
            evaluate_user_group(
                user_df.reset_index(
                    drop=True
                )
            )
        )

    user_results_df = pd.DataFrame(
        user_results
    )

    summary = {
        "test_user_count": int(
            user_results_df.shape[0]
        ),
        "locations_per_user": int(
            prediction_df.groupby(
                GROUP_COLUMN
            ).size().median()
        ),
        "top_1_accuracy": round(
            float(
                user_results_df[
                    "top_1_correct"
                ].mean()
            ),
            6,
        ),
        "mean_top_3_overlap": round(
            float(
                user_results_df[
                    "top_3_overlap"
                ].mean()
            ),
            6,
        ),
        "mean_top_5_overlap": round(
            float(
                user_results_df[
                    "top_5_overlap"
                ].mean()
            ),
            6,
        ),
        "mean_top_10_overlap": round(
            float(
                user_results_df[
                    "top_10_overlap"
                ].mean()
            ),
            6,
        ),
        "mean_ndcg_at_5": round(
            float(
                user_results_df[
                    "ndcg_at_5"
                ].mean()
            ),
            6,
        ),
        "mean_ndcg_at_10": round(
            float(
                user_results_df[
                    "ndcg_at_10"
                ].mean()
            ),
            6,
        ),
        "mean_reciprocal_rank": round(
            float(
                user_results_df[
                    "reciprocal_rank"
                ].mean()
            ),
            6,
        ),
    }

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    user_results_df.to_csv(
        USER_RANKING_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    with RANKING_REPORT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            ensure_ascii=False,
            indent=2,
        )

    sample_df = create_sample_recommendations(
        prediction_df,
        user_count=5,
        top_k=10,
    )

    sample_df.to_csv(
        TOP_RECOMMENDATIONS_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("=" * 70)
    print("SIRALAMA DEĞERLENDİRMESİ")
    print("=" * 70)

    print(
        f"Test kullanıcısı: "
        f"{summary['test_user_count']}"
    )

    print(
        f"Kullanıcı başına lokasyon: "
        f"{summary['locations_per_user']}"
    )

    print(
        f"Top-1 doğruluğu: "
        f"{summary['top_1_accuracy']:.4f}"
    )

    print(
        f"Top-3 örtüşmesi: "
        f"{summary['mean_top_3_overlap']:.4f}"
    )

    print(
        f"Top-5 örtüşmesi: "
        f"{summary['mean_top_5_overlap']:.4f}"
    )

    print(
        f"Top-10 örtüşmesi: "
        f"{summary['mean_top_10_overlap']:.4f}"
    )

    print(
        f"NDCG@5: "
        f"{summary['mean_ndcg_at_5']:.4f}"
    )

    print(
        f"NDCG@10: "
        f"{summary['mean_ndcg_at_10']:.4f}"
    )

    print(
        f"MRR: "
        f"{summary['mean_reciprocal_rank']:.4f}"
    )

    print("\nOluşturulan dosyalar:")
    print(f"- {RANKING_REPORT_PATH}")
    print(f"- {USER_RANKING_PATH}")
    print(f"- {TOP_RECOMMENDATIONS_PATH}")


if __name__ == "__main__":
    main()
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)
from sklearn.tree import DecisionTreeRegressor


RANDOM_SEED = 42
TEST_SIZE = 0.20

INPUT_PATH = Path(
    "datasets/training/"
    "rome_user_location_training.csv"
)

MODELS_DIR = Path("models")
REPORTS_DIR = Path("reports")

MODEL_OUTPUT_PATH = (
    MODELS_DIR / "location_recommender_v2.joblib"
)

METRICS_CSV_PATH = (
    REPORTS_DIR / "model_comparison.csv"
)

METRICS_JSON_PATH = (
    REPORTS_DIR / "model_metrics.json"
)

TEST_PREDICTIONS_PATH = (
    REPORTS_DIR / "test_predictions.csv"
)

FEATURE_COLUMNS_PATH = (
    MODELS_DIR / "feature_columns.json"
)

MODEL_METADATA_PATH = (
    MODELS_DIR / "model_metadata.json"
)


TARGET_COLUMN = "suitability_score"
GROUP_COLUMN = "user_profile_id"


# Bu sütunlar doğrudan hedef puanın hesaplanmasında
# kullanılan ara cevapları içeriyor.
# Modele verilirse veri sızıntısı oluşur.
TARGET_COMPONENT_COLUMNS = [
    "target_interest_score",
    "target_importance_score",
    "target_budget_score",
    "target_tempo_score",
    "target_time_score",
    "target_weather_score",
    "target_family_score",
]


# Modelin öğrenmesi için anlamlı olmayan kimlik/metin alanları.
NON_FEATURE_COLUMNS = [
    TARGET_COLUMN,
    GROUP_COLUMN,
    "location_name",
]


def load_dataset() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Eğitim veri seti bulunamadı: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    if df.empty:
        raise ValueError(
            "Eğitim veri seti boş."
        )

    required_columns = {
        TARGET_COLUMN,
        GROUP_COLUMN,
    }

    missing_columns = (
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Eksik zorunlu sütunlar: "
            + ", ".join(sorted(missing_columns))
        )

    return df


def prepare_features(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    columns_to_drop = (
        NON_FEATURE_COLUMNS
        + TARGET_COMPONENT_COLUMNS
    )

    existing_drop_columns = [
        column
        for column in columns_to_drop
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

    invalid_target_count = int(
        y.isna().sum()
    )

    if invalid_target_count > 0:
        raise ValueError(
            f"Hedef sütunda {invalid_target_count} "
            "geçersiz değer bulundu."
        )

    # Sonsuz değerleri temizliyoruz.
    X = X.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    return X, y, groups


def split_by_user(
    X: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.Series,
    pd.Series,
    pd.Series,
    pd.Series,
]:
    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
    )

    train_indices, test_indices = next(
        splitter.split(
            X,
            y,
            groups=groups,
        )
    )

    X_train = X.iloc[
        train_indices
    ].reset_index(drop=True)

    X_test = X.iloc[
        test_indices
    ].reset_index(drop=True)

    y_train = y.iloc[
        train_indices
    ].reset_index(drop=True)

    y_test = y.iloc[
        test_indices
    ].reset_index(drop=True)

    groups_train = groups.iloc[
        train_indices
    ].reset_index(drop=True)

    groups_test = groups.iloc[
        test_indices
    ].reset_index(drop=True)

    overlapping_users = set(
        groups_train.unique()
    ).intersection(
        set(groups_test.unique())
    )

    if overlapping_users:
        raise RuntimeError(
            "Eğitim ve test kullanıcıları "
            "arasında çakışma bulundu."
        )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        groups_train,
        groups_test,
    )


def detect_column_types(
    X_train: pd.DataFrame,
) -> tuple[list[str], list[str]]:
    categorical_columns = (
        X_train.select_dtypes(
            include=[
                "object",
                "category",
                "string",
            ]
        )
        .columns
        .tolist()
    )

    numeric_columns = [
        column
        for column in X_train.columns
        if column not in categorical_columns
    ]

    return (
        numeric_columns,
        categorical_columns,
    )


def build_preprocessor(
    numeric_columns: list[str],
    categorical_columns: list[str],
) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                numeric_columns,
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_columns,
            ),
        ],
        remainder="drop",
    )

    return preprocessor


def create_models() -> dict[str, Any]:
    return {
        "linear_regression": (
            LinearRegression()
        ),
        "decision_tree": (
            DecisionTreeRegressor(
                max_depth=12,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=RANDOM_SEED,
            )
        ),
        "random_forest": (
            RandomForestRegressor(
                n_estimators=250,
                max_depth=18,
                min_samples_split=6,
                min_samples_leaf=2,
                max_features="sqrt",
                n_jobs=-1,
                random_state=RANDOM_SEED,
            )
        ),
        "gradient_boosting": (
            GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=4,
                min_samples_split=8,
                min_samples_leaf=4,
                loss="squared_error",
                random_state=RANDOM_SEED,
            )
        ),
    }


def calculate_metrics(
    y_true: pd.Series,
    predictions: np.ndarray,
) -> dict[str, float]:
    mae = mean_absolute_error(
        y_true,
        predictions,
    )

    mse = mean_squared_error(
        y_true,
        predictions,
    )

    rmse = float(np.sqrt(mse))

    r2 = r2_score(
        y_true,
        predictions,
    )

    return {
        "mae": round(float(mae), 6),
        "mse": round(float(mse), 6),
        "rmse": round(float(rmse), 6),
        "r2": round(float(r2), 6),
    }


def train_and_evaluate_models(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    numeric_columns: list[str],
    categorical_columns: list[str],
) -> tuple[
    pd.DataFrame,
    dict[str, Pipeline],
    dict[str, np.ndarray],
]:
    models = create_models()

    results = []
    trained_pipelines: dict[
        str,
        Pipeline,
    ] = {}

    predictions_by_model: dict[
        str,
        np.ndarray,
    ] = {}

    for model_name, estimator in models.items():
        print("\n" + "=" * 70)
        print(f"Model eğitiliyor: {model_name}")

        preprocessor = build_preprocessor(
            numeric_columns,
            categorical_columns,
        )

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    preprocessor,
                ),
                (
                    "model",
                    estimator,
                ),
            ]
        )

        start_time = time.perf_counter()

        pipeline.fit(
            X_train,
            y_train,
        )

        training_seconds = (
            time.perf_counter()
            - start_time
        )

        predictions = pipeline.predict(
            X_test
        )

        predictions = np.clip(
            predictions,
            0,
            100,
        )

        metrics = calculate_metrics(
            y_test,
            predictions,
        )

        result = {
            "model_name": model_name,
            **metrics,
            "training_seconds": round(
                training_seconds,
                4,
            ),
        }

        results.append(result)

        trained_pipelines[
            model_name
        ] = pipeline

        predictions_by_model[
            model_name
        ] = predictions

        print(
            f"MAE:  {metrics['mae']:.4f}"
        )
        print(
            f"RMSE: {metrics['rmse']:.4f}"
        )
        print(
            f"R²:   {metrics['r2']:.4f}"
        )
        print(
            "Eğitim süresi: "
            f"{training_seconds:.2f} sn"
        )

    results_df = pd.DataFrame(
        results
    ).sort_values(
        by=[
            "mae",
            "rmse",
        ],
        ascending=[
            True,
            True,
        ],
    ).reset_index(drop=True)

    return (
        results_df,
        trained_pipelines,
        predictions_by_model,
    )


def save_results(
    results_df: pd.DataFrame,
    best_model_name: str,
    best_pipeline: Pipeline,
    best_predictions: np.ndarray,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    groups_train: pd.Series,
    groups_test: pd.Series,
    numeric_columns: list[str],
    categorical_columns: list[str],
) -> None:
    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        best_pipeline,
        MODEL_OUTPUT_PATH,
    )

    results_df.to_csv(
        METRICS_CSV_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    metrics_payload = {
        "best_model": best_model_name,
        "selection_metric": (
            "lowest_mae"
        ),
        "models": results_df.to_dict(
            orient="records"
        ),
    }

    with METRICS_JSON_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metrics_payload,
            file,
            ensure_ascii=False,
            indent=2,
        )

    feature_payload = {
        "input_feature_count": (
            len(X_train.columns)
        ),
        "input_features": (
            X_train.columns.tolist()
        ),
        "numeric_features": (
            numeric_columns
        ),
        "categorical_features": (
            categorical_columns
        ),
        "excluded_target_components": (
            TARGET_COMPONENT_COLUMNS
        ),
    }

    with FEATURE_COLUMNS_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            feature_payload,
            file,
            ensure_ascii=False,
            indent=2,
        )

    metadata_payload = {
        "model_version": "v2",
        "model_name": best_model_name,
        "random_seed": RANDOM_SEED,
        "test_size": TEST_SIZE,
        "training_rows": len(X_train),
        "test_rows": len(X_test),
        "training_user_count": int(
            groups_train.nunique()
        ),
        "test_user_count": int(
            groups_test.nunique()
        ),
        "feature_count_before_encoding": (
            len(X_train.columns)
        ),
        "target_column": TARGET_COLUMN,
        "group_column": GROUP_COLUMN,
        "model_file": str(
            MODEL_OUTPUT_PATH
        ),
    }

    with MODEL_METADATA_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metadata_payload,
            file,
            ensure_ascii=False,
            indent=2,
        )

    prediction_df = X_test[
        [
            column
            for column in [
                "location_id",
            ]
            if column in X_test.columns
        ]
    ].copy()

    prediction_df[
        "user_profile_id"
    ] = groups_test.values

    prediction_df[
        "actual_suitability_score"
    ] = y_test.values

    prediction_df[
        "predicted_suitability_score"
    ] = np.round(
        best_predictions,
        4,
    )

    prediction_df[
        "absolute_error"
    ] = np.round(
        np.abs(
            y_test.values
            - best_predictions
        ),
        4,
    )

    prediction_df.to_csv(
        TEST_PREDICTIONS_PATH,
        index=False,
        encoding="utf-8-sig",
    )


def main() -> None:
    df = load_dataset()

    print(
        f"Toplam veri boyutu: {df.shape}"
    )
    print(
        "Toplam kullanıcı profili: "
        f"{df[GROUP_COLUMN].nunique()}"
    )

    X, y, groups = prepare_features(
        df
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
        groups_train,
        groups_test,
    ) = split_by_user(
        X,
        y,
        groups,
    )

    print("\nKullanıcı bazlı veri ayrımı:")
    print(
        f"Eğitim satırı: {len(X_train)}"
    )
    print(
        f"Test satırı: {len(X_test)}"
    )
    print(
        "Eğitim kullanıcısı: "
        f"{groups_train.nunique()}"
    )
    print(
        "Test kullanıcısı: "
        f"{groups_test.nunique()}"
    )

    (
        numeric_columns,
        categorical_columns,
    ) = detect_column_types(
        X_train
    )

    print("\nÖzellik bilgisi:")
    print(
        "Toplam ham özellik: "
        f"{len(X_train.columns)}"
    )
    print(
        "Sayısal özellik: "
        f"{len(numeric_columns)}"
    )
    print(
        "Kategorik özellik: "
        f"{len(categorical_columns)}"
    )

    (
        results_df,
        trained_pipelines,
        predictions_by_model,
    ) = train_and_evaluate_models(
        X_train,
        X_test,
        y_train,
        y_test,
        numeric_columns,
        categorical_columns,
    )

    best_model_name = str(
        results_df.iloc[0][
            "model_name"
        ]
    )

    best_pipeline = trained_pipelines[
        best_model_name
    ]

    best_predictions = (
        predictions_by_model[
            best_model_name
        ]
    )

    save_results(
        results_df=results_df,
        best_model_name=best_model_name,
        best_pipeline=best_pipeline,
        best_predictions=best_predictions,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        groups_train=groups_train,
        groups_test=groups_test,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
    )

    print("\n" + "=" * 70)
    print("MODEL KARŞILAŞTIRMASI")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )

    print("\nEn iyi model:")
    print(best_model_name)

    print("\nOluşturulan dosyalar:")
    print(f"- {MODEL_OUTPUT_PATH}")
    print(f"- {METRICS_CSV_PATH}")
    print(f"- {METRICS_JSON_PATH}")
    print(f"- {TEST_PREDICTIONS_PATH}")
    print(f"- {FEATURE_COLUMNS_PATH}")
    print(f"- {MODEL_METADATA_PATH}")


if __name__ == "__main__":
    main()
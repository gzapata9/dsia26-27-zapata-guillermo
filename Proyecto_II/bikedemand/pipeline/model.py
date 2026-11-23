# Modelo scikit-learn: entrenamiento reproducible, evaluación, persistencia (joblib) e inferencia.
# Regresión de la demanda horaria (`cnt`) con HistGradientBoostingRegressor.
# Evaluación con split temporal (entrenar con el pasado, evaluar con el futuro) y
# comparación con una línea base ingenua (media histórica por hora y tipo de día).

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ..errors import DataContractError, ModelNotFoundError
from .features import FEATURES, TARGET

logger = logging.getLogger("bikedemand.model")

MODEL_NAME = "HistGradientBoostingRegressor"


@dataclass
class TrainResult:
    bundle: dict
    card: dict


def build_estimator(random_state: int = 42, max_iter: int = 400) -> HistGradientBoostingRegressor:
    return HistGradientBoostingRegressor(
        max_iter=max_iter, learning_rate=0.08, random_state=random_state,
    )


def _metrics(y_true, y_pred) -> dict:
    return {
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 2),
        "rmse": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 2),
        "r2": round(float(r2_score(y_true, y_pred)), 4),
    }


def _baseline_predict(train: pd.DataFrame, test: pd.DataFrame) -> np.ndarray:
    """Media histórica de `cnt` por (hora, día laborable)"""
    means = train.groupby(["hr", "workingday"])[TARGET].mean()
    keys = pd.MultiIndex.from_frame(test[["hr", "workingday"]])
    return means.reindex(keys).fillna(train[TARGET].mean()).to_numpy()


def _data_hash(gold: pd.DataFrame) -> str:
    return hashlib.sha256(pd.util.hash_pandas_object(gold, index=False).values.tobytes()).hexdigest()[:16]


def train_model(gold: pd.DataFrame, test_from: str, random_state: int = 42, max_iter: int = 400) -> TrainResult:
    missing = [c for c in FEATURES + [TARGET, "timestamp"] if c not in gold.columns]
    if missing:
        raise DataContractError(f"La tabla gold no tiene las columnas {missing}")

    ts = pd.to_datetime(gold["timestamp"])
    test_mask = ts >= pd.Timestamp(test_from)
    train, test = gold.loc[~test_mask], gold.loc[test_mask]
    if len(train) == 0 or len(test) == 0:
        raise DataContractError(f"El split temporal en {test_from} deja train o test vacío")
    logger.info("train_start rows_train=%d rows_test=%d test_from=%s", len(train), len(test), test_from)

    model = build_estimator(random_state, max_iter).fit(train[FEATURES], train[TARGET])
    pred = np.clip(model.predict(test[FEATURES]), 0, None)
    test_metrics = _metrics(test[TARGET], pred)
    baseline_metrics = _metrics(test[TARGET], _baseline_predict(train, test))

    imp = permutation_importance(model, test[FEATURES], test[TARGET], n_repeats=3,
                                 random_state=random_state, scoring="neg_mean_absolute_error")
    importances = dict(sorted(zip(FEATURES, imp.importances_mean.round(2).tolist()),
                              key=lambda kv: kv[1], reverse=True))

    # Modelo de producción: se reentrena con TODO el histórico (las métricas son las del holdout)
    final = build_estimator(random_state, max_iter).fit(gold[FEATURES], gold[TARGET])

    trained_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    card = {
        "model": MODEL_NAME,
        "task": "regresión de alquileres por hora (cnt)",
        "features": FEATURES,
        "target": TARGET,
        "trained_at": trained_at,
        "sklearn_version": sklearn.__version__,
        "data_hash": _data_hash(gold),
        "rows_total": int(len(gold)),
        "split": {"type": "temporal", "test_from": test_from,
                  "rows_train": int(len(train)), "rows_test": int(len(test))},
        "metrics_test": test_metrics,
        "metrics_baseline": baseline_metrics,
        "permutation_importance_mae": importances,
        "params": {"max_iter": max_iter, "learning_rate": 0.08, "random_state": random_state},
    }
    logger.info("train_done mae=%.2f rmse=%.2f r2=%.4f baseline_r2=%.4f",
                test_metrics["mae"], test_metrics["rmse"], test_metrics["r2"], baseline_metrics["r2"])
    bundle = {"model": final, "features": FEATURES, "trained_at": trained_at,
              "sklearn_version": sklearn.__version__}
    return TrainResult(bundle=bundle, card=card)


def save_model(result: TrainResult, model_path: Path, card_path: Path) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(result.bundle, model_path, compress=3)
    card_path.write_text(json.dumps(result.card, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("model_saved path=%s card=%s", model_path, card_path)


def load_model(model_path: Path) -> dict:
    if not model_path.exists():
        raise ModelNotFoundError(f"No hay modelo en {model_path}. Ejecuta: python -m bikedemand train")
    bundle = joblib.load(model_path)
    if not isinstance(bundle, dict) or not {"model", "features"} <= set(bundle):
        raise ModelNotFoundError(f"{model_path} no es un bundle de modelo válido")
    if bundle.get("sklearn_version") != sklearn.__version__:
        logger.warning("model_version_mismatch trained=%s runtime=%s (recomendado reentrenar)",
                       bundle.get("sklearn_version"), sklearn.__version__)
    return bundle


def predict(bundle: dict, features: pd.DataFrame) -> pd.Series:
    """Predicción de alquileres por hora"""
    missing = [c for c in bundle["features"] if c not in features.columns]
    if missing:
        raise DataContractError(f"Faltan features para predecir: {missing}")
    pred = bundle["model"].predict(features[bundle["features"]])
    return pd.Series(np.clip(np.round(pred), 0, None).astype(int), index=features.index, name="pred_cnt")

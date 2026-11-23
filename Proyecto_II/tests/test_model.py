"""Tests del modelo sklearn: entrenamiento, persistencia, carga e inferencia."""
import joblib
import pandas as pd
import pytest

from bikedemand.errors import DataContractError, ModelNotFoundError
from bikedemand.pipeline import features, model, quality
from conftest import PROJECT


@pytest.fixture
def gold(raw_df):
    return features.build_training_table(quality.validate(raw_df).clean)


def test_train_save_load_predict(tmp_path, gold):
    result = model.train_model(gold, test_from="2012-09-20", max_iter=60)
    card = result.card
    assert card["split"]["type"] == "temporal"
    assert card["metrics_test"]["r2"] > card["metrics_baseline"]["r2"] - 0.05
    assert card["metrics_test"]["mae"] < 40

    path, card_path = tmp_path / "m.joblib", tmp_path / "card.json"
    model.save_model(result, path, card_path)
    bundle = model.load_model(path)
    pred = model.predict(bundle, gold.head(48))
    assert len(pred) == 48 and (pred >= 0).all() and pred.dtype.kind == "i"
    # El patrón sintético es aprendible: hora punta laborable > madrugada
    peak = gold[(gold.hr == 8) & (gold.workingday == 1)].head(5)
    night = gold[gold.hr == 3].head(5)
    assert model.predict(bundle, peak).mean() > model.predict(bundle, night).mean() + 100


def test_train_rejects_bad_split(gold):
    with pytest.raises(DataContractError):
        model.train_model(gold, test_from="2030-01-01")


def test_train_rejects_missing_columns(gold):
    with pytest.raises(DataContractError):
        model.train_model(gold.drop(columns=["hr"]), test_from="2012-09-20")


def test_load_model_missing(tmp_path):
    with pytest.raises(ModelNotFoundError):
        model.load_model(tmp_path / "none.joblib")


def test_load_model_invalid_bundle(tmp_path):
    path = tmp_path / "bad.joblib"
    joblib.dump({"foo": 1}, path)
    with pytest.raises(ModelNotFoundError):
        model.load_model(path)


def test_predict_missing_features(tmp_path, gold):
    bundle = model.train_model(gold, test_from="2012-09-20", max_iter=20).bundle
    with pytest.raises(DataContractError):
        model.predict(bundle, gold.drop(columns=["temp_c"]))


@pytest.mark.integration
def test_versioned_model_loads_and_predicts():
    """El artefacto versionado en models/ se carga y predice con sentido."""
    path = PROJECT / "models" / "demand_model.joblib"
    if not path.exists():
        pytest.skip("No hay modelo versionado; ejecuta `python -m bikedemand train`")
    bundle = model.load_model(path)
    base = dict(system_year=1, season=3, mnth=7, holiday=0, weekday=3, workingday=1, weathersit=1,
                temp_c=25.0, feels_like_c=27.0, humidity_pct=55.0, wind_kmh=10.0)
    rows = pd.DataFrame([{**base, "hr": 8}, {**base, "hr": 3}, {**base, "hr": 8, "weathersit": 3}])
    rush, night, rainy_rush = model.predict(bundle, rows)
    assert rush > 300 and night < 50 and rainy_rush < rush

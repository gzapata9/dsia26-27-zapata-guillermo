from pathlib import Path

import pandas as pd
import pytest

from validator_under_test import load_sales, split_valid_invalid

COURSE_CSV = (
    Path(__file__).resolve().parents[3]
    / "1_programacion_avanzada_python"
    / "Datos"
    / "ventas.csv"
)


@pytest.fixture
def mini_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "unidades": [2, None, 5],
            "precio_unitario": [10.0, 20.0, -1.0],
        }
    )


def test_split_counts(mini_frame):
    valid, invalid = split_valid_invalid(mini_frame)
    assert len(valid) == 1
    assert len(invalid) == 2


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_sales(Path("/tmp/no-existe-dsia-ventas.csv"))


@pytest.mark.parametrize(
    ("units", "price", "is_valid"),
    [
        (1, 1.0, True),
        (0, 1.0, False),
        (1, 0.0, False),
        (1, -1.0, False),
    ],
)
def test_price_and_units_rules(units, price, is_valid):
    frame = pd.DataFrame({"unidades": [units], "precio_unitario": [price]})
    valid, invalid = split_valid_invalid(frame)
    assert (len(valid) == 1) is is_valid
    assert (len(invalid) == 1) is (not is_valid)


@pytest.mark.integration
def test_course_csv_eight_valid():
    frame = load_sales(COURSE_CSV)
    valid, invalid = split_valid_invalid(frame)
    assert len(valid) == 8
    assert len(invalid) == 2

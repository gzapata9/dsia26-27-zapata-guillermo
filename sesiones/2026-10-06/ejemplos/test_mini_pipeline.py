import pandas as pd

from mini_pipeline import transform


def test_transform_drops_invalid_rows():
    frame = pd.DataFrame(
        {
            "fecha": ["2026-01-01", "2026-01-02"],
            "region": ["Norte", "Sur"],
            "producto": ["A", "B"],
            "unidades": [1, None],
            "precio_unitario": [10.0, 5.0],
            "cliente_id": ["C1", "C2"],
        }
    )
    clean, report = transform(frame)
    assert report["rows_out"] == 1
    assert report["rows_dropped"] == 1
    assert "importe" in clean.columns

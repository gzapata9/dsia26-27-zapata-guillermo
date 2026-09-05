"""Demo de teoría pandas — sesión 15 sep 2026."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[3] / "1_programacion_avanzada_python" / "Datos" / "ventas.csv"


def validar_ventas(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = frame.copy()
    work["unidades"] = pd.to_numeric(work["unidades"], errors="coerce")
    work["precio_unitario"] = pd.to_numeric(work["precio_unitario"], errors="coerce")
    ok = (
        work["unidades"].notna()
        & (work["unidades"] > 0)
        & work["precio_unitario"].notna()
        & (work["precio_unitario"] > 0)
    )
    validos = work.loc[ok].copy()
    errores = work.loc[~ok].copy()
    validos["importe"] = validos["unidades"] * validos["precio_unitario"]
    return validos, errores


def main() -> None:
    df = pd.read_csv(DATA)
    print("shape:", df.shape)
    print("nulos:\n", df.isna().sum(), sep="")
    validos, errores = validar_ventas(df)
    print(f"válidos={len(validos)} errores={len(errores)}")
    print(validos.groupby("region")["importe"].sum().sort_values(ascending=False))
    informe = {
        "filas_totales": int(len(df)),
        "filas_validas": int(len(validos)),
        "filas_invalidas": int(len(errores)),
        "importe_total": float(validos["importe"].sum()),
    }
    print(json.dumps(informe, indent=2, ensure_ascii=False))
    assert len(validos) == 8 and len(errores) == 2


if __name__ == "__main__":
    main()

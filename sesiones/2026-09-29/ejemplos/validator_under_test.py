"""Unidad bajo prueba — validación mínima de ventas."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_sales(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def split_valid_invalid(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = frame.copy()
    work["unidades"] = pd.to_numeric(work["unidades"], errors="coerce")
    work["precio_unitario"] = pd.to_numeric(work["precio_unitario"], errors="coerce")
    ok = work["unidades"].notna() & (work["unidades"] > 0) & (work["precio_unitario"] > 0)
    return work.loc[ok].copy(), work.loc[~ok].copy()

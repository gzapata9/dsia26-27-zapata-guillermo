"""Ejemplo SOLID — sesión 22 sep 2026."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import pandas as pd


class DataLoadError(Exception):
    pass


@dataclass(frozen=True)
class SalesRecord:
    region: str
    product: str
    units: float
    unit_price: float

    @property
    def amount(self) -> float:
        return self.units * self.unit_price


class SalesRepository(Protocol):
    def load(self) -> pd.DataFrame: ...


class CsvSalesRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> pd.DataFrame:
        if not self._path.exists():
            raise DataLoadError(f"No existe: {self._path}")
        return pd.read_csv(self._path)


class SalesValidator:
    def split(self, frame: pd.DataFrame) -> tuple[list[SalesRecord], pd.DataFrame]:
        work = frame.copy()
        work["unidades"] = pd.to_numeric(work["unidades"], errors="coerce")
        work["precio_unitario"] = pd.to_numeric(work["precio_unitario"], errors="coerce")
        ok = work["unidades"].notna() & (work["unidades"] > 0) & (work["precio_unitario"] > 0)
        records = [
            SalesRecord(str(r.region), str(r.producto), float(r.unidades), float(r.precio_unitario))
            for r in work.loc[ok].itertuples(index=False)
        ]
        return records, work.loc[~ok]


class SalesMetrics:
    def total_by_region(self, records: list[SalesRecord]) -> dict[str, float]:
        totals: dict[str, float] = {}
        for rec in records:
            totals[rec.region] = totals.get(rec.region, 0.0) + rec.amount
        return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))

    def total_by_product(self, records: list[SalesRecord]) -> dict[str, float]:
        totals: dict[str, float] = {}
        for rec in records:
            totals[rec.product] = totals.get(rec.product, 0.0) + rec.amount
        return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))


def main() -> None:
    path = Path(__file__).resolve().parents[3] / "1_programacion_avanzada_python" / "Datos" / "ventas.csv"
    repo: SalesRepository = CsvSalesRepository(path)
    records, errors = SalesValidator().split(repo.load())
    metrics = SalesMetrics()
    print(f"válidos={len(records)} inválidos={len(errors)}")
    print("Por región:", metrics.total_by_region(records))
    print("Por producto:", metrics.total_by_product(records))


if __name__ == "__main__":
    main()

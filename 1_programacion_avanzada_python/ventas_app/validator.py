from pathlib import Path
import pandas as pd

class ValidationError(Exception):
    """Datos que no cumplen reglas de negocio."""

class SalesValidator:
    """Single Responsibility: solo valida."""

    def split(self, frame: pd.DataFrame) -> tuple[list[SalesRecord], pd.DataFrame]:
        work = frame.copy()
        work["unidades"] = pd.to_numeric(work["unidades"], errors="coerce")
        work["precio_unitario"] = pd.to_numeric(work["precio_unitario"], errors="coerce")
        ok = work["unidades"].notna() & (work["unidades"] > 0) & (work["precio_unitario"] > 0)
        valid_rows = [
            SalesRecord(
                region=str(row.region),
                product=str(row.producto),
                units=float(row.unidades),
                unit_price=float(row.precio_unitario),
            )
            for row in work.loc[ok].itertuples(index=False)
        ]
        return valid_rows, work.loc[~ok]
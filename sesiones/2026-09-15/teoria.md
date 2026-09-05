# Teoría (30 min) — 15 sep 2026  
## Procesamiento de datos con pandas

**Material de apoyo:** `../../1_programacion_avanzada_python/02_pandas_procesamiento.ipynb` · `Datos/ventas.csv`

---

## 1. Introducción (5 min)

Antes de “meter IA”, hay que **confiar en los datos**. Un CSV típico trae:

- tipos incorrectos (`"12"` como texto),
- nulos,
- valores de negocio imposibles (precio negativo).

Hoy aprendemos el ciclo:

```text
cargar → tipar → validar → transformar/agregar → exportar
```

---

## 2. Conceptos

### 2.1 Estructuras pandas

| Objeto | Qué es |
| --- | --- |
| `Series` | Columna (1D) con índice |
| `DataFrame` | Tabla (2D) de Series alineadas |
| `Index` | Etiquetas de filas/columnas |
| `dtype` | Tipo de cada columna (`int64`, `float64`, `object`, …) |

### 2.2 Operaciones clave

| Operación | Uso |
| --- | --- |
| `read_csv` | Ingesta |
| `isna` / `fillna` | Nulos |
| `to_numeric(..., errors="coerce")` | Tipado seguro (basura → `NaN`) |
| máscaras booleanas | Filtrar filas que cumplen reglas |
| `groupby` + agregaciones | Resúmenes de negocio |
| `to_csv` / JSON | Persistencia |

### 2.3 Validación vs limpieza silenciosa

- **Mal:** dropear filas sin dejar rastro.
- **Bien:** devolver `(validos, errores)` + informe de calidad.

Reglas del dataset del curso:

- `unidades > 0`
- `precio_unitario > 0`
- ambos numéricos (no nulos tras coerción)

---

## 3. Código y ejemplos

### 3.1 Carga y diagnóstico

```python
from pathlib import Path
import pandas as pd

df = pd.read_csv(Path("1_programacion_avanzada_python/Datos/ventas.csv"))
df.shape, df.dtypes, df.isna().sum()
```

### 3.2 Validación

```python
def validar_ventas(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = frame.copy()
    work["unidades"] = pd.to_numeric(work["unidades"], errors="coerce")
    work["precio_unitario"] = pd.to_numeric(work["precio_unitario"], errors="coerce")
    ok = (
        work["unidades"].notna() & (work["unidades"] > 0)
        & work["precio_unitario"].notna() & (work["precio_unitario"] > 0)
    )
    validos = work.loc[ok].copy()
    errores = work.loc[~ok].copy()
    validos["importe"] = validos["unidades"] * validos["precio_unitario"]
    return validos, errores
```

Con el CSV del curso: **8 válidas, 2 inválidas**.

### 3.3 Agregaciones

```python
validos.groupby("region")["importe"].sum().sort_values(ascending=False)
validos.groupby("producto")["importe"].sum().nlargest(3)
```

Ejemplo runnable: `ejemplos/demo_pandas_ventas.py`.

---

## 4. Resumen

- Tipado con `coerce` evita crashes y hace visibles los errores.
- La validación es parte del producto.
- `groupby` responde preguntas de negocio, no solo “estadística”.

→ `ejercicios.md`

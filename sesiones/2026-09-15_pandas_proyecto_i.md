# 15 sep 2026 — Pandas y procesamiento de datos + Proyecto I

**Duración total:** 1 h 45 min  
**Material:** `1_programacion_avanzada_python/02_pandas_procesamiento.ipynb` · `ejercicios/E1_pandas.md` · `proyectos/proyecto_i/`

| Bloque | Min | Qué hacer |
| --- | --- | --- |
| Exposición + demo | 0–30 | Guion abajo |
| Ejercicios | 30–60 | E1 con checkpoints |
| Presentación Proyecto I + arranque | 60–105 | Enunciado, rúbrica, primer commit |

---

## Objetivos de aprendizaje

Al terminar la sesión, el alumnado debe ser capaz de:

1. Cargar CSV con `pathlib` + pandas y diagnosticar tipos/`NaN`.
2. Aplicar reglas de validación de negocio y separar válidos/errores.
3. Agregar con `groupby` y exportar resultados + informe de calidad.
4. Entender el alcance del **Proyecto I (10 %)**.

---

## Bloque A — Exposición (30 min)

### A1. Por qué pandas en soluciones de IA (5 min)

- El cuello de botella suele ser **datos sucios**, no el modelo.
- Pipeline mental: **ingesta → tipado → validación → transformación → exportación**.
- Diferencia entre *análisis exploratorio* (notebook) y *código de producto* (funciones + tests).

### A2. Anatomía de un DataFrame (8 min) — live

Abrir `Datos/ventas.csv` y el notebook:

1. `read_csv`, `shape`, `dtypes`, `isna().sum()`, `describe(include="all")`.
2. Conversiones: `to_numeric(..., errors="coerce")`, `to_datetime`.
3. Indexación: `loc` vs boolean masks.
4. Anti-patrón: mutar el DataFrame original sin `.copy()`.

**Pregunta al aula:** ¿qué filas del CSV de ventas son inválidas y por qué?

### A3. Validación como contrato (8 min) — live

Implementar/repasar `validar_ventas`:

- Reglas: `unidades > 0`, `precio_unitario > 0`, no nulos.
- Salida doble: `(validos, errores)` — no silenciar basura.
- Columna derivada `importe`.
- Informe JSON de calidad (conteos + importe total).

Mensaje clave: **la validación es parte del producto**, no un paso opcional del notebook.

### A4. Agregaciones y exportación (5 min)

- `groupby` + `sum` / `size`.
- Top-N con `sort_values` + `head`.
- Export: `to_csv` / `json.dumps` con `pathlib`.
- Cierre: de notebook a **funciones reutilizables** (puente a la sesión 22 sep).

### A5. Transición al Proyecto I (4 min)

Mostrar `proyectos/proyecto_i/README.md`: peso 10 %, rúbrica, fecha orientativa, repo GitHub obligatorio.

---

## Bloque B — Ejercicios (30 min)

Enunciado completo: `ejercicios/E1_pandas.md` (versión ampliada).

| Min | Checkpoint |
| --- | --- |
| 0–8 | Cargar CSV, imprimir dtypes y nulos por columna |
| 8–18 | Función `validar_ventas` + DataFrame `errores` |
| 18–26 | Agregaciones (región, top productos, clientes recurrentes) |
| 26–30 | Exportar `ventas_limpias.csv` + `calidad_datos.json` |

**Criterio de “hecho”:** el JSON de calidad coincide con 8 válidas / 2 inválidas en el dataset del curso.

---

## Bloque C — Presentación Trabajo Intermedio / Proyecto I (~45 min)

1. Leer enunciado y rúbrica en voz alta (10 min).
2. Q&A (10 min).
3. Trabajo individual: repo + README + esqueleto de funciones (25 min).

**Salida esperada hoy:** repo creado, CSV cargado en código propio, al menos una función de validación committed.

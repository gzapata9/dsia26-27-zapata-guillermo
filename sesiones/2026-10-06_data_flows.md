**Materiales de aula:** [`2026-10-06/teoria.md`](2026-10-06/teoria.md) · [`2026-10-06/ejercicios.md`](2026-10-06/ejercicios.md) · [`2026-10-06/ejemplos/`](2026-10-06/ejemplos/)

# 6 oct 2026 — Construcción de flujos de datos (data flows)

**Material:** `3_automatizacion_e_ia/01_data_flows.md` · `ejemplos/pipeline_ventas.py` · `ejercicios/E4_pipeline.md`

| Bloque | Min |
| --- | --- |
| Exposición + demo | 0–30 |
| Ejercicios | 30–60 |
| Proyecto II | 60–105 |

---

## Objetivos

1. Modelar un pipeline por etapas con contratos claros.
2. Separar I/O de lógica pura (testeable).
3. Añadir logging, códigos de salida y umbrales de calidad.
4. Pensar en idempotencia y reproducibilidad.

---

## Bloque A — Exposición (30 min)

### A1. Qué es un data flow en producción (6 min)

```text
Ingesta → Validación → Transformación → Persistencia → Observabilidad
```

Propiedades deseables:

- **Reproducible** (mismos inputs → mismos outputs).
- **Observable** (logs + métricas).
- **Falla ruidosa** (mejor abortar que publicar basura).
- **Idempotente** (re-ejecutar no duplica corrupción).

Comparar notebook ad-hoc vs CLI `pipeline_ventas.py`.

### A2. Diseño por etapas (10 min) — live

Recorrer `pipeline_ventas.py`:

1. `load` — solo I/O.
2. `transform` — puro: DataFrame → (clean, report).
3. `save` — solo I/O.
4. `main` — orquestación + `argparse`.

Demostrar ejecución:

```bash
python ejemplos/pipeline_ventas.py \
  --input Datos/ventas.csv \
  --output-dir Datos/salida
```

Inspeccionar `metrics.json`.

### A3. Contratos y calidad (7 min)

- Columnas obligatorias: ¿qué pasa si falta `precio_unitario`?
- Umbral `--max-error-rate`: si se dropea demasiado, `sys.exit(1)`.
- Versionar el schema (aunque sea un set de columnas en una constante).

### A4. Scheduling mental (7 min)

Dónde viviría este job: cron, GitHub Actions `schedule`, Airflow/Prefect (mencionar sin profundizar).
Puente a Proyecto II: el pipeline es el esqueleto; la IA se enchufa después.

---

## Bloque B — Ejercicios (30 min)

| Min | Checkpoint |
| --- | --- |
| 0–8 | Añadir validación de columnas requeridas al `load`/`transform` |
| 8–16 | `--max-error-rate` + `SystemExit` / código ≠ 0 |
| 16–24 | Log a fichero `run.log` además de consola |
| 24–30 | Test unitario de `transform` con DataFrame sintético (sin disco) |

**Hecho:** pipeline falla de forma controlada si error_rate > umbral; test de transform en verde.

---

## Bloque C — Proyecto II (~45 min)

Arrancar repo/carpeta del Proyecto II; integrar el pipeline como módulo base.

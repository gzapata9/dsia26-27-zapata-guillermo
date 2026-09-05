**Materiales de aula:** [`2026-11-03/teoria.md`](2026-11-03/teoria.md) · [`2026-11-03/ejercicios.md`](2026-11-03/ejercicios.md) · [`2026-11-03/ejemplos/`](2026-11-03/ejemplos/)

# 3 nov 2026 — Despliegue y puesta en producción

**Material:** `5_desarrollo_end_to_end/03_despliegue.md` · `ejercicios/E9_despliegue.md`

| Bloque | Min |
| --- | --- |
| Exposición + demo | 0–30 |
| Ejercicios | 30–60 |
| Proyecto III | 60–105 |

---

## Objetivos

1. Empaquetar una app Python de forma reproducible.
2. Definir proceso de producción (Gunicorn/uvicorn + variables de entorno).
3. Preparar checklist de release (health, logs, secretos, rollback).
4. Dejar evidencia de despliegue o de “listo para desplegar”.

---

## Bloque A — Exposición (30 min)

### A1. Local ≠ producción (5 min)

| Local | Producción |
| --- | --- |
| `app.run(debug=True)` | Gunicorn/uvicorn |
| `.env` en disco | secretos del PaaS |
| un usuario | concurrencia |
| prints | logs agregados |

### A2. Empaquetado mínimo (10 min)

Ficheros que deben existir:

- `requirements.txt` (versiones acotadas)
- runtime Python documentado (`runtime.txt` / setting del PaaS)
- `Procfile` o `startCommand`
- `.env.example`
- `README` con URL o pasos de deploy

Ejemplo Gunicorn para Flask:

```text
web: gunicorn --timeout 120 app:app
```

(Si usan FastAPI: `uvicorn app:app --host 0.0.0.0 --port $PORT`.)

### A3. Estrategia de release (8 min)

1. Tests CI en verde.
2. Tag `v0.x.y`.
3. Deploy.
4. Verificar `/health`.
5. Smoke test del endpoint crítico.
6. Rollback = redesplegar tag anterior.

### A4. Opciones de hosting (7 min)

Render / Fly.io / Cloud Run / Hugging Face Spaces — criterios: coste, cold start, logs, variables de entorno.
No se exige un proveedor concreto; sí evidencia reproducible.

---

## Bloque B — Ejercicios (30 min)

| Min | Checkpoint |
| --- | --- |
| 0–8 | Añadir `Procfile` + `runtime`/nota de Python 3.12 al proyecto |
| 8–16 | Crear `.env.example` completo y revisar que `.env` está ignorado |
| 16–24 | Script `scripts/smoke_test.sh` (curl health + analyze) |
| 24–30 | Sección README “Despliegue” con pasos numerados |

**Hecho:** un compañero puede seguir el README y levantar la app en local en < 10 min.

---

## Bloque C — Proyecto final (~45 min)

Intentar deploy real o dry-run completo; capturar URL o logs para la exposición.

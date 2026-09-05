# Teoría (30 min) — 3 nov 2026  
## Despliegue y puesta en producción

**Demo:** `ejemplos/packaging/`

---

## 1. Introducción (5 min)

Local ≠ producción. En producción necesitas:

- proceso estable (Gunicorn/uvicorn),
- dependencias fijadas,
- secretos fuera del código,
- health + smoke test,
- plan de rollback.

---

## 2. Conceptos

| Artefacto | Para qué |
| --- | --- |
| `requirements.txt` | Reproducir librerías |
| Runtime Python | Misma major/minor en PaaS |
| `Procfile` / start command | Cómo arranca el servicio |
| Variables de entorno | Config + secretos |
| Healthcheck | Orquestador sabe si estás vivo |
| Smoke test | Verificación post-deploy |
| Tag Git | Versión desplegable / rollback |

### Local vs prod

| Local | Prod |
| --- | --- |
| `app.run(debug=True)` | `gunicorn app:app` |
| un usuario | workers |
| `.env` fichero | secretos del proveedor |

---

## 3. Código y ejemplos

Revisa `ejemplos/packaging/`:

- `app.py` con `app` Flask
- `Procfile`
- `runtime.txt`
- `.env.example`
- `scripts/smoke_test.sh`

```bash
cd sesiones/2026-11-03/ejemplos/packaging
pip install -r requirements.txt
python app.py
bash scripts/smoke_test.sh http://127.0.0.1:8012
```

---

## 4. Resumen

- Empaquetar = dejar que otra persona (o el PaaS) lo levante.
- Smoke + health son parte del entregable.
- El proveedor (Render/Fly/…) es secundario frente a la reproducibilidad.

→ `ejercicios.md`

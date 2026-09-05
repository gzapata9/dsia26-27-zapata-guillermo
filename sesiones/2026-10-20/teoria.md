# Teoría (30 min) — 20 oct 2026  
## E2E I: Ingesta → Procesamiento → API de IA

**Demo:** `ejemplos/e2e_mini/` · plantilla Tema 5

---

## 1. Introducción (5 min)

Una solución DSIA no es solo un modelo: es un **flujo conectado**.

```text
CSV → clean/transform → prompt/IA → API HTTP → cliente
```

Hoy montamos el esqueleto del **Proyecto III**.

---

## 2. Conceptos

| Pieza | Responsabilidad |
| --- | --- |
| Ingesta | Leer origen + tipar |
| Validación/proceso | Reglas de negocio + features |
| Cliente IA | Resumen/clasificación/extracción |
| API | Contrato HTTP estable |
| Health | ¿El servicio está vivo? |
| Tests | Camino feliz + error de validación |

### Contrato de API (ejemplo)

`POST /analyze`

```json
{"text": "texto a analizar"}
```

Respuesta:

```json
{"summary": "...", "provider": "mock"}
```

Errores de input → **400**. Dependencia caída → **5xx** (próxima sesión).

---

## 3. Código y ejemplos

```bash
cd sesiones/2026-10-20/ejemplos/e2e_mini
python ingest.py --input ../../../../1_programacion_avanzada_python/Datos/ventas.csv --output data/clean.csv
python app.py
# otra terminal:
curl -s http://127.0.0.1:8010/health
curl -s -X POST http://127.0.0.1:8010/analyze -H 'Content-Type: application/json' \
  -d '{"text":"Necesito un resumen breve de este texto de ejemplo para la demo E2E"}'
pytest -q
```

Señalar en `app.py`: validación de payload, separación `summarize()`, objeto listo para cambiar mock→proveedor real.

---

## 4. Resumen

- Define contratos antes de embellecer.
- Mock en CI; proveedor real en demo si hay clave.
- El Trabajo Final parte de este esqueleto.

→ `ejercicios.md`

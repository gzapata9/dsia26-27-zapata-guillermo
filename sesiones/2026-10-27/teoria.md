# Teoría (30 min) — 27 oct 2026  
## Robustez, errores y logging

**Demo:** `ejemplos/api_robusta.py`

---

## 1. Introducción (5 min)

En E2E I el camino feliz funciona. En producción fallan:

- inputs basura,
- timeouts del proveedor,
- discos llenos,
- bugs propios.

Hoy diseñamos **fallos útiles**.

---

## 2. Conceptos

| Tipo de fallo | HTTP | Log |
| --- | --- | --- |
| Validación | 400 | WARNING |
| Dependencia IA | 502/503 | ERROR |
| Timeout | 504 | ERROR |
| Bug | 500 | ERROR + request_id |

### Logging

- Niveles: DEBUG / INFO / WARNING / ERROR  
- Correlación: `request_id`  
- Nunca loguear API keys ni PII completa  

### Health útil

```json
{"status": "ok|degraded", "checks": {"api": "ok", "ai": "ok"}}
```

---

## 3. Código y ejemplos

```bash
python sesiones/2026-10-27/ejemplos/api_robusta.py
# FORCE_AI_FAIL=1 para simular dependencia caída
```

El ejemplo incluye:

- `request_id` en respuesta y logs
- `latency_ms`
- 503 si el “proveedor” falla
- `/health` con checks

---

## 4. Resumen

- Taxonomía de errores → códigos coherentes.
- Logs accionables.
- Tests también del camino de error.

→ `ejercicios.md`

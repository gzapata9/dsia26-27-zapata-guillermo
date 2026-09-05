# 27 oct 2026 — E2E II: Robustez, errores y logging

**Material:** `5_desarrollo_end_to_end/02_robustez_logging.md` · `ejercicios/E8b_robustez.md`

| Bloque | Min |
| --- | --- |
| Exposición + demo | 0–30 |
| Ejercicios | 30–60 |
| Proyecto III | 60–105 |

---

## Objetivos

1. Clasificar errores (validación vs infraestructura vs proveedor IA).
2. Añadir timeouts, reintentos y respuestas HTTP coherentes.
3. Introducir logging estructurado sin filtrar secretos.
4. Exponer salud del sistema más allá de un “ok” trivial.

---

## Bloque A — Exposición (30 min)

### A1. Taxonomía de fallos (6 min)

| Tipo | Ejemplo | Respuesta |
| --- | --- | --- |
| Validación | JSON sin `text` | 400 |
| Dependencia | API IA caída | 502/503 + log |
| Timeout | proveedor > 10 s | 504 / reintento |
| Bug propio | KeyError interno | 500 + log con request_id |

Principio: **fallar de forma útil** (mensaje claro, sin stacktrace al cliente).

### A2. Logging que sirve en producción (10 min) — live

```python
logger.info("analyze_ok", extra={"chars": n, "provider": "mock", "latency_ms": 12})
```

Buenas prácticas:

- Niveles: DEBUG / INFO / WARNING / ERROR.
- Correlación: `request_id`.
- Nunca loguear API keys ni prompts con datos personales.
- Formato consistente para grep/`jq`.

Demo: añadir timing alrededor de `summarize`.

### A3. Resiliencia en clientes HTTP/IA (8 min)

- Timeout explícito.
- Reintentos con backoff solo en 429/5xx.
- Circuit breaker mental: tras N fallos, degradar a mock o cola.
- Idempotencia de `POST` (cuidado con efectos laterales).

### A4. Healthchecks útiles (6 min)

`/health` ampliado:

```json
{"status": "ok", "checks": {"disk": "ok", "ai_provider": "mock"}}
```

Diferencia liveness vs readiness (mencionar).

---

## Bloque B — Ejercicios (30 min)

| Min | Checkpoint |
| --- | --- |
| 0–8 | Añadir `request_id` (uuid) a logs de `/analyze` |
| 8–16 | Simular fallo del proveedor → 503 JSON `{"error": "..."}` |
| 16–24 | Medir `latency_ms` y loguearlo |
| 24–30 | Extender `/health` con check del path de datos |

**Hecho:** un test verifica 503 (o el código elegido) cuando el cliente IA lanza error.

---

## Bloque C — Proyecto final (~45 min)

Aplicar robustez real al Trabajo Final; actualizar README con “comportamiento ante errores”.

# Ejercicios (30 min) — 27 oct 2026  
## Repaso de robustez y logging

---

### Ej. 1 — Conceptos (5 min)

1. Asigna status code a: JSON sin `text`, OpenAI 500, bug `KeyError` interno.
2. ¿Qué NO debes meter en un log?
3. Diferencia liveness vs readiness (1–2 frases).

### Ej. 2 — Probar la API robusta (8 min)

```bash
python sesiones/2026-10-27/ejemplos/api_robusta.py
```

Prueba `/analyze` normal y con `FORCE_AI_FAIL=1`. Observa `request_id`.

### Ej. 3 — Añadir un check (10 min)

Extiende `/health` para verificar que existe un path de datos (`DATA_PATH` env o default). Si no existe → `degraded` + 503.

### Ej. 4 — Test del 503 (7 min)

Escribe un test que fuerce el fallo del proveedor y espere 503.

### Criterio de cierre

- [ ] Sabes mapear error→HTTP  
- [ ] Health degradado funciona  
- [ ] Test 503 en verde  

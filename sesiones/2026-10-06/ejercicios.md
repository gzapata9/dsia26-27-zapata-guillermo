# Ejercicios (30 min) — 6 oct 2026  
## Repaso de data flows

Usa `ejemplos/mini_pipeline.py` (o el pipeline del Tema 3).

---

### Ej. 1 — Conceptos (5 min)

1. ¿Qué etapas deben ser “puras” y por qué?
2. ¿Qué significa idempotencia en un job que escribe `ventas_limpias.csv`?
3. ¿Cuándo usarías exit code 1 vs 2?

### Ej. 2 — Ejecutar y leer métricas (7 min)

Corre el pipeline con umbral 0.5. Abre `metrics.json` y anota `error_rate`.

Repite con `0.05` y comprueba el código de salida.

### Ej. 3 — Extender el contrato (10 min)

Añade la columna opcional `moneda`. Si existe, debe ser `EUR` o `USD`; si no, cuenta como error de fila **o** rechaza el batch (elige una política y documéntala en 2 líneas).

### Ej. 4 — Test puro (8 min)

Escribe un test de `transform` con DataFrame en memoria (sin disco) que verifique `rows_dropped`.

```bash
pytest -q sesiones/2026-10-06/ejemplos
```

### Criterio de cierre

- [ ] Sabes interpretar `metrics.json`  
- [ ] Umbral provoca exit 1  
- [ ] Hay al menos 1 test de `transform`  

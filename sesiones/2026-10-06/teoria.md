# Teoría (30 min) — 6 oct 2026  
## Flujos de datos (data flows)

**Demo:** `ejemplos/mini_pipeline.py` · pipeline completo del Tema 3

---

## 1. Introducción (5 min)

Un **pipeline** es un job reproducible, no una sesión interactiva de notebook.

```text
Ingesta → Validación → Transformación → Persistencia → Observabilidad
```

En producción importa: fallar claro, dejar métricas y poder re-ejecutar.

---

## 2. Conceptos

| Concepto | Definición |
| --- | --- |
| Etapa | Función con responsabilidad única |
| Contrato de datos | Columnas/tipos mínimos esperados |
| Lógica pura | Transformación testeable sin disco |
| I/O de borde | `load` / `save` |
| Idempotencia | Re-ejecutar no corrompe el resultado |
| Umbral de calidad | Abortar si hay demasiados errores |
| Observabilidad | Logs + `metrics.json` |

### Separación clave

```python
def transform(df) -> tuple[pd.DataFrame, dict]:
    """Puro: no lee ni escribe ficheros."""
    ...
```

---

## 3. Código y ejemplos

```bash
python sesiones/2026-10-06/ejemplos/mini_pipeline.py \
  --input 1_programacion_avanzada_python/Datos/ventas.csv \
  --output-dir /tmp/dsia-flow \
  --max-error-rate 0.5
```

Fuerza fallo de calidad:

```bash
python ... --max-error-rate 0.05   # exit code 1 con el CSV del curso
```

Elementos a señalar en el código:

1. Validación de columnas requeridas.
2. `error_rate` en el report.
3. Log a fichero + consola.
4. `sys.exit` con códigos distintos (1 calidad, 2 input).

---

## 4. Resumen

- Contratos + umbrales evitan publicar basura.
- Lo puro se testea; el I/O se integra.
- El report JSON es el embrión de monitorización.

→ `ejercicios.md`

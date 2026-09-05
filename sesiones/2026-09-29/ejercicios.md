# Ejercicios (30 min) — 29 sep 2026  
## Repaso de pytest

Parte de `ejemplos/` de esta sesión.

---

### Ej. 1 — Conceptos (5 min)

1. Diferencia unitario vs integración con un ejemplo de ventas.
2. ¿Para qué sirve `parametrize`?
3. ¿Qué problema hay si un test depende del orden de ejecución?

### Ej. 2 — Ejecutar y leer fallos (5 min)

```bash
cd sesiones/2026-09-29/ejemplos
pytest -q
```

Cambia un `assert` a propósito, ejecuta `pytest -vv`, lee el diff, y restáuralo.

### Ej. 3 — Ampliar la suite (12 min)

Añade al menos **3 tests nuevos**:

1. Una fila con `unidades=None` → inválida.
2. Dos filas válidas → `importe` correcto en la agregación (si aplica) o conteo.
3. `@pytest.mark.integration` leyendo el `ventas.csv` real del curso (8 válidas).

### Ej. 4 — Filtrar marcadores (8 min)

```bash
pytest -q -m "not integration"
pytest -q -m integration
```

Documenta en 2 líneas cuándo usarías cada comando en CI vs local.

### Criterio de cierre

- [ ] ≥ 3 tests nuevos en verde  
- [ ] Sabes explicar un fallo de pytest  
- [ ] Marcadores funcionan  

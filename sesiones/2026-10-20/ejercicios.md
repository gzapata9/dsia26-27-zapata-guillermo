# Ejercicios (30 min) — 20 oct 2026  
## Repaso del flujo E2E

Trabaja sobre `ejemplos/e2e_mini/` o tu copia del Proyecto III.

---

### Ej. 1 — Conceptos (5 min)

1. Nombra las 4 etapas del flujo visto en teoría.
2. ¿Qué status code usarías si falta `text`?
3. ¿Por qué `/health` no debería ejecutar el modelo completo?

### Ej. 2 — Levantar el mini E2E (8 min)

Sigue los comandos de la teoría. Captura (o anota) las dos respuestas JSON.

### Ej. 3 — Enchufar el cliente mock (10 min)

Sustituye el resumen “naive” por una función `complete_mock(prompt)` que devuelva `[mock] …` (puedes copiar la idea de la sesión 13 oct).

La respuesta debe incluir `"provider": "mock"`.

### Ej. 4 — Test de teoría aplicada (7 min)

Añade/verifica:

- test happy path `/analyze`
- test 400 si `text` vacío

```bash
pytest -q
```

### Criterio de cierre

- [ ] API responde  
- [ ] provider mock visible  
- [ ] tests en verde  

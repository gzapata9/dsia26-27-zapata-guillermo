# Ejercicios (30 min) — 10 nov 2026  
## Repaso del uso de IA en desarrollo

---

### Ej. 1 — Conceptos (5 min)

1. ¿Qué es una alucinación en código generado? Da un ejemplo.
2. ¿Por qué pedir un *plan* antes de implementar?
3. ¿Qué debe incluir `AI_USAGE.md`?

### Ej. 2 — Explicar deuda (7 min)

Abre `ejemplos/modulo_deuda.py`. Con tu asistente (o a mano si no hay tool):

- resume en 5 líneas qué hace y qué huele mal;
- pégalo en `AI_USAGE.md`.

### Ej. 3 — Plan + un fix (10 min)

1. Pide un plan de refactor (sin código).
2. Implementa **solo el ítem 1** (p. ej. renombres o extraer función).
3. Diff pequeño.

### Ej. 4 — Tests y rechazo (8 min)

1. Pide 3 tests.
2. Ejecuta pytest.
3. Si alguno alucina, bórralo y documenta el rechazo.

### Criterio de cierre

- [ ] AI_USAGE con explicación + plan + aceptación/rechazo  
- [ ] Un refactor real committed  
- [ ] Al menos 1 test útil en verde  

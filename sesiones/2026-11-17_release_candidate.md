**Materiales de aula:** [`2026-11-17/teoria.md`](2026-11-17/teoria.md) · [`2026-11-17/ejercicios.md`](2026-11-17/ejercicios.md) · [`2026-11-17/ejemplos/`](2026-11-17/ejemplos/)

# 17 nov 2026 — Revisión, refactor, tests/docs con IA + Release Candidate

**Material:** `ejercicios/E7_refactor_tests_docs.md` · catálogo de prompts · Proyecto III

| Bloque | Min |
| --- | --- |
| Exposición + demo | 0–30 |
| Taller / ejercicios | 30–60 |
| Integración RC | 60–105 |

---

## Objetivos

1. Conducir una code review asistida por IA centrada en riesgos.
2. Generar documentación y tests faltantes con supervisión humana.
3. Cerrar un **Release Candidate** (`v0.9.0-rc1`).
4. Preparar guion de la exposición de diciembre.

---

## Bloque A — Exposición (30 min)

### A1. Qué es un Release Candidate (5 min)

- Feature freeze razonable.
- Tests verdes + smoke de deploy.
- Issues conocidos documentados (no sorpresas en la demo).

### A2. Code review con IA (10 min) — live

Prompt tipo:

```text
Revisa este diff centrado en: secretos, validación de inputs,
timeouts, manejo de errores y complejidad.
Lista hallazgos por severidad. No reescribas todo el archivo.
```

Triaje en pizarra: crítico / mayor / menor / ruido.

### A3. Generación de docs y tests (10 min)

- README orientado a demos (instalación en 5 pasos + curl de ejemplo).
- Tests del camino feliz E2E + 2 errores controlados.
- Evitar docs genéricas (“this project is a Python project”).

### A4. Guion de exposición (5 min)

Estructura 5–7 min:

1. Problema (45 s)
2. Arquitectura (1 min)
3. Demo en vivo (2–3 min)
4. Tests/despliegue (1 min)
5. Limitaciones + uso de IA (45 s)

---

## Bloque B — Taller (30 min)

| Min | Checkpoint |
| --- | --- |
| 0–8 | Review IA → seleccionar 3 hallazgos reales y fix |
| 8–16 | Completar README de demo |
| 16–24 | Tests faltantes + pytest verde |
| 24–30 | Tag `v0.9.0-rc1` + checklist RC firmada en `AI_USAGE.md` o `RELEASE.md` |

**Hecho:** tag RC en Git + README reproducible + suite verde.

---

## Bloque C — Integración final (~45 min)

Ensayo corto de demo por parejas; lista de pendientes pre-diciembre (solo blockers).

# Teoría (30 min) — 17 nov 2026  
## Review, refactor, tests/docs con IA + Release Candidate

**Material:** `ejemplos/checklist_rc.md` · `ejemplos/prompt_review.md`

---

## 1. Introducción (5 min)

Un **Release Candidate** es “casi final”:

- features congeladas (salvo blockers),
- tests verdes,
- demo ensayada,
- issues conocidos escritos.

Hoy cerramos el Trabajo Final hacia `v0.9.0-rc1`.

---

## 2. Conceptos

| Concepto | Práctica |
| --- | --- |
| Code review | Buscar riesgos, no estilo cosmética |
| Severidad | crítico / mayor / menor / ruido |
| Feature freeze | No añadir “una idea más” |
| README de demo | 5 pasos para un desconocido |
| Guion de exposición | 5–7 min cronometrados |
| Tag RC | `v0.9.0-rc1` |

### Review con IA (enfoque)

Prioriza: secretos, validación, timeouts, errores, complejidad.  
Ignora sugerencias genéricas tipo “añade más comentarios”.

---

## 3. Código / artefactos de ejemplo

- `ejemplos/prompt_review.md` — prompt de review por severidad.
- `ejemplos/checklist_rc.md` — lista de cierre.
- Plantilla de guion de demo (en el checklist).

---

## 4. Resumen

- RC = evidencia, no sentimiento.
- IA ayuda a revisar; tú priorizas y corriges.
- La exposición se ensaya, no se improvisa.

→ `ejercicios.md`

# 10 nov 2026 — Herramientas de desarrollo con IA generativa

**Material:** `4_entornos_ia_generativa/` · `prompts/catalogo_prompts.md` · `ejercicios/E6_asistentes.md`

| Bloque | Min |
| --- | --- |
| Exposición + demo | 0–30 |
| Ejercicios | 30–60 |
| Proyecto III | 60–105 |

---

## Objetivos

1. Usar Cursor / Claude Code / Gemini CLI sobre **código existente**.
2. Aplicar un flujo Contexto → Prompt → Revisión → Tests.
3. Detectar alucinaciones y deuda introducida por la IA.
4. Registrar el uso en `AI_USAGE.md`.

---

## Bloque A — Exposición (30 min)

### A1. IA como copiloto, no como autor (5 min)

- Responsabilidad académica y de producto.
- Citar herramienta = obligatorio cuando aporta partes relevantes.
- Riesgos: código inseguro, dependencias inventadas, APIs obsoletas.

### A2. Comparativa de herramientas (8 min)

| Herramienta | Fortaleza en clase |
| --- | --- |
| **Cursor** | Edición multiarchivo en el IDE |
| **Claude Code** | Agente CLI con tareas largas |
| **Gemini CLI** | Exploración rápida / prototipos |

Demo corta (una herramienta): “explica este módulo” sobre `plantilla_proyecto/app.py`.

### A3. Ingeniería de prompts para código (10 min)

Usar el catálogo:

1. Explicar sin reescribir.
2. Plan de refactor (sin implementar).
3. Implementar un cambio pequeño.
4. Generar tests.
5. Code review de seguridad.

Enseñar a **acotar contexto**: fichero, firma pública, restricciones (“no nuevas dependencias”).

### A4. Protocolo de aceptación (7 min)

Checklist en voz alta antes de `git commit`:

- ¿Lo entiendo?
- ¿Pasan tests?
- ¿Hay secretos nuevos?
- ¿El diff es mínimo?

---

## Bloque B — Ejercicios (30 min)

| Min | Checkpoint |
| --- | --- |
| 0–5 | Elegir un smell real del Proyecto III |
| 5–12 | Prompt de explicación + pegar resumen en `AI_USAGE.md` |
| 12–22 | Prompt de plan → implementar solo 1 ítem del plan |
| 22–30 | Pedir 3 tests; ejecutar pytest; descartar los que fallen por alucinación |

**Hecho:** 1 PR/commit de refactor revisado + entrada en `AI_USAGE.md`.

---

## Bloque C — Proyecto final (~45 min)

Seguir refactorizando con el mismo protocolo; preparar lista de módulos a revisar el 17 nov.

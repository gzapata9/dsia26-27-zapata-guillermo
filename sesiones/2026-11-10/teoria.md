# Teoría (30 min) — 10 nov 2026  
## Herramientas de desarrollo con IA generativa

**Material:** `ejemplos/modulo_deuda.py` · `prompts_clase.md`

---

## 1. Introducción (5 min)

La IA acelera, pero **tú firmas** el código.  
Flujo profesional:

```text
Contexto → Prompt → Borrador → Revisión humana → Tests → Commit
```

Trabajamos sobre **código existente** (deuda real), no sobre un repo vacío.

---

## 2. Conceptos

| Idea | Práctica |
| --- | --- |
| Contexto acotado | Pega un módulo, no todo el monorepo |
| Prompt de explicación | Entender antes de reescribir |
| Prompt de plan | Pedir pasos sin código |
| Alucinación | APIs inventadas, imports fantasma |
| AI_USAGE.md | Trazabilidad académica |
| Diff mínimo | Aceptar solo cambios que entiendes |

### Herramientas

| Tool | Encaje |
| --- | --- |
| Cursor | Edición multiarchivo en IDE |
| Claude Code | Agente CLI |
| Gemini CLI | Exploración / prototipos |

---

## 3. Código y ejemplos

Módulo con deuda deliberada: `ejemplos/modulo_deuda.py`.

Prompts de clase: `ejemplos/prompts_clase.md` (explicar → plan → tests).

Demo en vivo: explicar el módulo, proponer plan, aplicar **un** cambio, generar tests, rechazar lo alucinado.

---

## 4. Resumen

- Protocolo de aceptación > modelo “mágico”.
- Citar es parte de la entrega.
- Tests son el freno de mano.

→ `ejercicios.md`

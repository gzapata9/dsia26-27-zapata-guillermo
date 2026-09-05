# Ejercicios (30 min) — 13 oct 2026  
## Repaso de APIs de IA

---

### Ej. 1 — Conceptos (5 min)

1. ¿Por qué el modo `mock` debe existir aunque tengas API key?
2. ¿Qué metes en `.env.example` vs `.env`?
3. ¿Reintentarías un 401? ¿Por qué sí/no?

### Ej. 2 — Smoke mock (5 min)

```bash
python sesiones/2026-10-13/ejemplos/cliente_ia_teoria.py \
  --provider mock --prompt "Hola DSIA"
```

### Ej. 3 — Batch JSONL (12 min)

1. Edita `ejemplos/prompts.txt` con 5 prompts.
2. Genera `respuestas.jsonl`.
3. Verifica que hay 5 líneas y campos `prompt`, `provider`, `text`.

### Ej. 4 — Diseño de resiliencia (8 min)

Implementa (o pseudocódigo si falta tiempo) **1 reintento** cuando una función interna simula fallo la primera vez (`--fail-once`).

Documenta en `AI_USAGE.md` si usaste un asistente para esta parte.

### Criterio de cierre

- [ ] Batch con 5 respuestas  
- [ ] Respuestas Ej. 1  
- [ ] Idea de retry documentada o implementada  

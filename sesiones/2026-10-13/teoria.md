# Teoría (30 min) — 13 oct 2026  
## Integración de servicios de IA vía API

**Demo:** `ejemplos/cliente_ia_teoria.py` · Tema 3 `ai_api_client.py`

---

## 1. Introducción (5 min)

Las capacidades de IA suelen consumirse como **servicios HTTP** (OpenAI, Anthropic, Hugging Face).  
Tu código debe tratarlos como **dependencias inestables**: con secretos, timeouts y fallback.

```text
App → Cliente unificado → Proveedor (mock | openai | anthropic | hf)
```

---

## 2. Conceptos

| Concepto | Detalle |
| --- | --- |
| API key | Secreto; vive en env / `.env`, nunca en Git |
| SDK | Biblioteca oficial que encapsula HTTP |
| Proveedor | Backend de modelos |
| Mock | Implementación local para desarrollo/CI |
| Normalización | Misma estructura de respuesta (`provider`, `text`) |
| Retry/backoff | Reintentar 429/5xx con espera |
| Fallback | Si falla el proveedor → mock o cola |

### Política del curso

- Modo `mock` **obligatorio** para poder trabajar sin claves.
- Citar uso de IA en `AI_USAGE.md` cuando genere partes del trabajo.

---

## 3. Código y ejemplos

```bash
python sesiones/2026-10-13/ejemplos/cliente_ia_teoria.py --provider mock --prompt "Resume SOLID en 3 bullets"
python sesiones/2026-10-13/ejemplos/cliente_ia_teoria.py --batch ejemplos/prompts.txt --output /tmp/out.jsonl
```

El ejemplo muestra:

1. `AIResponse` dataclass.
2. `complete(provider, prompt)`.
3. Batch → JSONL.
4. Error explícito si falta API key en proveedores reales.

---

## 4. Resumen

- Unifica proveedores detrás de una interfaz.
- Secretos fuera del código.
- Diseña para fallo (retry + mock).

→ `ejercicios.md`

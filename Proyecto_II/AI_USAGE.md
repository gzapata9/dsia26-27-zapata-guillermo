# AI_USAGE — Proyecto II

## 1. IA dentro del producto (borde de modelos vía API)

| Campo | Valor |
|---|---|
| Proveedores | `mock` (por defecto, tests y CI) · `hf` Hugging Face Inference Providers · `nvidia` NVIDIA API Catalog |
| Tarea | `chat_completion` (LLM instruct) |
| Modelos | `nvidia`: `nvidia/nemotron-3.5-bolt-e4b` · `hf`: modelo del Hub `meta-llama/Llama-3.1-8B-Instruct` |
| Entrada | Solo agregados de la previsión de sklearn: horas punta, ventanas valle, horas de lluvia y festivos. Sin datos personales |
| Salida | Briefing operativo en español (≤150 palabras) para reequilibrado y mantenimiento |
| Prompt | `bikedemand/integrations/prompts.py`, versión `briefing-v1` |
| Parámetros | `temperature=0.3`, `max_tokens=500`, timeout de 30 s, hasta 3 intentos solo en fallos transitorios |
| Secretos | `HF_TOKEN` y `NVIDIA_API_KEY` solo en `.env` (ignorado por Git). `Settings` no los muestra (`repr=False`) y no se escriben en el log |
| Salvaguardas | El LLM no decide ni predice. El informe incluye siempre la tabla del modelo y el resumen por reglas para poder contrastar lo que dice. Si la IA falla, el job sigue en modo `degraded` |

## 2. IA usada durante el desarrollo

| Herramienta | Uso |
|---|---|
| Claude (Anthropic), asistente conversacional | Propuesta de la arquitectura modular, primera versión de algunos ficheros de código, refinamiento de tests, comprobaciones de workflows de GitHub Actions, diagrama de arquitectura y borradores del README |

### Comandos de uso

```bash
pytest -q 
python -m bikedemand run-all                    
python -m bikedemand forecast 
```

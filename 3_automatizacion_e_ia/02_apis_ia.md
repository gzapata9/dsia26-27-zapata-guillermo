# Sesión 6 (13 oct 2026): Integración de servicios de IA vía API

## Objetivos

- Consumir APIs de OpenAI, Anthropic y Hugging Face.
- Gestionar claves con `.env` (nunca en el código).
- Diseñar un cliente con **fallback** y modo `mock` para desarrollo.

## Preparación

```bash
cp .env.example .env
# edita .env con tus claves (opcionales si usas --provider mock)
pip install openai anthropic huggingface_hub   # según proveedor
```

## Demo

```bash
cd 3_automatizacion_e_ia/ejemplos
python ai_api_client.py --provider mock --prompt "Explica un data pipeline en 5 líneas"
```

## Ejercicio

Ver `ejercicios/E5_apis_ia.md`.

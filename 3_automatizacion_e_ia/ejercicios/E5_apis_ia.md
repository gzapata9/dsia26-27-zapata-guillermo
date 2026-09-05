# E5 — Cliente multi-API de IA

1. Parte de `ejemplos/ai_api_client.py`.
2. Añade reintentos con backoff ante errores 429/5xx.
3. Implementa un modo `batch`: lee prompts desde un fichero `.txt` (uno por línea) y guarda respuestas en JSONL.
4. Documenta en el README qué proveedor usaste y **cita el uso de IA** si generaste parte del código con un asistente.

Criterio mínimo: funciona con `--provider mock` sin claves.

# Sesión 7 (20 oct 2026): E2E I — flujo completo

## Arquitectura de referencia

```text
[CSV / API origen]
        │
        ▼
   Ingesta + validación
        │
        ▼
   Procesamiento / features
        │
        ▼
   Servicio de IA (API)
        │
        ▼
   API propia (Flask/FastAPI) ──► Cliente / dashboard
        │
        ▼
   Logs + métricas
```

## Requisitos mínimos del Trabajo Final

1. Código modular con tests.
2. Al menos una integración real o mockeable con un servicio de IA.
3. Endpoint HTTP documentado.
4. Instrucciones de ejecución local y de despliegue.

Usa la plantilla en `plantilla_proyecto/` como punto de partida opcional.

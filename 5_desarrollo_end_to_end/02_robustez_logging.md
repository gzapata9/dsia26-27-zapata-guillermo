# Sesión 8 (27 oct 2026): E2E II — robustez, errores y logging

## Prácticas

- Excepciones de dominio vs excepciones de infraestructura.
- Timeouts y reintentos en llamadas HTTP.
- Logging estructurado (`level`, `event`, `duration_ms`).
- No registrar secretos ni payloads sensibles completos.

## Ejemplo de logger

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("dsia.e2e")
logger.info("prediction_ok", extra={"latency_ms": 120, "provider": "mock"})
```

## Ejercicio en clase

Añade a tu API:

1. Validación de input con mensajes 400 claros.
2. Timeout en el cliente de IA.
3. Endpoint `GET /health` que reporte estado del pipeline.

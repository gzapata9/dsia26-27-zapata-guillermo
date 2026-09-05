# E2 — Arquitectura modular, Clean Code y SOLID

## Contexto

Partiendo del ejercicio de ventas, refactoriza tu solución en un **paquete pequeño**:

```text
ventas_app/
  __init__.py
  loader.py      # carga CSV
  validator.py   # reglas de validación
  metrics.py     # agregaciones
  cli.py         # punto de entrada
```

## Tareas

1. Aplica al menos **3 principios SOLID** (documenta cuál y dónde).
2. Sustituye “números mágicos” y strings repetidos por constantes o configuración.
3. Define excepciones de dominio (`ValidationError`, `DataLoadError`).
4. Añade un `README` de 15–20 líneas explicando cómo ejecutar el CLI:

```bash
python -m ventas_app.cli --input Datos/ventas.csv --output Datos/ventas_limpias.csv
```

## Entrega orientativa

Este ejercicio alimenta el **Proyecto I** (`proyectos/proyecto_i/`).

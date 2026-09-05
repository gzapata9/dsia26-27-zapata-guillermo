# E3 — Tests del pipeline de ventas

## Objetivo

Añade una carpeta `tests/` a tu solución del Proyecto I / ejercicio E2 y cubre:

1. Carga correcta de CSV existente.
2. Error controlado si el fichero no existe.
3. Separación de filas válidas / inválidas (usa el `ventas.csv` del curso).
4. Cálculo de importe por región con un dataset pequeño **en memoria** (fixture).

## Criterios

- Al menos **8 tests** pasando con `pytest -q`.
- Cobertura de casos límite (precio negativo, unidades vacías).
- Un test marcado como `@pytest.mark.integration` que lea el CSV real.

## Entrega

Incluye en el README del proyecto cómo ejecutar los tests.

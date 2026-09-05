# Sesión 5 (6 oct 2026): Flujos de datos (data flows)

## Idea clave

Un **pipeline** es una secuencia reproducible:

```text
Ingesta → Validación → Transformación → Persistencia → Observabilidad
```

Cada etapa:

- tiene una responsabilidad clara,
- falla de forma controlada,
- deja rastro (logs / métricas).

## Ejemplo del curso

```bash
cd 3_automatizacion_e_ia
python ejemplos/pipeline_ventas.py \
  --input Datos/ventas.csv \
  --output-dir Datos/salida
```

## Patrones útiles

- **Idempotencia**: re-ejecutar no corrompe el resultado.
- **Contratos de datos**: schema mínimo esperado (columnas, tipos).
- **Separación I/O vs lógica**: facilita los tests.

## Ejercicio

Ver `ejercicios/E4_pipeline.md`.

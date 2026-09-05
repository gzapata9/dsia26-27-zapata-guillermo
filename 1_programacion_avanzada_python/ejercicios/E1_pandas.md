# E1 — Procesamiento de datos con pandas

Dataset: `Datos/ventas.csv`

## Tareas

1. Carga el CSV y muestra `shape`, tipos y primeras filas.
2. Calcula el **importe** = `unidades * precio_unitario` (gestiona valores nulos).
3. Detecta filas inválidas (unidades nulas, precio ≤ 0) y sepáralas en un DataFrame `errores`.
4. Sobre los datos válidos:
   - Ventas totales por `region`
   - Top 3 productos por importe
   - Clientes con más de una compra
5. Exporta el resultado limpio a `Datos/ventas_limpias.csv` y un informe de calidad a `Datos/calidad_datos.json` con conteos de filas válidas/inválidas.

## Criterios de calidad

- Código en funciones reutilizables (`cargar`, `validar`, `agregar`, `exportar`).
- Docstrings breves.
- Sin hardcodear rutas absolutas: usa `pathlib.Path`.

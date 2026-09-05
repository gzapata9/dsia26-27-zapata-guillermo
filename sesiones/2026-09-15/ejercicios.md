# Ejercicios (30 min) — 15 sep 2026  
## Repaso de la teoría de pandas

Dataset: `1_programacion_avanzada_python/Datos/ventas.csv`  
Puedes basarte en `ejemplos/demo_pandas_ventas.py` o en el notebook del Tema 1.

---

### Ej. 1 — Conceptos (5 min)

En un markdown o comentarios:

1. ¿Qué hace `errors="coerce"` en `to_numeric`?
2. ¿Por qué devolvemos también el DataFrame de `errores`?
3. Diferencia entre `loc` con máscara booleana y filtrar “a mano” con un bucle.

### Ej. 2 — Reproducir el diagnóstico (7 min)

Escribe un script `mi_e1.py` que imprima:

- `shape`
- `dtypes`
- nulos por columna
- las filas con `unidades` nula o `precio_unitario <= 0`

### Ej. 3 — Implementar `validar_ventas` (10 min)

Sin mirar la solución al principio:

- implementa la función de la teoría;
- assert mental / print: 8 válidas, 2 inválidas;
- calcula `importe`.

Comprueba con:

```bash
python sesiones/2026-09-15/ejemplos/demo_pandas_ventas.py
```

### Ej. 4 — Agregar + exportar (8 min)

1. Importe por región (desc).
2. Top 3 productos.
3. Clientes con >1 compra.
4. Escribe `ventas_limpias.csv` y `calidad_datos.json` con conteos e `importe_total`.

### Criterio de cierre

- [ ] Respuestas Ej. 1  
- [ ] 8/2 en validación  
- [ ] JSON de calidad generado  

Extensión: parsea `fecha` a datetime y agrega por semana.

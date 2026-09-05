# Ejercicios (30 min) — 22 sep 2026  
## Repaso Clean Code / SOLID

Demo: `ejemplos/solid_ventas.py`

---

### Ej. 1 — Conceptos (6 min)

Responde brevemente:

1. ¿Qué responsabilidad tiene `SalesValidator` y cuál **no** debería tener?
2. Si mañana leemos JSON en lugar de CSV, ¿qué clase cambias y cuáles no (DIP)?
3. Pon un ejemplo de violación de SRP en un notebook típico.

### Ej. 2 — Leer y trazar el ejemplo (7 min)

Ejecuta la demo. Luego, en un diagrama ASCII de 5 líneas, dibuja el flujo de llamadas desde `main`.

Rompe a propósito el path del CSV y comprueba que aparece `DataLoadError`.

### Ej. 3 — Extender sin romper (10 min) — OCP

Añade a `SalesMetrics` un método `total_by_product` **sin modificar** `SalesValidator` ni el repository.

Imprímelo en `main`.

### Ej. 4 — Mini paquete (7 min)

Crea (aunque sea esqueleto) en tu repo:

```text
ventas_app/loader.py
ventas_app/validator.py
ventas_app/metrics.py
ventas_app/cli.py
```

Mueve/copia responsabilidades. Documenta en `DESIGN.md` **3 principios SOLID** con anclaje a fichero.

### Criterio de cierre

- [ ] Ej. 1 contestado  
- [ ] `total_by_product` funciona  
- [ ] DESIGN.md con 3 principios  

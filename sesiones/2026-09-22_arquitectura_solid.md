# 22 sep 2026 — Arquitectura modular, Clean Code y SOLID

**Material:** `1_programacion_avanzada_python/03_oop_clean_code_solid.py` · `03_arquitectura_patrones.md` · `ejercicios/E2_arquitectura.md`

| Bloque | Min |
| --- | --- |
| Exposición + demo | 0–30 |
| Ejercicios | 30–60 |
| Proyecto I | 60–105 |

---

## Objetivos

1. Separar responsabilidades en módulos (loader / validator / metrics / CLI).
2. Aplicar al menos SRP, OCP y DIP con un ejemplo concreto.
3. Introducir excepciones de dominio y dataclasses.
4. Reconocer code smells frecuentes en notebooks convertidos a “producción”.

---

## Bloque A — Exposición (30 min)

### A1. Del notebook al paquete (5 min)

- Síntomas de deuda: celda de 80 líneas, rutas absolutas, prints como logging.
- Objetivo: **mismo comportamiento**, mejor estructura.
- Diagrama:

```text
CLI → Repository → Validator → Metrics → Output
```

### A2. Clean Code esencial (7 min)

Checklist en pizarra / slides:

| Sí | No |
| --- | --- |
| Nombres que revelan intención | `df2`, `tmp`, `x` |
| Funciones cortas, un nivel de abstracción | Mega-función “hace-todo” |
| Constantes con nombre | Números mágicos (`0.3`, `19.5`) |
| Errores explícitos | `except: pass` |

Ejemplo rápido: renombrar y extraer una función del notebook de la sesión anterior.

### A3. SOLID con el caso ventas (12 min) — live sobre `03_oop_clean_code_solid.py`

Recorrer el script línea a línea:

1. **SRP** — `SalesValidator` solo valida; `SalesMetrics` solo agrega.
2. **OCP** — nuevas métricas sin tocar el validador.
3. **LSP** — cualquier `SalesRepository` debe poder `load()`.
4. **ISP** — Protocol pequeño (`load`), no interfaz dios.
5. **DIP** — `main` depende del Protocol, no del CSV concreto.

Demostrar `DataLoadError` si el path no existe.

**Pregunta:** ¿dónde meterías un `JsonSalesRepository` sin reescribir métricas?

### A4. Patrones ligeros útiles en DSIA (6 min)

- **Repository** (acceso a datos).
- **Pipeline / Pipeline stage** (cadena de transformaciones).
- **Strategy** (cambiar validador o proveedor de IA).
- Evitar over-engineering: no hace falta Factory + Abstract Singleton en un CSV de 10 filas.

Cierre: el Proyecto I se evalúa también por diseño, no solo por que “corra”.

---

## Bloque B — Ejercicios (30 min)

Enunciado: `ejercicios/E2_arquitectura.md`.

| Min | Checkpoint |
| --- | --- |
| 0–10 | Crear paquete `ventas_app/` con 4 módulos vacíos + imports |
| 10–20 | Mover carga + validación; lanzar `DataLoadError` / `ValidationError` |
| 20–28 | CLI con `argparse` (`--input`, `--output`) |
| 28–30 | Documentar en 5 líneas qué principio SOLID aplicaste dónde |

**Hecho:** `python -m ventas_app.cli --input Datos/ventas.csv --output Datos/out.csv` funciona.

---

## Bloque C — Proyecto intermedio (~45 min)

Refactor del trabajo de la semana anterior hacia el esqueleto modular. Commits pequeños (`Extract validator`, `Add CLI`).

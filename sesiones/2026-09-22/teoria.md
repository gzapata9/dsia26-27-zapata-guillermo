# Teoría (30 min) — 22 sep 2026  
## Arquitectura modular, Clean Code y SOLID

**Código demo:** `ejemplos/solid_ventas.py` · también `../../1_programacion_avanzada_python/03_oop_clean_code_solid.py`

---

## 1. Introducción (5 min)

El notebook del 15 sep **funciona**, pero no escala:

- difícil de testear,
- difícil de reutilizar,
- un cambio de CSV rompe agregaciones mezcladas en la misma celda.

Hoy convertimos el mismo problema de ventas en un **diseño modular**.

```text
CLI / main → Repository → Validator → Metrics → salida
```

---

## 2. Conceptos

### 2.1 Clean Code (mínimo viable)

| Sí | No |
| --- | --- |
| Nombres que revelan intención | `df2`, `x`, `tmp` |
| Funciones cortas, un nivel | Mega-función de 80 líneas |
| Constantes con nombre | Números mágicos |
| Errores explícitos (`raise`) | `except: pass` |

### 2.2 SOLID (con ejemplos de datos/IA)

| Principio | Pregunta | Ejemplo del curso |
| --- | --- | --- |
| **S** Single Responsibility | ¿Esta clase tiene un solo motivo de cambio? | `SalesValidator` solo valida |
| **O** Open/Closed | ¿Puedo extender sin modificar? | Nuevas métricas sin tocar el validador |
| **L** Liskov | ¿Puedo sustituir implementaciones? | Cualquier `Repository` con `load()` |
| **I** Interface Segregation | ¿La interfaz es pequeña? | `Protocol` con un método |
| **D** Dependency Inversion | ¿Dependo de abstracciones? | `main` usa `SalesRepository`, no CSV a pelo |

### 2.3 Patrones útiles (sin over-engineering)

- **Repository** — origen de datos intercambiable (CSV hoy, API mañana).
- **Pipeline stages** — etapas puras + I/O en los bordes.
- **Strategy** — cambiar proveedor de IA / validador.

### 2.4 Excepciones de dominio

```python
class DataLoadError(Exception): ...
class ValidationError(Exception): ...
```

Separar “no encuentro el fichero” de “el fichero está mal” ayuda a la API y a los tests.

---

## 3. Código y ejemplos

Ver `ejemplos/solid_ventas.py` (dataclass `SalesRecord`, Protocol, validator, metrics).

Ejecutar:

```bash
python sesiones/2026-09-22/ejemplos/solid_ventas.py
```

Observa:

1. `CsvSalesRepository.load` lanza `DataLoadError` si no existe el path.
2. `SalesMetrics` no sabe de pandas ni de CSV.
3. `main` orquesta; no valida “a mano”.

---

## 4. Resumen

- Modularizar = poder testear y cambiar piezas.
- SOLID se demuestra en el código, no en un slide.
- Empieza simple: 3–4 módulos bastan para el Proyecto I.

→ `ejercicios.md`

# Arquitectura modular, Clean Code y SOLID — notas de clase

**Sesión:** 22 sep 2026 y `03_oop_clean_code_solid.py`.

## Del notebook al sistema

Un notebook excelente para explorar suele ser un mal artefacto de producción:

| Notebook | Paquete |
| --- | --- |
| Estado global en celdas | Funciones/clases con inputs explícitos |
| Orden de ejecución frágil | CLI / job determinista |
| Difícil de testear | Tests unitarios por etapa |
| Rutas absolutas del autor | `pathlib` relativo / config |

## Clean Code (mínimo viable)

1. Nombres que digan *qué* y *por qué*.
2. Funciones de un nivel de abstracción.
3. Evitar efectos laterales ocultos.
4. Errores explícitos (`raise`) en lugar de valores mágicos.
5. Comentarios para *porqués*, no para narrar el código obvio.

## SOLID aplicado a datos + IA

| Principio | Ejemplo en DSIA |
| --- | --- |
| **S** | `Validator` no escribe CSV |
| **O** | Nuevas métricas sin tocar validación |
| **L** | Cualquier `Repository` se comporta como `load()` |
| **I** | Interfaces pequeñas (Protocol con 1–2 métodos) |
| **D** | El orquestador depende de abstracciones, no de CSV/OpenAI concretos |

## Patrones que sí compensan en este curso

- **Repository** — origen de datos intercambiable.
- **Pipeline stages** — etapas puras + I/O en los bordes.
- **Strategy** — proveedor de IA (`mock` / `openai` / …).
- **Facade** — CLI o API que simplifica el uso interno.

## Anti-patrones frecuentes

- “Utils.py” de 800 líneas.
- Capturar `Exception` y continuar.
- Mezclar descarga HTTP, pandas y prompt de IA en una sola función.
- Abstract Factory para un único CSV.

## Demo

```bash
python 03_oop_clean_code_solid.py
```

Luego refactoriza tu Proyecto I hacia `ventas_app/` (`ejercicios/E2_arquitectura.md`).

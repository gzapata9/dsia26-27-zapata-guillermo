# Teoría (30 min) — 29 sep 2026  
## Pruebas unitarias con pytest

**Demos:** `ejemplos/` · también `../../2_pruebas_y_despliegue/ejemplos/`

---

## 1. Introducción (5 min)

Sin tests, cada refactor del Proyecto I es una ruleta.  
Los tests son una **especificación ejecutable** del comportamiento.

Pirámide:

```text
        /\     E2E (pocos)
       /  \    Integración
      /____\   Unitarios (muchos, rápidos)
```

---

## 2. Conceptos

| Concepto | Significado |
| --- | --- |
| Unitario | Prueba una función/clase sin I/O real (idealmente) |
| Integración | Cruza módulos / disco / red |
| Assert | Condición que debe cumplirse |
| Fixture | Datos/contexto reutilizable |
| Parametrize | Mismo test, varios inputs |
| Marcador | Etiqueta (`@pytest.mark.integration`) |

### Arrange / Act / Assert

```python
def test_add():
    # arrange
    a, b = 2, 3
    # act
    result = add(a, b)
    # assert
    assert result == 5
```

### Qué testear en DSIA

- Reglas de validación (bordes: 0, negativo, `None`).
- Paths inexistentes → excepción.
- Métricas con DataFrame sintético en memoria.

---

## 3. Código y ejemplos

```bash
cd sesiones/2026-09-29/ejemplos
pytest -q
pytest -vv
pytest -q -m "not integration"
```

Ficheros:

- `validator_under_test.py` — función a probar
- `test_validator.py` — unitarios + parametrize + integration

Patrones:

```python
with pytest.raises(FileNotFoundError):
    load("no-existe.csv")

@pytest.mark.parametrize("price, ok", [(1.0, True), (0.0, False), (-1.0, False)])
def test_price_rules(price, ok):
    ...
```

---

## 4. Resumen

- Nombre del test = documentación.
- Unitarios sin red; integración marcada.
- CI ejecuta la suite en cada push.

→ `ejercicios.md`

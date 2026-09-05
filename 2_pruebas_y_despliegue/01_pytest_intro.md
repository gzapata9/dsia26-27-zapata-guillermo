# Sesión 4 (29 sep 2026): pytest, test suites y aserciones

## Objetivos

- Escribir pruebas unitarias con **pytest**.
- Organizar `test_*.py` y usar fixtures.
- Distinguir pruebas unitarias vs de integración.
- Ejecutar tests en local y entender el papel de CI.

## Arranque rápido

```bash
cd 2_pruebas_y_despliegue
pytest -q ejemplos/
```

## Conceptos clave

```python
def test_suma():
    assert add(2, 3) == 5
```

- **Arrange / Act / Assert**
- `pytest.raises` para excepciones esperadas
- Fixtures (`@pytest.fixture`) para datos reutilizables
- Marcadores: `@pytest.mark.integration`

## Buenas prácticas

- Un assert principal por test (cuando sea razonable).
- Nombres descriptivos: `test_divide_by_zero_raises`.
- No dependas de red ni de reloj real en unitarios (mockea).

## Ejercicio

Completa `ejercicios/E3_pytest.md` aplicando tests al validador de ventas del Tema 1.

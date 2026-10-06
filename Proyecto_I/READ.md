# Proyecto I: Pipeline de Ventas (Parte A)

Este proyecto implementa un pipeline robusto para la ingesta, validación y análisis de datos de ventas. Está desarrollado en Python aplicando Programación Orientada a Objetos (OOP), manejo de excepciones de dominio personalizado y buenas prácticas de desarrollo.

## Requisitos e Instalación

El código ha sido desarrollado con la versión de Python 3.13.15 (se recomienda 3.13 o superior). Para instalar las dependencias necesarias para las pruebas, ejecuta:

```bash
pip install pytest pytest-cov
```

## Uso de la Aplicación (CLI)
El proyecto incluye una interfaz de línea de comandos (CLI) usable. Puedes ejecutar el pipeline completo especificando la ruta al archivo de datos mediante el flag --file:

```bash
python -m ventas_app --file .Datos/ventas.csv
```

El programa se encargará de:

1. Cargar y validar fila a fila los datos (descartando registros con unidades/precios negativos o fechas inválidas).

2. Calcular e imprimir métricas de negocio (Importe total global, importe por región e importe por producto).

## Tests y Cobertura
El proyecto cuenta con una suite de pruebas unitarias que validan el comportamiento de todos los módulos (loader, validator, metrics y cli), logrando una cobertura de código superior al 60%. Para ejecutar los tests localmente:

```bash
pytest --cov=ventas_app
```

## Integración Continua (CI)
Este repositorio utiliza GitHub Actions para la Integración Continua. Cada vez que se realiza un push o pull request a la rama main, se ejecutan automáticamente los tests unitarios. El pipeline de CI fallará si la cobertura de código desciende por debajo del 60%.
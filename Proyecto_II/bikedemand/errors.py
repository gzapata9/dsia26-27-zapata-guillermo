"""Taxonomía de errores del proyecto.

| Excepción              | Exit CLI | HTTP       | Log     | Causa                                  |
|------------------------|----------|------------|---------|----------------------------------------|
| QualityGateError       | 1        | 422        | ERROR   | datos o modelo por debajo del umbral    |
| DataContractError      | 2        | 400        | ERROR   | fichero/columnas/config inválidos       |
| ModelNotFoundError     | 2        | 503        | ERROR   | no hay modelo entrenado                 |
| UpstreamError          | 3        | 502/503/504| ERROR   | API externa caída o sin respuesta       |
"""
from __future__ import annotations


class BikeDemandError(Exception):
    """Base de todas las excepciones propias"""

    exit_code = 1


class QualityGateError(BikeDemandError):
    """Los datos o el modelo no superan el umbral de calidad"""

    exit_code = 1


class DataContractError(BikeDemandError):
    """Entrada inválida: fichero inexistente, columnas que faltan o configuración incorrecta"""

    exit_code = 2


class ModelNotFoundError(DataContractError):
    """No existe el artefacto del modelo o no es un bundle válido"""


class UpstreamError(BikeDemandError):
    """Una dependencia externa (API de datos) ha fallado"""

    exit_code = 3

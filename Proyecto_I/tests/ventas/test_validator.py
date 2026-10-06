import pytest
from ventas_app.validator import (
    SalesValidator, InvalidDateError, 
    InvalidUnitsError, InvalidPriceError
)

def test_validate_row_valid():
    row = {
        'fecha': '2026-01-09',
        'region': 'Sur',
        'producto': 'Cable Kit',
        'unidades': '7',
        'precio_unitario': '12.5',
        'cliente_id': 'C005'
    }
    valid_row = SalesValidator.validate_row(row)
    assert valid_row['unidades'] == 7
    assert valid_row['precio_unitario'] == 12.5
    assert valid_row['fecha'] == '2026-01-09'

def test_validate_row_invalid_date():
    row = {'fecha': '09/01/2026', 'unidades': '7', 'precio_unitario': '12.5'}
    with pytest.raises(InvalidDateError):
        SalesValidator.validate_row(row)

def test_validate_row_invalid_units():
    row = {'fecha': '2026-01-09', 'unidades': '-2', 'precio_unitario': '12.5'}
    with pytest.raises(InvalidUnitsError):
        SalesValidator.validate_row(row)

def test_validate_row_invalid_price():
    row = {'fecha': '2026-01-09', 'unidades': '5', 'precio_unitario': '-10.0'}
    with pytest.raises(InvalidPriceError):
        SalesValidator.validate_row(row)
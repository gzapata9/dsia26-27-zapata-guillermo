import pytest
from bikes_app.validator import BikesValidator, BikeValidationError, InvalidCoordinatesError, InvalidCapacityError

def test_validate_row_valid():
    row = {'station_id': '1', 'name': 'Central Park', 'lat': '40.78', 'lon': '-73.96', 'capacity': '30', 'num_bikes_available': '15'}
    valid_row = BikesValidator.validate_row(row)
    assert valid_row['capacity'] == 30
    assert valid_row['lat'] == 40.78

'''
Errores comprobados:
Nombre vacio
Latitud fuera de rango (>90)
Capacidad fuera de rango (negativa)
Mas bicicletas que la capacidad maxima
'''
@pytest.mark.parametrize("invalid_row, expected_exception", [
    ({'station_id': '1', 'name': '', 'lat': '40.0', 'lon': '-73.0', 'capacity': '10', 'num_bikes_available': '5'}, BikeValidationError),
    ({'station_id': '1', 'name': 'A', 'lat': '100.0', 'lon': '-73.0', 'capacity': '10', 'num_bikes_available': '5'}, InvalidCoordinatesError),
    ({'station_id': '1', 'name': 'A', 'lat': '40.0', 'lon': '-73.0', 'capacity': '-5', 'num_bikes_available': '5'}, InvalidCapacityError),
    ({'station_id': '1', 'name': 'A', 'lat': '40.0', 'lon': '-73.0', 'capacity': '10', 'num_bikes_available': '15'}, InvalidCapacityError),
])
def test_validate_row_invalid_cases(invalid_row, expected_exception):
    with pytest.raises(expected_exception):
        BikesValidator.validate_row(invalid_row)
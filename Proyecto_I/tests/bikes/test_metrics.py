import pytest
from bikes_app.metrics import BikesMetrics

@pytest.fixture
def mock_stations():
    return [
        {'name': 'Station A', 'capacity': 10, 'num_bikes_available': 5},
        {'name': 'Station B', 'capacity': 50, 'num_bikes_available': 0},
        {'name': 'Station C', 'capacity': 20, 'num_bikes_available': 20},
        {'name': 'Station D', 'capacity': 5, 'num_bikes_available': 0},
        {'name': 'Station E', 'capacity': 30, 'num_bikes_available': 10},
        {'name': 'Station F', 'capacity': 40, 'num_bikes_available': 2}
    ]

def test_metrics_calculations(mock_stations):
    # Arrange
    metrics = BikesMetrics(mock_stations)
    
    # Act & Assert
    assert metrics.total_bikes_available() == 37
    assert metrics.empty_stations_count() == 2
    
    top_5 = metrics.top_5_largest_stations()
    assert len(top_5) == 5
    assert 'Station B' in top_5
    assert top_5['Station B'] == 50
    # Comprueba que la sexta se queda fuera del top 5
    assert 'Station D' not in top_5
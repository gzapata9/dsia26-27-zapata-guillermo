import pytest
import csv
from pathlib import Path
from bikes_app.loader import BikeDataLoader

def test_load_data_file_not_found():
    loader = BikeDataLoader("ruta_inexistente.csv")
    with pytest.raises(FileNotFoundError):
        loader.load_data()

def test_load_data_success(tmp_path):
    '''
    Archivo temporal (tmp_path) para no depender de archivos reales
    '''
    csv_file = tmp_path / "test_bikes.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['station_id', 'name', 'lat', 'lon', 'capacity', 'num_bikes_available'])
        writer.writerow(['1', 'Test Station', '40.0', '-73.0', '20', '10'])

    loader = BikeDataLoader(csv_file)
    data = loader.load_data()
    assert len(data) == 1
    assert data[0]['name'] == 'Test Station'

@pytest.mark.integration
def test_integration_real_dataset():
    '''
    Test con archivo real que verifica que el archivo de datos existe y se puede procesar
    '''
    real_csv = Path("Datos/bikes.csv")
    if not real_csv.exists():
        pytest.skip("El archivo de datos real no existe aún.")
    
    loader = BikeDataLoader(real_csv)
    data = loader.load_data()
    # Debe cargar al menos una estacion
    assert len(data) > 0
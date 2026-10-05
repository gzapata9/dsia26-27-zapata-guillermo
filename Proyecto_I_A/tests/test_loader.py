import pytest
import csv
from ventas_app.loader import SalesLoader

def test_load_data_file_not_found():
    loader = SalesLoader("ruta_falsa_que_no_existe.csv")
    with pytest.raises(FileNotFoundError):
        loader.load_data()

def test_load_data_success(tmp_path):
    # CSV temporal
    csv_file = tmp_path / "test_ventas.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['fecha', 'region', 'producto', 'unidades', 'precio_unitario', 'cliente_id'])
        writer.writerow(['2026-01-01', 'Norte', 'Sensor A', '10', '15.0', 'C001'])
        writer.writerow(['2026-01-02', 'Sur', 'Hub IoT', '5', '50.0', 'C002'])

    loader = SalesLoader(csv_file)
    data = loader.load_data()
    
    assert len(data) == 2
    assert data[0]['producto'] == 'Sensor A'
    assert data[1]['unidades'] == 5
    assert data[1]['precio_unitario'] == 50.0
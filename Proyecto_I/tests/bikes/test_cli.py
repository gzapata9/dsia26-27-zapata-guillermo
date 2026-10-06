from unittest.mock import patch
import sys
from bikes_app.cli import main

def test_cli_smoke_test(tmp_path, capsys):
    csv_file = tmp_path / "mock_bikes.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        f.write("station_id,name,lat,lon,capacity,num_bikes_available\n")
        f.write("1,A,40.0,-73.0,10,5\n")

    test_args = ["bikes_app.cli", "--file", str(csv_file)]
    
    with patch.object(sys, 'argv', test_args):
        main()
        
    captured = capsys.readouterr()
    assert "Se han cargado 1 estaciones válidas" in captured.out
    assert "MÉTRICAS DE MOVILIDAD" in captured.out
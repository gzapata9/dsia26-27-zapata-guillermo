import pytest
from unittest.mock import patch
import sys
from ventas_app.cli import main

def test_cli_success(tmp_path, capsys):
    # Creamos un CSV temporal básico
    csv_file = tmp_path / "test_ventas_cli.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        f.write("fecha,region,producto,unidades,precio_unitario,cliente_id\n")
        f.write("2026-01-01,Norte,Sensor A,10,15.0,C001\n")

    # Simulamos los argumentos de la terminal: python -m ventas_app --file ruta_al_csv
    test_args = ["ventas_app", "--file", str(csv_file)]
    
    with patch.object(sys, 'argv', test_args):
        main()
        
    # Capturamos lo que el programa imprimió en consola
    captured = capsys.readouterr()
    
    assert "Se han cargado 1 registros válidos" in captured.out
    assert "=== MÉTRICAS DE NEGOCIO ===" in captured.out
    assert "Importe Total Global:" in captured.out
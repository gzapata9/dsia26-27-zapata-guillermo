import argparse
from pathlib import Path
import sys

from .loader import SalesLoader
from .metrics import SalesMetrics

def main():
    parser = argparse.ArgumentParser(description="Pipeline de procesamiento de ventas.")
    parser.add_argument(
        '--file', 
        type=str, 
        required=True, 
        help="Ruta al archivo CSV de ventas"
    )
    
    args = parser.parse_args()
    filepath = Path(args.file)

    print(f"Cargando datos desde: {filepath}")
    
    try:
        # 1. Cargar y validar
        loader = SalesLoader(filepath)
        valid_data = loader.load_data()
        print(f"Se han cargado {len(valid_data)} registros válidos.\n")

        # 2. Calcular métricas
        metrics = SalesMetrics(valid_data)
        
        print("MÉTRICAS DE NEGOCIO")
        print(f"Importe Total Global: ${metrics.importe_total_global():.2f}")
        
        print("\nImporte por Región:")
        for region, importe in metrics.importe_por_region().items():
            print(f"{region}: ${importe:.2f}")

        print("\nImporte por Producto:")
        for producto, importe in metrics.importe_por_producto().items():
            print(f"{producto}: ${importe:.2f}")

    except Exception as e:
        print(f"Error en el pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
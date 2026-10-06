import argparse
import sys
from pathlib import Path

from .loader import BikeDataLoader
from .metrics import BikesMetrics

def main():
    parser = argparse.ArgumentParser(description="Pipeline de datos de movilidad urbana en bicicleta por Nueva Yoprk.")
    parser.add_argument(
        '--file', 
        type=str, 
        required=True, 
        help="Ruta al archivo CSV de bicicletas"
    )
    parser.add_argument(
        '--update', 
        action='store_true', 
        help="Esta variable actualiza los datos con la API antes de procesar."
    )
    
    args = parser.parse_args()
    filepath = Path(args.file)

    try:
        loader = BikeDataLoader(filepath)

        # Actualizar los datos
        if args.update:
            print("Iniciando actualización de datos desde internet...")
            loader.update_from_api()

        print(f"Cargando datos locales desde: {filepath}")
        
        # Cargar y validar
        valid_data = loader.load_data()
        print(f"Se han cargado {len(valid_data)} estaciones válidas.\n")

        # Calcular metricas
        metrics = BikesMetrics(valid_data)
        
        print("MÉTRICAS DE MOVILIDAD (CITIBIKE NYC)")
        print(f"Bicicletas totales disponibles: {metrics.total_bikes_available()}")
        print(f"Estaciones completamente vacías: {metrics.empty_stations_count()}")
        
        print("\nTop 5 Estaciones con mayor capacidad:")
        for estacion, capacidad in metrics.top_5_largest_stations().items():
            print(f"  - {estacion}: {capacidad} plazas")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Sugerencia: Ejecuta el comando con --update para descargar los datos por primera vez.")
        sys.exit(1)
    except Exception as e:
        print(f"Error crítico en el pipeline de bicis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
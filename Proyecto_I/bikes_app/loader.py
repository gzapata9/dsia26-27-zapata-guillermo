import csv
import requests
import pandas as pd
from pathlib import Path
from .validator import BikesValidator, BikeValidationError

class BikeDataLoader:
    """
    Gestionar, descargar y cargar el dataset de movilidad actualizado
    """
    
    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)

    def update_from_api(self):
        """
        Descarga los datos de la API y actualiza el CSV local (reemplaza)
        """
        # Variables para conectar con la API
        print("Conectando a la API de CitiBike")
        url_info = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
        url_status = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
        
        # Extraer y transformar los datos
        res_info = requests.get(url_info).json()
        df_info = pd.DataFrame(res_info['data']['stations'])[['station_id', 'name', 'lat', 'lon', 'capacity']]
        
        res_status = requests.get(url_status).json()
        df_status = pd.DataFrame(res_status['data']['stations'])[['station_id', 'num_bikes_available']]
        
        # Merge de ambas tablas
        df_merged = pd.merge(df_info, df_status, on='station_id', how='inner')
        df_merged.to_csv(self.filepath, index=False)
        print(f"Datos actualizados y guardados en: {self.filepath}")

    def load_data(self) -> list[dict]:
        """
        Cargar el CSV local, valida los datos y devuelve una lista
        """
        # Error en caso de no encontrar el archivo
        if not self.filepath.exists():
            raise FileNotFoundError(f"El archivo no existe en la ruta: {self.filepath}")
        
        valid_stations = []
        with open(self.filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for line_num, row in enumerate(reader, start=1):
                try:
                    valid_row = BikesValidator.validate_row(row)
                    valid_stations.append(valid_row)
                except BikeValidationError as e:
                    # Saltamos los que no se validen
                    pass
                    
        return valid_stations
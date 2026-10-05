from pathlib import Path
import pandas as pd


class DataLoaderError(Exception):
    """
    Excepción lanzada cuando ocurre un error al cargar el archivo.
    """


def load(path: str) -> pd.DataFrame:
    """
    Carga un fichero CSV y devuelve un DataFrame.
    Falla si el archivo no existe.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise DataLoaderError(f"El archivo {path} no existe.")

    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise DataLoaderError(
            f"Error al leer el archivo {path}: {e}"
        ) from e

load('archivofalso.csv')
import csv
from pathlib import Path
from .validator import SalesValidator, ValidationError

class SalesLoader:
    """Encargado de cargar y procesar el dataset de ventas."""
    
    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)

    def load_data(self) -> list[dict]:
        """Carga el CSV, valida los datos y retorna una lista de diccionarios limpios."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"El archivo no se encuentra en la ruta: {self.filepath}")
        
        valid_sales = []
        with open(self.filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for line_num, row in enumerate(reader, start=1):
                try:
                    # Pasamos la fila al validador
                    validated_row = SalesValidator.validate_row(row)
                    valid_sales.append(validated_row)
                except ValidationError as e:
                    # En un entorno real podríamos usar logging. Aquí imprimimos el error de dominio.
                    print(f"Aviso - Fila {line_num} descartada: {e}")
                    
        return valid_sales
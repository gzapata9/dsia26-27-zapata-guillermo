from datetime import datetime

class ValidationError(Exception):
    """Excepción base para errores de validación de ventas."""
    pass

class InvalidUnitsError(ValidationError):
    """Lanzada cuando las unidades son negativas o inválidas."""
    pass

class InvalidPriceError(ValidationError):
    """Lanzada cuando el precio unitario es negativo."""
    pass

class InvalidDateError(ValidationError):
    """Lanzada cuando la fecha no tiene el formato correcto."""
    pass

class SalesValidator:
    """Clase para validar los datos de ventas fila por fila."""
    
    @staticmethod
    def validate_row(row: dict) -> dict:
        try:
            # Validación de fecha (formato YYYY-MM-DD)
            fecha_str = row.get('fecha', '')
            try:
                datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                raise InvalidDateError(f"Formato de fecha inválido: {fecha_str}. Se esperaba YYYY-MM-DD.")

            # Validación de unidades
            unidades = int(row.get('unidades', 0))
            if unidades < 0:
                raise InvalidUnitsError(f"Las unidades no pueden ser negativas: {unidades}")
            
            # Validación de precio unitario
            precio_unitario = float(row.get('precio_unitario', 0.0))
            if precio_unitario < 0:
                raise InvalidPriceError(f"El precio unitario no puede ser negativo: {precio_unitario}")
                
            return {
                'fecha': fecha_str,
                'region': str(row.get('region', '')).strip(),
                'producto': str(row.get('producto', '')).strip(),
                'unidades': unidades,
                'precio_unitario': precio_unitario,
                'cliente_id': str(row.get('cliente_id', '')).strip()
            }
        except ValueError as e:
            raise ValidationError(f"Error de formato numérico: {e}")
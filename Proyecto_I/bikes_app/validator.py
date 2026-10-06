class BikeValidationError(Exception):
    """
    Excepción base para errores de validación de estaciones de bicicletas
    """
    pass

class InvalidCoordinatesError(BikeValidationError):
    """
    Latitud o longitud están fuera de rango
    """
    pass

class InvalidCapacityError(BikeValidationError):
    """
    Capacidad o disponibilidad es negativa o incoherente
    """
    pass

class BikesValidator:
    """
    Validador para las filas del dataset
    """
    
    @staticmethod
    def validate_row(row: dict) -> dict:
        try:
            # Validar nombre nulo o vacío
            name = str(row.get('name', '')).strip()
            if not name:
                raise BikeValidationError("El nombre de la estación no puede estar vacío.")

            # Validar coordenadas (-90<=latitud<= 90, -180<=longitud<=180)
            lat = float(row.get('lat', 0.0))
            lon = float(row.get('lon', 0.0))
            if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
                raise InvalidCoordinatesError(f"Coordenadas inválidas: {lat}, {lon}")

            # Validar capacidad y disponibilidad
            capacity = int(row.get('capacity', 0))
            bikes_avail = int(row.get('num_bikes_available', 0))
            
            if capacity < 0 or bikes_avail < 0:
                raise InvalidCapacityError("La capacidad y las bicis disponibles no pueden ser negativas.")
            if bikes_avail > capacity:
                raise InvalidCapacityError(f"Las bicis disponibles ({bikes_avail}) superan la capacidad ({capacity}).")

            return {
                'station_id': str(row.get('station_id', '')).strip(),
                'name': name,
                'lat': lat,
                'lon': lon,
                'capacity': capacity,
                'num_bikes_available': bikes_avail
            }
            
        except ValueError as e:
            raise BikeValidationError(f"Error de tipo numérico en la fila: {e}")
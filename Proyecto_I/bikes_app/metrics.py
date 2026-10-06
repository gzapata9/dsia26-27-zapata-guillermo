class BikesMetrics:
    """
    Calcular metricas de negocio
    """

    def __init__(self, stations_data: list[dict]):
        self.stations_data = stations_data

    def total_bikes_available(self) -> int:
        """
        Total de bicicletas disponibles
        """
        return sum(station['num_bikes_available'] for station in self.stations_data)

    def empty_stations_count(self) -> int:
        """
        Estaciones con 0 bicicletas disponibles
        """
        return sum(1 for station in self.stations_data if station['num_bikes_available'] == 0)

    def top_5_largest_stations(self) -> dict:
        """
        Las cinco estaciones con mayor capacidad
        """
        # Ordenamos la lista por 'capacity' de mayor a menor
        sorted_stations = sorted(self.stations_data, key=lambda x: x['capacity'], reverse=True)
        top_5 = sorted_stations[:5]
        
        return {station['name']: station['capacity'] for station in top_5}
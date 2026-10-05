class SalesMetrics:
    """Clase para calcular métricas de negocio a partir de datos de ventas validados."""

    def __init__(self, sales_data: list[dict]):
        """
        Inicializa las métricas con los datos de ventas.
        Se asume que sales_data ya pasó por el SalesValidator.
        """
        self.sales_data = sales_data

    def _calcular_importe_total(self, venta: dict) -> float:
        """Calcula el importe total de una venta individual."""
        return venta['unidades'] * venta['precio_unitario']

    def importe_total_global(self) -> float:
        """Calcula el importe total de todas las ventas registradas."""
        return sum(self._calcular_importe_total(venta) for venta in self.sales_data)

    def importe_por_region(self) -> dict:
        """Agrupa y suma el importe total de las ventas por cada región."""
        metricas = {}
        for venta in self.sales_data:
            region = venta['region']
            importe = self._calcular_importe_total(venta)
            metricas[region] = metricas.get(region, 0.0) + importe
        return metricas

    def importe_por_producto(self) -> dict:
        """Agrupa y suma el importe total de las ventas por cada producto."""
        metricas = {}
        for venta in self.sales_data:
            producto = venta['producto']
            importe = self._calcular_importe_total(venta)
            metricas[producto] = metricas.get(producto, 0.0) + importe
        return metricas
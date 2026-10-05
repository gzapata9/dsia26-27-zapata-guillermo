from ventas_app.metrics import SalesMetrics

def test_metrics_calculations():
    # Datos simulados ya limpios
    datos_mock = [
        {'fecha': '2026-01-01', 'region': 'Sur', 'producto': 'Cable Kit', 'unidades': 2, 'precio_unitario': 10.0, 'cliente_id': 'C1'},
        {'fecha': '2026-01-02', 'region': 'Sur', 'producto': 'Sensor', 'unidades': 1, 'precio_unitario': 20.0, 'cliente_id': 'C2'},
        {'fecha': '2026-01-03', 'region': 'Norte', 'producto': 'Cable Kit', 'unidades': 3, 'precio_unitario': 10.0, 'cliente_id': 'C3'}
    ]
    metrics = SalesMetrics(datos_mock)
    
    # Test Importe global
    assert metrics.importe_total_global() == 70.0  # (2*10) + (1*20) + (3*10)
    
    # Test Importe por región
    region_metrics = metrics.importe_por_region()
    assert region_metrics['Sur'] == 40.0
    assert region_metrics['Norte'] == 30.0
    
    # Test Importe por producto
    prod_metrics = metrics.importe_por_producto()
    assert prod_metrics['Cable Kit'] == 50.0
    assert prod_metrics['Sensor'] == 20.0
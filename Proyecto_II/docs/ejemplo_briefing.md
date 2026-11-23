> **Ejemplo generado sin red**: la previsión meteorológica es simulada (15 °C, lluvia las últimas 8 h) y el proveedor de IA es `mock`. Con red, `python -m bikedemand forecast` usa Open-Meteo y Nager.Date reales.

# Previsión de demanda — Washington, DC

Periodo: **26/11 00:00 → 27/11 23:00** (48 h) · Total previsto: **7701** alquileres · media **160.4**/h

## Horas punta

| Hora | Alquileres previstos | Tiempo | °C |
|---|---|---|---|
| 27/11 08:00 | 648 | despejado | 15.0 |
| 27/11 17:00 | 397 | lluvia o nieve débil | 15.0 |
| 27/11 07:00 | 357 | despejado | 15.0 |

## Resumen por reglas (determinista)

- Pico principal: 27/11 08:00 con ~648 alquileres/h; reequilibrar estaciones céntricas 1 h antes.
- Ventana de mantenimiento: 26/11 03:00 → 26/11 06:00 (~5.7/h).
- Ventana de mantenimiento: 27/11 02:00 → 27/11 05:00 (~12.7/h).
- Precipitación prevista en 8 h (desde 27/11 16:00): esperar menos demanda.
- Festivo en el periodo: Thanksgiving Day (26/11) (patrón de fin de semana).

## Briefing operativo (IA)

[mock] Recibido prompt de 662 caracteres. Previsión de demanda para Washington, DC (26/11 00:00 → 27/11 23:00, 48 horas).

_Generado por `mock` · modelo `mock` · 0.0 ms · prompt briefing-v1_

## Estado de las dependencias

- weather: `ok`
- holidays: `ok`
- ai: `ok`

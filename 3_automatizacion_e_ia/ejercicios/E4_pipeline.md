# E4 — Pipeline automatizado

Extiende `ejemplos/pipeline_ventas.py` para:

1. Aceptar varios CSV de entrada (glob `*.csv`).
2. Escribir un log rotativo o al menos un `run.log`.
3. Fallar con código de salida ≠ 0 si la tasa de filas inválidas supera un umbral (`--max-error-rate 0.3`).
4. Añadir tests del transform **sin I/O de disco** (DataFrame sintético).

Entregable orientativo del **Proyecto II**.

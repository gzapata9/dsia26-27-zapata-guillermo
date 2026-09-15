from __future__ import annotations

from datetime import date
from pathlib import Path
import json
import pandas as pd
import numpy as np

'''
Parte 1 
Importar los datos de ventas con PATH relativo y comprobar que el directorio existe.
'''

print("pandas:", pd.__version__)
print("cwd idea:", Path.cwd())
DATA_DIR = Path("1_programacion_avanzada_python/Datos")
print("Datos existe:", DATA_DIR.exists())


'''
Parte 2
Definir una función que cargue los datos de ventas desde un fichero CSV y devuelva un DataFrame
utilizando el PATH relativo.
'''

def cargar_ventas(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe el fichero: {path}")
    return pd.read_csv(path)


raw = cargar_ventas(DATA_DIR / "ventas.csv")
print(f"\n{'='*80}\n\nDatos cargados desde: {DATA_DIR / 'ventas.csv'}")
print(raw.head())

# Imprimir la informacion de los datos raw
print(f"Info de los datos raw:\n{raw.info()}")
print(f"Forma de los datos raw: {raw.shape}")
print(f"Tipos de datos de las columnas:\n{raw.dtypes}")
print(f"Valores nulos por columna:\n{raw.isnull().sum()}")


'''
Definir una funcion que valide los datos de ventas y devuelva dos dataframes: uno
con los datos válidos y otro con los datos que contienen errores en las columnas "unidades"
y "precio_unitario"
'''


def validar_ventas(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Haciendo una copia del DataFrame para no modificar el original
    df = frame.copy()
    # Convertir las columnas "unidades" y "precio_unitario" a tipo numérico
    df["unidades"] = pd.to_numeric(df["unidades"], errors="coerce")
    df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce")

    # Crear una variable con True y False para identificar si la fila es valida
    df['valido'] = (
        df["unidades"].notna()
        & (df["unidades"] > 0)
        & df["precio_unitario"].notna()
        & (df["precio_unitario"] > 0)
    )

    # Crear dos dataframes distintos para los valores validos y los que contienen errores
    # eliminando la nueva columna de validacon
    validos = df[df['valido']==True].drop(columns=['valido'])
    errores = df[df['valido']==False].drop(columns=['valido'])
    validos["importe"] = validos["unidades"] * validos["precio_unitario"]
    return validos, errores

'''
Ejecutar la función devolviendo las filas del dataframe de errores para poder comprobar que
las filas que contienen errores son las correctas.
'''

validos, errores = validar_ventas(raw)
print(f"\n{'='*80}\n\nDatos validados:")
print(f"\nválidas: {len(validos)} | inválidas: {len(errores)}")
print(f"\nTabla de datos con los {len(errores)} no validados:")
print(errores.head())

'''
Parte 3
Calcular el importe total por región y mostrar los tres mejores productos 
según el importe total.
'''
# Importe total por region (orden descendente)
print(f"\n{'='*80}\n\nImporte total por región:\n{validos.groupby(
    "region")["importe"].sum().sort_values(ascending=False)}")

# Top 3 productos por importe total (orden descendente).
print(f"Top 3 productos por importe total:\n{validos.groupby(
    'producto')['importe'].sum().sort_values(ascending=False).head(3)}")

# Mostrar los valores que han convertido en invalidas las filas
print(f"\n{'='*80}\n\nValores que han convertido en invalidas las filas:\n{errores[['unidades', 'precio_unitario']]}")
print(f"En estas dos columnas tienen que mostrarse minimo un error por fila.\nEstos valores que provocan errores pueden ser:\n- Valores nulos\n- Valores igual o menor que cero")

'''
Parte 4
Exportar los datos validados a un fichero CSV y JSON con PATH relativo.
CSV: datos limpios de ventas
JSON: calidad de los datos de ventas (filas totales, filas válidas, filas inválidas, importe total)
'''

# Crear el PATH para los ficheros de salida
VALIDOS_PATH = DATA_DIR / "ventas_limpias.csv"
QUALITY_PATH = DATA_DIR / "calidad_datos.json"
print(f"\n{'='*80}\n\nExportando los datos validados")

# Exportar los datos limpios a un nuevo fichero CSV
validos.to_csv(VALIDOS_PATH, index=False)
print(f"Datos limpios exportados a: {VALIDOS_PATH}")

# Crear una variable con la información
quality_report = {
    "filas_totales": len(raw),
    "filas_validas": len(validos),
    "filas_invalidas": len(errores),
    "importe_total": validos["importe"].sum(),
}
print(f"Calidad de los datos:\n{quality_report}")

# Exportar los datos de calidad a un fichero JSON
with open(QUALITY_PATH, "w", encoding="utf-8") as f:
    json.dump(quality_report, f, indent=4)
print(f"Datos de calidad exportados a: {QUALITY_PATH}")
print(f"\n{'='*80}\n\nFin del programa\n\n{'='*80}")
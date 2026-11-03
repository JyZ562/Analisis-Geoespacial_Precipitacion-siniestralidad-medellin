"""
Depuración de las bases de siniestralidad vial y mortalidad de Medellín (2022–2024).

Quita los registros que no tienen coordenadas (Latitud o Longitud vacías) y
guarda las bases depuradas en CSV y Excel, en la misma carpeta de este script.

Entradas (carpeta datos/siniestros/):
    BD_2022-2024_siniestralidad.csv / .xlsx
    BD_2022-2024_mortalidad.csv / .xlsx

Salidas (carpeta datos/siniestros/depurados/):
    BD_2022-2024_siniestralidad_depurados.csv / .xlsx
    BD_2022-2024_mortalidad_depurados.csv / .xlsx

Resultado esperado:
    siniestralidad: 85.793 -> 79.467 registros
    mortalidad:        836 ->     795 registros

Uso:
    pip install pandas openpyxl
    python depuracion_coordenadas.py
"""

from pathlib import Path

import pandas as pd

CARPETA_SALIDA = Path(__file__).resolve().parent      # datos/siniestros/depurados
CARPETA_ENTRADA = CARPETA_SALIDA.parent               # datos/siniestros

# nombre de la base -> hoja del Excel original que contiene los registros
BASES = {
    "siniestralidad": "Hoja1",
    "mortalidad": "BD",
}


def tiene_coordenadas(df: pd.DataFrame) -> pd.Series:
    """True para las filas con Latitud y Longitud no vacías."""
    def no_vacia(col: pd.Series) -> pd.Series:
        return col.notna() & (col.astype(str).str.strip() != "")

    return no_vacia(df["Latitud"]) & no_vacia(df["Longitud"])


def depurar_csv(nombre: str) -> None:
    entrada = CARPETA_ENTRADA / f"BD_2022-2024_{nombre}.csv"
    salida = CARPETA_SALIDA / f"BD_2022-2024_{nombre}_depurados.csv"

    # Se lee todo como texto para no alterar el formato original de los valores
    df = pd.read_csv(entrada, sep=";", encoding="latin1", dtype=str, keep_default_na=False)
    depurado = df[tiene_coordenadas(df)]

    depurado.to_csv(salida, sep=";", encoding="latin1", index=False, lineterminator="\r\n")
    print(f"{entrada.name}: {len(df):,} -> {len(depurado):,} registros "
          f"({len(df) - len(depurado):,} sin coordenadas)")


def depurar_excel(nombre: str, hoja: str) -> None:
    entrada = CARPETA_ENTRADA / f"BD_2022-2024_{nombre}.xlsx"
    salida = CARPETA_SALIDA / f"BD_2022-2024_{nombre}_depurados.xlsx"

    df = pd.read_excel(entrada, sheet_name=hoja).dropna(how="all")
    depurado = df[tiene_coordenadas(df)]

    depurado.to_excel(salida, sheet_name=hoja, index=False)
    print(f"{entrada.name} [{hoja}]: {len(df):,} -> {len(depurado):,} registros "
          f"({len(df) - len(depurado):,} sin coordenadas)")


if __name__ == "__main__":
    for nombre, hoja in BASES.items():
        depurar_csv(nombre)
        depurar_excel(nombre, hoja)

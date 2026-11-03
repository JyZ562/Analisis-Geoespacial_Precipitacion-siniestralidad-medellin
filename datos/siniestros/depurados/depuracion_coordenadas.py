"""
Depuración de las bases de siniestralidad vial y mortalidad de Medellín (2022–2024).

Filtros que aplica, en este orden:
    1. Coordenadas: quita los registros sin Latitud o Longitud.
    2. Fecha: quita los registros sin fecha, con fecha que no se pueda leer
       o con fecha por fuera del periodo 2022-01-01 a 2024-12-31.

Columna de fecha usada en cada base:
    siniestralidad -> FECHA_INCIDENTE   (CSV: "01/ene/2022"; Excel: fecha)
    mortalidad     -> Fecha Ocurrencia  (CSV: número serial de Excel; Excel: fecha)

Entradas (carpeta datos/siniestros/):
    BD_2022-2024_siniestralidad.csv / .xlsx
    BD_2022-2024_mortalidad.csv / .xlsx

Salidas (carpeta datos/siniestros/depurados/):
    BD_2022-2024_siniestralidad_depurados.csv / .xlsx
    BD_2022-2024_mortalidad_depurados.csv / .xlsx

Uso:
    pip install pandas openpyxl
    python depuracion_coordenadas.py
"""

from pathlib import Path

import pandas as pd

CARPETA_SALIDA = Path(__file__).resolve().parent      # datos/siniestros/depurados
CARPETA_ENTRADA = CARPETA_SALIDA.parent               # datos/siniestros

FECHA_INICIO = pd.Timestamp("2022-01-01")
FECHA_FIN = pd.Timestamp("2024-12-31")

# nombre de la base -> (hoja del Excel original con los registros, columna de fecha)
BASES = {
    "siniestralidad": ("Hoja1", "FECHA_INCIDENTE"),
    "mortalidad": ("BD", "Fecha Ocurrencia"),
}

MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
         "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}


# ---------------------------------------------------------------- filtros ---

def no_vacia(col: pd.Series) -> pd.Series:
    """True para las celdas con algún valor."""
    return col.notna() & (col.astype(str).str.strip() != "")


def tiene_coordenadas(df: pd.DataFrame) -> pd.Series:
    """True para las filas con Latitud y Longitud no vacías."""
    return no_vacia(df["Latitud"]) & no_vacia(df["Longitud"])


def leer_fecha(valor) -> pd.Timestamp:
    """Convierte una fecha en cualquiera de los formatos de las bases a Timestamp.

    Acepta: fecha de Excel ya leída, número serial de Excel (p. ej. 44562),
    "01/ene/2022" y "01/01/2022". Devuelve NaT si no se puede leer.
    """
    if isinstance(valor, pd.Timestamp):
        return valor
    texto = str(valor).strip()
    if texto in {"", "nan", "NaT", "None", "-"}:
        return pd.NaT
    try:
        # número serial de Excel (días desde 1899-12-30)
        serial = float(texto.replace(",", "."))
        return pd.Timestamp("1899-12-30") + pd.Timedelta(days=int(serial))
    except ValueError:
        pass
    try:
        dia, mes, anio = texto.split()[0].split("/")
        mes = MESES[mes.lower()[:3]] if not mes.isdigit() else int(mes)
        return pd.Timestamp(int(anio), mes, int(dia))
    except (ValueError, KeyError):
        return pd.NaT


def tiene_fecha_valida(df: pd.DataFrame, columna: str) -> pd.Series:
    """True para las filas con fecha legible dentro del periodo 2022–2024."""
    fechas = df[columna].map(leer_fecha)
    return fechas.notna() & (fechas >= FECHA_INICIO) & (fechas <= FECHA_FIN)


def depurar(df: pd.DataFrame, columna_fecha: str, etiqueta: str) -> pd.DataFrame:
    """Aplica los filtros e imprime cuántos registros quita cada uno."""
    n_inicial = len(df)

    df = df[tiene_coordenadas(df)]
    n_coord = len(df)

    df = df[tiene_fecha_valida(df, columna_fecha)]
    n_fecha = len(df)

    print(f"{etiqueta}")
    print(f"    registros originales:        {n_inicial:>7,}")
    print(f"    quitados sin coordenadas:    {n_inicial - n_coord:>7,}")
    print(f"    quitados sin fecha válida:   {n_coord - n_fecha:>7,}")
    print(f"    registros depurados:         {n_fecha:>7,}")
    return df


# ------------------------------------------------------------- archivos ---

def depurar_csv(nombre: str, columna_fecha: str) -> None:
    entrada = CARPETA_ENTRADA / f"BD_2022-2024_{nombre}.csv"
    salida = CARPETA_SALIDA / f"BD_2022-2024_{nombre}_depurados.csv"

    # Se lee todo como texto para no alterar el formato original de los valores
    df = pd.read_csv(entrada, sep=";", encoding="latin1", dtype=str, keep_default_na=False)
    depurado = depurar(df, columna_fecha, entrada.name)
    depurado.to_csv(salida, sep=";", encoding="latin1", index=False, lineterminator="\r\n")


def depurar_excel(nombre: str, hoja: str, columna_fecha: str) -> None:
    entrada = CARPETA_ENTRADA / f"BD_2022-2024_{nombre}.xlsx"
    salida = CARPETA_SALIDA / f"BD_2022-2024_{nombre}_depurados.xlsx"

    df = pd.read_excel(entrada, sheet_name=hoja).dropna(how="all")
    depurado = depurar(df, columna_fecha, f"{entrada.name} [{hoja}]")
    depurado.to_excel(salida, sheet_name=hoja, index=False)


if __name__ == "__main__":
    for nombre, (hoja, columna_fecha) in BASES.items():
        depurar_csv(nombre, columna_fecha)
        depurar_excel(nombre, hoja, columna_fecha)

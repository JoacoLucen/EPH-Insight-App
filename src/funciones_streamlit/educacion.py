import json
from pathlib import Path

import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st

from src.funciones_streamlit.funciones_en_comun import (
    convertir_csv,
)

# ----------------------------------------------------------------------------------------------------------------------
# PROCESAMIENTO DE NIVELES EDUCATIVOS
# ----------------------------------------------------------------------------------------------------------------------

def procesar_niveles_educativos(df_trimestral, df_por_anio):
    """
    Mapea y renombra los códigos de nivel educativo a descripciones legibles.

    También genera un resumen trimestral de la cantidad de personas por nivel.

    Args:
        df_trimestral (pandas.DataFrame): DataFrame con datos trimestrales (columnas 'NIVEL_ED', 'PONDERA').
        df_por_anio (pandas.DataFrame): DataFrame con datos anuales (columna 'NIVEL_ED').

    Returns:
        tuple: (pandas.DataFrame de resumen trimestral, pandas.DataFrame anual modificado).
    """
    valores_originales = [1, 2, 3, 4, 5, 6]
    nombres = [
        "Primario incompleto", "Primario completo",
        "Secundario incompleto", "Secundario completo",
        "Superior incompleto", "Superior completo",
    ]
    diccionario_mapeo = dict(zip(valores_originales, nombres))

    resumen_trimestre = pd.DataFrame()

    if isinstance(df_trimestral, pd.DataFrame) and not df_trimestral.empty:
        if "NIVEL_ED" in df_trimestral.columns:
            df_trimestral = df_trimestral[
                df_trimestral["NIVEL_ED"].isin(valores_originales)
            ].copy()
            df_trimestral["NIVEL_ED"] = df_trimestral["NIVEL_ED"].replace(
                diccionario_mapeo
            )

            resumen_trimestre = (
                df_trimestral.groupby("NIVEL_ED")["PONDERA"]
                .sum()
                .reset_index()
                .sort_values(by="PONDERA", ascending=True)
                .rename(columns={
                    "NIVEL_ED": "Niveles Educativos",
                    "PONDERA": "Cantidad Maxima",
                })
            )

    if isinstance(df_por_anio, pd.DataFrame) and not df_por_anio.empty:
        if "NIVEL_ED" in df_por_anio.columns:
            df_por_anio = df_por_anio[
                df_por_anio["NIVEL_ED"].isin(valores_originales)
            ].copy()
            df_por_anio["NIVEL_ED"] = df_por_anio["NIVEL_ED"].replace(
                diccionario_mapeo
            )

    return resumen_trimestre, df_por_anio


# ----------------------------------------------------------------------------------------------------------------------
# FUNCIONES PUNTO 1.6.2
# ----------------------------------------------------------------------------------------------------------------------

def agrupamiento(df_por_anio, opciones):
    """
    Calcula el nivel educativo más común por grupo etario.

    Filtra por edad y agrupa para encontrar el nivel predominante en cada rango.

    Args:
        df_por_anio (pandas.DataFrame): DataFrame con datos de individuos (columnas 'ANO4', 'NIVEL_ED', 'CH06', 'PONDERA').
        opciones (list): Lista de cadenas con rangos de edad (ej., ["20-29", "+60"]).

    Returns:
        dict: Diccionario {rango_edad: (nivel_mas_comun, conteo_ponderado)}. Vacío si no hay datos.
    """
    if df_por_anio.empty:
        st.warning("El DataFrame para agrupamiento está vacío.")
        return {}

    df_filtrado = df_por_anio[df_por_anio["CH06"] >= 20]

    df_mascomun = (
        df_filtrado.groupby(["ANO4", "NIVEL_ED", "CH06"])["PONDERA"]
        .sum()
        .reset_index()
    )
    resultados_por_grupos = {}

    for rango in opciones:
        try:
            if rango == "+60":
                df_rango = df_mascomun[df_mascomun["CH06"] >= 60]
            else:
                li, ls = map(int, rango.split("-"))
                df_rango = df_mascomun[
                    (df_mascomun["CH06"] >= li) & (df_mascomun["CH06"] <= ls)
                ]

            df_nivel = df_rango.groupby("NIVEL_ED")["PONDERA"].sum().reset_index()
            if not df_nivel.empty:
                nivel_mas_comun = df_nivel.loc[df_nivel["PONDERA"].idxmax()]
                resultados_por_grupos[rango] = (
                    nivel_mas_comun["NIVEL_ED"],
                    nivel_mas_comun["PONDERA"],
                )
        except Exception as e:
            st.warning(f"No se pudo procesar el rango {rango}: {e}")

    return resultados_por_grupos


def grafico_barras(resultados_por_grupos, orden_etario):
    """
    Genera un gráfico de barras del nivel educativo más común por grupo etario.

    Visualiza los resultados del agrupamiento de niveles educativos por edad.

    Args:
        resultados_por_grupos (dict): Diccionario {rango_edad: (nivel_comun, cantidad_ponderada)}.
        orden_etario (list): Lista de cadenas para ordenar los grupos etarios en el eje X.

    Returns:
        plotly.graph_objects.Figure: Objeto figura de Plotly. None si no hay datos.
    """
    if not resultados_por_grupos:
        st.warning("No hay datos para graficar.")
        return None

    df_grafico = pd.DataFrame(
        [
            {"Grupo Etario": r, "Nivel Educativo": n, "PONDERA": p}
            for r, (n, p) in resultados_por_grupos.items()
        ]
    )

    df_grafico["Grupo Etario"] = pd.Categorical(
        df_grafico["Grupo Etario"],
        categories=orden_etario,
        ordered=True,
    )
    df_grafico = df_grafico.sort_values("Grupo Etario")

    fig = px.bar(
        df_grafico,
        x="Grupo Etario",
        y="PONDERA",
        color="Nivel Educativo",
        title="Nivel educativo más común por grupo etario",
        labels={"PONDERA": "Total ponderado"},
        height=500,
    )
    fig.update_traces(textposition="outside", width=0.35)
    fig.update_layout(
        xaxis_title="Grupo Etario",
        yaxis_title="PONDERA",
        legend_title="Nivel Educativo",
    )

    return fig


# ----------------------------------------------------------------------------------------------------------------------
# FUNCIONES PUNTO 1.6.3
# ----------------------------------------------------------------------------------------------------------------------

arc_json = (
    Path(__file__).resolve().parent.parent.parent
    / "utils" / "data" / "aglomerados_coordenadas.json"
)


def exportar_csv(data, nombre_archivo="ranking_aglomerados.csv"):
    """
    Convierte datos de ranking de aglomerados a CSV, añadiendo nombres desde un JSON.

    Args:
        data (dict): Diccionario {código_aglomerado: datos}.
        nombre_archivo (str, optional): Nombre del archivo CSV a guardar. Por defecto es "ranking_aglomerados.csv".

    Returns:
        pandas.DataFrame: El DataFrame convertido a CSV. Cadena vacía si hay errores de archivo JSON.
    """
    try:
        with open(arc_json, encoding="utf-8") as f:
            aglo_data = json.load(f)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo JSON: {arc_json}")
        return ""
    except json.JSONDecodeError as e:
        st.error(f"Error al leer el JSON: {e}")
        return ""

    ranking_con_nombres = {
        aglo_data.get(str(cod).zfill(2), {}).get("nombre", f"Aglomerado {cod}"): datos
        for cod, datos in data.items()
    }

    df = pd.DataFrame.from_dict(ranking_con_nombres, orient="index")
    convertir_csv(df, nombre_archivo=nombre_archivo)

    return df


# ----------------------------------------------------------------------------------------------------------------------
# FUNCIONES PUNTO 1.6.4
# ----------------------------------------------------------------------------------------------------------------------

def grafica_porcentajes_lectura(años, porcentajes_sabe, porcentajes_nosabe):
    """
    Genera un gráfico de línea interactivo de porcentajes de lectura por año.

    Muestra la evolución de "sabe leer" y "no sabe leer" a lo largo del tiempo.

    Args:
        años (list): Lista de años.
        porcentajes_sabe (list): Porcentajes de personas que "saben leer" por año.
        porcentajes_nosabe (list): Porcentajes de personas que "no saben leer" por año.

    Returns:
        altair.Chart: Gráfico Altair combinado. Gráfico vacío si hay error.
    """
    try:
        df = pd.DataFrame({
            "Año": años,
            "Sabe leer": porcentajes_sabe,
            "No sabe leer": porcentajes_nosabe,
        })
        df = df.melt(id_vars=["Año"], var_name="Lectura", value_name="Porcentaje")
    except Exception as e:
        st.error(f"Error al crear DataFrame para la gráfica: {e}")
        return alt.Chart(pd.DataFrame())

    chart_sabe = (
        alt.Chart(df[df["Lectura"] == "Sabe leer"])
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=60), strokeWidth=3)
        .encode(
            x=alt.X("Año:O", axis=alt.Axis(title="Año")),
            y=alt.Y(
                "Porcentaje:Q",
                title="Sabe leer (%)",
                scale=alt.Scale(domain=[90, 100]),
            ),
            color=alt.value("#1f77b4"),
            tooltip=["Año", "Lectura", "Porcentaje"],
        )
        .properties(height=200)
    )

    chart_nosabe = (
        alt.Chart(df[df["Lectura"] == "No sabe leer"])
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=60), strokeWidth=3)
        .encode(
            x=alt.X("Año:O", axis=alt.Axis(title="Año")),
            y=alt.Y(
                "Porcentaje:Q",
                title="No sabe leer (%)",
                scale=alt.Scale(domain=[0, 10]),
            ),
            color=alt.value("#d62728"),
            tooltip=["Año", "Lectura", "Porcentaje"],
        )
        .properties(height=200)
    )

    return alt.vconcat(chart_sabe, chart_nosabe).resolve_scale(x="shared")
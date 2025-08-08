import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import folium

ESTADO_LABORAL = "ESTADO"

def muestra_tasa(tasa, evolucion):
    if evolucion:
        fig, ax = plt.subplots()
        anios = list(evolucion.keys())
        tasas = list(evolucion.values())
        ax.bar(anios, tasas, color="skyblue")
        ax.set_xlabel("Año")
        ax.set_ylabel(f"Tasa de {tasa} (%)")
        ax.set_title(f"Evolución de la tasa de {tasa}")
        st.pyplot(fig)
    else:
        st.warning("Por favor, elije una opción")

# 1.5.1
def calcular_desocupados_por_nivel(df, anio, trimestre, NIVEL_EDUCATIVO):
    # Creo una copia para asegurarme de no modificar el dataframe original.
    df_filtrado = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre) & (df[ESTADO_LABORAL] == 2)].copy()
    #le cambio el tipo de dato en la columna PONDERA, aca es donde modifico el dataframe, por eso la copia.
    df_filtrado['PONDERA'] = df_filtrado['PONDERA'].astype(int)
    df_filtrado["NIVEL_ED"] = df_filtrado["NIVEL_ED"].map(NIVEL_EDUCATIVO)
    # agrupa el dataframe filtrado por nivel educacional, y hace la suma por cada nivel segun la cantidad ponderada. Esto genera una serie donde muestra la cantidad total de personas segun nivel educativo, y lo ordena por indice.
    conteo = (df_filtrado.groupby("NIVEL_ED")['PONDERA'].sum().sort_index())
    return conteo

# 1.5.2

def tasa_des_empleo(df, tipo, aglo=None):
    evolucion = {}
    # Creo una copia para proteger de modificaciones el dataframe original
    df = df.copy()
    # Cambio el tipo de la columna PONDERA
    df["PONDERA"] = df["PONDERA"].astype(float)
    if aglo not in (None, "pais"):
        df = df[df["AGLOMERADO"] == aglo]

    for anio in sorted(df["ANO4"].unique()):
        df_anio = df[df["ANO4"] == anio]
        # .isin([1, 2]): devuelve una serie booleana (en el dataframe filtrado por año), con True para aquellos registros cuyo estado sea 1 (ocupado) o 2 (desocupado) y False para cualquier otro valor (por ejemplo, 3=inactivo).
        df_anio = df_anio[df_anio[ESTADO_LABORAL].isin([1, 2])]
        # Hago las sumatorias desde la columna PONDERA, .loc me deja seleccionar columna y fila a la vez. En este caso, filtra las filas dependiendo el estado laboral, y me retorna los datos de la columna PONDERA. Despues, hace .sum() sobre esa serie.
        desocupados = df_anio.loc[df_anio[ESTADO_LABORAL] == 2, "PONDERA"].sum()
        ocupados = df_anio.loc[df_anio[ESTADO_LABORAL] == 1, "PONDERA"].sum()
        total = desocupados + ocupados
        if tipo == "desempleo":
            if total > 0 :
                tasa = (desocupados / total) * 100
            else:
                tasa= 0
        elif tipo == "empleo":
            if total > 0 :
                tasa = (ocupados / total) * 100
            else:
                tasa= 0
        evolucion[anio] = tasa
    return None if aglo is None else evolucion


# 1.5.4
TIPO_EMPLEO = "PP04A"  # OCUPACION PRINCIPAL
TIPO_EMPLEO_STR = "PP04A_str"

def tipo_empleo(cat):
    if cat == '1':
        return "Estatal"
    elif cat == '2':
        return "Privado"
    else:
        return "Otro"

def ocupados_por_nivel(df):
    df_filtrado = df[(df[ESTADO_LABORAL] == 1)].copy()
    # creo una columna nueva donde me muestra el tipo de empleo en texto.
    df_filtrado[TIPO_EMPLEO_STR] = df_filtrado[TIPO_EMPLEO].apply(tipo_empleo)
    # serie de dos indices que agrupa por aglomerado y tipo de empleo, y me retorna la suma de la columna PONDERA
    agrupado = df_filtrado.groupby(["AGLOMERADO", TIPO_EMPLEO_STR])["PONDERA"].sum()
    # Transformar a diccionario final
    porcentajes = {}

    for aglomerado in agrupado.index.get_level_values(0).unique():
        # valores es una serie unidimensional, diferente a agrupado, que me retorna los valores de cada aglomerado.
        valores = agrupado.loc[aglomerado]
        # total es la cantidad total de empleados por aglomerado.
        total = valores.sum()
        # guardo en el diccionario los porcentajes por cada aglomerado. round redondea el resultado en 2 decimales maximo.
        porcentajes[aglomerado] = {
            "Total": total,
            "% Estatal": round(valores.get("Estatal", 0) / total * 100, 2),
            "% Privado": round(valores.get("Privado", 0) / total * 100, 2),
            "% Otro": round(valores.get("Otro", 0) / total * 100, 2),
        }
    return porcentajes
# 1.5.5
def tasa_aglomerado(df):
    df = df.copy()
    # Cambio el tipo de la columna PONDERA
    df["PONDERA"] = df["PONDERA"].astype(float)
    df_filtrado = df[df[ESTADO_LABORAL].isin([1,2])]
    # .drop_duplicates() elimina las filas repetidas.Si hay varias filas con el mismo año y trimestre, se queda solo con una de cada combinación.
    # .values.tolist() Convierte ese DataFrame en una lista de listas (o sea, una lista de pares [año, trimestre]).
    fechas = sorted(df_filtrado[["ANO4", "TRIMESTRE"]].drop_duplicates().values.tolist())
    fecha_min = fechas[0]  # año y trimestre más antiguo
    fecha_max = fechas[-1]  # año y trimestre más reciente
    # reduzco el dataframe solo con los datos que corresponden a las fechas pedidas
    df_reducido = df_filtrado[
        (df_filtrado["ANO4"] == fecha_min[0])
        & (df_filtrado["TRIMESTRE"] == fecha_min[1])
        | (df_filtrado["ANO4"] == fecha_max[0])
        & (df_filtrado["TRIMESTRE"] == fecha_max[1])]
    # Cada grupo es un subconjunto del DataFrame original, que contiene solo las filas que pertenecen a una combinación específica de:
    # aglo: el número del aglomerado
    # anio: el año
    # trim: el trimestre
    tasas = {}
    for (aglo, anio, trim), grupo in df_reducido.groupby(['AGLOMERADO', 'ANO4', 'TRIMESTRE']):
        # Recorre cada clave de grupo (la tupla con aglomerado, año y trimestre), y guarda el sub-DataFrame correspondiente en grupo
        ocupados = grupo.loc[grupo[ESTADO_LABORAL] == 1, 'PONDERA'].sum()
        desocupados = grupo.loc[grupo[ESTADO_LABORAL] == 2, 'PONDERA'].sum()
        total = ocupados + desocupados
        if total > 0:
            tasa_empleo = round((ocupados / total) * 100, 2)
            tasa_desempleo = round((desocupados / total) * 100, 2)
        else:
            tasa_empleo = tasa_desempleo = 0

        if aglo not in tasas:
            tasas[aglo] = {
                "empleo": {},
                "desempleo": {},
            }

        if [anio, trim] == fecha_min:
            tasas[aglo]["empleo"]["inicio"] = tasa_empleo
            tasas[aglo]["desempleo"]["inicio"] = tasa_desempleo
        elif [anio, trim] == fecha_max:
            tasas[aglo]["empleo"]["fin"] = tasa_empleo
            tasas[aglo]["desempleo"]["fin"] = tasa_desempleo

    return tasas


def colores_aglomerado(tipo, tasas):
    colores = {}
    for aglo, datos in tasas.items():
        if tipo not in datos:
            continue

        inicio = datos[tipo].get("inicio")
        fin = datos[tipo].get("fin")

        if inicio is None or fin is None:
            continue  # No se puede comparar si falta alguno

        if tipo == "empleo":
            colores[aglo] = "green" if fin > inicio else "red"
        elif tipo == "desempleo":
            colores[aglo] = "red" if fin > inicio else "green"

    return colores


def graficar_mapa(coordenadas_aglomerados, colores):
    #creo el mapa
    mapa = folium.Map(location=[-34.6, -58.4], zoom_start=4.5)

    # Paso 3: Agregar puntos
    for aglo_cod, color in colores.items():
        aglo_cod_str = str(aglo_cod).zfill(2)
        if aglo_cod_str in coordenadas_aglomerados:
            data = coordenadas_aglomerados[aglo_cod_str]
            nombre = data["nombre"]
            lat, lon = data["coordenadas"]
            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                popup=f"{nombre}",
            ).add_to(mapa)
    return mapa 

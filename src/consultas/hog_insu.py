# solicitar año, elegir el ultimo trimestre
# CH12 >= 7
# CONDICION_DE_HABITABILIDAD == Insuficiente
# AÑO = INPUT => TRIMESTRE == 4
# PUNTO 13 PARTE B
from pathlib import Path
import csv
import sys
import os
import importlib
import cond_hab
import materialhogares
importlib.reload(cond_hab)
importlib.reload(materialhogares)


sys.path.append(os.path.abspath("../src"))
ruta_hogares = Path("../utils/HogaresTotal.csv").resolve()

NIVEL_EDUCATIVO = "CH12"
CODIGO_RELACIONAL = 'CODUSU'

def funciones_hogares():
    with open(ruta_hogares, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        hogares = list(lector)
    headers = lector.fieldnames
    cond = "CONDICION_DE_HABITABILIDAD"
    if not cond in headers:
        materialhogares.material_techumbre(hogares)
        cond_hab.condicion_de_habitabilidad(hogares)
    return hogares  


def hog_insu():
    hogares = funciones_hogares()
    anio_usuario = input("Ingrese el año a buscar.")
    hogares_insuficientes = {}
    ruta_individuos = Path(__file__).resolve().parent.parent.parent / "utils" / "IndividuosTotal.csv"

    # Primero detectar el trimestre más alto disponible
    trimestres = []
    for hogar in hogares:
        if hogar["ANO4"] == anio_usuario:
            trimestres.add(int(hogar["TRIMESTRE"]))  # guardamos como int para ordenar bien

    if not trimestres:
        print(f"No hay datos para el año {anio_usuario}")
        return

    ultimo_trimestre = max(trimestres)

    for hogar in hogares:
        if hogar['ANO4'] == anio_usuario and hogar['TRIMESTRE'] == str(ultimo_trimestre) and hogar['CONDICION_DE_HABITABILIDAD'] == 'Insuficiente':
            clave = (hogar[CODIGO_RELACIONAL], hogar["NRO_HOGAR"])
            hogares_insuficientes[clave] = True
    contador = 0
    with open(ruta_individuos, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        for persona in lector:
            if persona['ANO4'] == anio_usuario and persona['TRIMESTRE'] == str(ultimo_trimestre):
                clave = (persona[CODIGO_RELACIONAL], persona["NRO_HOGAR"])
                if clave in hogares_insuficientes and persona[NIVEL_EDUCATIVO] >= "7":
                    contador += int(persona['PONDERA'])

    print(f"Cantidad de personas en viviendas con condición insuficiente y nivel universitario o superior: {contador}")

#  REGION
#  II7 == 03
# crear un diccionario con cada region como key, cada valor es su porcentaje de inquilinos
# PUNTO 8 PARTE B
from pathlib import Path
import csv


def porcentaje_inqui():
    ruta_hogares = Path(__file__).resolve().parent.parent.parent / "utils" / "HogaresTotal.csv"

    region_totales = {}

    with open(ruta_hogares, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        for hogar in lector:
            region = hogar['REGION']
            ponderacion = int(hogar['PONDERA'])
            clave = region

            if not clave in region_totales:
                region_totales[clave] = {'inquilinos': 0, 'total': 0}

            region_totales[clave]['total'] += ponderacion
            if hogar["II7"] == "3":
                region_totales[clave]['inquilinos'] += ponderacion

    region_porcentaje = []

    for clave, valor in region_totales.items():
        porcentaje = (valor['inquilinos'] / valor['total'] * 100)
        region_porcentaje.append({
            'region': clave,
            'porcentaje_inquilinos': porcentaje
        })

    region_porcentaje.sort(key=lambda x: x["porcentaje_inquilinos"], reverse=True) #me ordena de manera descendente los datos de region_porcentaje con el porcentaje como parametro.
    print(region_porcentaje)


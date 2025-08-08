# PUNTO 3 PARTE B
import csv
from pathlib import Path

ANIO_REGISTRO = 'ANO4'
ESTADO_LABORAL = 'ESTADO'
def menor_des():
    desocupacion = {}

    ruta_individuos = Path(__file__).resolve().parent.parent.parent / "utils" / "IndividuosTotal.csv"

    with open(ruta_individuos, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        for persona in lector:
            anio = persona[ANIO_REGISTRO]
            trimestre = persona['TRIMESTRE']
            estado = persona[ESTADO_LABORAL]
            ponderacion = int(persona['PONDERA'])
            clave = (anio, trimestre)

            if clave not in desocupacion:
                desocupacion[clave] = {'desocupados': 0, 'total': 0}

            desocupacion[clave]['total'] += ponderacion
            if estado == '2':  
                desocupacion[clave]["desocupados"] += ponderacion

    resultados = []

    for clave, valores in desocupacion.items():
        porcentaje = (valores['desocupados'] / valores['total']) * 100
        resultados.append({
            'año': clave[0],
            'trimestre': clave[1],
            'porcentaje_desocupacion': porcentaje
        })

    resultado_min = min(resultados, key=lambda x: x['porcentaje_desocupacion'])

    print(f"El año {resultado_min['año']} y trimestre {resultado_min['trimestre']} tienen el menor porcentaje de desocupación: {int(resultado_min['porcentaje_desocupacion'])}%.")

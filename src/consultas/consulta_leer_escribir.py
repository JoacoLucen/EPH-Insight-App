import csv
from pathlib import Path


def cargar_datos(archivo_csv):
    """ Carga los datos desde un archivo CSV y devuelve una lista de diccionarios. """
    datos = []
    with open(archivo_csv, encoding="utf-8") as individuos:
        reader = csv.DictReader(individuos, delimiter=';')
        for row in reader:
            datos.append(row)
    return datos


def obtener_años_trimestres(datos):
    """
    Obtengo los años  y el último trimestre para cada año en los datos.
    Para devolver un diccionario donde las claves son los años y los valores
    son los últimos trimestres de cada año.
    """
    año_trimestre = {}
    for row in datos:
        año = row['ANO4']
        trimestre = int(row['TRIMESTRE'])
        if año not in año_trimestre:
            año_trimestre[año] = 0  
        año_trimestre[año] = max(año_trimestre[año], trimestre)  
    return año_trimestre


def calcular_porcentajes_lectura():
    """ Calcula el porcentaje de personas capaces e incapaces de leer por año. """
    
    archivo_csv = Path(__file__).resolve().parent.parent.parent / "utils" / "IndividuosTotal.csv"
    datos = cargar_datos(archivo_csv)

    año_trimestre = obtener_años_trimestres(datos)
    año_trimestreordenado = sorted(año_trimestre.items())

    años = []
    porcentajes_sabe = []
    porcentajes_nosabe = []

    for año, ultimo_trimestre in año_trimestreordenado:
        cont_poblacion = 0
        cont_sabe = 0
        cont_nosabe = 0
        for row in datos:
            if row['ANO4'] == año and int(row['TRIMESTRE']) == ultimo_trimestre:
                edad = int(row['CH06'])
                sabe_leer = row['CH09']
                if edad >= 6:
                    cont_poblacion += int(row['PONDERA'])
                    if sabe_leer == '1':
                        cont_sabe += int(row['PONDERA'])
                    elif sabe_leer == '2':
                        cont_nosabe += int(row['PONDERA'])

        if cont_poblacion > 0:
            porcentaje_sabe = round((cont_sabe / cont_poblacion) * 100, 2)
            porcentaje_nosabe = round((cont_nosabe / cont_poblacion) * 100, 2)
        else:
            porcentaje_sabe = 0
            porcentaje_nosabe = 0

        años.append(int(año))
        porcentajes_sabe.append(porcentaje_sabe)
        porcentajes_nosabe.append(porcentaje_nosabe)

    return años, porcentajes_sabe, porcentajes_nosabe,
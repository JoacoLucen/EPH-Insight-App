import csv
from pathlib import Path
from mayores_nivel_ed import aglomerados_map

def cargar_datos_hogares(archivo_csv):
    """Carga los datos de hogares desde un archivo CSV."""
    
    datos_hogares = []
    with open(archivo_csv, encoding="utf-8") as hogares:
        reader = csv.DictReader(hogares, delimiter=';')
        for row in reader:
            datos_hogares.append(row)
    return datos_hogares

def filtrar_viviendas_precarias(datos_hogares):
    """Filtro las viviendas que tienen más de 2 ocupantes y no tienen baño.
        Para devolver una Lista[diccionarios] ya con las viviendas en las condiciones precarias."""
    viviendas_precarias = []
    for vivienda in datos_hogares:
        cantidad_ocupantes = int(vivienda.get("IX_TOT", 0))
        tiene_baño = vivienda.get("IV8") == '2'
        if tiene_baño and cantidad_ocupantes >= 2:
            viviendas_precarias.append(vivienda)
    return viviendas_precarias

def contar_viviendas_por_aglomerado(viviendas_precarias):
    """Cuento la cantidad de viviendas precarias por aglomerado."""
    conteo_por_aglomerado = {}
    for vivienda in viviendas_precarias:
        aglomerado = vivienda["AGLOMERADO"]
        conteo_por_aglomerado[aglomerado] = conteo_por_aglomerado.get(aglomerado, 0) + int(vivienda["PONDERA"])
    return conteo_por_aglomerado

def aglomerado_con_mas_viviendas_precarias(conteo_por_aglomerado):
    """busco dentro de 'conteo_por_aglomerado' el aglomerado con más viviendas precarias y su cantidad."""
    if not conteo_por_aglomerado:
        return "Ninguno", 0 # Por si no hay viviendas en condiciones "precarias"
    aglomerado_maximo = max(conteo_por_aglomerado, key=conteo_por_aglomerado.get)
    cantidad_maxima = conteo_por_aglomerado[aglomerado_maximo]
    return aglomerado_maximo, cantidad_maxima

def filtrar_y_contar_viviendas_precarias():
    """ - Cargo los datos.
        - Los filtro por viviendas precarias.
        - Los cuento por aglomerados.
        - Busco el máximo entre los aglomerados. 
        - Imprimo el aglomerado con mayor cantidad y cual es."""
    
    archivo_csv = Path(__file__).resolve().parent.parent.parent / 'utils' / 'HogaresTotal.csv'
    
    datos_hogares = cargar_datos_hogares(archivo_csv)
    viviendas_precarias = filtrar_viviendas_precarias(datos_hogares)
    conteo_por_aglomerado = contar_viviendas_por_aglomerado(viviendas_precarias)
    aglomerado_maximo, cantidad_maxima = aglomerado_con_mas_viviendas_precarias(conteo_por_aglomerado)
    aglomerados = aglomerados_map()
    print(f"📈 El aglomerado con mayor cantidad de viviendas con más de dos ocupantes y sin baño es {aglomerados[aglomerado_maximo]} con {cantidad_maxima} viviendas.")
import os
import sys
from pathlib import Path
import csv

#Obtengo ruta absoluta de utils
ruta_const = Path(__file__).resolve().parents[2] / "utils"
sys.path.append(str(ruta_const))

# Importar la constante de nombres de aglomerados
from constantes import NOMBRES_AGLOMERADOS

#Calcula los porcentajes por aglomerado según el tipo de individuo que se pase
def calcular_porcentajes_por_aglomerado(individuos,NOMBRES_AGLOMERADOS, tipo_individuo, hogares = None):
    
    #Subfunción para verificar si un hogar tiene condición de habitabilidad insuficiente
    def tiene_habitabilidad_insuficiente(cod_usu):
        for hogar in hogares:
            if  hogar['CODUSU'] == cod_usu and hogar["CONDICION_DE_HABITABILIDAD"] == "Insuficiente":
                return True
        return False
    #Analizo si tengo individuos para analizar
    if individuos is None:
        print("No hay individuos para analizar.")
    else:
        #Inicialización de contadores por aglomerado
        total_por_aglomerado = {}
        cumplen_por_aglomerado = {}
        
        for p in individuos:
            aglo = p["AGLOMERADO"]
            total_por_aglomerado[aglo] = total_por_aglomerado.get(aglo, 0) + int(p['PONDERA'])

            #Tipo de individuo 0 personas que cursaron universidad
            if tipo_individuo == 'ind_universitario':
                if p.get("CH12") in ("6", "7", "8"):
                    cumplen_por_aglomerado[aglo] = cumplen_por_aglomerado.get(aglo, 0) + int(p['PONDERA'])

            #Tipo de individuo 1 jubilados en hogares con habitabilidad insuficiente
            elif tipo_individuo == 'jubilado' and hogares is not None:
                if p["CAT_INAC"] == "1" and tiene_habitabilidad_insuficiente(p['CODUSU']):
                    cumplen_por_aglomerado[aglo] = cumplen_por_aglomerado.get(aglo, 0) + int(p['PONDERA'])
        
    #Cálculo de porcentajes finales
    porcentajes = {}
    for aglo in total_por_aglomerado:
        total = total_por_aglomerado[aglo]
        cumplen = cumplen_por_aglomerado.get(aglo, 0)
        nombre = NOMBRES_AGLOMERADOS.get(aglo)
        porcentajes[nombre] = round((cumplen / total) * 100, 2)
    
    #Se devuelve ordenado de menor a mayor porcentaje
    return dict(sorted(porcentajes.items(), key=lambda item: item[1], reverse=False))

def obtener_ultimo_trimestre(personas):
    ult_anio = max(p["ANO4"] for p in personas)
    trimestres_de_ult_anio = [p["TRIMESTRE"] for p in personas if p["ANO4"] == ult_anio]
    return max(trimestres_de_ult_anio),ult_anio

#Imprime en consola los porcentajes calculados
def imprimir_porcentajes_por_aglomerado(porcentajes, descripcion):
    print("-"*90)
    print(f"Porcentaje de {descripcion} ")
    print("-"*90)
    for key,value in porcentajes.items():
        print(f"{key} : {value}")

#Lee el archivo de individuos y devuelve la lista de diccionarios
def obtener_individuos():
        
        ruta_individuos = Path(__file__).resolve().parent.parent.parent / "utils" / "IndividuosTotal.csv"

        if not ruta_individuos.exists():
            print(f" No se encontró el archivo en: {ruta_individuos.resolve()}")
            return 
        else:
            with open(ruta_individuos, mode='r', encoding='utf-8') as individuos_file:
                individuos = list(csv.DictReader(individuos_file, delimiter=";"))
                return individuos

#Lee el archivo de hogares y devuelve la lista de diccionarios
def obtener_hogares():
        ruta_hogares = Path(__file__).resolve().parent.parent.parent / "utils" / "HogaresTotal.csv"
        
        if not ruta_hogares.exists():
            print(f" No se encontró el archivo en: {ruta_hogares.resolve()}")
            return 
        else:
            with open(ruta_hogares, mode='r', encoding='utf-8') as individuos_file:
                hogares = list(csv.DictReader(individuos_file, delimiter=";"))
                return hogares

#Lee el archivo de individuos y devuelve la lista de registros
def porcentaje_universitarios_por_aglomerado(individuos):
    porcentajes = calcular_porcentajes_por_aglomerado(individuos, NOMBRES_AGLOMERADOS,'ind_universitario')
    
    imprimir_porcentajes_por_aglomerado(porcentajes,"personas, por aglomerado, que cursaron al menos un nivel universitario.")

#Calcula e imprime el porcentaje de jubilados en hogares con condición insuficiente
def porcentaje_jubilados_condicion_insuficiente(individuos):
    hogares = obtener_hogares()
    #Obtenemos el último trimestre del ultimo anio
    ult_trim,ult_anio = obtener_ultimo_trimestre(individuos)
    #Filtramos las personas del último trimestre del ultimo anio
    personas_ultimo_trimestre = [p for p in individuos if p["ANO4"] == ult_anio and p["TRIMESTRE"] == ult_trim]

    porcentajes = calcular_porcentajes_por_aglomerado(personas_ultimo_trimestre,NOMBRES_AGLOMERADOS,'jubilado',hogares)
    
    imprimir_porcentajes_por_aglomerado(porcentajes, "jubilados en el ultimo trimestre, por aglomerado, que se encuentran en condicion de habitabilidad insuficiente")
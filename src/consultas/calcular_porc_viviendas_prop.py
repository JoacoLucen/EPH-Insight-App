import os
from pathlib import Path
import csv

from pathlib import Path
import csv

def obtener_nombre_aglomerados():
    """Devuelve un diccionario con los códigos y nombres de los aglomerados"""
    return {
        "2": "Gran La Plata", 
        "3": "Bahía Blanca - Cerri", 
        "4": "Gran Rosario", 
        "5": "Gran Santa Fé", 
        "6": "Gran Paraná", 
        "7": "Posadas", 
        "8": "Gran Resistencia", 
        "9": "Comodoro Rivadavia - Rada Tilly", 
        "10": "Gran Mendoza", 
        "12": "Corrientes", 
        "13": "Gran Córdoba", 
        "14": "Concordia", 
        "15": "Formosa", 
        "17": "Neuquén - Plottier", 
        "18": "Santiago del Estero - La Banda", 
        "19": "Jujuy - Palpalá", 
        "20": "Río Gallegos", 
        "22": "Gran Catamarca", 
        "23": "Gran Salta", 
        "25": "La Rioja", 
        "26": "Gran San Luis", 
        "27": "Gran San Juan", 
        "29": "Gran Tucumán - Tafí Viejo", 
        "30": "Santa Rosa - Toay", 
        "31": "Ushuaia - Río Grande", 
        "32": "Ciudad Autonoma de Buenos Aires", 
        "33": "Partidos del GBA", 
        "34": "Mar del Plata", 
        "36": "Río Cuarto", 
        "38": "San Nicolás - Villa Constitución", 
        "91": "Rawson - Trelew", 
        "93": "Viedma - Carmen de Patagones"
    }

def porcentaje_viviendas_propias_por_aglomerado(hogares, nombre_aglomerados):
    """Calcula el porcentaje de viviendas propias por aglomerado"""
    total_por_aglomerado = {}
    propietarios_por_aglomerado = {}

    for hogar in hogares:
        aglomerado = hogar["AGLOMERADO"]
        ponderado = int(hogar['PONDERA'])
        total_por_aglomerado[aglomerado] = total_por_aglomerado.get(aglomerado, 0) + ponderado

        if hogar["II7"] in ("1", "2"):
            propietarios_por_aglomerado[aglomerado] = propietarios_por_aglomerado.get(aglomerado, 0) + ponderado

    porcentajes = {}
    for aglomerado, total in total_por_aglomerado.items():
        propietarios = propietarios_por_aglomerado.get(aglomerado, 0)
        nombre = nombre_aglomerados.get(aglomerado)
        porcentajes[nombre] = round((propietarios / total) * 100, 2)

    return dict(sorted(porcentajes.items(), key=lambda item: item[1]))

def obtener_hogares():
    """Lee el archivo de hogares y devuelve la lista de diccionarios"""
    ruta_hogares = Path(__file__).resolve().parent.parent.parent / "utils" / "HogaresTotal.csv"

    if not ruta_hogares.exists():
        print(f" No se encontró el archivo en: {ruta_hogares.resolve()}")
        return
    else:
        with open(ruta_hogares, mode='r', encoding='utf-8') as individuos_file:
            hogares = list(csv.DictReader(individuos_file, delimiter=";"))
            return hogares

def imprimir_viviendas_propias_por_aglomerado():
    """Imprime el porcentaje de viviendas propias por aglomerado"""
    hogares = obtener_hogares()
    porcentajes = porcentaje_viviendas_propias_por_aglomerado(hogares, obtener_nombre_aglomerados())

    print("-"*90)
    print("Porcentaje de viviendas propias, por aglomerado")
    print("-"*90)
    for key, value in porcentajes.items():
        print(f"{key} : {value}")
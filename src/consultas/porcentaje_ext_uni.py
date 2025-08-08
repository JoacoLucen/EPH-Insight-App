from pathlib import Path
import csv

LUGAR_NACIMIENTO = 'CH15'
NIVEL_EDUCACION = 'CH12'

def porcentaje_extranjeros_universitarios():
    
    #Define la ruta al archivo de individuos
    ruta_individuos = Path(__file__).resolve().parent.parent.parent / "utils" / "IndividuosTotal.csv"

    #Para que no se genere un error en caso de no existir el archivo
    if not ruta_individuos.exists():
        print(f"No se encontró el archivo en: {ruta_individuos.resolve()}")
        return
    
    #Solicita al usuario el año y trimestre que desea analizar
    year = input("Ingrese el año(YYYY): ").strip()
    quarter = input("Ingrese el trimeste (1, 2, 3 o 4): ").strip()
    
    total = 0  #Total de personas en el período seleccionado
    pers = 0   #Total de personas extranjeras con nivel universitario o superior
    
    #Se abre el archivo csv y recorremos 1 por 1 a los individuos
    with open(ruta_individuos, mode='r', encoding='utf-8') as individuos_file:
        individuos = csv.DictReader(individuos_file, delimiter=";")
        #Itero sobre cada individuo
        for i in individuos:
            #Filtrar por año y trimestre indicados por el usuario
            if i['ANO4'] == year and i['TRIMESTRE'] == quarter:
                total += int(i['PONDERA'])
                #Si la persona no nació en Argentina y tiene nivel universitario o superior
                if i[LUGAR_NACIMIENTO] in ('4', '5') and i[NIVEL_EDUCACION] in ('5', '6'):
                    pers += int(i['PONDERA'])
    
    #Imprime el resultado y verifica que no se divida por 0 para no generar un error
    print(f"El porcentaje de personas no nacidas en Argentina con nivel universitario o superior es: {round(pers/total * 100, 2)}%") if total != 0 else print("No hay datos disponibles para el período seleccionado.")
from pathlib import Path
import csv


def aglomerados_map():
    """Retorna un diccionario con todos los aglomerados disponibles."""
    return {
        '2': 'Gran La Plata',
        '3': 'Bahía Blanca - Cerri',
        '4': 'Gran Rosario',
        '5': 'Gran Santa Fé',
        '6': 'Gran Paraná',
        '7': 'Posadas',
        '8': 'Gran Resistencia',
        '9': 'Comodoro Rivadavia - Rada Tilly',
        '10': 'Gran Mendoza',
        '12': 'Corrientes',
        '13': 'Gran Córdoba',
        '14': 'Concordia',
        '15': 'Formosa',
        '17': 'Neuquén - Plottier',
        '18': 'Santiago del Estero - La Banda',
        '19': 'Jujuy - Palpalá',
        '20': 'Río Gallegos',
        '22': 'Gran Catamarca',
        '23': 'Gran Salta',
        '25': 'La Rioja',
        '26': 'Gran San Luis',
        '27': 'Gran San Juan',
        '29': 'Gran Tucumán - Tafí Viejo',
        '30': 'Santa Rosa - Toay',
        '31': 'Ushuaia - Río Grande',
        '32': 'Ciudad Autónoma de Buenos Aires',
        '33': 'Partidos del GBA',
        '34': 'Mar del Plata',
        '36': 'Río Cuarto',
        '38': 'San Nicolás - Villa Constitución',
        '91': 'Rawson - Trelew',
        '93': 'Viedma - Carmen de Patagones'
    }


def planilla_mas18_con_aglomerado():
    """
    Carga e imprime una planilla con la suma ponderada de mayores de edad
    según nivel educativo por aglomerado seleccionado.
    """
    planilla = {}
    ruta_individuos = Path(__file__).resolve().parent.parent.parent / "utils" / "IndividuosTotal.csv"
    mapa_aglomerados = aglomerados_map()

    print("Aglomerados disponibles:")
    for codigo, nombre in sorted(mapa_aglomerados.items(), key=lambda x: int(x[0])):
        print(f"{codigo} - {nombre}")

    seleccion = input('Seleccione el número de aglomerado: ').strip()
    while seleccion not in mapa_aglomerados:
        print("Código inválido. Intente nuevamente.")
        seleccion = input('Seleccione el número de aglomerado: ').strip()

    try:
        with open(ruta_individuos, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=";")
            for ind in reader:
                try:
                    if ind.get('AGLOMERADO') != seleccion:
                        continue

                    edad = int(ind.get('CH06', 0))
                    if edad < 18:
                        continue

                    anio = ind['ANO4']
                    trimestre = ind['TRIMESTRE']
                    clave = f'{anio} - T {trimestre}'
                    pondera = float(ind.get('PONDERA', '1'))
                    nivel_ed = ind.get('NIVEL_ED_str', '')

                    if clave not in planilla:
                        planilla[clave] = {
                            'Primario incompleto': 0.0,
                            'Primario completo': 0.0,
                            'Secundario incompleto': 0.0,
                            'Secundario completo': 0.0,
                            'Superior o universitario': 0.0
                        }

                    if nivel_ed in planilla[clave]:
                        planilla[clave][nivel_ed] += pondera

                except ValueError:
                    continue

    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_individuos}")
        return
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return

    if planilla:
        print(f"\nPlanilla de personas +18 según su nivel de estudios para el aglomerado de {mapa_aglomerados[seleccion]}:\n")
        print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format(
            'Año-trimestre', 'Primario inc.', 'Primario comp.',
            'Secundario inc.', 'Secundario comp.', 'Superior'))
        print("-" * 120)

        for clave in sorted(planilla):
            datos = planilla[clave]
            print("{:<20} {:<20.2f} {:<20.2f} {:<20.2f} {:<20.2f} {:<20.2f}".format(
                clave,
                datos['Primario incompleto'],
                datos['Primario completo'],
                datos['Secundario incompleto'],
                datos['Secundario completo'],
                datos['Superior o universitario']))
    else:
        print("No hay datos para el aglomerado seleccionado.")
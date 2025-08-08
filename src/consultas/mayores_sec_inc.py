from pathlib import Path
import csv

def aglomerados_map ():
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
        '32': 'Ciudad Autonoma de Buenos Aires',
        '33': 'Partidos del GBA',
        '34': 'Mar del Plata',
        '36': 'Río Cuarto',
        '38': 'San Nicolás - Villa Constitución',
        '91': 'Rawson - Trelew',
        '93': 'Viedma - Carmen de Patagones'
    }

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


def calc_sec_inc_trim():
    individuos = obtener_individuos()
    if not individuos:
        return

    mapa_aglomerados = aglomerados_map()

    print("Aglomerados disponibles:")
    for codigo, nombre in sorted(mapa_aglomerados.items(), key=lambda x: int(x[0])):
        print(f"{codigo} - {nombre}")

    aglo_a = input('Seleccione el número del primer aglomerado: ').strip()
    aglo_b = input('Seleccione el número del segundo aglomerado: ').strip()

    resultados = {}

    for persona in individuos:
        if not persona["CH06"].isdigit():
            continue

        edad = int(persona["CH06"])
        if edad < 18:
            continue

        año = persona["ANO4"]
        trimestre = persona["TRIMESTRE"]
        aglo = persona["AGLOMERADO"]
        key = f"{año}-T{trimestre}"

        if aglo not in (aglo_a, aglo_b):
            continue

        if key not in resultados:
            resultados[key] = {
                aglo_a: {"total": 0, "incompleto": 0},
                aglo_b: {"total": 0, "incompleto": 0}
            }

        resultados[key][aglo]["total"] += 1
        if persona["NIVEL_ED"] == "3":  # Secundario incompleto
            resultados[key][aglo]["incompleto"] += 1

    
    if resultados:
        print(f"\nPlanilla de personas +18 con secundario incompleto:")
        print("{:<15} {:<30} {:<30}".format("Año-Trimestre", mapa_aglomerados.get(aglo_a, aglo_a), mapa_aglomerados.get(aglo_b, aglo_b)))
        print("-" * 80)
        for año_trimestre in sorted(resultados.keys()):
            dato = resultados[año_trimestre]
            val_a = dato[aglo_a]
            val_b = dato[aglo_b]
            porc_a = round((val_a["incompleto"] / val_a["total"]) * 100, 2) if val_a["total"] > 0 else 0
            porc_b = round((val_b["incompleto"] / val_b["total"]) * 100, 2) if val_b["total"] > 0 else 0
            print("{:<15} {:<30} {:<30}".format(f"{año_trimestre}", f"{porc_a}%", f"{porc_b}%"))

    else:
        print("No hay datos para los aglomerados seleccionados.")
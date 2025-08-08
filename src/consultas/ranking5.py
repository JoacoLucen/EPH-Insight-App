from pathlib import Path
import csv
from collections import defaultdict


def max_ano_trimestre(ruta_hogares):
    """
    Encuentra el año y trimestre más reciente en el archivo de hogares.
    """
    max_ano = 0
    max_trimestre = 0

    try:
        with open(ruta_hogares, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for r in reader:
                try:
                    ano = int(r['ANO4'])
                    trimestre = int(r['TRIMESTRE'])

                    if ano > max_ano or (ano == max_ano and trimestre > max_trimestre):
                        max_ano, max_trimestre = ano, trimestre
                except ValueError:
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_hogares}")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo de hogares: {e}")

    print(f"El año seleccionado fue {max_ano} y el trimestre fue {max_trimestre}")
    return max_ano, max_trimestre


def cargar_individuos(ruta_individuos, ano, trimestre):
    """
    Carga los datos de individuos ponderando según PONDERA.
    """
    individuos_dict = defaultdict(float)

    try:
        with open(ruta_individuos, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for ind in reader:
                try:
                    if (int(ind['ANO4']) == ano and
                        int(ind['TRIMESTRE']) == trimestre and
                        ind.get('NIVEL_ED_str') == 'Superior o universitario'):

                        codusu = ind['CODUSU']
                        pondera = float(ind.get('PONDERA', '1'))
                        individuos_dict[codusu] += pondera
                except ValueError:
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_individuos}")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo de individuos: {e}")

    return individuos_dict


def procesar_hogares(ruta_hogares, ano, trimestre, individuos_dict):
    """
    Procesa los hogares ponderando por PONDERA y genera resultados por aglomerado.
    """
    resultados = defaultdict(lambda: {'Total': 0.0, 'Tiene Superior': 0.0})

    try:
        with open(ruta_hogares, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for r in reader:
                try:
                    if int(r['ANO4']) == ano and int(r['TRIMESTRE']) == trimestre:
                        aglomerado = r['AGLOMERADO']
                        codusu = r['CODUSU']
                        ix_tot = int(r['IX_TOT'])
                        pondera = float(r.get('PONDERA', '1'))

                        resultados[aglomerado]['Total'] += pondera

                        if ix_tot >= 2 and individuos_dict.get(codusu, 0) >= 2:
                            resultados[aglomerado]['Tiene Superior'] += pondera
                except ValueError:
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_hogares}")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo de hogares: {e}")

    return resultados


def top5(resultados):
    """
    Calcula el top 5 de aglomerados por porcentaje de educación superior.
    """
    aglomerados = []

    for aglomerado, data in resultados.items():
        total = data['Total']
        superior = data['Tiene Superior']
        porcentaje = superior / total if total > 0 else 0
        aglomerados.append((aglomerado, porcentaje))

    aglomerados.sort(key=lambda x: x[1], reverse=True)

    return {
        k: {
            'Total': resultados[k]['Total'],
            'Tiene Superior': resultados[k]['Tiene Superior'],
            'Porcentaje': round(v * 100, 2)
        }
        for k, v in aglomerados[:5]
    }


def ranking_aglomerados_nivel_sup():
    """
    Función principal que coordina el cálculo del ranking.
    """
    base_path = Path(__file__).resolve().parent.parent.parent / "utils"
    ruta_individuos = base_path / "IndividuosTotal.csv"
    ruta_hogares = base_path / "HogaresTotal.csv"

    ano, trimestre = max_ano_trimestre(ruta_hogares)
    individuos_dict = cargar_individuos(ruta_individuos, ano, trimestre)
    resultados = procesar_hogares(ruta_hogares, ano, trimestre, individuos_dict)
    return top5(resultados)
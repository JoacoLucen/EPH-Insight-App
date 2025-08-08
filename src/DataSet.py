import os
import zipfile
import csv
from pathlib import Path


def dataset_indi_hogares(zip_individuos, zip_hogares):
    """Leo todos los archivos individuos.txt dentro de los zips por cada año-trimestre
        para luego guardarlos en la lista de diccionarios.

    Args:
        zip_folder (carpeta): donde estan los archivos zip que dentro tiene un txt de individuos y de hogares

    Returns:
        all_individuals: devuelve la lista de diccionarios con todos los datos de individuos de cada año-trimestre cargados.
    """
    if zip_individuos is not None:
        all_individuals = []
        for file in os.listdir(zip_individuos):
            if file.endswith(".zip"):
                zip_path = zip_individuos / file
                with zipfile.ZipFile(zip_path) as all_txt:
                    for zips_individuals in all_txt.namelist():
                        if (
                            "usu_individual" in zips_individuals.lower()
                            and zips_individuals.endswith(".txt")
                        ):
                            with all_txt.open(zips_individuals) as txt_individuals:
                                reader = csv.DictReader(
                                    txt_individuals.read().decode("utf-8").splitlines(),
                                    delimiter=";",
                                )
                                all_individuals.extend(reader)
        # Verificación
        print(f"✅ Se cargaron {len(all_individuals)} registros de individuos.")
        return all_individuals

    if zip_hogares is not None:
        all_hogares = []
        for file in os.listdir(zip_hogares):
            if file.endswith(".zip"):
                zip_path = zip_hogares / file
                with zipfile.ZipFile(zip_path) as all_txt:
                    for zips_hogares in all_txt.namelist():
                        if "usu_hogar" in zips_hogares.lower() and zips_hogares.endswith(
                            ".txt"
                        ):
                            with all_txt.open(zips_hogares) as txt_hogares:
                                reader = csv.DictReader(
                                    txt_hogares.read().decode("utf-8").splitlines(),
                                    delimiter=";",
                                )
                                all_hogares.extend(reader)
        # Verificación
        print(f"✅ Se cargaron {len(all_hogares)} registros de hogares.")
        return all_hogares
    
# RECIBO LA LISTA DE DICCIONARIOS Y CREO UN ARCHIVO CSV CON ESOS DATOS EN CARPETA DATA
def guardar_como_csv(nombre_archivo, lista_diccionarios, delimitador=";"):
    if not lista_diccionarios:
        print("⚠️ La lista está vacía, no se creó ningún archivo.")
        return

    # Obtener los nombres de columnas del primer diccionario
    columnas = sorted(set().union(*(d.keys() for d in lista_diccionarios)))

    # Ruta de salida en la carpeta "datos"

    ruta_archivo = (
        Path(__file__).resolve().parent.parent / "utils" / f"{nombre_archivo}.csv"
    )

    with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas, delimiter=delimitador)
        writer.writeheader()
        writer.writerows(lista_diccionarios)

    print(f"✅ Archivo {nombre_archivo} guardado en: {ruta_archivo}")


def año_trimestre():
    """
    Devuelve una tupla que contiene tuplas con (año, trimestre) en el archivo de Hogares
    """

    ruta_hogares = Path(__file__).resolve().parent.parent / "utils" / "HogaresTotal.csv"
    
    if not os.path.exists(ruta_hogares):
        return False

    registro = set()

    with open(ruta_hogares, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for r in reader:
            año = int(r["ANO4"])
            trimestre = int(r["TRIMESTRE"])
            registro.add((año, trimestre))
    
    return registro

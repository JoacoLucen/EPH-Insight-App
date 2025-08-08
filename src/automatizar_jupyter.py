import nbformat #Permite leer y escribir archivos Jupyter Notebook
from nbconvert.preprocessors import ExecutePreprocessor #Proporciona una clase que permite ejecutar todas las celdas de un notebook
import os
from pathlib import Path

def ejecutar_notebook(ruta_notebook, tiempo_espera=600, kernel_name='python3'):
    """
    Ejecuta automáticamente todas las celdas de un notebook Jupyter.
    
    Parámetros:
    -----------
    ruta_notebook : Ruta completa al archivo .ipynb que se desea ejecutar
    tiempo_espera : Tiempo máximo de espera por cada celda (en segundos, default 600)
    kernel_name : Nombre del kernel a utilizar (default 'python3')
    """
    try:
        # Se lee el notebook y se convierte a estructura de datos Python que representa el notebook (f contiene texto JSON)
        with open(ruta_notebook, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4) #as_version=4 es la version estandar actual utilizada para la interpretacion del notebook
        
        # Se crea un objeto para usar en la ejecucion de las celdas del notebook
        ep = ExecutePreprocessor(timeout=tiempo_espera, kernel_name=kernel_name)
        
        # Ejecutar todas las celdas cargadas en la variable nb
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(ruta_notebook)}})
            
        print(f"Notebook {os.path.basename(ruta_notebook)} ejecutado exitosamente!")
    
    except Exception as e:
        print(f"Error al ejecutar el notebook: {str(e)}")
        raise #sirve para relanzar la excepción que fue capturada

def rutas ():
    """Funcion principal para resetear los csv en base a los archivos disponibles"""

    ruta_archivo = Path(__file__).resolve().parent.parent / "notebooks" / "individuos.ipynb"
    ruta_archivo2 = Path(__file__).resolve().parent.parent / "notebooks" / "hogares.ipynb"
    ejecutar_notebook(ruta_archivo)
    ejecutar_notebook(ruta_archivo2)

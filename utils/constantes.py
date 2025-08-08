from pathlib import Path

PROJECT_PATH = Path(__file__).parents[1].resolve() #Raiz del proyecto
UTILS_PATH = PROJECT_PATH / 'utils'
DATA_PATH = UTILS_PATH / 'data' # Ruta donde se almacena los datos
SRC_PATH = PROJECT_PATH / 'src' # Ruta de funciones
NOTEBOOKS_PATH = PROJECT_PATH / 'notebooks' # Jupyter Notebooks
STREAMLIT_PATH = PROJECT_PATH / 'streamlit' # App Streamlit
MAPA_PATH = UTILS_PATH / "mapa_aglomerados.html" # Mapa interactivo

#Archivos CSV
HOGARES_CSV = UTILS_PATH / 'HogaresTotal.csv' #Archivo CSV de Hogares
INDIVIDUOS_CSV = UTILS_PATH / 'IndividuosTotal.csv' #Archivo CSV de Individuos
CANASTA_BASICA_CSV = DATA_PATH / "valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv" # Constantes específicas para ingresos

NOMBRES_AGLOMERADOS = {
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
    "32": "Ciudad Autónoma de Buenos Aires",
    "33": "Partidos del GBA",
    "34": "Mar del Plata",
    "36": "Río Cuarto",
    "38": "San Nicolás - Villa Constitución",
    "91": "Rawson - Trelew",
    "93": "Viedma - Carmen de Patagones",
}

TIPOS_VIVIENDAS = {
    1: 'Casa',
    2: 'Departamento',
    3: 'Pieza en inquilinato',
    4: 'Pieza en hotel/pensión',
    5: 'Local no construido para habitación',
    6: 'Otros',
}

TIPOS_PISOS = {
    1: 'mosaico/baldosa/madera/cerámica/alfombra',
    2: 'cemento/ladrillo fijo',
    3: 'ladrillo suelto/tierra',
}

UBICACION_BANIOS = {
    1: 'Dentro de la vivienda',
    2: 'Fuera de la vivienda pero dentro del terreno',
    3: 'Fuera del terreno',
}

DERECHO_PROPIEDAD = {
    1: 'Propietario de la vivienda y el terreno',
    2: 'Propietario de la vivienda solamente',
    3: 'Inquilino/arrendatario de la vivienda',
    4: 'Ocupante por pago de impuestos/expensas',
    5: 'Ocupante en relación de dependencia',
    6: 'Ocupante gratuito (con permiso)',
    7: 'Ocupante de hecho (sin permiso)',
    8: 'Está en sucesión',
}

NIVEL_EDUCATIVO = {
    1: 'Primario incompleto',
    2: 'Primario completo',
    3: 'Secundario incompleto',
    4: 'Secundario completo',
    5: 'Superior universitario incompleto',
    6: 'Superior universitario completo',
    7: 'Sin instrucción',
    9: 'Ns/Nr',
}


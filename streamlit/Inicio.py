import streamlit as st
from pathlib import Path
import sys
import os 
import shutil

project_root = Path(__file__).parent.parent  # Ajusta según niveles necesarios
sys.path.append(str(project_root))

from src import DataSet as dt
from src import automatizar_jupyter as aj
#from src.DataSet import año_trimestre
#from src.automatizar_jupyter import rutas

# Ruta donde se guardan los archivos .zip
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "utils", "data")

# Crear la carpeta si no existe
os.makedirs(DATA_FOLDER, exist_ok=True)

# Configuración general de la página
st.set_page_config(page_title='EPH Insight', layout='wide')
st.title("EPH Insight")

# Ruta relativa para los links
PAGES_DIR = Path("pages")

tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "⬆️ Carga de Datos", "📄 Información Legal"])

# TAB 1: Página de inicio con links
with tab1:
    st.info("""
    **Esta aplicación permite explorar y analizar los datos provenientes de la Encuesta Permanente de Hogares (EPH) de Argentina, una operación estadística continua realizada por el INDEC.  
    La EPH recopila información socioeconómica de los hogares urbanos en Argentina, datos como: empleo, ingresos, educación, características del hogar, integrantes, entre muchos más.**
    **Para comenzar, por favor ingresa a la sección de Carga de Datos.**
    """)
    st.markdown("[Pagina Oficial del INDEC](https://www.indec.gob.ar/)")
    st.divider()

    cols = st.columns(3)
    secciones = [
        ("📊", "Características Demográficas", "1_Caracteristicas_Demograficas.py"),
        ("🏘️", "Características de la Vivienda", "2_Características_de_la_Vivienda.py"),
        ("💼⚙️", "Actividad y Empleo", "3_Actividad_y_Empleo.py"),
        ("🧑‍🎓📚️", "Educación", "4_Educacion.py"),
        ("📈💸", "Línea de Pobreza e Indigencia", "5_Ingresos_Pobreza.py"),

    ]

    for i, (icono, texto, archivo) in enumerate(secciones):
        with cols[i % 3]:
            st.markdown(f"### {icono} {texto}")
            st.page_link(str(PAGES_DIR / archivo), label="Acceder")

# TAB 2: Carga de Datos
with tab2:
    st.info("""
    **Esta sección permite cargar los archivos .zip de la EPH y realizar una verificación automática para asegurar que la información esté completa.
    El sistema revisa que, entre el año y trimestre mínimo y el año y trimestre máximo detectados en los archivos cargados, se encuentren todos los años y trimestres intermedios sin faltantes. 
    Esto garantiza que la base de datos cubra de forma continua el período analizado, y en caso contrario que se sepa que faltan.**""")
    """***Tenga en cuenta que solo se pueden subir archivos hasta el 3er trimestre de 2024 inclusive***"""
    st.divider()
    st.subheader("Carga de Archivos ZIP")
    uploaded_files = st.file_uploader("Sube los archivos .zip de la EPH y actualiza los datos...", type=["zip"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Guardar el archivo en la carpeta DATA_FOLDER
            file_path = os.path.join(DATA_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Archivo {uploaded_file.name} cargado correctamente.")
    st.markdown("[Descargar los Datos de la EPH aqui](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos)")
    if st.button("Actualizar"):
        aj.rutas() 
        st.cache_data.clear()  # limpia el caché global
        st.session_state["datos_actualizados"] = True  
        st.rerun()
    st.divider()
    st.subheader("Verificación de Datos") 
    rango_fechas = dt.año_trimestre()

    try:
        if not rango_fechas: #Si rango_fechas = false, va directamente a la excepcion
            raise ValueError("La lista rango_fechas está vacía")  

        rango_fechas_ordenado = sorted(rango_fechas)
        
        anio_inicio, trimestre_inicio = rango_fechas_ordenado[0]
        anio_fin, trimestre_fin = rango_fechas_ordenado[-1]
        
        periodo_esperado = []
        anio, trimestre = anio_inicio, trimestre_inicio

        while (anio < anio_fin) or (anio == anio_fin and trimestre <= trimestre_fin):
            periodo_esperado.append((anio, trimestre))
            if trimestre == 4:
                anio += 1
                trimestre = 1
            else:
                trimestre += 1

        # Agrupar faltantes por año usando un diccionario común
        faltantes = {}
        for a, t in periodo_esperado:
            if (a, t) not in rango_fechas_ordenado:
                if a not in faltantes:
                    faltantes[a] = []
                faltantes[a].append(f"T{t}")

        # Mostrar resultado
        if not faltantes:
            st.success(f"""***El sistema contiene información desde el {trimestre_inicio}° trimestre del año {anio_inicio} hasta el {trimestre_fin}° trimestre del año {anio_fin}.***
                       ✅ El chequeo resultó exitoso y no se encontraron inconsistencias""")
        else:
            vuelta = 0
            mensaje = f"""***El sistema contiene información desde el {trimestre_inicio}° trimestre del año {anio_inicio} hasta el {trimestre_fin}° trimestre del año {anio_fin}.***\n\n
            ⚠️ El chequeo resultó inconsistente, los periodos faltantes son: """
            for a in sorted(faltantes.keys()):
                trimestres = ", ".join(faltantes[a])
                if vuelta == 0:
                    mensaje += f"{a}: {trimestres}"
                    vuelta += 1
                else:
                    mensaje += f" || {a}: {trimestres}"
            st.error(mensaje)

    except ValueError:
        st.error("El sistema no contiene informacion de ningun trimestre y año.")


    except ValueError:
        st.error("El sistema no contiene informacion de ningun trimestre y año.")

# TAB 3: Información legal y autores
with tab3:
    st.subheader("Licencia MIT")
    st.markdown("""
    **Copyright (c) 2025 [Grupo 26]**

    Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados, para utilizar el Software sin restricciones, incluyendo, sin limitación, los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del Software, y a permitir a las personas a quienes se les proporcione el Software hacerlo, sujeto a las siguientes condiciones:

    El aviso de copyright anterior y este aviso de permiso deberán incluirse en todas las copias o partes sustanciales del Software.

    **EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO**, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITÁNDOSE A LAS GARANTÍAS DE COMERCIALIZACIÓN, IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O LOS TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN, DAÑO O OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN CONTRACTUAL, AGRAVIO O DE OTRO TIPO, QUE SURJA DE O EN CONEXIÓN CON EL SOFTWARE O EL USO U OTROS TRATOS EN EL SOFTWARE.
    """)

    # Sección centrada vertical y horizontalmente
    st.markdown("""
    <div style="height: 40vh; display: flex; align-items: center; justify-content: center;">
        <div style="text-align: center;">
            <h4>Desarrollado por</h4>
            <p>Lucentini Joaquin | Loredo Lautaro | Rodriguez Ulises | Morano Axel Martin | Arrechea Diego</p>
        </div>
    </div>
    """, unsafe_allow_html=True)






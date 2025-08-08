<!-- Título centrado -->
<h1 align="center">📁 EPH Insight</h1>

<!-- Tabla de contenidos -->
## 📑 Tabla de Contenidos
- [Acerca del Proyecto](#-acerca-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Utilizacion de Streamlit](#-utilizacion-de-streamlit)
- [Integrantes](#-integrantes)
- [Estructura del Proyecto](#-estructura-del-proyecto)

--------------------------------------------------------------------
## 🌟 Acerca del Proyecto
"Programa diseñado para, en base a los EPH de diferentes años y trimestres, generar nuevos datos (columnas), csv con estos nuevos datos y los viejos y consultar sobre estos. Por otro lado tambien esta el diseño de una pagina en Streamlit donde se pueden visualizar e interactuar con diferentes tareas"

--------------------------------------------------------------------
## 🌳 Requisitos

- **Python 3**
- **Editor de código**
- **Terminal/Consola**

--------------------------------------------------------------------
## 🛠️ Instalación

Sigue estos pasos para configurar el entorno de desarrollo:

1. **Clonar el repositorio**:
   ```bash
   Clone con SSH
    git clone git@gitlab.catedras.linti.unlp.edu.ar:python-2025/proyectos/grupo26/code.git
   Clone con HTTPS
    git clone https://gitlab.catedras.linti.unlp.edu.ar/python-2025/proyectos/grupo26/code.git

2. **Entrar a la carpeta del proyecto**:

        cd INDEC

3. **Crear y activar el entorno virtual**:
    **Windows**

    python -m venv venv  ----------  .\venv\Scripts\activate

    **Linux/Mac**

    python3 -m venv venv  ---------  source venv/bin/activate

4. **Instala el requirements**:

        pip install -r requirements.txt

4. **Agregar archivos**: Se puede hacer desde la pagina de Streamlit o de forma local, como se muestra a continuacion..
    
    1. Descarga archivos .zip de la Encuesta Permanente de Hogares (EPH) de la [página oficial del INDEC](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos)
    2. Colocarlos en la carpeta /utils/data
        **Estructura final:**

            |──EPH-Insight-App
            │   ├── utils                           
            │         ├── data                 
            │               ├── data_2_2019.zip
            |               ├── data_1_2020.zip
            |               ├── valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv
            |               ├── aglomerados_coordenadas.json

    ***⚠️ Al descargarse los archivos en extension .zip no habra faltantes en Individuos u Hogares para el mismo año y trimestre***
--------------------------------------------------------------------
## 👨‍💻 Utilizacion de Streamlit

#### 1. **Entrar a la carpeta de Streamlit**

- Posicionarse en la carpeta del trabajo `EPH-Insight-App`.
- Ingresar a la carpeta de Streamlit:

```bash
cd streamlit/
```

#### 2. **Ejecutar el programa de Streamlit**

```bash
streamlit run Inicio.py
```

#### 3. **Cargar los datos**
- En la pagina "Carga de datos" presionar el boton "Actualizar datos", el mismo cargara los datos y mostrara uno de los siguientes mensajes:

    - ✅ El chequeo resultó exitoso y no se encontraron inconsistencias, en caso de no haber archivos faltantes entre el Año y Trimestre maximo y minimo

    - ⚠️ En caso de haber un faltante, se informara por pantalla el Año y Trimestre faltante

#### 4. **Pagina lista para ser utilizada e interactuar con ella**

--------------------------------------------------------------------
## 👥 Integrantes

- Lucentini Joaquin --> Legajo 18143/6
- Loredo Lautaro --> Legajo 18137/7
- Rodriguez Ulises --> Legajo 18304/4
- Morano Axel Martin --> Legajo 18212/1
- Arrechea Diego --> Legajo 17821/7

--------------------------------------------------------------------
## 🌳 Estructura del Proyecto

**Como es la estructura?**
- En la carpeta notebooks se encuentran la seccion A (individuos y hogares) y la seccion B (consultas) donde se encuentran separados cada uno de los puntos para ejecutar por separado
- La carpeta src tiene: 
    1. La funcion que me permite unir todos los DataSet de individuos y hogares (por separado)
    2. La funcion para poner ejecutar los Jupyter de la seccion A y B de forma automatizada
    3. Una carpeta funciones con todas las funciones necesarias para la seccion A
    4. Una carpeta consultas con todas las funciones necesarias para la seccion B
- La carpeta streamlit contiene la pagina principal y una carpeta con el orden de las demas paginas donde se resuelven los ejercicios mencionados en la parte 2 de la entrega del TP Integrador
- La carpeta Utils va a contener los csv cuando se generen con todos los DataSets y sus datos nuevos, tambien un archivo con constantes a utilizar durante la ejecucion del programa. Ademas va a contener una carpeta data donde contendra los archivos .zip del EPH suministrado por la pagina oficial del INDEC, coordenadas de los aglomerados y un archivo .csv con los valores de la canasta basica de alimentos

**Tree**

```bash
EPH-Insight-App/
├── notebooks/
│   ├── consultas.ipynb
│   ├── hogares.ipynb
│   └── individuos.ipynb
├── src/
│   ├── automatizar_jupyter.py
│   ├── consultas/          
│   ├── DataSet.py
│   ├── funciones/          
│   ├── __init__.py
│   └── funciones_streamlit/ 
├── streamlit/          
│   ├── pages/
│   ├── Inicio.py
├── utils/
│   ├── constantes.py
│   ├── data/    
│   ├── mapa_aglomerados.html  
│   └── __init__.py
├── README.md
├── requirements.txt
├── license.txt
└── .gitignore
```

--------------------------------------------------------------------
<details>
<summary>📝 Licencia MIT</summary>

Copyright (c) 2025 [Grupo 26]  

Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados, para utilizar el Software sin restricciones, incluyendo, sin limitación, los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del Software, y a permitir a las personas a quienes se les proporcione el Software hacerlo, sujeto a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso deberán incluirse en todas las copias o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITÁNDOSE A LAS GARANTÍAS DE COMERCIALIZACIÓN, IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O LOS TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN, DAÑO O OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN CONTRACTUAL, AGRAVIO O DE OTRO TIPO, QUE SURJA DE O EN CONEXIÓN CON EL SOFTWARE O EL USO U OTROS TRATOS EN EL SOFTWARE.

</details>
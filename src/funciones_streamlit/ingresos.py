import pandas as pd
import streamlit as st
from utils.constantes import CANASTA_BASICA_CSV

# ---------------------------------------------------------------------------------------------------------------------
# CARGA Y PREPARACIÓN DE DATOS
# ---------------------------------------------------------------------------------------------------------------------

@st.cache_data
def cargar_datos_canasta_basica():
    """
    Carga el DataFrame de canasta básica familiar desde 2016.
    Procesa las fechas y prepara los datos para cálculos trimestrales.
    """
    try:
        df = pd.read_csv(CANASTA_BASICA_CSV)
        
        if df.empty:
            st.error("⚠️ El archivo de canasta básica está vacío")
            return None

        # Procesar la columna de fechas
        df['indice_tiempo'] = pd.to_datetime(df['indice_tiempo'])
        df['ANO4'] = df['indice_tiempo'].dt.year
        df['MES'] = df['indice_tiempo'].dt.month
        
        # Calcular trimestre basado en el mes
        df['TRIMESTRE'] = df['MES'].apply(lambda x: (x - 1) // 3 + 1)
        
        columnas_relevantes = [
            'ANO4', 'MES', 'TRIMESTRE', 
            'canasta_basica_total', 'linea_pobreza', 'linea_indigencia'
        ]
        
        return df[columnas_relevantes].copy()
        
    except FileNotFoundError:
        st.error(f"⚠️ No se encontró el archivo de canasta básica: {CANASTA_BASICA_CSV}")
        return None
    except Exception as e:
        st.error(f"⚠️ Error al cargar canasta básica: {e}")
        return None


# ---------------------------------------------------------------------------------------------------------------------
# FUNCIONES DE PROCESAMIENTO DE CANASTA BÁSICA
# ---------------------------------------------------------------------------------------------------------------------

def obtener_valor_canasta_trimestral(df_canasta, anio, trimestre):
    """
    Obtiene el valor promedio de la canasta básica para un año y trimestre específico.
    
    Parámetros:
    - df_canasta: DataFrame con datos de canasta básica
    - anio: Año seleccionado
    - trimestre: Trimestre seleccionado (1-4)
    
    Retorna:
    - Diccionario con valores promedio de canasta básica, línea de pobreza e indigencia
    """
    if df_canasta is None or df_canasta.empty:
        return None
    
    # Asegurar tipos de datos correctos
    df_canasta = df_canasta.copy()
    df_canasta['ANO4'] = df_canasta['ANO4'].astype(int)
    df_canasta['TRIMESTRE'] = df_canasta['TRIMESTRE'].astype(int)
    
    # Filtrar datos por año y trimestre
    df_filtrado = df_canasta[
        (df_canasta['ANO4'] == anio) & 
        (df_canasta['TRIMESTRE'] == trimestre)
    ].copy()
    
    if df_filtrado.empty:
        st.warning(f"⚠️ No hay datos de canasta básica para {anio}-T{trimestre}")
        return None
    
    # Calcular promedios trimestrales
    canasta_basica = df_filtrado['canasta_basica_total'].mean()
    linea_pobreza = df_filtrado['linea_pobreza'].mean()
    linea_indigencia = df_filtrado['linea_indigencia'].mean()
    
    return {
        'canasta_basica': round(canasta_basica, 2),
        'linea_pobreza': round(linea_pobreza, 2),
        'linea_indigencia': round(linea_indigencia, 2)
    }

# ---------------------------------------------------------------------------------------------------------------------
# FUNCIONES DE ANÁLISIS DE POBREZA E INDIGENCIA
# ---------------------------------------------------------------------------------------------------------------------

def calcular_pobreza_indigencia(df_hogares, valores_canasta, anio, trimestre):
    """
    Calcula la cantidad y porcentajes de hogares en situación de pobreza e indigencia.
    
    Parámetros:
    - df_hogares: DataFrame de hogares con ITF calculado
    - valores_canasta: Diccionario con valores de canasta básica
    - anio: Año de análisis
    - trimestre: Trimestre de análisis
    
    Retorna:
    - Diccionario con resultados del análisis
    """
    if df_hogares is None or df_hogares.empty or valores_canasta is None:
        return None
    
    # Convertir campos a int
    df_hogares = df_hogares.copy()
    df_hogares['ANO4'] = df_hogares['ANO4'].astype(int)
    df_hogares['TRIMESTRE'] = df_hogares['TRIMESTRE'].astype(int)
    df_hogares['IX_TOT'] = df_hogares['IX_TOT'].astype(int)
    
    # Filtrar por año, trimestre y hogares con 4 integrantes
    df_filtrado = df_hogares[
        (df_hogares['ANO4'] == anio) & 
        (df_hogares['TRIMESTRE'] == trimestre) &
        (df_hogares['IX_TOT'] == 4)
    ].copy()
    
    if df_filtrado.empty:
        st.warning(f"⚠️ No hay hogares con 4 integrantes para {anio}-T{trimestre}")
        return None
    
    # Verificar que la columna ITF existe y usar valores reales
    if 'ITF' not in df_filtrado.columns:
        st.error("❌ La columna ITF no se encontró en el dataset de hogares")
        return None
    
    # Convertir ITF a numérico para cálculos seguros
    df_filtrado['ITF'] = pd.to_numeric(df_filtrado['ITF'], errors='coerce')
    
    # Filtrar hogares con ITF válido (no nulos)
    df_filtrado = df_filtrado.dropna(subset=['ITF'])
    
    if df_filtrado.empty:
        st.warning("⚠️ No hay hogares con ITF válido en el período seleccionado")
        return None
    
    # Obtener líneas de pobreza e indigencia
    linea_pobreza = valores_canasta['linea_pobreza']
    linea_indigencia = valores_canasta['linea_indigencia']
    
    # Clasificar hogares
    df_filtrado['situacion'] = 'No pobre'
    df_filtrado.loc[df_filtrado['ITF'] < linea_pobreza, 'situacion'] = 'Pobre'
    df_filtrado.loc[df_filtrado['ITF'] < linea_indigencia, 'situacion'] = 'Indigente'
    
    # Calcular totales ponderados
    total_hogares = df_filtrado['PONDERA'].sum()
    hogares_indigencia = df_filtrado[df_filtrado['situacion'] == 'Indigente']['PONDERA'].sum()
    hogares_pobreza = df_filtrado[df_filtrado['situacion'].isin(['Pobre', 'Indigente'])]['PONDERA'].sum()
    hogares_no_pobres = total_hogares - hogares_pobreza
    
    # Calcular porcentajes
    porc_indigencia = round((hogares_indigencia / total_hogares) * 100, 2) if total_hogares > 0 else 0
    porc_pobreza = round((hogares_pobreza / total_hogares) * 100, 2) if total_hogares > 0 else 0
    porc_no_pobres = round((hogares_no_pobres / total_hogares) * 100, 2) if total_hogares > 0 else 0
    
    return {
        'total_hogares': int(total_hogares),
        'hogares_indigencia': int(hogares_indigencia),
        'hogares_pobreza': int(hogares_pobreza),
        'hogares_no_pobres': int(hogares_no_pobres),
        'porcentaje_indigencia': porc_indigencia,
        'porcentaje_pobreza': porc_pobreza,
        'porcentaje_no_pobres': porc_no_pobres,
        'linea_pobreza': linea_pobreza,
        'linea_indigencia': linea_indigencia
    }


# ---------------------------------------------------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------------------------------------------------------------------

def mostrar_info_canasta_basica(valores_canasta):
    """
    Muestra información detallada sobre los valores de canasta básica utilizados.
    """
    if valores_canasta is None:
        return
    
    st.write("**Valores utilizados para el cálculo:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Canasta Básica Total", 
            f"${valores_canasta['canasta_basica']:,.2f}",
            help="Valor utilizado para el cálculo de la pobreza e indigencia"
        )
    
    with col2:
        st.metric(
            "Línea de Pobreza", 
            f"${valores_canasta['linea_pobreza']:,.2f}",
            help="Valor por debajo del cual un hogar se considera pobre"
        )
    
    with col3:
        st.metric(
            "Línea de Indigencia", 
            f"${valores_canasta['linea_indigencia']:,.2f}",
            help="Valor por debajo del cual un hogar se considera indigente"
        ) 
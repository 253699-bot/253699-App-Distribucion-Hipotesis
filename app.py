import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Analisis Estadistico",
    layout="wide",
)

st.title("Aplicacion de Analisis Estadistico")

st.sidebar.header("Entrada de Datos")

fuente_datos = st.sidebar.radio(
    "Seleccione la fuente de datos:",
    ("Subir archivo CSV", "Generar datos sinteticos"),
)

datos = None
variable_seleccionada = None

if fuente_datos == "Subir archivo CSV":
    archivo = st.sidebar.file_uploader("Cargue su archivo CSV", type=["csv"])

    if archivo is not None:
        df = pd.read_csv(archivo)
        columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

        if not columnas_numericas:
            st.error("El archivo CSV no contiene columnas numericas.")
        else:
            variable_seleccionada = st.sidebar.selectbox(
                "Seleccione la variable a analizar:",
                columnas_numericas,
            )
            datos = df[variable_seleccionada]

elif fuente_datos == "Generar datos sinteticos":
    n = st.sidebar.number_input(
        "Tamano de la muestra (n)",
        min_value=30,
        max_value=10000,
        value=100,
        step=10,
    )
    media = st.sidebar.number_input(
        "Media",
        value=50.0,
        step=1.0,
        format="%.2f",
    )
    desviacion = st.sidebar.number_input(
        "Desviacion estandar",
        min_value=0.01,
        value=10.0,
        step=0.5,
        format="%.2f",
    )

    np.random.seed(42)
    valores = np.random.normal(loc=media, scale=desviacion, size=int(n))
    datos = pd.Series(valores, name="valor_sintetico")
    variable_seleccionada = "valor_sintetico"

if datos is not None:
    st.subheader(f"Variable seleccionada: {variable_seleccionada}")
    df_vista = pd.DataFrame(datos).head(5)
    st.dataframe(df_vista, use_container_width=True)

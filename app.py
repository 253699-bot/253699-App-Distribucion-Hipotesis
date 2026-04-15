import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

    st.divider()
    st.subheader("Visualizacion de la Distribucion")

    col1, col2, col3 = st.columns(3)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.hist(datos, bins=20, color="#4C72B0", edgecolor="black")
        ax1.set_title("Histograma")
        ax1.set_xlabel(variable_seleccionada)
        ax1.set_ylabel("Frecuencia")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        sns.kdeplot(datos, ax=ax2, fill=True, color="#55A868")
        ax2.set_title("KDE (Kernel Density Estimation)")
        ax2.set_xlabel(variable_seleccionada)
        ax2.set_ylabel("Densidad")
        st.pyplot(fig2)

    with col3:
        fig3, ax3 = plt.subplots()
        sns.boxplot(x=datos, ax=ax3, color="#C44E52")
        ax3.set_title("Boxplot")
        ax3.set_xlabel(variable_seleccionada)
        st.pyplot(fig3)

    st.divider()
    st.subheader("Analisis Exploratorio - Cuestionario")

    st.text_area(
        "1. Basandose en los graficos, la distribucion parece normal? Justifique.",
        key="pregunta_normalidad",
        height=100,
    )

    st.text_area(
        "2. Hay presencia de sesgo (asimetria) en la distribucion? Explique.",
        key="pregunta_sesgo",
        height=100,
    )

    st.text_area(
        "3. Se observan valores atipicos (outliers) en el boxplot? Describa.",
        key="pregunta_outliers",
        height=100,
    )

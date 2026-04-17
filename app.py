import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import google.generativeai as genai

def configurar_pagina():
    st.set_page_config(page_title="Analisis Estadistico", layout="wide")
    st.title("Aplicacion de Analisis Estadistico")

def cargar_csv():
    archivo = st.sidebar.file_uploader("Cargue su archivo CSV", type=["csv"])
    if archivo is not None:
        try:
            df = pd.read_csv(archivo)
            columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
            if not columnas_numericas:
                st.error("El archivo CSV no contiene columnas numericas.")
                return None, None
            variable_seleccionada = st.sidebar.selectbox(
                "Seleccione la variable a analizar:",
                columnas_numericas,
            )
            return df[variable_seleccionada], variable_seleccionada
        except Exception as e:
            st.error(f"Error al procesar el archivo CSV: {str(e)}")
            return None, None
    return None, None

def generar_sinteticos():
    n = st.sidebar.number_input("Tamano de la muestra (n)", min_value=1, max_value=10000, value=100, step=10)
    media = st.sidebar.number_input("Media", value=50.0, step=1.0, format="%.2f")
    desviacion = st.sidebar.number_input("Desviacion estandar", min_value=0.01, value=10.0, step=0.5, format="%.2f")
    
    np.random.seed(42)
    valores = np.random.normal(loc=media, scale=desviacion, size=int(n))
    datos = pd.Series(valores, name="valor_sintetico")
    return datos, "valor_sintetico"

def obtener_datos():
    st.sidebar.header("Entrada de Datos")
    fuente_datos = st.sidebar.radio(
        "Seleccione la fuente de datos:",
        ("Subir archivo CSV", "Generar datos sinteticos"),
    )
    if fuente_datos == "Subir archivo CSV":
        return cargar_csv()
    else:
        return generar_sinteticos()

def mostrar_vista_previa(datos, variable_seleccionada):
    st.subheader(f"Variable seleccionada: {variable_seleccionada}")
    df_vista = pd.DataFrame(datos).head(5)
    st.dataframe(df_vista, use_container_width=True)

def mostrar_visualizaciones(datos, variable_seleccionada):
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

def cuestionario_exploratorio():
    st.divider()
    st.subheader("Analisis Exploratorio - Cuestionario")
    st.text_area("1. Basandose en los graficos, la distribucion parece normal? Justifique.", key="pregunta_normalidad", height=100)
    st.text_area("2. Hay presencia de sesgo (asimetria) en la distribucion? Explique.", key="pregunta_sesgo", height=100)
    st.text_area("3. Se observan valores atipicos (outliers) en el boxplot? Describa.", key="pregunta_outliers", height=100)

def graficar_prueba_z(z_calc, z_crit_izq, z_crit_der, tipo_prueba):
    fig_z, ax_z = plt.subplots(figsize=(10, 5))
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)
    ax_z.plot(x, y, color="black", linewidth=2)

    if tipo_prueba == "Bilateral":
        x_shade_left = x[x <= z_crit_izq]
        ax_z.fill_between(x_shade_left, stats.norm.pdf(x_shade_left, 0, 1), color="#D62728", alpha=0.5, label="Region de Rechazo")
        x_shade_right = x[x >= z_crit_der]
        ax_z.fill_between(x_shade_right, stats.norm.pdf(x_shade_right, 0, 1), color="#D62728", alpha=0.5)
    elif tipo_prueba == "Cola izquierda":
        x_shade_left = x[x <= z_crit_izq]
        ax_z.fill_between(x_shade_left, stats.norm.pdf(x_shade_left, 0, 1), color="#D62728", alpha=0.5, label="Region de Rechazo")
    else:
        x_shade_right = x[x >= z_crit_der]
        ax_z.fill_between(x_shade_right, stats.norm.pdf(x_shade_right, 0, 1), color="#D62728", alpha=0.5, label="Region de Rechazo")

    ax_z.axvline(x=z_calc, color="#1F77B4", linestyle="--", linewidth=2, label=f"Z Calculado = {z_calc:.2f}")
    ax_z.set_title("Distribucion Normal Estandar (Prueba Z)")
    ax_z.set_xlabel("Puntuacion Z")
    ax_z.set_ylabel("Densidad de Probabilidad")
    ax_z.legend(loc="upper right")
    ax_z.grid(True, alpha=0.3)
    st.pyplot(fig_z)

def asistente_ia(media_muestral, n_obs, desviacion_muestral, alpha, tipo_prueba, z_calc, p_value):
    st.divider()
    st.subheader("Asistente Estadistico con IA")
    api_key = st.text_input("Ingrese su API Key de Google Gemini", type="password")

    if st.button("Consultar a la IA"):
        if not api_key:
            st.error("Por favor, ingrese una API Key valida.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"Se realizo una prueba Z con los siguientes parametros: media muestral = {media_muestral:.4f}, n = {n_obs}, desviacion estandar = {desviacion_muestral:.4f}, alpha = {alpha}, tipo de prueba = {tipo_prueba}. El estadistico Z fue = {z_calc:.4f} y el p-value = {p_value:.4f}. Se rechaza H0? Explica la decision y si los supuestos de la prueba son razonables."
                
                with st.spinner("Consultando a Gemini..."):
                    response = model.generate_content(prompt)
                    st.info(response.text)
            except Exception as e:
                st.error(f"Error al conectar con la API de Gemini: {str(e)}")

    st.text_area("Compare su conclusion con la de la IA. Escriba sus observaciones:", key="comparacion_ia", height=100)

def modulo_prueba_z(datos):
    st.divider()
    st.subheader("Prueba de Hipotesis (Prueba Z)")

    n_obs = len(datos)
    if n_obs < 30:
        st.warning("El tamano de la muestra es menor a 30. La prueba Z asume una muestra grande o distribucion normal subyacente. Se recomienda precaucion con los resultados.")

    col_h0, col_test, col_alpha = st.columns(3)
    with col_h0:
        valor_h0 = st.number_input("Valor de la Hipotesis Nula (H0)", value=50.0, step=1.0)
    with col_test:
        tipo_prueba = st.selectbox("Tipo de prueba", ["Bilateral", "Cola izquierda", "Cola derecha"])
    with col_alpha:
        alpha = st.selectbox("Nivel de significancia (alpha)", [0.01, 0.05, 0.10], index=1)

    media_muestral = datos.mean()
    desviacion_muestral = datos.std(ddof=1)
    error_estandar = desviacion_muestral / np.sqrt(n_obs)

    if error_estandar == 0:
        st.error("Error estandar es 0, no se puede calcular Z.")
        return

    z_calc = (media_muestral - valor_h0) / error_estandar

    if tipo_prueba == "Bilateral":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_calc)))
        z_crit_izq = stats.norm.ppf(alpha / 2)
        z_crit_der = stats.norm.ppf(1 - alpha / 2)
    elif tipo_prueba == "Cola izquierda":
        p_value = stats.norm.cdf(z_calc)
        z_crit_izq = stats.norm.ppf(alpha)
        z_crit_der = None
    else:
        p_value = 1 - stats.norm.cdf(z_calc)
        z_crit_izq = None
        z_crit_der = stats.norm.ppf(1 - alpha)

    decision = "Rechazar H0" if p_value < alpha else "No rechazar H0"

    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("Media Muestral", f"{media_muestral:.4f}")
    col_res2.metric("Estadistico Z", f"{z_calc:.4f}")
    col_res3.metric("Valor p", f"{p_value:.4f}")
    col_res4.metric("Decision", decision)

    graficar_prueba_z(z_calc, z_crit_izq, z_crit_der, tipo_prueba)
    asistente_ia(media_muestral, n_obs, desviacion_muestral, alpha, tipo_prueba, z_calc, p_value)

def main():
    configurar_pagina()
    datos, variable_seleccionada = obtener_datos()
    if datos is not None and len(datos) > 0:
        mostrar_vista_previa(datos, variable_seleccionada)
        mostrar_visualizaciones(datos, variable_seleccionada)
        cuestionario_exploratorio()
        modulo_prueba_z(datos)

if __name__ == "__main__":
    main()

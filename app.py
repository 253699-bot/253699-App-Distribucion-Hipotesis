import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def configurar_pagina():
    st.set_page_config(page_title="Analisis Estadistico", layout="wide")
    
    # CSS Customizado Minimalista y Neutro
    st.markdown("""
        <style>
        .stApp {
            background-color: #F9F9F9;
        }
        .css-1d391kg {
            background-color: #FFFFFF;
        }
        .stButton>button {
            background-color: #FFFFFF;
            color: #333333;
            border: 1px solid #DDDDDD;
            border-radius: 4px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            border-color: #888888;
            color: #111111;
        }
        h1, h2, h3 {
            color: #2C3E50;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        hr {
            border-top: 1px solid #E0E0E0;
        }
        </style>
    """, unsafe_allow_html=True)

def cargar_csv():
    archivo = st.sidebar.file_uploader("Cargue su archivo CSV", type=["csv"])
    if archivo is not None:
        try:
            df = pd.read_csv(archivo)
            columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
            if not columnas_numericas:
                st.sidebar.error("El archivo CSV no contiene columnas numericas.")
                return None, None
            variable_seleccionada = st.sidebar.selectbox(
                "Seleccione la variable a analizar:",
                columnas_numericas,
            )
            return df[variable_seleccionada], variable_seleccionada
        except Exception as e:
            st.sidebar.error(f"Error al procesar el archivo CSV: {str(e)}")
            return None, None
    return None, None

def generar_sinteticos():
    n = st.sidebar.number_input("Tamano de la muestra (n)", min_value=1, max_value=10000, value=100, step=10)
    media = st.sidebar.number_input("Media Poblacional Simulada", value=75.0, step=1.0, format="%.2f")
    desviacion = st.sidebar.number_input("Desviacion Estandar Simulada", min_value=0.01, value=12.0, step=0.5, format="%.2f")
    
    np.random.seed(42)
    valores = np.random.normal(loc=media, scale=desviacion, size=int(n))
    datos = pd.Series(valores, name="valor_sintetico")
    return datos, "valor_sintetico"

def obtener_datos():
    st.sidebar.title("Analisis Estadistico")
    st.sidebar.markdown("---")
    st.sidebar.header("Entrada de Datos")
    fuente_datos = st.sidebar.radio(
        "Seleccione la fuente:",
        ("Subir archivo CSV", "Generar datos sinteticos"),
    )
    if fuente_datos == "Subir archivo CSV":
        return cargar_csv()
    else:
        return generar_sinteticos()

def mostrar_vista_previa(datos, variable_seleccionada):
    st.header("1. Vista Previa de Datos")
    st.markdown(f"**Variable actual en analisis:** `{variable_seleccionada}`")
    df_vista = pd.DataFrame(datos).head(5)
    st.dataframe(df_vista, use_container_width=True)

def mostrar_visualizaciones(datos, variable_seleccionada):
    st.divider()
    st.header("2. Visualizacion de la Distribucion")
    col1, col2, col3 = st.columns(3)
    
    color_graficos = "#607D8B"

    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.hist(datos, bins=20, color=color_graficos, edgecolor="white")
        ax1.set_title("Histograma", fontsize=10)
        ax1.set_xlabel(variable_seleccionada)
        ax1.set_ylabel("Frecuencia")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.kdeplot(datos, ax=ax2, fill=True, color=color_graficos)
        ax2.set_title("KDE (Kernel Density Estimation)", fontsize=10)
        ax2.set_xlabel(variable_seleccionada)
        ax2.set_ylabel("Densidad")
        st.pyplot(fig2)

    with col3:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.boxplot(x=datos, ax=ax3, color=color_graficos)
        ax3.set_title("Boxplot", fontsize=10)
        ax3.set_xlabel(variable_seleccionada)
        st.pyplot(fig3)

def cuestionario_exploratorio():
    st.divider()
    st.header("3. Analisis Exploratorio - Cuestionario")
    
    st.markdown("**A. Basandose en los graficos, la distribucion parece normal?**")
    st.selectbox("Seleccione una opcion para la distribucion:", ["(Seleccionar opción)", "Si, se aproxima a una campana de Gauss", "No, difiere significativamente", "No estoy seguro visualmente"], key="pregunta_normalidad", label_visibility="collapsed")
    
    st.markdown("**B. Hay presencia de sesgo (asimetria) en la distribucion?**")
    st.selectbox("Seleccione el tipo de sesgo:", ["(Seleccionar opción)", "Si, sesgo a la izquierda (cola izquierda)", "Si, sesgo a la derecha (cola derecha)", "No, parece simetrica"], key="pregunta_sesgo", label_visibility="collapsed")
    
    st.markdown("**C. Se observan valores atipicos (outliers) en el boxplot?**")
    st.selectbox("Seleccione una observacion sobre los outliers:", ["(Seleccionar opción)", "Si, multiples valores atipicos", "Si, solo uno o dos aislados", "No se observan valores atipicos"], key="pregunta_outliers", label_visibility="collapsed")

def graficar_prueba_z(z_calc, z_crit_izq, z_crit_der, tipo_prueba):
    fig_z, ax_z = plt.subplots(figsize=(10, 4))
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)
    
    # Sombreado default de No Rechazo (color neutro gris claro)
    ax_z.fill_between(x, y, color="#ECEFF1", alpha=0.7, label="Region de NO Rechazo")
    ax_z.plot(x, y, color="#455A64", linewidth=1.5)

    color_rechazo = "#E57373"

    if tipo_prueba == "Bilateral":
        x_shade_left = x[x <= z_crit_izq]
        ax_z.fill_between(x_shade_left, stats.norm.pdf(x_shade_left, 0, 1), color=color_rechazo, alpha=0.8, label="Region de Rechazo")
        x_shade_right = x[x >= z_crit_der]
        # Label only once to avoid duplication in legend
        ax_z.fill_between(x_shade_right, stats.norm.pdf(x_shade_right, 0, 1), color=color_rechazo, alpha=0.8)
    elif tipo_prueba == "Cola izquierda":
        x_shade_left = x[x <= z_crit_izq]
        ax_z.fill_between(x_shade_left, stats.norm.pdf(x_shade_left, 0, 1), color=color_rechazo, alpha=0.8, label="Region de Rechazo")
    else:
        x_shade_right = x[x >= z_crit_der]
        ax_z.fill_between(x_shade_right, stats.norm.pdf(x_shade_right, 0, 1), color=color_rechazo, alpha=0.8, label="Region de Rechazo")

    ax_z.axvline(x=z_calc, color="#1976D2", linestyle="--", linewidth=2.5, label=f"Z Calculado = {z_calc:.2f}")
    
    ax_z.set_title("Distribucion Normal Estandar (Z-Test)", fontsize=12, pad=10)
    ax_z.set_xlabel("Puntuacion Z (Desviaciones Estandar)")
    ax_z.set_ylabel("Densidad")
    ax_z.legend(loc="upper left")
    
    # Hide top and right spines for a cleaner minimalist look
    ax_z.spines['top'].set_visible(False)
    ax_z.spines['right'].set_visible(False)
    
    st.pyplot(fig_z)

def asistente_ia(media_muestral, n_obs, desviacion_muestral, alpha, tipo_prueba, z_calc, p_value, decision):
    st.divider()
    st.header("5. Asistente Estadistico con IA")
    api_key = os.environ.get("GEMINI_API_KEY")

    if st.button("Consultar Conclusion con la IA"):
        if not api_key:
            st.error("Por favor, configure la GEMINI_API_KEY en el archivo .env en la raiz de la app.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = (f"Se realizo una prueba Z con estos caracteristicas: "
                          f"N = {n_obs}, Media = {media_muestral:.4f}, Desv = {desviacion_muestral:.4f}, "
                          f"Z = {z_calc:.4f}, P-Value = {p_value:.4f}, Alpha = {alpha}, "
                          f"Decision matematica calculada: {decision}. "
                          f"Redacta una explicacion muy profesional, limpia (sin emojis) e interpreta este resultado.")
                
                with st.spinner("Conectando con Google Gemini..."):
                    response = model.generate_content(prompt)
                    st.info(response.text)
            except Exception as e:
                st.error(f"Error de API: {str(e)}")

    st.text_area("Observaciones Finales Manuales:", key="comparacion_ia", height=100)

def modulo_prueba_z(datos):
    st.divider()
    st.header("4. Planteamiento de la Prueba de Hipotesis (Z)")

    n_obs = len(datos)
    if n_obs < 30:
        st.warning("El tamano de la muestra es menor a 30. Esto puede afectar la validez del estadistico Z.")

    col_conf1, col_conf2, col_conf3 = st.columns(3)
    with col_conf1:
        valor_h0 = st.number_input("Valor esperado (µ para H0):", value=70.0, step=1.0)
    with col_conf2:
        tipo_prueba = st.selectbox("Tipo de contraste:", ["Bilateral", "Cola izquierda", "Cola derecha"])
    with col_conf3:
        alpha = st.selectbox("Nivel de significancia (α):", [0.01, 0.05, 0.10], index=1)

    st.markdown("### Hipotesis Planteadas")
    
    col_latex1, col_latex2 = st.columns(2)
    with col_latex1:
        st.latex(f"H_0: \mu = {valor_h0}")
    
    with col_latex2:
        if tipo_prueba == "Bilateral":
            st.latex(f"H_1: \mu \\neq {valor_h0}")
        elif tipo_prueba == "Cola izquierda":
            st.latex(f"H_1: \mu < {valor_h0}")
        else:
            st.latex(f"H_1: \mu > {valor_h0}")

    media_muestral = datos.mean()
    desviacion_muestral = datos.std(ddof=1)
    error_estandar = desviacion_muestral / np.sqrt(n_obs)

    if error_estandar == 0:
        st.error("La desviacion estándar es 0, impidiendo el cálculo del error estandar.")
        return

    z_calc = (media_muestral - valor_h0) / error_estandar

    if tipo_prueba == "Bilateral":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_calc)))
        z_crit_izq = stats.norm.ppf(alpha / 2)
        z_crit_der = stats.norm.ppf(1 - alpha / 2)
        str_region = f"Z < {z_crit_izq:.2f} o Z > {z_crit_der:.2f}"
    elif tipo_prueba == "Cola izquierda":
        p_value = stats.norm.cdf(z_calc)
        z_crit_izq = stats.norm.ppf(alpha)
        z_crit_der = None
        str_region = f"Z < {z_crit_izq:.2f}"
    else:
        p_value = 1 - stats.norm.cdf(z_calc)
        z_crit_izq = None
        z_crit_der = stats.norm.ppf(1 - alpha)
        str_region = f"Z > {z_crit_der:.2f}"

    decision = "Rechazar H0" if p_value < alpha else "No rechazar H0"

    st.markdown("### Resultados Estadisticos")
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("Estadistico Z", f"{z_calc:.4f}")
    col_res2.metric("P-Value", f"{p_value:.4f}")
    col_res3.metric("Region Critica", str_region)
    col_res4.metric("Decision Automatica", decision)

    st.markdown("### Visualizacion de Zonas")
    graficar_prueba_z(z_calc, z_crit_izq, z_crit_der, tipo_prueba)
    
    asistente_ia(media_muestral, n_obs, desviacion_muestral, alpha, tipo_prueba, z_calc, p_value, decision)

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

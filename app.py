import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from google import genai
import os
from dotenv import load_dotenv
from fpdf import FPDF
import io

load_dotenv()

def configurar_pagina():
    st.set_page_config(page_title="LuminaData", layout="wide")
    
    # Configuración global de Matplotlib para estilo minimalista orgánico
    plt.rcParams.update({
        'figure.facecolor': '#FFF9E1',
        'axes.facecolor': '#FFF9E1',
        'font.family': 'sans-serif',
        'font.sans-serif': ['Montserrat', 'Inter', 'DejaVu Sans', 'Arial'],
        'text.color': '#553D2A',
        'axes.labelcolor': '#553D2A',
        'xtick.color': '#553D2A',
        'ytick.color': '#553D2A',
        'axes.edgecolor': '#553D2A',
        'grid.color': '#C7B69F',
        'grid.linestyle': ':'
    })
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif;
        }
        
        p, h1, h2, h3, h4, h5, h6, span {
            color: #1A1A1A;
        }

        .stApp {
            background-color: #F5F0E6;
        }

        /* Styling the top header bar */
        [data-testid="stHeader"] {
            background-color: #E6D5B8 !important;
            border-bottom: 1px solid #D7C4A5;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            height: 3.5rem;
        }

        /* Adding the app name to the header */
        [data-testid="stHeader"]::before {
            content: "LuminaData";
            position: absolute;
            width: 100%;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            text-align: center;
            font-weight: 700;
            font-size: 1.6rem;
            color: #3E2A20;
            letter-spacing: -0.5px;
            font-family: 'Montserrat', sans-serif;
            text-shadow: 1px 1px 0px rgba(255,255,255,0.3);
            pointer-events: none;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #3e2a20 0%, #111111 100%);
        }
        
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
            color: #FFFFFF !important;
        }
        
        .stButton>button {
            background-color: #a2fdd5 !important;
            color: #111111 !important;
            border: none !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            font-weight: 600;
        }
        
        .stButton>button:hover {
            box-shadow: 0 4px 10px rgba(162, 253, 213, 0.4);
            transform: translateY(-2px);
        }

        [data-testid="metric-container"], .css-1r6slb0 {
            background-color: #F7F7F7;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid #EBEBEB;
        }
        
        [data-testid="metric-container"] label, [data-testid="metric-container"] div {
            color: #1A1A1A !important;
        }

        /* Estilo para las conclusiones de la IA */
        .ia-response {
            background-color: #E6D5B8;
            color: #3E2A20;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #A2FDD5;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin: 15px 0;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        
        /* Divisor parcial para el sidebar */
        .sidebar-divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, #A2FDD5, transparent);
            width: 70%;
            margin: 10px auto 25px auto;
            border-radius: 2px;
        }
        
        /* Modificar el titulo del sidebar manual via clase CSS ya que esta embebido en st.sidebar.markdown */
        .jade-cobra-title {
            color: #a2fdd5 !important;
            font-weight: 800;
            font-size: 34px;
            letter-spacing: 1px;
            text-align: center;
            margin-bottom: 20px;
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
    st.sidebar.markdown('<p class="jade-cobra-title">LuminaData</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.sidebar.header("Entrada de Datos")
    fuente_datos = st.sidebar.radio(
        "Seleccione la fuente:",
        ("Subir archivo CSV", "Generar datos sintéticos"),
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
    st.header("2. Visualización de la Distribución")
    col1, col2, col3 = st.columns(3)
    
    color_graficos = "#553D2A"

    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.hist(datos, bins=20, color=color_graficos, edgecolor="#FFF9E1")
        ax1.set_title("Histograma", fontsize=10, fontweight='bold')
        ax1.set_xlabel(variable_seleccionada)
        ax1.set_ylabel("Frecuencia")
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(True, axis='y', alpha=0.3)
        st.pyplot(fig1, transparent=True)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.kdeplot(datos, ax=ax2, fill=True, color=color_graficos, alpha=0.7)
        ax2.set_title("KDE (Estimación de Densidad)", fontsize=10, fontweight='bold')
        ax2.set_xlabel(variable_seleccionada)
        ax2.set_ylabel("Densidad")
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2, transparent=True)

    with col3:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.boxplot(x=datos, ax=ax3, color=color_graficos)
        # Ajustar colores del boxplot para contraste
        plt.setp(ax3.artists, edgecolor='#553D2A', facecolor='#7E634E')
        ax3.set_title("Boxplot (Diagrama de Caja)", fontsize=10, fontweight='bold')
        ax3.set_xlabel(variable_seleccionada)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.grid(True, axis='x', alpha=0.3)
        st.pyplot(fig3, transparent=True)

def cuestionario_exploratorio():
    st.divider()
    st.header("3. Análisis Exploratorio - Cuestionario")
    
    st.markdown("**A. Basándose en los gráficos, ¿la distribución parece normal?**")
    st.selectbox("Seleccione una opción para la distribución:", ["(Seleccionar opción)", "Sí, se aproxima a una campana de Gauss", "No, difiere significativamente", "No estoy seguro visualmente"], key="pregunta_normalidad", label_visibility="collapsed")
    
    st.markdown("**B. ¿Hay presencia de sesgo (asimetría) en la distribución?**")
    st.selectbox("Seleccione el tipo de sesgo:", ["(Seleccionar opción)", "Sí, sesgo a la izquierda (cola izquierda)", "Sí, sesgo a la derecha (cola derecha)", "No, parece simétrica"], key="pregunta_sesgo", label_visibility="collapsed")
    
    st.markdown("**C. ¿Se observan valores atípicos (outliers) en el boxplot?**")
    st.selectbox("Seleccione una observación sobre los outliers:", ["(Seleccionar opción)", "Sí, múltiples valores atípicos", "Sí, solo uno o dos aislados", "No se observan valores atípicos"], key="pregunta_outliers", label_visibility="collapsed")

def graficar_prueba_z(z_calc, z_crit_izq, z_crit_der, tipo_prueba):
    fig_z, ax_z = plt.subplots(figsize=(10, 4))
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)
    
    # Sombreado default de No Rechazo (color neutro hueso oscuro)
    ax_z.fill_between(x, y, color="#E3D7BF", alpha=0.6, label="Región de NO Rechazo")
    ax_z.plot(x, y, color="#553D2A", linewidth=2)

    color_rechazo = "#AB9680"

    if tipo_prueba == "Bilateral":
        x_shade_left = x[x <= z_crit_izq]
        ax_z.fill_between(x_shade_left, stats.norm.pdf(x_shade_left, 0, 1), color=color_rechazo, alpha=0.5, label="Región Crítica (Rechazo)")
        x_shade_right = x[x >= z_crit_der]
        ax_z.fill_between(x_shade_right, stats.norm.pdf(x_shade_right, 0, 1), color=color_rechazo, alpha=0.5)
    elif tipo_prueba == "Cola izquierda":
        x_shade_left = x[x <= z_crit_izq]
        ax_z.fill_between(x_shade_left, stats.norm.pdf(x_shade_left, 0, 1), color=color_rechazo, alpha=0.5, label="Región Crítica (Rechazo)")
    else:
        x_shade_right = x[x >= z_crit_der]
        ax_z.fill_between(x_shade_right, stats.norm.pdf(x_shade_right, 0, 1), color=color_rechazo, alpha=0.5, label="Región Crítica (Rechazo)")

    ax_z.axvline(x=z_calc, color="#7E634E", linestyle="--", linewidth=2.5, label=f"Z Calculado = {z_calc:.2f}")
    
    ax_z.set_title("Distribución Normal Estándar (Prueba Z)", fontsize=12, pad=10, fontweight='bold')
    ax_z.set_xlabel("Puntuación Z (Desviaciones Estándar)")
    ax_z.set_ylabel("Densidad")
    ax_z.legend(loc="upper left", frameon=False)
    
    ax_z.spines['top'].set_visible(False)
    ax_z.spines['right'].set_visible(False)
    ax_z.grid(True, linestyle=':', color='#C7B69F', alpha=0.5)
    
    st.pyplot(fig_z, transparent=True)

def generar_pdf_conclusiones(texto):
    pdf = FPDF()
    pdf.add_page()
    
    # Configurar colores (Paleta LuminaData)
    # Fondo ligero: #F5F0E6 (245, 240, 230)
    pdf.set_fill_color(245, 240, 230)
    pdf.rect(0, 0, 210, 297, "F")
    
    # Título Principal
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(62, 42, 32) # #3E2A20
    pdf.cell(0, 20, "LuminaData - Reporte IA", ln=True, align="C")
    
    # Línea decorativa
    pdf.set_draw_color(162, 253, 213) # #A2FDD5
    pdf.set_line_width(1)
    pdf.line(50, 30, 160, 30)
    
    pdf.ln(15)
    
    # Título de Sección
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(62, 42, 32)
    pdf.cell(0, 10, "Conclusiones del Analisis Estadistico", ln=True)
    
    pdf.ln(5)
    
    # Contenido de la conclusión
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(26, 26, 26) # #1A1A1A
    
    # Reemplazar caracteres no compatibles con latin-1 si es necesario
    try:
        safe_text = texto.encode('latin-1', 'replace').decode('latin-1')
    except:
        safe_text = texto
        
    pdf.multi_cell(0, 10, safe_text)
    
    pdf.ln(20)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(126, 99, 78)
    pdf.cell(0, 10, "Generado automaticamente por LuminaData Assistant", ln=True, align="R")
    
    # Retornar como Bytes
    return pdf.output()

def asistente_ia(media_muestral, n_obs, desviacion_muestral, alpha, tipo_prueba, z_calc, p_value, decision):
    st.divider()
    st.header("5. Asistente Estadístico con IA")
    api_key = os.environ.get("GEMINI_API_KEY")

    # Inicializar estado si no existe
    if 'ia_conclusion' not in st.session_state:
        st.session_state.ia_conclusion = None

    if st.button("Consultar Conclusión con la IA"):
        if not api_key:
            st.error("Por favor, configure la GEMINI_API_KEY en el archivo .env en la raíz de la app.")
        else:
            try:
                client = genai.Client(api_key=api_key)
                prompt = (f"Se realizó una prueba Z con estos características: "
                          f"N = {n_obs}, Media = {media_muestral:.4f}, Desv = {desviacion_muestral:.4f}, "
                          f"Z = {z_calc:.4f}, P-Value = {p_value:.4f}, Alpha = {alpha}, "
                          f"Decisión matemática calculada: {decision}. "
                          f"Redacta una explicación muy profesional, limpia (sin emojis) e interpreta este resultado.")
                
                with st.spinner("Conectando con Google Gemini..."):
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt
                    )
                    st.session_state.ia_conclusion = response.text
            except Exception as e:
                st.error(f"Error de API: {str(e)}")

    # Mostrar conclusión si existe
    if st.session_state.ia_conclusion:
        st.markdown(f'<div class="ia-response">{st.session_state.ia_conclusion}</div>', unsafe_allow_html=True)
        
        # Generar enlace de descarga
        try:
            pdf_bytes = generar_pdf_conclusiones(st.session_state.ia_conclusion)
            st.download_button(
                label="📄 Descargar Conclusión (PDF)",
                data=pdf_bytes,
                file_name="conclusion_luminadata.pdf",
                mime="application/pdf",
                key="download_pdf_btn"
            )
        except Exception as e:
            st.error(f"No se pudo generar el PDF: {str(e)}")

    st.text_area("Observaciones Finales Manuales:", key="comparacion_ia", height=100)

def modulo_prueba_z(datos):
    st.divider()
    st.header("4. Planteamiento de la Prueba de Hipótesis (Z)")

    n_obs = len(datos)
    if n_obs < 30:
        st.warning("El tamaño de la muestra es menor a 30. Esto puede afectar la validez del estadístico Z.")

    col_conf1, col_conf2, col_conf3 = st.columns(3)
    with col_conf1:
        valor_h0 = st.number_input("Valor esperado (µ para H₀):", value=70.0, step=1.0)
    with col_conf2:
        tipo_prueba = st.selectbox("Tipo de contraste:", ["Bilateral", "Cola izquierda", "Cola derecha"])
    with col_conf3:
        alpha = st.selectbox("Nivel de significancia (α):", [0.01, 0.05, 0.10], index=1)

    st.markdown("### Hipótesis Planteadas")
    
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
        st.error("La desviación estándar es 0, impidiendo el cálculo del error estándar.")
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

    st.markdown("### Resultados Estadísticos")
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("Estadístico Z", f"{z_calc:.4f}")
    col_res2.metric("Valor p", f"{p_value:.4f}")
    col_res3.metric("Región Crítica", str_region)
    col_res4.metric("Decisión Automática", decision)

    st.markdown("### Visualización de Parámetros")
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

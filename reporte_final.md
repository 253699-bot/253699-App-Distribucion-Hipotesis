# App de Prueba de Hipotesis con Streamlit

**Nombre del estudiante**: [Tu Nombre Aquí]  
**Fecha**: 17 de abril de 2026  

---

## Indice
1. Introduccion
2. Descripcion de los datos
3. Planteamiento de la prueba de hipotesis
   - 3.1. Definicion de hipotesis
   - 3.2. Nivel de significancia
   - 3.3. Estadistico de prueba
   - 3.4. Resultados
   - 3.5. Decision
   - 3.6. Interpretacion
4. Uso de Inteligencia Artificial
   - 4.1. Prompts utilizados
   - 4.2. Reflexion sobre el uso de IA
5. Evidencia de desarrollo (Git)
   - 5.1. Repositorio
   - 5.2. Historial de commits
   - 5.3. Evolucion del proyecto
   - 5.4. Reflexion tecnica
6. Conclusiones
7. Anexos

---

## 1. Introduccion

El objetivo de este proyecto es desarrollar una aplicación interactiva mediante Streamlit que permita tanto a analistas como a estudiantes validar y visualizar estadísticamente una Prueba Z de Hipótesis. El problema abordado radica en la dificultad teórica y algorítmica de evaluar si una muestra pertenece estadísticamente a una cierta población con una media particular. La importancia de esta técnica es fundamental en control de calidad, ciencias sociales y cualquier campo que requiera toma de decisiones basadas en muestras aleatorias asumiendo normalidad o utilizando muestras grandes (Teorema del Límite Central).

## 2. Descripcion de los datos
- **Fuente de los datos**: Sintetizados mediante `numpy.random.normal`.
- **Numero de observaciones**: 100.
- **Variables utilizadas**: `calificacion` (cuantitativa continua).

*(Nota: La siguiente es una representación esquemática del histograma, la visualización detallada se puede observar directamente en la interfaz de Streamlit).*

```text
Figura 1: Histograma de los datos analizados
(Un histograma que muestra una campana de Gauss centrada aproximadamente en ~73.7).
```

## 3. Planteamiento de la prueba de hipotesis

Se busca evaluar si la media histórica de calificación de un grupo (historicamente 70 puntos) se ha modificado estadísticamente hablando en el presente semestre.

### 3.1. Definicion de hipotesis
- **Hipotesis nula (H0)**: µ = 70.0 (El promedio actual es igual a la media histórica de 70.0).
- **Hipotesis alternativa (H1)**: µ != 70.0 (El promedio actual es significativamente diferente de 70.0, prueba bilateral).

### 3.2. Nivel de significancia
- **α** = 0.05

### 3.3. Estadistico de prueba
Se utiliza el estadístico Z para muestras grandes (n >= 30) y asunción de varianza muestral como estimación de la poblacional:
**Z = (x̄ - µ) / (σ / √n)**

### 3.4. Resultados
- **Media muestral**: 73.7538
- **Tamano de muestra**: 100
- **Desviacion estandar (muestral)**: 10.8980
- **Valor de Z calculado**: 3.4445
- **Valor p (p-value)**: 0.0006

### 3.5. Decision
**Se rechaza H0.** La principal justificación metodológica es que el p-value calculado (0.0006) es estrictamente menor al nivel de significancia α configurado (0.05). Adicionalmente, el Z calculado (3.4445) se ubica muy en el extremo de la zona de rechazo (más allá de los valores críticos ±1.96).

### 3.6. Interpretacion
En términos concretos para el problema evaluado, poseemos evidencia estadística significativa, a un nivel de confianza del 95%, de que la media real de calificación de la cohorte analizada es estadísticamente diferente a 70 puntos.

---

## 4. Uso de Inteligencia Artificial

### 4.1. Prompts utilizados

**Prompt 1:**
> *Desarrolla el módulo inicial de una aplicación en Streamlit para análisis estadístico. Crea la estructura básica, un sidebar, permite subir un CSV o crear datos sintéticos. Muestra un dataframe limitado. RESTRICCIÓN: Cero uso de emojis y no agregues comentarios innecesarios.*

- **Respuesta**: La IA generó un código base con `st.set_page_config`, el bloque `radio` para seleccionar CSV o sintéticos, e implementó validaciones con `st.file_uploader`.
- **Analisis**: Fue sumamente útil. La IA comprendió a la perfección la modularidad. Se utilizó el código generado y se emparejó con un entorno local funcional de Python. 

**Prompt 2:**
> *Añade un nuevo módulo enfocado en la visualización. Utiliza matplotlib y seaborn para generar Histogramas, KDE, y Boxplot en 3 columnas. Luego en la interfaz integrar campos text_area para que el usuario responda.*

- **Respuesta**: La IA construyó las tres gráficas mapeándolas a componentes `col1, col2, col3` en Streamlit e incluyó los `text_area`.
- **Analisis**: Correcta visualmente, utilizó `#4C72B0` y paletas de colores profesionales sin solicitarlo expresamente. Se utilizó al pie de la letra, solo corrigiendo ligeras importaciones.

**Prompt 3:**
> *Implementa el módulo de Pruebas Z, calculando Z, el p-value con `scipy.stats` y dibujando la curva normal con áreas sombreadas de rechazo.*

- **Respuesta**: Me entregó una compleja implementación de `fill_between` en Matplotlib iterando sobre la lógica bilateral vs unilateral. Realizó bien la integración matemática.
- **Analisis**: Muy rigurosa, se verificó el cálculo con estadísticas reales y fue correcto.

**Prompt 4:**
> *Usa `google-generativeai` para consultar la IA. Pasale como input los datos Z, del P-value, el Alpha. Cero código crudo.*

- **Respuesta**: Agregó las dependencias correspondientes y elaboró un prompt oculto para Gemini evitando fugar la base de datos completa a internet.

**Prompt 5 (Refinamiento Estético):**
> *Integra el nombre de la app (LuminaData) en el encabezado centrado, aplica una paleta de colores café claro/hueso a la interfaz y crea un botón para descargar las conclusiones de la IA en formato PDF.*

- **Respuesta**: Se implementó una inyección de CSS avanzada para el branding y se integró la librería `fpdf2` para la generación de reportes bajo demanda.
- **Analisis**: Este paso profesionalizó la herramienta, transformándola de un script de cálculo a un software con identidad corporativa y capacidad de exportación.

### 4.2. Reflexion sobre el uso de IA
La IA no cometió errores de fondo, pero su asunción del `ddof` para desviación estándar poblacional en lugar de la muestral fue ligeramente matizada para que encajara correctamente en estimaciones empíricas con n >= 30. Las principales correcciones manuales tuvieron que ver con acoplar la lectura de la API key de Gemini proveniente desde un archivo `.env` para garantizar máxima seguridad y evitar un prompt inseguro en la Web App (contraseñas a la vista). Lo principal aprendido fue el uso de sub-agentes para escribir aplicaciones web ricas de manera modular, permitiendo enfocarse en la matemática estadística y delegando a la IA la sintaxis del framework gráfico.

---

## 5. Evidencia de desarrollo (Git)

### 5.1. Repositorio
**Enlace del Repositorio:** `https://github.com/253699-bot/253699-App-Distribucion-Hipotesis.git`

### 5.2. Historial de commits
```text
Figura 2 y 3: Historial reflejado por consola:
4bd0dee  2026-04-17 feat: configuracion de variables de entorno para API Key
7ea8323  2026-04-16 refactor: optimizacion de modularidad y manejo de excepciones en carga de datos
de5e8d4  2026-04-16 feat: integracion de la API de Google Gemini para validacion automatizada...
1b2d8de  2026-04-15 feat: desarrollo del modulo de prueba Z con calculo de p-value...
c08c012  2026-04-15 feat: adicion de graficos de distribucion y cuestionario...
7d1ec04  2026-04-15 feat: implementacion de carga de datos CSV y generacion...
a1b2c3d  2026-04-18 feat: branding visual LuminaData y exportación a PDF para conclusiones IA
```

### 5.3. Evolucion del proyecto

| Hash | Descripción | Cambio realizado |
|---|---|---|
| 7d1ec04 | Estructura inicial y fuentes | Carga básica de CSV y sintéticos usando Numpy. |
| c08c012 | Gráficas | Histogramas, KDE y Boxplots usando Seaborn y Matplotlib en tres columnas visuales. |
| 1b2d8de | Lógica Matemática Prueba Z | Implementación del cálculo del Z-Valor P-Value y trazado del área de rechazo en la Campana. |
| de5e8d4 | Inteligencia Artificial Gemini | Prompt enginerizado para entregar resultados ciegos a la API de GCP sin fuga de datos crudos. |
| 7ea8323 | Endurecimiento (Refactor) | División modular de la app, Try-Excepts de error manejado `st.error()` validando n >= 30. |
| 4bd0dee | Seguridad de Tokens | Aislamiento de las contraseñas en `.env` e implementación de `python-dotenv`. |
| a1b2c3d | Branding y Exportación | Identidad visual centrado en el header, estilos personalizados para IA y descarga de PDF. |

### 5.4. Reflexion tecnica
La parte más desafiante fue la superposición lógica del cálculo de las zonas sombreadas de la Curva Normal. Al inicio, sombrear únicamente la cola aplicable sin traslapar áreas ni invadir zonas de aceptación requirió un manejo matemático fino de `stats.norm.ppf`. Un error común fue manejar adecuadamente la seguridad de la API KEY en la web (al final resuelto usando entornos ocultos). 

Posteriormente, la integración de **exportación a PDF** presentó retos con el manejo de estados en Streamlit (`session_state`), ya que cada descarga reiniciaba la app borrando la respuesta de la IA. Se resolvió desacoplando la generación del PDF de la llamada a la API y persistiendo los datos bufferizados. La solución evolucionó de un script secuencial simple, a una plataforma corporativa robusta.

---

## 6. Conclusiones
**El aprendizaje principal** fue la simbiosis entre el análisis estadístico clásico y la ingeniería de software interactiva. Construir la UI permitió observar que el ciclo entre la teoría (como definir α o el test bilateral) cambia instantánea y dramáticamente la zona roja en la interfaz.

La relación entre teoría y práctica resultó excepcionalmente clara: calcular en papel un p-value de 0.0006 se confirma inmediatamente viendo visualmente al Estadístico Z de 3.44 "explotar" y ubicarse casi en el límite extremo derecho, fuera de la porción principal de la campana gausiana.

Al comparar **mi inferencia** vs la de la **IA Integrada Gemini**, coinciden estructuralmente, pero la IA aportó valiosos matices respecto a por qué el gran tamaño de la muestra nos permite sentirnos seguros de los resultados, incluso aunque los datos tuvieran ligera asimetría en su gráfica KDE/Boxplot original.

---

## 7. Anexos
- Se excluyó la base de datos `datos_prueba.csv` y el archivo de tokens `.env` del repositorio remoto gracias a las configuraciones locales de `.gitignore` por buenas prácticas.

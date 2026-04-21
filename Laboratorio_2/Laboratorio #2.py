# Databricks notebook source
# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #Laboratorio #2

# COMMAND ----------

# MAGIC %md
# MAGIC Las Librerías que se utilizan son:
# MAGIC - Matplotlib: el abuelo, es la librería más antigua y robusta, casi todas las demas se contruyeron conesto
# MAGIC - Seaborn: Está hecha específicamente para que los gráficos estadísticos se vean bonitos con poco esfuerzo
# MAGIC - Ploty: Genera gráficos interactivos, hacer zoom y filtrar datos
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##Ejercicio #1

# COMMAND ----------

import pandas as pd
import requests
import io

url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"

try:
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    
    print("--- Análisis de Tipos de Datos ---")
    print(df.info())
    
    print("\n--- Análisis de Variables Cuantitativas (Numéricas) ---")
    df_guate = df[df['Country Name'] == 'Guatemala']
    print(df_guate['Value'].describe())
    
    print("\n--- Análisis de Variables Cualitativas (Categorías) ---")
    print(df['Country Code'].value_counts().head(10))

except Exception as e:
    print(f"Error al procesar: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC **¿Cómo se relaciona este análisis con las metodologías vistas en clase (DLM, DL,CRISP-DM)?**

# COMMAND ----------

# MAGIC %md
# MAGIC CRISP-DM: Se ubica en la fase de Comprensión de Datos. Aquí es donde verificas si los datos "hacen sentido" antes de intentar crear un modelo o una gráfica. Por ejemplo, si el GDP tuviera valores negativos, lo detectarías aquí.
# MAGIC
# MAGIC DLM (Data Lifecycle Management): Se relaciona con la Verificación y Limpieza. Al revisar los tipos de datos (df.info()), aseguras que el ciclo de vida del dato sea correcto desde su ingreso al sistema.
# MAGIC
# MAGIC DL (Data Literacy): Es la capacidad de interpretar los resultados. No solo es correr el código, sino entender que si la media del GDP es alta, pero la desviación estándar también, hay mucha desigualdad o cambios bruscos en el tiempo.

# COMMAND ----------

# MAGIC %md
# MAGIC #Ejercicio #2

# COMMAND ----------

import matplotlib.pyplot as plt
import seaborn as sns

paises = ['Guatemala', 'El Salvador', 'Honduras', 'Nicaragua', 'Costa Rica']
df_ca = df[df['Country Name'].isin(paises)]

plt.figure(figsize=(10, 5))
sns.scatterplot(data=df_ca, x='Year', y='Value', hue='Country Name')
plt.title('Relación Año vs GDP (Centroamérica)')
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(data=df_ca, x='Country Name', y='Value')
plt.title('GDP Promedio por País')
plt.show()

plt.figure(figsize=(10, 5))
sns.histplot(df_ca['Value'], bins=20, kde=True)
plt.title('Distribución de los valores de GDP')
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC **¿Cómo se podría identificar el tipo de gráfico ideal para presentar información de un dataset?**

# COMMAND ----------

# MAGIC %md
# MAGIC Relación: Si quieres ver cómo una variable afecta a otra (ej. ¿A más años, más GDP?), usa Dispersión (Scatter Plot).
# MAGIC
# MAGIC Comparación: Si quieres ver quién tiene más o menos de algo (ej. ¿Qué país tiene más presupuesto?), usa Barras (Bar Plot).
# MAGIC
# MAGIC Distribución: Si quieres ver en qué rangos se agrupan tus datos (ej. ¿La mayoría de los salarios son bajos o altos?), usa un Histograma.
# MAGIC
# MAGIC Evolución: Si quieres ver cambios a través del tiempo, usa un Gráfico de Líneas.

# COMMAND ----------

# MAGIC %md
# MAGIC #Ejercicio #3
# MAGIC

# COMMAND ----------

import matplotlib.pyplot as plt
import seaborn as sns

# 1. Análisis de Variable Cuantitativa (GDP de Guatemala)
df_guate = df[df['Country Name'] == 'Guatemala']

print("--- Estadística Cuantitativa (GDP Guatemala) ---")
print(df_guate['Value'].describe())

# Gráfico: Histograma para ver la distribución de la riqueza en el tiempo
plt.figure(figsize=(8, 4))
sns.histplot(df_guate['Value'], kde=True, color='skyblue')
plt.title('Distribución Histórica del GDP en Guatemala')
plt.xlabel('Valor (USD)')
plt.show()

# 2. Análisis de Variable Cualitativa (Comparación Regional)
paises_ca = ['Guatemala', 'El Salvador', 'Honduras', 'Nicaragua', 'Costa Rica']
df_ca = df[df['Country Name'].isin(paises_ca)]

print("\n--- Estadística Cualitativa (Frecuencia por País) ---")
# Mostramos cuántos años de registros tenemos por país
print(df_ca['Country Name'].value_counts())

# Gráfico: Barras para comparar el GDP promedio por país
plt.figure(figsize=(10, 5))
sns.barplot(data=df_ca, x='Country Name', y='Value', palette='viridis')
plt.title('Comparativa de GDP Promedio en Centroamérica')
plt.ylabel('GDP Promedio (USD)')
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC **¿Tendría sentido incluir un Análisis Exploratorio de Datos en un pipeline de datos?**

# COMMAND ----------

# MAGIC %md
# MAGIC Sí, tendría muchisimo sentido. En la ingeniería de datos moderna, incluir un "paso de EDA" automatizado (a menudo llamado Data Profiling) dentro de un pipeline es fundamental por las siguientes razones:
# MAGIC
# MAGIC Detección de Anomalías: Si el pipeline recibe datos nuevos, un mini-EDA puede detectar automáticamente si hay valores nulos inesperados o si los números están fuera de rango (ej. un GDP negativo) antes de que lleguen a la base de datos final.
# MAGIC
# MAGIC Calidad del Dato (Data Quality): Permite generar alertas. Si la distribución de los datos cambia drásticamente (Data Drift), el pipeline puede detenerse para evitar que los modelos de Inteligencia Artificial aprendan de datos erróneos.
# MAGIC
# MAGIC Documentación Automática: Generar gráficos y estadísticas en cada ejecución del pipeline ayuda a los científicos de datos a entender cómo evolucionan los datos sin tener que hacer el análisis manualmente cada vez.

# COMMAND ----------

# MAGIC %md
# MAGIC #Ejercicio #4

# COMMAND ----------

# MAGIC %md
# MAGIC Ver permisos, tamaño, dueño y fecha de modificación:
# MAGIC ls -l gdp.csv
# MAGIC
# MAGIC Ver el tipo de codificación del archivo:
# MAGIC file gdp.csv
# MAGIC
# MAGIC Ver las primeras 5 líneas para entender la estructura (metadatos implícitos):
# MAGIC head -n 5 gdp.csv

# COMMAND ----------

#En Python
import pandas as pd
import platform

# Metadata del paquete
print(f"Versión de Pandas: {pd.__version__}")

# Metadata del sistema (Sistema operativo, procesador)
print(f"Sistema Operativo: {platform.system()}")
print(f"Versión del OS: {platform.release()}")

# Metadata del Dataset (vía Pandas)
# Esto nos da el uso de memoria y tipos de almacenamiento
print("\nMetadata del DataFrame:")
df.info()

# COMMAND ----------

# MAGIC %md
# MAGIC **¿Cómo beneficiaría un buen manejo de metadata a un pipeline de datos?**

# COMMAND ----------

# MAGIC %md
# MAGIC Un pipeline sin metadata es como una fábrica a oscuras. El buen manejo beneficia en:
# MAGIC
# MAGIC Linaje de Datos (Data Lineage): Permite saber exactamente de dónde vino un dato, qué transformaciones sufrió y quién es el responsable. Si un número sale mal al final del pipeline, la metadata te ayuda a rastrear el error hacia atrás.
# MAGIC
# MAGIC Reproducibilidad: Si guardas la metadata de las versiones de los paquetes (ej. Pandas 2.1), te aseguras de que el pipeline corra igual hoy y en dos años, evitando el famoso "en mi computadora sí funcionaba".
# MAGIC
# MAGIC Auditoría y Seguridad: La metadata registra quién accedió a los datos y cuándo. En industrias reguladas (banca, salud), esto es obligatorio por ley.
# MAGIC
# MAGIC Eficiencia: El pipeline puede leer la metadata del archivo (tamaño) antes de procesarlo. Si el archivo es demasiado grande o está vacío, el pipeline puede decidir no ejecutar el proceso, ahorrando tiempo y costos de nube.

# COMMAND ----------

# MAGIC %md
# MAGIC #Ejercicio #5
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Repositorio en Github:
# MAGIC https://github.com/Dhidel/Introducci-n_a_datos_2026/tree/main

# COMMAND ----------

# MAGIC %md
# MAGIC Github pages: (Por el momento básica pues falta hacer cambios): https://dhidel.github.io/Introducci-n_a_datos_2026/

# COMMAND ----------

# MAGIC %md
# MAGIC **¿Cuál sería el archivo ideal para mostrar los proyectos en una página de Portafolio?**

# COMMAND ----------

# MAGIC %md
# MAGIC El archivo Readme sería el ideal pues es lo primero que se ve al ingresar en Github Pages

# COMMAND ----------

# MAGIC %md
# MAGIC #Resumen y conclusión

# COMMAND ----------

# MAGIC %md
# MAGIC ¡Buenísimo! Has armado un flujo de trabajo súper completo, desde la obtención de datos crudos hasta el despliegue de resultados. Aquí tienes el resumen ejecutivo y la conclusión de lo que logramos hoy, perfecto para documentar tu proyecto en la UFM:
# MAGIC
# MAGIC ###Resumen del Proyecto:
# MAGIC 1. Análisis de Datos (EDA)
# MAGIC Implementamos un Análisis Exploratorio de Datos robusto usando pandas.
# MAGIC
# MAGIC Identificación: Revisamos tipos de datos (df.info()) y valores nulos para asegurar la integridad del dataset.
# MAGIC
# MAGIC Cuantificación: Analizamos el GDP mediante estadísticas descriptivas (describe()), enfocándonos en el caso de Guatemala.
# MAGIC
# MAGIC Cualitativa: Usamos frecuencias y conteos para entender la distribución por países.
# MAGIC
# MAGIC 2. Visualización Estratégica
# MAGIC Transformamos los números en información visual usando matplotlib y seaborn:
# MAGIC
# MAGIC Dispersión: Para observar la evolución del GDP a través de los años.
# MAGIC
# MAGIC Barras: Para comparar el desempeño económico entre países de la región.
# MAGIC
# MAGIC Histogramas: Para entender la distribución de los valores de riqueza.
# MAGIC
# MAGIC 3. Ingeniería de Datos y Trazabilidad
# MAGIC Metadata: Aprendimos que manejar metadatos (vía terminal o Python) es vital para que un pipeline sea escalable y seguro.
# MAGIC
# MAGIC Serialización: Usamos pickle para guardar estados de objetos, permitiendo "congelar" el progreso de un análisis complejo.
# MAGIC
# MAGIC 4. Despliegue y Portafolio
# MAGIC GitHub Pages: Activamos el hosting para convertir tu repositorio en una página web viva.
# MAGIC
# MAGIC Databricks: Centralizamos la documentación de tus avances, integrando links de Git y recursos multimedia.
# MAGIC
# MAGIC ## Conclusión
# MAGIC La principal conclusión de este ejercicio es que la ciencia de datos no ocurre en el vacío. No basta con escribir un código que funcione; la verdadera eficiencia reside en seguir metodologías estructuradas como CRISP-DM.
# MAGIC
# MAGIC El proceso de hoy demuestra que:
# MAGIC
# MAGIC El EDA es el "filtro de calidad" indispensable en cualquier pipeline automatizado.
# MAGIC
# MAGIC La Visualización correcta reduce la complejidad, permitiendo que cualquier stakeholder entienda tendencias económicas complejas en segundos.
# MAGIC
# MAGIC El uso de Portafolios (GitHub/Pages) es la herramienta definitiva para un Ingeniero en Sistemas, ya que permite que tu código hable por ti, mostrando no solo qué hiciste, sino cómo lo documentaste y desplegaste.
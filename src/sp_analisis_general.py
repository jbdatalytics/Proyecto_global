import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def analisis_descriptivo(df):
    """
    Realiza un análisis descriptivo del DataFrame, mostrando un resumen estadístico y distribuciones de ventas, beneficios y cantidad.

    - Muestra el resumen estadístico de las columnas numéricas.
    - Genera histogramas para visualizar la distribución de las columnas "Sales", "Profit" y "Quantity".

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas "Sales", "Profit" y "Quantity" para realizar el análisis y las visualizaciones.

    Retorno:
    None (muestra el resumen y los gráficos directamente).
    """
    
    resumen = df.describe()
    print("\nResumen Estadístico:\n", resumen)
    
    # Ver distribución de ventas, beneficios y cantidad
    numeric_cols = ['Sales', 'Profit', 'Quantity']
    df[numeric_cols].hist(bins=50, figsize=(12, 6))
    plt.suptitle("Distribución de Ventas, Beneficios y Cantidad")
    plt.show()
    

def impacto_descuento(df):
    """
    Analiza la relación entre el descuento y la rentabilidad utilizando un gráfico de dispersión con línea de tendencia.

    - Utiliza un gráfico de dispersión para mostrar la relación entre el descuento aplicado y la rentabilidad (Profit).
    - Añade una línea de tendencia para visualizar la correlación.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas "Discount" y "Profit" para realizar la visualización.

    Retorno:
    None (muestra el gráfico directamente).
    """

    plt.figure(figsize=(8, 5))

    # Gráfico de dispersión con línea de tendencia
    sns.regplot(x=df["Discount"], y=df["Profit"], scatter_kws={"alpha": 0.6}, line_kws={"color": "red"})

    plt.title("Relación entre Descuento y Rentabilidad", fontsize=14)
    plt.xlabel("Descuento", fontsize=12)
    plt.ylabel("Rentabilidad (Profit)", fontsize=12)
    plt.show()


def evolucion_ventas(df):
    """
    Analiza la evolución de las ventas a lo largo del tiempo, mostrando la suma de ventas por mes.

    - Convierte la columna "Order_Date" a formato datetime.
    - Agrupa los datos por mes y calcula la suma de las ventas para cada mes.
    - Genera un gráfico de línea que muestra cómo evolucionaron las ventas mes a mes.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas "Order_Date" y "Sales" para realizar el análisis.

    Retorno:
    None (muestra el gráfico directamente).
    """
   
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    ventas_por_mes = df.groupby(df['Order_Date'].dt.to_period('M'))['Sales'].sum()
    
    plt.figure(figsize=(8, 5))
    ventas_por_mes.plot()
    plt.title("Evolución de Ventas por Mes", fontsize=14)
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Ventas", fontsize=12)
    plt.show()
    

def relacion_pib_ventas(df):
    """
    Analiza la relación entre el PIB per cápita y las ventas utilizando un gráfico de dispersión y una línea de tendencia.

    - Crea un gráfico de dispersión donde el tamaño de los puntos representa las ventas y el color se utiliza para diferenciar los mercados.
    - Añade una línea de tendencia con el gráfico de dispersión para mostrar la relación entre las variables.
    - Utiliza un gráfico de dispersión para visualizar cómo el crecimiento del PIB está relacionado con las ventas totales.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas "GDP_Growth(%)", "Sales" y "Market" para realizar el análisis.

    Retorno:
    None (muestra el gráfico directamente).
    """
   
    plt.figure(figsize=(8, 5))

    # Gráfico de dispersión con línea de tendencia
    ax = sns.scatterplot(x=df["GDP_Growth(%)"], y=df["Sales"], hue=df["Market"], size=df["Sales"], palette="coolwarm", legend=True, sizes=(20, 200))
    sns.regplot(x=df["GDP_Growth(%)"], y=df["Sales"], scatter=False, color="black", line_kws={"linestyle": "dashed"})  

    plt.title("Relación entre PIB per cápita y Ventas", fontsize=14)
    plt.xlabel("PIB per cápita (%)", fontsize=12)
    plt.ylabel("Ventas Totales", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


def impacto_inflacion(df):
    """
    Analiza el impacto de la inflación en los márgenes de beneficio utilizando un gráfico de dispersión y una línea de tendencia.

    - Crea un gráfico de dispersión que muestra la relación entre la inflación y el beneficio (Profit).
    - Añade una línea de tendencia (regresión lineal) para observar cómo la inflación afecta a los márgenes de beneficio.

    Parámetros:
    df (pd.DataFrame): DataFrame que debe contener las columnas "Inflation(%)" y "Profit" para realizar el análisis.

    Retorno:
    None (muestra el gráfico directamente).
    """

    plt.figure(figsize=(8, 5))

    # Gráfico de dispersión
    sns.scatterplot(data=df, x="Inflation(%)", y="Profit", alpha=0.6)

    # Línea de tendencia
    sns.regplot(data=df, x="Inflation(%)", y="Profit", scatter=False, color='red')

    # Personalización del gráfico
    plt.title("Impacto de la Inflación en los Márgenes de Beneficio")
    plt.xlabel("Inflación (%)")
    plt.ylabel("Profit")
    plt.grid(True)
    plt.show()


def correlaciones_heatmap(df):
    """
    Crea un mapa de calor (heatmap) para visualizar las correlaciones entre las variables numéricas del DataFrame.

    - Filtra las columnas numéricas del DataFrame.
    - Calcula la matriz de correlación entre las variables numéricas.
    - Muestra la matriz de correlación como un mapa de calor, donde cada valor se representa con una escala de colores.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las variables numéricas para calcular las correlaciones.

    Retorno:
    None (muestra el gráfico del heatmap directamente).
    """
    
    numeric_df = df.select_dtypes(include=['number'])  # Filtrar solo numéricas
    plt.figure(figsize=(10, 5))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Matriz de Correlación")
    plt.show()


def distribucion_prioridad_envio(df):
    """
    Visualiza la distribución de las columnas de prioridad de pedido y modo de envío en el DataFrame.

    - Muestra dos histogramas con la distribución de las columnas 'Order_Priority' y 'Ship_Mode'.
    - Se incluye un gráfico de densidad (KDE) para ver la distribución suavizada de los datos.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas 'Order_Priority' y 'Ship_Mode' para analizar la distribución.

    Retorno:
    None (muestra los gráficos de distribución).
    """

    exp_cols = ['Order_Priority', 'Ship_Mode']
    
    plt.figure(figsize=(10, 5))
    
    for i, column in enumerate(exp_cols):
        plt.subplot(1, 2, i + 1)
        sns.histplot(data=df, x=column, kde=True, bins=30)
        plt.title(f'Distribución de {column}')
        plt.xticks(rotation=45)
        plt.tight_layout()
    plt.show()


def eficiencia_metodos_envio(df):
    """
    Calcula y visualiza la eficiencia de los diferentes métodos de envío, en términos de:
    - Tiempo de entrega promedio.
    - Coste de envío promedio.
    - Rentabilidad promedio por método de envío.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas 'Order_Date', 'Ship_Date', 'Shipping_Cost', 'Profit' y 'Ship_Mode'.

    Retorno:
    None (muestra los gráficos de barras con la información calculada).
    """
    
    # Asegurar que las fechas son de tipo datetime
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])
    
    # Calcular días de entrega
    df['Delivery_Time'] = (df['Ship_Date'] - df['Order_Date']).dt.days

    # Agrupar por método de envío
    envio_stats = df.groupby("Ship_Mode").agg(
        Avg_Delivery_Time=('Delivery_Time', 'mean'),
        Avg_Shipping_Cost=('Shipping_Cost', 'mean'),
        Avg_Profit=('Profit', 'mean')
    ).reset_index()

    # Visualización
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    sns.barplot(x='Ship_Mode', y='Avg_Delivery_Time', data=envio_stats, ax=axes[0])
    axes[0].set_title("Tiempo medio de entrega")

    sns.barplot(x='Ship_Mode', y='Avg_Shipping_Cost', data=envio_stats, ax=axes[1])
    axes[1].set_title("Coste medio de envío")

    sns.barplot(x='Ship_Mode', y='Avg_Profit', data=envio_stats, ax=axes[2])
    axes[2].set_title("Rentabilidad por método de envío")

    plt.show()


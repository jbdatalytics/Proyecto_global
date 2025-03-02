
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import math


def subplot_col_cat(df, top_n=10):
    """
    Genera subgráficos para mostrar la distribución de las columnas categóricas de un DataFrame.

    - Selecciona las columnas categóricas y muestra un gráfico de barras para las categorías más frecuentes.
    - Para cada columna, muestra un gráfico de barras con los `top_n` valores más frecuentes.

    Parámetros:
    df (pd.DataFrame): DataFrame con las columnas categóricas.
    top_n (int, opcional): Número de categorías principales a mostrar en cada gráfico (por defecto 10).

    Retorno:
    None (muestra los gráficos directamente).
    """
    # seleccionar columnas categóricas
    categorical_cols = df.select_dtypes(include=['object']).columns

    if len(categorical_cols) == 0:
        print('No hay columnas categóricas en el dataframe')
        return

    # configurar el tamaño de la figura  
    num_cols = len(categorical_cols)
    rows = math.ceil(num_cols / 3)
    fig, axes = plt.subplots(rows, 3, figsize=(15, rows * 5))
    axes = axes.flatten()

    # generar gráficos para cada columna categórica 
    for i, col in enumerate(categorical_cols):
        top_categories = df[col].value_counts().nlargest(top_n).index
        filtered_df = df[df[col].isin(top_categories)]

        sns.countplot(data=filtered_df, x=col, ax=axes[i], hue=col, palette='tab10', legend=False)
        axes[i].set_title(f'Distribución de {col} (Top {top_n})')
        axes[i].tick_params(axis='x', rotation=45)

    # eliminar ejes sobrantes si hay menos columnas que subplots
    for j in range(i+1, len(axes)):
        fig.delaxes(axes[j])

    # ajustar diseño
    plt.tight_layout()
    plt.show()


def subplot_col_num(df,col):
    """
    Genera un conjunto de gráficos (histograma y boxplot) para las columnas numéricas especificadas.

    - Para cada columna numérica, muestra un histograma con la distribución de los datos y un boxplot para detectar posibles outliers.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas numéricas a analizar.
    col (list): Lista de nombres de columnas numéricas para las que se generarán los gráficos.

    Retorno:
    None (muestra los gráficos directamente).
    """

# Creo una sola paleta de gráficos de histogramas y boxplot 
    num_graphs=len(col)
    rows= math.ceil(num_graphs / 2) 
    fig, axes= plt.subplots(num_graphs, 2, figsize=(15, rows * 5))     

    for i, col in enumerate(col):
        sns.histplot(data=df, x=col, ax=axes[i,0], bins=200)
        axes[i,0].set_title(f'Distribución de {col}')

        sns.boxplot(data=df, x=col, ax=axes[i,1])
        axes[i,1].set_title(f'Boxplot de {col}')

    for j in range(i+1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def boxplot_con_nulos(df):
    """
    Crea un gráfico de boxplot para las columnas numéricas de un DataFrame e incluye el porcentaje de valores nulos.

    - Para cada columna numérica, genera un boxplot y muestra el porcentaje de valores nulos encima del gráfico correspondiente.

    Parámetros:
    df (pd.DataFrame): DataFrame con las columnas numéricas a analizar.

    Retorno:
    None (muestra el gráfico directamente).
    """
   
    # Seleccionar solo columnas numéricas
    numeric_cols = df.select_dtypes(include=['number']).columns

    if len(numeric_cols) == 0:
        print("No hay columnas numéricas en el DataFrame.")
        return

    # Calcular porcentaje de valores nulos
    null_percentage = df[numeric_cols].isnull().mean() * 100

    # Crear el gráfico de boxplot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df[numeric_cols], ax=ax)

    # Configurar los ticks de los ejes
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha="right")
    ax.set_ylim(0, 1000)

    # Agregar el porcentaje de nulos sobre cada boxplot
    for i, col in enumerate(numeric_cols):
        max_value = min(df[col].dropna().max(), 1000)
        ax.text(i, max_value, f'{null_percentage[col]:.2f}%', 
                ha='center', va='bottom', fontsize=10, color='red')

    plt.title("Boxplot con porcentaje de valores nulos")
    plt.show()


def categorias_mas_vendidas(df):
    """
    Crea visualizaciones de las categorías y subcategorías más vendidas en función de las ventas.

    - Genera un gráfico de pastel para mostrar la distribución de ventas por categorías.
    - Genera un gráfico de barras horizontales para mostrar las subcategorías más vendidas.

    Parámetros:
    df (pd.DataFrame): DataFrame con las columnas "Category", "Sub_Category" y "Sales" para realizar el análisis.

    Retorno:
    None (muestra los gráficos directamente).
    """
   
    # Agrupar datos por categorías y subcategorías
    ventas_categoria = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    ventas_subcategoria = df.groupby("Sub_Category")["Sales"].sum().sort_values(ascending=False)

    # Crear la figura y los subgráficos en una fila
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico de pastel de categorías más vendidas
    axes[0].pie(ventas_categoria.values, labels=ventas_categoria.index, autopct='%1.1f%%', colors=sns.color_palette("Blues_r", len(ventas_categoria)))
    axes[0].set_title("Categorías más vendidas", fontsize=14)

    # Gráfico de barras horizontales de subcategorías más vendidas
    sns.barplot(y=ventas_subcategoria.index, x=ventas_subcategoria.values, ax=axes[1], hue=ventas_subcategoria.index, palette="mako", legend=False)
    axes[1].set_title("Subcategorías más vendidas", fontsize=14)
    axes[1].set_xlabel("Ventas", fontsize=12)
    axes[1].set_ylabel("Subcategoría", fontsize=12)

    plt.tight_layout()
    plt.show()


def mercados_rentabilidad(df):
    """
    Crea un gráfico de barras para mostrar la rentabilidad total por mercado.

    - Agrupa los datos por "Market" y calcula la rentabilidad total (Profit) para cada uno.
    - Genera un gráfico de barras verticales para visualizar la rentabilidad de cada mercado.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas "Market" y "Profit" para realizar el análisis.

    Retorno:
    None (muestra el gráfico directamente).
    """
   
    plt.figure(figsize=(8, 5))

    # Agrupar por Market y sumar el Profit
    market_profit = df.groupby("Market")["Profit"].sum()

    # Crear gráfico de barras verticales
    ax = sns.barplot(x=market_profit.index, y=market_profit.values, palette="plasma", hue=market_profit.index, legend=False)

    plt.title("Rentabilidad por Mercado", fontsize=14)
    plt.xlabel("Mercado", fontsize=12)
    plt.ylabel("Rentabilidad Total (Profit)", fontsize=12)

    plt.xticks(rotation=45, ha="right")  
    plt.show()


def comparativa_mercado_segmento(df):
    """
    Crea una comparativa de ventas y beneficios por mercado y segmento.

    - Genera dos gráficos de barras: uno para comparar las ventas y otro para comparar los beneficios en diferentes mercados y segmentos.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas "Market", "Sales", "Profit" y "Segment" para realizar la comparación.

    Retorno:
    None (muestra los gráficos directamente).
    """

    # Crear subgráficos
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(9, 9))

    # Comparar las ventas en diferentes mercados usando un gráfico de barras
    sns.barplot(ax=axes[0], x='Market', y='Sales', data=df, hue='Segment', palette='pastel')
    axes[0].set_title('Comparación de Ventas por Mercados y Segmentos')

    # Comparar los beneficios en diferentes mercados usando un gráfico de barras
    sns.barplot(ax=axes[1], x='Market', y='Profit', data=df, hue='Segment', palette='dark')
    axes[1].set_title('Comparación de Beneficios por Mercados y Segmentos')

    plt.tight_layout()
    plt.show()


def impacto_variables_beneficio(df):
    """
    Analiza el impacto de las variables "Shipping_Cost", "Discount" y "Sales" sobre el beneficio ("Profit").

    - Genera tres gráficos de dispersión con una línea de regresión para mostrar la relación entre cada variable y el beneficio.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas "Shipping_Cost", "Discount", "Sales" y "Profit" para realizar el análisis.

    Retorno:
    None (muestra los gráficos directamente).
    """
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    variables = ["Shipping_Cost", "Discount", "Sales"]
    titles = ["Profit vs Shipping Cost", "Profit vs Discount", "Profit vs Sales"]

    for i, var in enumerate(variables):
        sns.regplot(data=df, x=var, y="Profit", scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=axes[i])
        axes[i].set_title(titles[i])

    plt.tight_layout()
    plt.show()


def tiempo_envio(df):
    """
    Calcula el tiempo de envío promedio por mercado y lo visualiza en un gráfico de barras.

    - Convierte las fechas de "Order_Date" y "Ship_Date" a formato datetime.
    - Calcula el tiempo de envío en días restando las fechas de pedido y envío.
    - Calcula el tiempo promedio de envío por mercado.
    - Genera un gráfico de barras para mostrar el tiempo promedio de envío por mercado.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas "Order_Date", "Ship_Date" y "Market" para realizar el cálculo.

    Retorno:
    None (muestra el gráfico directamente).
    """
    
    # Convertir fechas a formato datetime si no lo están
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])
    
    # Calcular el tiempo de envío en días
    df['Shipping_Time'] = (df['Ship_Date'] - df['Order_Date']).dt.days
    
    # Calcular el tiempo promedio de envío por mercado
    shipping_avg = df.groupby('Market')['Shipping_Time'].mean().reset_index()
    
    # Visualizar los resultados en un gráfico de barras
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Market', y='Shipping_Time', data=shipping_avg, hue='Market', palette='viridis', legend=False)
    plt.title("Tiempo Promedio de Envío por Mercado")
    plt.xlabel("Mercado")
    plt.ylabel("Días promedio de envío")
    plt.xticks(rotation=45)
    plt.show()


def coste_envio_mercado(df):
    """
    Visualiza el coste de envío por mercado y categoría en un gráfico de barras.

    - Utiliza un gráfico de barras para mostrar la relación entre el coste de envío, el mercado y la categoría.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas "Market", "Shipping_Cost" y "Category" para realizar la visualización.

    Retorno:
    None (muestra el gráfico directamente).
    """
       
    sns.catplot(x="Market", y="Shipping_Cost", data=df, hue="Category", kind="bar", height=5, aspect=1.5)
    
    plt.title("Coste de Envío por Mercado y Categoría", fontsize=14)
    plt.xlabel('Mercado', fontsize=12)
    plt.ylabel('Coste de Envío', fontsize=12)
    plt.show()















import pandas as pd
import numpy as np


def eda_preliminar(df):
    """
    Realiza un análisis exploratorio preliminar de un DataFrame.

    Muestra datos aleatorios de 4 filas, información general del DataFrame, 
    porcentaje de valores nulos por columna, número de filas duplicadas y 
    recuento de valores para las columnas categóricas.

    Parámetros:
    df (pd.DataFrame): DataFrame a analizar.

    Retorno:
    None
    """

    display(df.sample(4))
    
    print('-------------------------------------')

    print('INFO')

    display (df.info()) 

    print('-------------------------------------')

    print('NULOS')

    display (round(df.isnull().sum()/df.shape[0] *100, 2))

    print('-------------------------------------')

    print('DUPLICADOS')

    display (df.duplicated().sum())    

    print('-------------------------------------')

    print('VALUE COUNTS')

    for col in df.select_dtypes (include='O').columns:    
        print (df[col].value_counts())                 
        print('------------------------------------')



def convertir_col(df):
    """
    Convierte columnas específicas de un DataFrame a tipos de datos adecuados.

    - Convierte las columnas de fecha ("Order_Date" y "Ship_Date") a tipo datetime.
    - Convierte columnas económicas a valores numéricos.

    Parámetros:
    df (pd.DataFrame): DataFrame con las columnas a convertir.

    Retorno:
    None 
    """

    # Convertir fechas
    for col in ["Order_Date", "Ship_Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Convertir datos económicos 
    cols_to_convert = ["Inflation(%)", "Exports_GDP(%)", "Imports_GDP(%)", "GDP_Growth(%)"]
    cols_to_convert = [col for col in cols_to_convert if col in df.columns]
    
    if cols_to_convert:
        df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors='coerce')


def calcular_nulos (df):
    """
    Calcula el número y el porcentaje de valores nulos por columna en un DataFrame.

    Parámetros:
    df (pd.DataFrame): DataFrame a analizar.

    Retorno:
    tuple: Dos Series de pandas, la primera con el número de valores nulos por columna 
           y la segunda con el porcentaje de valores nulos por columna.
    """

    numero_nulos= df.isnull().sum()
    porcentaje_nulos= (df.isnull().sum()/df.shape[0]) *100
    return numero_nulos, porcentaje_nulos


def analisis_general_cat(df):
    """
    Realiza un análisis general de las columnas categóricas de un DataFrame.

    - Identifica las columnas categóricas.
    - Muestra la cantidad de valores únicos por columna.
    - Muestra la distribución de los valores en porcentaje.
    - Muestra estadísticas descriptivas de cada columna categórica.

    Parámetros:
    df (pd.DataFrame): DataFrame a analizar.

    Retorno:
    None.
    """

    col_cat=df.select_dtypes(include='O').columns 

    if len (col_cat) == 0:
        print ('No hay columnas categoricas')

    else:
        for col in col_cat:
            print(f'La distribución de la columna {col.upper()}')
            print(f'Esta columna tiene {len(df[col].unique())} valores únicos')
            display(df[col].value_counts(normalize=True))
            print('--------------------\n Describe')
            display(df[col].describe())
            print('--------------------')


def contar_outliers(df):
    """
    Cuenta los outliers en cada columna numérica de un DataFrame usando el método del rango intercuartílico (IQR).

    - Calcula los cuartiles Q1 y Q3 de cada columna numérica.
    - Determina los límites inferior y superior para detectar outliers.
    - Cuenta y muestra el número y porcentaje de outliers por columna.

    Parámetros:
    df (pd.DataFrame): DataFrame a analizar.

    Retorno:
    None (los resultados se muestran y se almacenan en un diccionario).
    """

    numeric_cols = df.select_dtypes(include=['number']).columns
    outlier_counts = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]
        percentage = round(outliers / df.shape[0] * 100, 2)

        outlier_counts[col] = {'count': outliers, 'percentage': percentage}
        print(f'Para la columna {col.upper()} tenemos {outliers} outliers, lo que representa un {percentage}% de los datos.')


def columnas_con_nulos(df, umbral=10):
    """
    Identifica las columnas con valores nulos en un DataFrame y las clasifica según un umbral.

    - Muestra un DataFrame con información sobre las columnas con nulos: nombre, tipo de dato, 
      cantidad de valores nulos y porcentaje de nulos.
    - Clasifica las columnas en dos listas según si el porcentaje de nulos es mayor o menor al umbral.

    Parámetros:
    df (pd.DataFrame): DataFrame a analizar.
    umbral (float, opcional): Porcentaje de nulos a partir del cual una columna se considera de alta 
                               cantidad de nulos (por defecto 10%).

    Retorno:
    tupla: Dos listas, la primera con las columnas que superan el umbral de nulos y 
           la segunda con las que tienen nulos pero están por debajo del umbral.
    """

    columns_with_nulls= df.columns[df.isnull().any()]

    null_columns_info= pd.DataFrame(
        {'Column': columns_with_nulls,
         'Datatype': [df[col].dtype for col in columns_with_nulls],
         'NullCount': [df[col].isnull().sum() for col in columns_with_nulls],
         'Null%': [((df[col].isnull().sum()/ df.shape[0])*100) for col in columns_with_nulls]}
         )

    display(null_columns_info)
    high_null_cols = null_columns_info[null_columns_info['Null%'] > umbral]['Column'].tolist()
    low_null_cols = null_columns_info[null_columns_info['Null%'] <= umbral]['Column'].tolist()

    return high_null_cols, low_null_cols


def ajustar_outliers(df, columnas_a_ajustar):
    """
    Ajusta los outliers de las columnas numéricas especificadas utilizando el método del rango intercuartílico (IQR).

    - Calcula los cuartiles Q1 y Q3 de cada columna.
    - Determina los límites inferior y superior para detectar outliers.
    - Recorta los valores que están fuera de estos límites, reemplazándolos por el valor más cercano dentro del rango permitido.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene las columnas a ajustar.
    columnas_a_ajustar (list): Lista de nombres de columnas numéricas en las que se ajustarán los outliers.

    Retorno:
    None (los valores se modifican directamente en el DataFrame original).
    """
    
    for col in columnas_a_ajustar:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        df[col] = df[col].clip(lower=lower_bound, upper=upper_bound) 


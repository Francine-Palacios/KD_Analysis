
import numpy as np
import pandas as pd
import streamlit as st

def Consideraciones_data():
    info_text = """
    En este análisis, procesaremos los datos mineros utilizando el concepto de 'tubos'. 
    Los 'tubos' se refieren a las muestras extraídas verticalmente desde la superficie hacia abajo 
    en coordenadas específicas (x, y). Estas muestras contienen información valiosa sobre la 
    distribución del mineral a lo largo de la profundidad (z).

    Al entrenar nuestro modelo de Kriging, seguiremos el orden natural en que se obtuvieron los datos, 
    es decir, respetando la secuencia de las muestras en los 'tubos'. Esto es crucial porque la 
    correlación espacial en la minería a menudo se presenta en la dirección vertical, y nuestro 
    modelo debe capturar esta relación para hacer predicciones precisas.


    """
    st.write(info_text)
    return None


def tubos(df, numero_de_tubos):

    df.columns = [column.replace(" ", "_") for column in df.columns]

    i=0
    combined_df = pd.DataFrame()
    combined_dfm = pd.DataFrame()

    while (combined_df.shape)[0]<numero_de_tubos:
        df_tem  = df.sample(n=1)
        # df_tem = df_tem.drop(columns=['id', 'z','blockvalue','destination','process_profit','tonn','CU%'])
        df_tem = df_tem[['x', 'y']]

        df_tem_two = np.array(df_tem)
        A = df_tem_two[0][0]
        B = df_tem_two[0][1]
        df_tem_three = df.query('x == @A and y == @B', inplace=False)
        if (combined_df.shape)[0]<150:
            combined_dfm = pd.concat([combined_dfm, df_tem_three], ignore_index=True)
            combined_dfm = combined_dfm.drop_duplicates()
        combined_df = pd.concat([combined_df, df_tem_three], ignore_index=True)
        combined_df = combined_df.drop_duplicates()
    i=i+1
    return combined_df, combined_dfm
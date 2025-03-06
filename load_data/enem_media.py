import os
import pandas as pd 
import numpy as np


def enem_media():
    caminho_arquivo = os.path.join(
        os.path.dirname(__file__),  # Diretório do arquivo atual
        "..", "data", "ENEM.csv"
    )
    df_enem = pd.read_csv(caminho_arquivo,sep=';')
    notas = ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT','NU_NOTA_REDACAO']
    df_enem['media'] = df_enem[notas].mean(axis=1)
    df_enem_final = df_enem.groupby('NO_MUNICIPIO_PROVA')['media'].mean().reset_index()
    df_enem_final = df_enem_final.rename(columns={'NO_MUNICIPIO_PROVA': 'Cidades','media':'Media_Enem'})
    return df_enem_final

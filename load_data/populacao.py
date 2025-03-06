import os
import pandas as pd


def populacao_df():
    caminho_arquivo = os.path.join(
        os.path.dirname(__file__),  # Diretório do arquivo atual
        "..", "data", "Populacao_2022.xlsx"
    )
    df_populacao = pd.read_excel(caminho_arquivo, header=None)
    df_populacao.columns = ['Cidades', 'populacao']
    df_populacao = df_populacao.reset_index(drop=True)
    return df_populacao

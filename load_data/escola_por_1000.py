import os
import pandas as pd
import numpy as np
from .populacao import populacao_df


def escola_por_1000():
    caminho_arquivo = os.path.join(os.path.dirname(__file__),  # Diretório do arquivo atual
    "..", "data", "escolas.xlsx")
    df_escola = pd.read_excel(caminho_arquivo, header=None)
    df_escola.columns = ['Cidades']
    contagem_cidades = df_escola['Cidades'].value_counts().reset_index()
    contagem_cidades.columns = ['Cidades', 'quantidade']
    df_escola_final = pd.merge(populacao_df(), contagem_cidades, on='Cidades', how='left')
    df_escola_final['taxa_escolas_por_habitante'] = (df_escola_final['quantidade'] / df_escola_final['populacao']) * 1000
    df_escola_final_taxa = df_escola_final[['Cidades', 'taxa_escolas_por_habitante']]
    return df_escola_final_taxa

resultado = escola_por_1000()
print(resultado)
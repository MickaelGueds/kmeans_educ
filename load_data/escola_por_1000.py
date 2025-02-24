import pandas as pd
import numpy as np
from populacao import população_df


def escola_por_1000():
    df_escola = pd.read_excel('../data/escolas.xlsx', header=None)
    df_escola.columns = ['cidade']
    contagem_cidades = df_escola['cidade'].value_counts().reset_index()
    contagem_cidades.columns = ['cidade', 'quantidade']
    df_escola_final = pd.merge(população_df(), contagem_cidades, on='cidade', how='left')
    df_escola_final['taxa_escolas_por_habitante'] = (df_escola_final['quantidade'] / df_escola_final['populacao']) * 1000
    df_escola_final_taxa = df_escola_final[['cidade', 'taxa_escolas_por_habitante']]
    return df_escola_final_taxa

resultado = escola_por_1000()
print(resultado)
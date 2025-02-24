import pandas as pd


def população_df():
    df_populacao = pd.read_excel('../data/Populacao_2022.xlsx', header=None)
    df_populacao.columns = ['cidade', 'populacao']
    df_populacao = df_populacao.reset_index(drop=True)
    return df_populacao

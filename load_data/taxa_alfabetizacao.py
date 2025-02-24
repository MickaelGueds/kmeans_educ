import pandas as pd


def taxa_alfabetizacao():
    df_taxa_alfabetizacao = pd.read_csv(
        '../data/taxa_alfabetizacao.csv',
        sep=';',  # Define o delimitador correto
        skiprows=4,  # Pula as 4 primeiras linhas de metadados
        header=0  # Define a primeira linha de dados como cabeçalho
    )

    df_taxa_alfabetizacao1 = df_taxa_alfabetizacao[df_taxa_alfabetizacao['Município'].str.endswith("(PI)", na=False)]

    return df_taxa_alfabetizacao1


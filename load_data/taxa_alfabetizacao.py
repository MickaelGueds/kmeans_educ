import os
import pandas as pd

def taxa_alfabetizacao():
    caminho_arquivo = os.path.join(
        os.path.dirname(__file__),
        "..", "data", "taxa_alfabetizacao.csv"
    )
    df_taxa_alfabetizacao = pd.read_csv(caminho_arquivo, sep=';', skiprows=4, header=0)
    df_taxa_alfabetizacao1 = df_taxa_alfabetizacao[df_taxa_alfabetizacao['Município'].str.endswith("(PI)", na=False)]
    df_taxa_alfabetizacao1 = df_taxa_alfabetizacao1.rename(columns={'Município': 'Cidades'})
    df_taxa_alfabetizacao1['Cidades'] = df_taxa_alfabetizacao1['Cidades'].str.replace(" \(PI\)$", "", regex=True)
    
    return df_taxa_alfabetizacao1
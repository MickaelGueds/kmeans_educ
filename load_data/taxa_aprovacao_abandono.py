import os
import pandas as pd
import numpy as np


def taxa_aprovacao_abandono():
    caminho_arquivo = os.path.join(
        os.path.dirname(__file__),  # Diretório do arquivo atual
        "..", "data", "taxa_aprovacao_abandono.xlsx"
    )
    df_taxa_aprovação_abandono = pd.read_excel(caminho_arquivo)
    cabecalho = df_taxa_aprovação_abandono.columns
    filtro = (df_taxa_aprovação_abandono['Dependencia'] == 'Pública') & (df_taxa_aprovação_abandono['Localizacao'] == 'Total')
    df_taxa_aprovação_abandono_final = df_taxa_aprovação_abandono[filtro]
    return df_taxa_aprovação_abandono_final


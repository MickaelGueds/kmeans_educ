import os
import pandas as pd
import numpy as np


def taxa_aprovacao_abandono():
    caminho_arquivo = os.path.join(
        os.path.dirname(__file__),  # Diretório do arquivo atual
        "..", "data", "taxa_aprovacao_abandono.xlsx"
    )
    colunas_taxa = [
    "Taxa aprovados fundamental total ",
    "Taxa aprovados total EM",
    "Taxa de abandonos EF",
    "Taxa de abandonos EM"
    ]
    df_taxa_aprovação_abandono = pd.read_excel(caminho_arquivo)
    cabecalho = df_taxa_aprovação_abandono.columns
    filtro = (df_taxa_aprovação_abandono['Dependencia'] == 'Pública') & (df_taxa_aprovação_abandono['Localizacao'] == 'Total')
    df_taxa_aprovação_abandono[colunas_taxa] = df_taxa_aprovação_abandono[colunas_taxa]\
    .applymap(lambda x: str(x).replace(",", ".").strip() if isinstance(x, str) else x)\
    .apply(pd.to_numeric, errors='coerce')  # Converte para float e ignora erros
    df_taxa_aprovação_abandono_final = df_taxa_aprovação_abandono[filtro]
    return df_taxa_aprovação_abandono_final


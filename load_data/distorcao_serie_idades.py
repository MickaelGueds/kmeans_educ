import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

def distorcao():
    df_distorção = pd.read_excel('../data/Distorcao_serie_idade.xlsx')
    df_distorção_filtro = df_distorção[(df_distorção['Localização'] == 'Total') & (df_distorção['Dependência Administrativa'] == 'Total')]
    df_distorção_final = df_distorção_filtro[[' Nome do Município','Total_M','Total_F']]
    df_distorção_final = df_distorção_final.rename(columns={
        'Total_M': 'tx_distorcao_medio',
        'Total_F': 'tx_distorcao_fundamental'
    })
    return df_distorção_final


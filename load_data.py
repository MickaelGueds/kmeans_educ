import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

def load_data():
    df_educacao = pd.read_csv('data/Var_Educa.csv',encoding='latin1')        
    return df_educacao                                                                                                 

colunas = [
    'IDEB fundamental', 
    'Matrículas no ensino fundamental',
    'Matrículas no ensino médio',
    'Docentes no ensino fundamental',
    'Docentes no ensino médio'
]

cols_volume = [
    'Matrículas no ensino fundamental',
    'Matrículas no ensino médio',
    'Docentes no ensino fundamental',
    'Docentes no ensino médio'
]

def tratamento_educacao(df_educacao):
    df_educacao.rename(columns={'IDEB  Anos finais do ensino fundamental (Rede pública)': 'IDEB fundamental'},inplace=True)
    df_educacao.drop(['Gentílico'],axis=1,inplace=True)

    columns_int = ['Matrículas no ensino fundamental', 'Matrículas no ensino médio', 'Docentes no ensino fundamental', 'Docentes no ensino médio', 'População no último censo']
    for coluna in columns_int:
        df_educacao[coluna] = df_educacao[coluna].str.extract(r'(\d+)', expand=False) 
        df_educacao[coluna] = pd.to_numeric(df_educacao[coluna], errors='coerce')

        df_educacao[colunas] = df_educacao[colunas].replace('-', np.nan)
    for coluna in colunas:
        df_educacao[coluna] = pd.to_numeric(df_educacao[coluna], errors='coerce')

    imputer = SimpleImputer(strategy='median')    
    #imputer = SimpleImputer(strategy='average')
    df_educacao[colunas] = imputer.fit_transform(df_educacao[colunas])
    for coluna in cols_volume:
        df_educacao[coluna + '_log'] = np.log1p(df_educacao[coluna])
    cols_volume_log = [c + '_log' for c in cols_volume]

    return df_educacao, cols_volume_log
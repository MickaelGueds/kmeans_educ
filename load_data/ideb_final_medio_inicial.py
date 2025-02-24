import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

df_ideb = pd.read_excel('../data/Ideb final_medio.xlsx')
df_ideb = df_ideb.drop(columns=['Unnamed: 1','Nome do Município'])
df_ideb = df_ideb.rename(columns={
    'IDEB\n2023\nEnsino Medio': 'ideb_ensino_medio',
    'Cidades' : 'Municipios',
    'IDEB\n2023\nAno final' : 'ideb_ano_final',
    'Ideb ano inicial': 'ideb_ano_inicial'
})
colunas_ideb = ['ideb_ano_final','ideb_ensino_medio','ideb_ano_inicial']

df_ideb[colunas_ideb] = df_ideb[colunas_ideb].replace('-', np.nan)
df_ideb[colunas_ideb] = df_ideb[colunas_ideb].apply(pd.to_numeric, errors ='coerce')


df_ideb[colunas_ideb] = df_ideb[colunas_ideb].fillna(df_ideb[colunas_ideb].mean())
df_ideb = df_ideb.drop(index=[0,1,2])

df_ideb = df_ideb.reset_index(drop=True) 

organizar = ['Municipios'] + [col for col in df_ideb.columns if col != 'Municipios']

df_ideb = df_ideb[organizar]
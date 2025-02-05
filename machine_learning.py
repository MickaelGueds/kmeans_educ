import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA

def aprendizado(df_educacao, cols_volume_log):
    scaler = RobustScaler()

    # Escalonar
    ideb_scaled = scaler.fit_transform(df_educacao[['IDEB fundamental']])
    volume_scaled = scaler.fit_transform(df_educacao[cols_volume_log])

    # Agregar as variáveis de volume com PCA (extraindo o primeiro componente)
    pca = PCA(n_components=1)
    volume_index = pca.fit_transform(volume_scaled)

    df_cluster = pd.DataFrame({
        'IDEB_scaled': ideb_scaled.flatten(),
        'Volume_index': volume_index.flatten()
    })
    return df_cluster
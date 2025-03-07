import streamlit as st
import pandas as pd

# Configurar layout wide
st.set_page_config(layout="wide")

# Título da página
st.title("Kmeans de educação")

# CSS para ajustar largura
st.markdown("""
    <style>
    .main .block-container {
        max-width: 90%;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar para navegação e controles
st.sidebar.title("Opções de Visualização")

# Carregando o dataframe
@st.cache_data
def load_data():
    df = pd.read_csv("resultado_clusters.csv")
    return df

df = load_data()

# Seção de características dos clusters
st.subheader("Médias por cluster:")

# Tabela de médias dos clusters - usando container width
cluster_data = {
    "Cluster": [0, 1, 2, 3, 4],
    "IDEB_scaled": [0.516239, 0.141026, -0.028736, 1.111111, -0.626126],
    "Volume_index": [-1.319312, 3.433563, 0.846913, 9.729542, -0.842809]
}
cluster_df = pd.DataFrame(cluster_data)
st.dataframe(cluster_df, use_container_width=True)  # Alteração aqui
# Variáveis utilizadas
st.subheader("Variáveis utilizadas na clusterização:")
st.markdown("""
- **IDEB Escalonado** (qualidade da educação)
- **Índice de Volume** (PCA das matrículas e docentes) (tamanho do sistema educacional)
""")

# Mapa interativo - ajustando width
st.subheader("Mapa de Clusters")
try:
    with open("mapa_interativo.html", "r", encoding="utf-8") as file:
        # Ajuste no componente HTML
        st.components.v1.html(file.read(), height=600, width=1200, scrolling=True)
except FileNotFoundError:
    st.error("Arquivo do mapa não encontrado!")

# Seção de interpretação em duas colunas
col1, col2 = st.columns(2)

with col1:
    # Interpretação dos clusters
    st.subheader("Interpretação:")
    st.markdown("""
    - **Cluster 0:** Desempenho educacional moderado, sistema educacional pequeno
    - **Cluster 1:** Desempenho educacional abaixo da média, sistema educacional grande
    - **Cluster 2:** Desempenho educacional ligeiramente abaixo da média, sistema educacional médio
    """)

with col2:
    st.subheader(" ")  # Espaço vazio para alinhamento
    st.markdown("""
    - **Cluster 3:** Desempenho educacional alto, sistema educacional muito grande
    - **Cluster 4:** Desempenho educacional baixo, sistema educacional pequeno
    """)

# Seção de dados expansível
st.subheader("Dados Educacionais")
st.write("Visualização dos dados utilizados na análise (230 linhas)")
with st.expander("Expandir para ver os dados"):
    st.dataframe(df, use_container_width=True)  # Alteração aqui
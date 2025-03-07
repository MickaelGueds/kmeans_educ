import streamlit as st
import pandas as pd

# -----------------------------------
# 🔹 Carregar Dados
# -----------------------------------
# Dados médios dos clusters
df_media_clusters = pd.read_csv("medias_clusters.csv")

# Dados com diagnóstico
df_clusters = pd.read_csv("diagnostico_clusters_3.csv")

# Dados detalhados de cada cidade e cluster
df_cidades = pd.read_csv("cidades_clusterizadas.csv")

# Mapeamento de nomes baseado em pontos fracos
cluster_nomes = {
    0: "Emergência Educacional",
    1: "Pouca infraestrutura",
    2: "Contradição Educacional"
}

# Adicionar coluna com nomes descritivos
df_clusters["Nome do Cluster"] = df_clusters["Cluster"].map(cluster_nomes)
df_media_clusters["Nome do Cluster"] = df_media_clusters["Cluster"].map(cluster_nomes)

# -----------------------------------
# 🔹 Configuração da Página
# -----------------------------------
st.set_page_config(page_title="Análise Educacional por Clusters", layout="wide")

st.title("📊 Análise Educacional por Clusters")
st.write("Este dashboard apresenta uma análise das condições educacionais dos municípios utilizando a técnica de K-Means.")

# -----------------------------------
# 🔹 Seção 1 - Variáveis Utilizadas
# -----------------------------------
st.header("📌 Variáveis Utilizadas")
st.markdown("""
- **Taxa de Distorção Idade-Série**: Percentual de alunos com idade acima da esperada para a série.
- **Taxa de Escolas por Habitante**: Número de escolas proporcional à população.
- **IDEB (Índice de Desenvolvimento da Educação Básica)**: Mede a qualidade do ensino.
- **Total de Alfabetização**: Percentual da população alfabetizada.
- **Taxa de Abandono Escolar**: Percentual de alunos que deixaram a escola.
""")

# -----------------------------------
# 🔹 Seção 2 - Média dos Clusters
# -----------------------------------
st.header("📊 Médias dos Clusters")
colunas_selecionadas = ["Nome do Cluster"] + list(df_media_clusters.columns[:-1])
st.dataframe(df_media_clusters[colunas_selecionadas])

# -----------------------------------
# 🔹 Seção 3 - Mapa Interativo
# -----------------------------------
st.header("🗺️ Mapa Interativo dos Clusters")
try:
    with open("mapa_interativo.html", "r", encoding="utf-8") as file:
        html_mapa = file.read()
    st.components.v1.html(html_mapa, height=600)
except FileNotFoundError:
    st.error("Arquivo 'mapa_interativo.html' não encontrado. Verifique o caminho e o nome do arquivo.")

# -----------------------------------
# 🔹 Seção 4 - Diagnóstico dos Clusters
# -----------------------------------
st.header("📋 Diagnóstico dos Clusters")
colunas_diagnostico = ["Nome do Cluster", "Pontos Fortes", "Pontos Fracos", "Recomendações"]
st.dataframe(df_clusters[colunas_diagnostico])

# -----------------------------------
# 🔹 Seção 5 - Dados Detalhados (Expansível)
# -----------------------------------
with st.expander("🔍 Ver Dados Completos por Município"):
    df_cidades["Nome do Cluster"] = df_cidades["Cluster"].map(cluster_nomes)
    st.dataframe(df_cidades)
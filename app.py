import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da página
st.set_page_config(page_title="Análise Multidimensional por Clusters", layout="wide")

# Configurações por tipo de análise
CONFIG = {
    "saude": {
        "titulo": "Análise de Saúde Municipal por Clusters",
        "descricao": "Este dashboard apresenta uma análise das condições de saúde dos municípios utilizando a técnica de K-Means.",
        "arquivos": {
            "medias": "output/medias_clusters_saude.csv",
            "diagnostico": "output/diagnostico_clusters_saude.csv",
            "cidades": "output/municipios_clusters_saude.csv",
            "mapa": "output/mapa_clusters_saude.html"
        },
        "colunas_cluster": {
            "df_medias": "cluster",
            "df_diagnostico": "cluster", 
            "df_cidades": "cluster"
        },
        "rotulos_cluster": {
            "0": "Alta Mortalidade Prematura",
            "1": "Baixa Cobertura Vacinal",
            "2": "Excelente Cobertura Vacinal",
            "3": "Alta Mortalidade Infantil"
        },
        "indicadores": """
        - **Mortalidade Prematura**: Taxa de mortalidade prematura (30-69 anos) por DCNT.
        - **Cobertura Vacinal**: Taxa de cobertura da vacina Penta (D3) para crianças menores de 1 ano.
        - **Mortalidade Infantil**: Taxa de mortalidade infantil (≤ 1 ano).
        - **Exames Especializados**: Número de exames especializados realizados.
        """,
        "perfis": """
        Através da análise estatística, identificamos 4 perfis distintos de municípios com base em seus indicadores de saúde:

        1. **Alta Mortalidade Prematura**: Municípios com alta mortalidade prematura (4.19), cobertura vacinal média (99.5%) e baixo acesso a exames especializados (305.95).

        2. **Baixa Cobertura Vacinal**: Municípios com indicadores equilibrados, baixa mortalidade prematura (2.17) e infantil (0.73), e acesso moderado a exames (375.50).

        3. **Excelente Cobertura Vacinal**: Municípios com excelente cobertura vacinal (128.2%) e baixa mortalidade infantil (0.65), mas acesso limitado a exames especializados (322.00).

        4. **Alta Mortalidade Infantil**: Municípios com alto acesso a exames especializados (5391.80) mas altíssima mortalidade infantil (5.95).
        """,
        "colunas_selecionadas": ["Número do Cluster", "Nome do Cluster", "mortalidade_prematura", 
                                "cobertura_penta", "mortalidade_infantil", "exames_especializados"],
        "colunas_diagnostico": ["Número do Cluster", "Perfil", "Pontos Fortes", "Pontos Fracos", "Recomendações"],
        "coluna_busca": "Cidades",
        "cor_grafico": {
            "Alta Mortalidade Prematura": "#d32f2f",
            "Baixa Cobertura Vacinal": "#ffa000",
            "Excelente Cobertura Vacinal": "#388e3c",
            "Alta Mortalidade Infantil": "#7b1fa2"
        },
        "metodologia": """
        ### Processamento dos Dados
        
        1. **Pré-processamento**: 
           - Tratamento de valores ausentes
           - Normalização das variáveis
           - Análise de correlação entre indicadores
        
        2. **Clustering**:
           - Algoritmo K-Means com 4 clusters
           - Número ideal de clusters determinado pelo método do cotovelo e silhueta
           - Visualização por PCA (Análise de Componentes Principais)
        
        3. **Interpretação**:
           - Análise das médias dos indicadores por cluster
           - Diagnóstico de pontos fortes e fracos
           - Elaboração de recomendações específicas por perfil
        """
    },
    "infancia": {
        "titulo": "Análise de Desenvolvimento Infantil Municipal por Clusters",
        "descricao": "Este dashboard apresenta uma análise dos indicadores de desenvolvimento infantil dos municípios utilizando a técnica de K-Means.",
        "arquivos": {
            "medias": "output/medias_clusters_criancas.csv",
            "diagnostico": "output/diagnostico_clusters_criancas.csv",
            "cidades": "output/municipios_clusters_criancas.csv",
            "mapa": "output/mapa_clusters_crianças.html"
        },
        "colunas_cluster": {
            "df_medias": "cluster",
            "df_diagnostico": "cluster", 
            "df_cidades": "cluster"
        },
        "rotulos_cluster": {
            "0": "Alta Mortalidade Infantil",
            "1": "Baixa Cobertura Vacinal",
            "2": "Melhor Alfabetização",
            "3": "Alfabetização Deficiente"
        },
        "indicadores": """
        - **Mortalidade Infantil**: Taxa de mortalidade infantil.
        - **Taxa de Alfabetização**: Percentual da população alfabetizada.
        - **Cobertura Vacinal BCG**: Taxa de cobertura da vacina BCG.
        - **Atendimento Educacional Infantil**: Percentual de crianças atendidas na educação infantil.
        """,
        "perfis": """
        Através da análise estatística, identificamos 4 perfis distintos de municípios com base em seus indicadores de desenvolvimento infantil:

        1. **Alta Mortalidade Infantil**: Municípios com mortalidade infantil alarmante (5.86), taxa de alfabetização baixa (53.64%) e atendimento educacional infantil em situação crítica (60.97%).

        2. **Baixa Cobertura Vacinal**: Municípios com mortalidade infantil baixa (0.66), cobertura vacinal BCG crítica (76.55%) e taxa de alfabetização muito baixa (48.50%).

        3. **Melhor Alfabetização**: Municípios com taxa de alfabetização excelente (87.45%), atendimento educacional infantil elevado (78.87%) e mortalidade infantil muito baixa (0.56).

        4. **Alfabetização Deficiente**: Municípios com cobertura vacinal BCG excelente (110.48%), taxa de alfabetização muito deficiente (52.14%) e mortalidade infantil moderada (1.08).
        """,
        "colunas_selecionadas": ["Número do Cluster", "Nome do Cluster", "Mortalidade Infantil", 
                                "Taxa de Alfabetização", "Cobertura Vacinal BCG", "Atendimento Educacional Infantil"],
        "colunas_diagnostico": ["Número do Cluster", "Perfil", "Pontos Fortes", "Pontos Fracos", "Recomendações"],
        "coluna_busca": "Cidades",
        "cor_grafico": {
            "Alta Mortalidade Infantil": "#d32f2f",
            "Baixa Cobertura Vacinal": "#ffa000",
            "Melhor Alfabetização": "#388e3c",
            "Alfabetização Deficiente": "#7b1fa2"
        },
        "metodologia": """
        ### Processamento dos Dados
        
        1. **Pré-processamento**: 
           - Tratamento de valores ausentes
           - Normalização das variáveis
           - Análise de correlação entre indicadores
        
        2. **Clustering**:
           - Algoritmo K-Means com 4 clusters
           - Número ideal de clusters determinado pelo método do cotovelo e silhueta
           - Visualização por PCA (Análise de Componentes Principais)
        
        3. **Interpretação**:
           - Análise das médias dos indicadores por cluster
           - Diagnóstico de pontos fortes e fracos
           - Elaboração de recomendações específicas por perfil
        """
    },
    "seguranca": {
        "titulo": "Análise de Segurança Municipal por Clusters",
        "descricao": "Este dashboard apresenta uma análise dos indicadores de segurança dos municípios utilizando a técnica de K-Means.",
        "arquivos": {
            "medias": "output/medias_clusters_seguranca.csv",
            "diagnostico": "output/diagnostico_clusters_seguranca.csv",
            "cidades": "output/municipios_clusters_seguranca.csv",
            "mapa": "output/mapa_clusters_seguranca.html"
        },
        "colunas_cluster": {
            "df_medias": "cluster",
            "df_diagnostico": "cluster", 
            "df_cidades": "cluster"
        },
        "rotulos_cluster": {
            "0": "Cluster 1: Baixos Índices Criminais (0.33 hom.) (105 municípios)",
            "1": "Cluster 2: Alto Roubo de Celulares (2.93%) (14 municípios)",
            "2": "Cluster 5: Mortalidade no Trânsito Moderada (1.11) (47 municípios)",
            "3": "Cluster 4: Alto Roubo de Veículos (1.71%) (45 municípios)",
            "4": "Cluster 3: Alta Mortalidade no Trânsito (6.00) (13 municípios)"
        },
        "indicadores": """
        - **Taxa de Homicídio**: Taxa de homicídios por habitante.
        - **Violência Sexual**: Taxa de violência sexual por habitante.
        - **Mortalidade no Trânsito**: Taxa de mortalidade no trânsito por habitante.
        - **Roubo de Veículos**: Taxa de roubo de veículos por habitante.
        - **Roubo de Celulares**: Taxa de roubo de celulares por habitante.
        """,
        "perfis": """
        Através da análise estatística, identificamos 5 perfis distintos de municípios com base em seus indicadores de segurança:

        1. **Baixos Índices Criminais**: Municípios pequenos (6.306 hab) com baixíssima criminalidade: taxa de homicídio (0.33), violência sexual (0.002), baixa mortalidade no trânsito (-0.18) e roubo de veículos (0.17).

        2. **Alto Roubo de Celulares**: Municípios de porte médio (36.463 hab) com alto roubo de celulares (2.93%), taxa de homicídio elevada (1.00), violência sexual alta (0.68), mortalidade no trânsito (2.23) e roubo de veículos (2.59).

        3. **Alta Mortalidade no Trânsito**: Municípios maiores (44.746 hab) com gravíssimos problemas de segurança no trânsito (6.00), alta taxa de homicídio (0.96) e elevado roubo de celulares (2.23).

        4. **Alto Roubo de Veículos**: Municípios pequenos (6.896 hab) com alto índice de roubo de veículos (1.71%), taxa de homicídio significativa (0.84) e violência sexual preocupante (0.22).

        5. **Mortalidade no Trânsito Moderada**: Municípios médios (10.199 hab) com mortalidade no trânsito moderada (1.11), índices de criminalidade mais controlados com taxa de homicídio (0.58) e baixo roubo de celulares (0.12).
        """,
        "colunas_selecionadas": ["Número do Cluster", "Nome do Cluster", "tx_mvi", 
                                "viol_sexual", "mortal_transito", "roubo_veiculos", "roubo_celular", "populacao"],
        "colunas_diagnostico": ["Número do Cluster", "Perfil", "Pontos Fortes", "Pontos Fracos", "Recomendações"],
        "coluna_busca": "Cidades",
        "cor_grafico": {
            "Baixos Índices Criminais": "#388e3c",
            "Alto Roubo de Celulares": "#d32f2f",
            "Alta Mortalidade no Trânsito": "#ffa000",
            "Alto Roubo de Veículos": "#7b1fa2",
            "Mortalidade no Trânsito Moderada": "#1976d2"
        },
        "metodologia": """
        ### Processamento dos Dados
        
        1. **Pré-processamento**: 
           - Tratamento de valores ausentes
           - Normalização das variáveis
           - Análise de correlação entre indicadores
        
        2. **Clustering**:
           - Algoritmo K-Means com 5 clusters
           - Número ideal de clusters determinado pelo método do cotovelo e silhueta
           - Visualização por PCA (Análise de Componentes Principais)
        
        3. **Interpretação**:
           - Análise das médias dos indicadores por cluster
           - Diagnóstico de pontos fortes e fracos
           - Elaboração de recomendações específicas por perfil
        """
    },
    "educacao": {
        "titulo": "Análise Educacional Municipal por Clusters",
        "descricao": "Este dashboard apresenta uma análise das condições educacionais dos municípios utilizando a técnica de K-Means.",
        "arquivos": {
            "medias": "output/medias_clusters_educacao.csv",
            "diagnostico": "output/diagnostico_clusters_educacao.csv",
            "cidades": "output/municipios_clusters_educacao.csv",
            "mapa": "output/mapa_clusters_educacao.html"
        },
        "colunas_cluster": {
            "df_medias": "cluster",
            "df_diagnostico": "cluster", 
            "df_cidades": "cluster"
        },
        "rotulos_cluster": {
            "0": "Baixo Desempenho Educacional",
            "1": "Excelência Educacional",
            "2": "Desempenho Educacional Intermediário"
        },
        "indicadores": """
            - **IDEB Anos Iniciais**: Índice de Desenvolvimento da Educação Básica para os anos iniciais.
            - **IDEB Anos Finais**: Índice de Desenvolvimento da Educação Básica para os anos finais.
            - **SAEPI Português**: Nota média da avaliação padronizada em Língua Portuguesa (2º ano).
            - **SAEPI Matemática**: Nota média da avaliação padronizada em Matemática (2º ano).
            - **Taxa de Evasão Anos Iniciais**: Percentual de alunos que deixaram a escola nos anos iniciais.
            - **Taxa de Evasão Anos Finais**: Percentual de alunos que deixaram a escola nos anos finais.
            - **Taxa de Abandono Anos Iniciais**: Percentual de abandono registrado nos anos iniciais.
            - **Taxa de Abandono Anos Finais**: Percentual de abandono registrado nos anos finais.
            - **SAEPI Média**: Média aritmética entre os resultados de Português e Matemática.
            - **IDEB Média**: Média entre IDEB Anos Iniciais e Finais.
            """,

        "perfis": """
Através da análise estatística, identificamos 3 perfis distintos de municípios com base em seus indicadores educacionais:

1. **Abandono Escolar Crítico**: Municípios com baixo IDEB (AI: 4.61, AF: 4.00), altas taxas de evasão e abandono (Abandono Anos Iniciais: 1.13%, Finais: 3.38%).

2. **Excelência Educacional**: Municípios com desempenho educacional muito alto em todos os indicadores, incluindo IDEB AI (6.15), SAEPI Português (690.37), e baixíssimo abandono.

3. **Desempenho Educacional Intermediário**: Municípios com IDEB médio (AI: 5.15), desempenho SAEPI levemente abaixo da média, e baixas taxas de evasão e abandono.
""",

       "colunas_selecionadas": [
    "Número do Cluster", "Nome do Cluster", 
    "IDEB Anos Iniciais", "IDEB Anos Finais",
    "SAEPI Português", "SAEPI Matemática",
    "Taxa de Evasão Anos Iniciais", "Taxa de Evasão Anos Finais",
    "Taxa de Abandono Anos Iniciais", "Taxa de Abandono Anos Finais",
    "IDEB Média", "SAEPI Média"
],
        "colunas_diagnostico": ["Número do Cluster", "Perfil", "Pontos Fortes", "Pontos Fracos", "Recomendações"],
        "coluna_busca": "Cidades",
        "cor_grafico": {
            "Baixo Desempenho Educacional": "#d32f2f",
            "Excelência Educacional": "#388e3c",
            "Desempenho Educacional Intermediário": "#ffa000"
        },
        "metodologia": """
        ### Processamento dos Dados
        
        1. **Pré-processamento**: 
           - Tratamento de valores ausentes
           - Normalização das variáveis
           - Análise de correlação entre indicadores
        
        2. **Clustering**:
           - Algoritmo K-Means com 3 clusters
           - Número ideal de clusters determinado pelo método do cotovelo e silhueta
           - Visualização por PCA (Análise de Componentes Principais)
        
        3. **Interpretação**:
           - Análise das médias dos indicadores por cluster
           - Diagnóstico de pontos fortes e fracos
           - Elaboração de recomendações específicas por perfil
        """
    }
}

# -----------------------------------
# 🔹 Menu de Navegação
# -----------------------------------
st.sidebar.title("📊 Navegação")
# Usando radio ao invés de selectbox para evitar a edição de texto
#pagina = st.sidebar.radio(
#    "Escolha o tipo de análise:",
#    ["🏠 Página Inicial", "🏥 Saúde", "👶 Desenvolvimento Infantil", "🛡️ Segurança", "🎓 Educação"]
#)
pagina = st.sidebar.radio(
    "Escolha o tipo de análise:",
    ["🏠 Página Inicial", "🎓 Educação"]
)

# -----------------------------------
# 🔹 Função para carregar dados
# -----------------------------------
def carregar_dados(tipo):
    config = CONFIG[tipo]
    dados = {}
    
    try:
        # Carregar arquivos conforme disponibilidade
        if "medias" in config["arquivos"]:
            caminho_arquivo = config["arquivos"]["medias"]
            if os.path.exists(caminho_arquivo):
                dados["df_medias"] = pd.read_csv(caminho_arquivo)
            else:
                caminho_alt = f"output/{caminho_arquivo}"
                if os.path.exists(caminho_alt):
                    dados["df_medias"] = pd.read_csv(caminho_alt)
                else:
                    st.warning(f"Arquivo de médias não encontrado: {caminho_arquivo}")
        
        if "diagnostico" in config["arquivos"]:
            caminho_arquivo = config["arquivos"]["diagnostico"]
            if os.path.exists(caminho_arquivo):
                dados["df_diagnostico"] = pd.read_csv(caminho_arquivo)
            else:
                caminho_alt = f"output/{caminho_arquivo}"
                if os.path.exists(caminho_alt):
                    dados["df_diagnostico"] = pd.read_csv(caminho_alt)
                else:
                    st.warning(f"Arquivo de diagnóstico não encontrado: {caminho_arquivo}")
        
        if "cidades" in config["arquivos"]:
            caminho_arquivo = config["arquivos"]["cidades"]
            if os.path.exists(caminho_arquivo):
                dados["df_cidades"] = pd.read_csv(caminho_arquivo)
            else:
                caminho_alt = f"output/{caminho_arquivo}"
                if os.path.exists(caminho_alt):
                    dados["df_cidades"] = pd.read_csv(caminho_alt)
                else:
                    st.warning(f"Arquivo de cidades não encontrado: {caminho_arquivo}")
        
        # Preparar rótulos de cluster
        col_cluster_medias = config["colunas_cluster"]["df_medias"]
        col_cluster_diagnostico = config["colunas_cluster"]["df_diagnostico"]
        col_cluster_cidades = config["colunas_cluster"]["df_cidades"]
        rotulos = config["rotulos_cluster"]
        
        # Função para criar rótulos com número do cluster
        def get_cluster_label_with_number(cluster_id, description):
            # Se o cluster_id for NaN, retornar um valor padrão
            if pd.isna(cluster_id):
                return "Não classificado"
            
            # Converter para string caso não seja
            try:
                cluster_num = int(cluster_id)
                return description
            except (ValueError, TypeError):
                return f"Cluster {cluster_id}"
        
        # Adicionar nomes descritivos aos DataFrames COM número do cluster
        if "df_medias" in dados:
            if col_cluster_medias in dados["df_medias"].columns:
                # Garantir que a coluna cluster seja numérica
                dados["df_medias"][col_cluster_medias] = pd.to_numeric(dados["df_medias"][col_cluster_medias], errors='coerce')
                
                # Adicionar coluna de número do cluster que começa em 1 (com tratamento de erro)
                try:
                    dados["df_medias"]["Número do Cluster"] = dados["df_medias"][col_cluster_medias].fillna(-1).astype(int) + 1
                    # Corrigir os valores que eram NaN
                    dados["df_medias"].loc[dados["df_medias"][col_cluster_medias].isna(), "Número do Cluster"] = None
                except (ValueError, TypeError):
                    # Se não for possível converter para int, usar um índice baseado na ordem
                    unique_clusters = dados["df_medias"][col_cluster_medias].dropna().unique()
                    cluster_map = {c: i+1 for i, c in enumerate(unique_clusters)}
                    dados["df_medias"]["Número do Cluster"] = dados["df_medias"][col_cluster_medias].map(cluster_map)
                
                nome_coluna = "Nome do Cluster"
                
                # Criar rótulos que incluem o número do cluster
                dados["df_medias"][nome_coluna] = dados["df_medias"].apply(
                    lambda row: get_cluster_label_with_number(
                        row[col_cluster_medias], 
                        rotulos.get(str(int(row[col_cluster_medias])) if not pd.isna(row[col_cluster_medias]) else "NA", 
                        f"Cluster {row['Número do Cluster']}")
                    ), 
                    axis=1
                )
                
                # Adicionar coluna de quantidade de municípios se não existir
                if "quantidade_municipios" not in dados["df_medias"].columns and "quantidade_registros" not in dados["df_medias"].columns:
                    # Contar municípios por cluster no df_cidades
                    if "df_cidades" in dados and col_cluster_cidades in dados["df_cidades"].columns:
                        # Garantir que a coluna cluster seja numérica em ambos os DataFrames
                        dados["df_cidades"][col_cluster_cidades] = pd.to_numeric(dados["df_cidades"][col_cluster_cidades], errors='coerce')
                        contagem = dados["df_cidades"][col_cluster_cidades].value_counts().reset_index()
                        contagem.columns = [col_cluster_medias, "quantidade_municipios"]
                        # Garantir que ambas as colunas sejam do mesmo tipo antes do merge
                        contagem[col_cluster_medias] = contagem[col_cluster_medias].astype(dados["df_medias"][col_cluster_medias].dtype)
                        dados["df_medias"] = dados["df_medias"].merge(contagem, on=col_cluster_medias, how="left")
        
        if "df_diagnostico" in dados:
            if col_cluster_diagnostico in dados["df_diagnostico"].columns:
                # Garantir que a coluna cluster seja numérica
                dados["df_diagnostico"][col_cluster_diagnostico] = pd.to_numeric(dados["df_diagnostico"][col_cluster_diagnostico], errors='coerce')
                
                # Adicionar coluna de número do cluster que começa em 1 (com tratamento de erro)
                try:
                    dados["df_diagnostico"]["Número do Cluster"] = dados["df_diagnostico"][col_cluster_diagnostico].fillna(-1).astype(int) + 1
                    # Corrigir os valores que eram NaN
                    dados["df_diagnostico"].loc[dados["df_diagnostico"][col_cluster_diagnostico].isna(), "Número do Cluster"] = None
                except (ValueError, TypeError):
                    # Se não for possível converter para int, usar um índice baseado na ordem
                    unique_clusters = dados["df_diagnostico"][col_cluster_diagnostico].dropna().unique()
                    cluster_map = {c: i+1 for i, c in enumerate(unique_clusters)}
                    dados["df_diagnostico"]["Número do Cluster"] = dados["df_diagnostico"][col_cluster_diagnostico].map(cluster_map)
                
                # Não precisamos adicionar a coluna "Nome do Cluster" aqui, pois já temos a coluna "Perfil"
        
        if "df_cidades" in dados:
            if col_cluster_cidades in dados["df_cidades"].columns:
                # Garantir que a coluna cluster seja numérica
                dados["df_cidades"][col_cluster_cidades] = pd.to_numeric(dados["df_cidades"][col_cluster_cidades], errors='coerce')
                
                # Adicionar coluna de número do cluster que começa em 1 (com tratamento de erro)
                try:
                    dados["df_cidades"]["Número do Cluster"] = dados["df_cidades"][col_cluster_cidades].fillna(-1).astype(int) + 1
                    # Corrigir os valores que eram NaN
                    dados["df_cidades"].loc[dados["df_cidades"][col_cluster_cidades].isna(), "Número do Cluster"] = None
                except (ValueError, TypeError):
                    # Se não for possível converter para int, usar um índice baseado na ordem
                    unique_clusters = dados["df_cidades"][col_cluster_cidades].dropna().unique()
                    cluster_map = {c: i+1 for i, c in enumerate(unique_clusters)}
                    dados["df_cidades"]["Número do Cluster"] = dados["df_cidades"][col_cluster_cidades].map(cluster_map)
                
                nome_coluna = "Nome do Cluster"
                
                if nome_coluna not in dados["df_cidades"].columns:
                    # Criar rótulos que incluem o número do cluster
                    dados["df_cidades"][nome_coluna] = dados["df_cidades"].apply(
                        lambda row: get_cluster_label_with_number(
                            row[col_cluster_cidades], 
                            rotulos.get(str(int(row[col_cluster_cidades])) if not pd.isna(row[col_cluster_cidades]) else "NA",
                            f"Cluster {row['Número do Cluster']}")
                        ), 
                        axis=1
                    )
        
        # Carregar mapa HTML se existir
        if "mapa" in config["arquivos"]:
            caminho_arquivo = config["arquivos"]["mapa"]
            caminho_alt = f"output/{caminho_arquivo}"
            
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "r", encoding="utf-8") as file:
                    dados["html_mapa"] = file.read()
            elif os.path.exists(caminho_alt):
                with open(caminho_alt, "r", encoding="utf-8") as file:
                    dados["html_mapa"] = file.read()
            else:
                st.warning(f"Arquivo de mapa não encontrado: {caminho_arquivo}")
        
        return dados
    
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        import traceback
        st.error(traceback.format_exc())
        return None

# -----------------------------------
# 🔹 Função de exibição de análise
# -----------------------------------
def exibir_analise(tipo):
    config = CONFIG[tipo]
    
    # Exibir título e descrição
    st.title(config["titulo"])
    st.write(config["descricao"])
    
    # Carregar dados
    dados = carregar_dados(tipo)
    if not dados:
        st.error(f"Não foi possível carregar os dados para a análise de {tipo}.")
        return
    
    # -----------------------------------
    # 🔹 Seção 1 - Variáveis Utilizadas
    # -----------------------------------
    st.header("📌 Indicadores Utilizados")
    st.markdown(config["indicadores"])

    # -----------------------------------
    # 🔹 Seção 2 - Contextualização dos Clusters
    # -----------------------------------
    st.header("🔍 Perfis Identificados")
    st.markdown(config["perfis"])

    # -----------------------------------
    # 🔹 Seção 3 - Média dos Clusters
    # -----------------------------------
    st.header("📊 Médias dos Indicadores por Cluster")
    if "df_medias" in dados:
        if "colunas_selecionadas" in config:
            # Verificar quais colunas existem no dataframe
            colunas_existentes = [col for col in config["colunas_selecionadas"] if col in dados["df_medias"].columns]
            
            # Se não houver colunas existentes, mostrar todas as colunas exceto a coluna original do cluster
            if not colunas_existentes:
                col_cluster = config["colunas_cluster"]["df_medias"]
                colunas_existentes = [col for col in dados["df_medias"].columns if col != col_cluster]
            
            # Exibir a tabela
            st.dataframe(dados["df_medias"][colunas_existentes], use_container_width=True)
        else:
            # Para outros casos, selecionamos todas exceto a coluna original do cluster
            col_cluster = config["colunas_cluster"]["df_medias"]
            colunas = [col for col in dados["df_medias"].columns if col != col_cluster]
            st.dataframe(dados["df_medias"][colunas], use_container_width=True)

    # -----------------------------------
    # 🔹 Seção 4 - Mapa Interativo
    # -----------------------------------
    st.header("🗺️ Mapa Interativo dos Clusters")
    if "html_mapa" in dados:
        st.components.v1.html(dados["html_mapa"], height=600)
    else:
        st.warning(f"Mapa interativo não disponível para {tipo}. Certifique-se de que o arquivo existe no caminho especificado.")

    # -----------------------------------
    # 🔹 Seção 5 - Diagnóstico dos Clusters
    # -----------------------------------
    st.header("📋 Diagnóstico dos Clusters")
    if "df_diagnostico" in dados and "colunas_diagnostico" in config:
        # Verificar quais colunas existem no dataframe
        colunas_existentes = [col for col in config["colunas_diagnostico"] if col in dados["df_diagnostico"].columns]
        
        # Se não houver colunas existentes, mostrar todas as colunas exceto a coluna original do cluster
        if not colunas_existentes:
            col_cluster = config["colunas_cluster"]["df_diagnostico"]
            colunas_existentes = [col for col in dados["df_diagnostico"].columns if col != col_cluster]
        
        # Exibir a tabela
        st.dataframe(dados["df_diagnostico"][colunas_existentes], use_container_width=True)
    else:
        st.warning(f"Dados de diagnóstico não disponíveis para {tipo}.")

    # -----------------------------------
    # 🔹 Seção 6 - Distribuição dos Municípios
    # -----------------------------------
    st.header("📊 Distribuição dos Municípios por Cluster")
    if "df_cidades" in dados:
        try:
            # Definir qual coluna contém o nome do cluster
            nome_coluna = "Nome do Cluster"
                
            # Verificar se as colunas necessárias existem
            if nome_coluna in dados["df_cidades"].columns and "Número do Cluster" in dados["df_cidades"].columns:
                # Criar dataframe de contagem com os números do cluster
                df_contagem = dados["df_cidades"][[nome_coluna, "Número do Cluster"]].groupby(nome_coluna).first().reset_index()
                df_contagem["Quantidade de Municípios"] = dados["df_cidades"][nome_coluna].value_counts().reindex(df_contagem[nome_coluna]).values
                
                # Ordenar pelo número do cluster
                df_contagem = df_contagem.sort_values("Número do Cluster")
                
                # Renomear coluna
                df_contagem = df_contagem.rename(columns={nome_coluna: "Perfil"})
                
                # Exibir contagem
                col1, col2 = st.columns([2, 3])
                with col1:
                    st.dataframe(df_contagem[["Número do Cluster", "Perfil", "Quantidade de Municípios"]], use_container_width=True)
                
                with col2:
                    # Gráfico de barras horizontal
                    fig = px.bar(df_contagem, 
                                x="Quantidade de Municípios", 
                                y="Perfil", 
                                orientation='h',
                                color="Perfil",
                                color_discrete_map=config.get("cor_grafico", None),
                                title="Distribuição de Municípios por Cluster")
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
            else:
                # Fallback se não encontrarmos as colunas esperadas
                st.warning("Dados completos para distribuição não disponíveis. Exibindo dados básicos:")
                if nome_coluna in dados["df_cidades"].columns:
                    contagem_simples = dados["df_cidades"][nome_coluna].value_counts().reset_index()
                    contagem_simples.columns = ["Perfil", "Quantidade de Municípios"]
                    st.dataframe(contagem_simples, use_container_width=True)
                else:
                    st.dataframe(dados["df_cidades"], use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao processar distribuição de municípios: {e}")
            # Exibir dataframe bruto em caso de erro
            st.dataframe(dados["df_cidades"], use_container_width=True)
    else:
        st.warning(f"Dados de municípios não disponíveis para {tipo}.")

    # -----------------------------------
    # 🔹 Seção 7 - Dados Detalhados (Expansível)
    # -----------------------------------
    with st.expander("🔍 Ver Dados Completos por Município"):
        if "df_cidades" in dados:
            # Adicionar campo de busca
            search = st.text_input("Buscar município:", key=f"search_{tipo}")
            
            # Definir coluna para busca
            coluna_busca = config.get("coluna_busca", "Cidades")
            
            # Filtrar dados se houver busca
            if search and coluna_busca in dados["df_cidades"].columns:
                filtered_df = dados["df_cidades"][dados["df_cidades"][coluna_busca].str.contains(search, case=False)]
            else:
                filtered_df = dados["df_cidades"]
            
            # Garantir que a coluna "Número do Cluster" apareça primeiro, se existir
            if "Número do Cluster" in filtered_df.columns:
                col_ordem = ["Número do Cluster"] + [col for col in filtered_df.columns if col != "Número do Cluster"]
                st.dataframe(filtered_df[col_ordem], use_container_width=True)
            else:
                # Se não existir, mostrar todas as colunas na ordem original
                st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("Dados detalhados por município não disponíveis.")

    # -----------------------------------
    # 🔹 Seção 8 - Metodologia
    # -----------------------------------
    with st.expander("📓 Metodologia"):
        st.markdown(config["metodologia"])

    # -----------------------------------
    # 🔹 Rodapé
    # -----------------------------------
    st.markdown("---")
    st.caption("Diretoria de Monitoramento de Políticas Públicas - DMP")

# -----------------------------------
# 🔹 Página Inicial
# -----------------------------------
if pagina == "🏠 Página Inicial":
    st.title("📊 Análise Multidimensional Municipal por Clusters")
    
    st.markdown("""
    ## Bem-vindo ao Dashboard Integrado de Análises Municipais
    
    Esta ferramenta proporciona uma visão integrada de quatro dimensões fundamentais para o desenvolvimento municipal:
    
    #    ### 🏥 **Saúde** 
    #    Avaliação dos indicadores de saúde pública, focando em mortalidade prematura, cobertura vacinal, mortalidade infantil e acesso a exames especializados.
    #    
    #    ### 👶 **Desenvolvimento Infantil** 
    #    Análise dos indicadores relacionados ao desenvolvimento infantil, incluindo mortalidade infantil, alfabetização, cobertura vacinal e atendimento educacional infantil.
    #    
    #    ### 🛡️ **Segurança** 
    #    Avaliação dos indicadores de segurança pública, incluindo taxas de homicídio, violência sexual, mortalidade no trânsito, roubo de veículos e roubo de celulares.
    #    
        ### 🎓 **Educação** 
        Diagnóstico das condições educacionais, considerando fatores como IDEB, evasão escolar e desempenho em avaliações padronizadas.
    
    ## Metodologia
    
    Todas as análises utilizam a técnica de clustering K-means para identificar grupos de municípios com características semelhantes. Este agrupamento permite:
    
    - **Diagnóstico preciso**: Identificação de perfis específicos de municípios com desafios similares
    - **Priorização eficiente**: Alocação otimizada de recursos baseada em necessidades reais
    - **Políticas customizadas**: Desenho de intervenções específicas para cada perfil identificado
    
    ## Como utilizar
    
    Utilize o menu lateral para navegar entre as diferentes dimensões de análise. Cada seção oferece:
    
    - Visualização interativa dos clusters em mapa
    - Indicadores médios por grupo
    - Diagnóstico detalhado com pontos fortes, fracos e recomendações
    - Busca por municípios específicos
    
    """)
    
    # Exibir mini-cards para navegação alternativa
    st.markdown("## Escolha uma dimensão para analisar:")

    # Primeira linha com 2 cards
    col1, col2 = st.columns(2)
    with col1:
        #st.info("### 🏥 Saúde")
        #if st.button("Ver análise de saúde", key="btn_saude"):
        #    st.session_state['pagina'] = "🏥 Saúde"
        #    st.rerun()
        pass
            
    with col2:
        #st.warning("### 👶 Desenvolvimento Infantil")
        #if st.button("Ver análise de desenvolvimento infantil", key="btn_infancia"):
        #    st.session_state['pagina'] = "👶 Desenvolvimento Infantil"
        #    st.rerun()
        pass

    # Segunda linha com 2 cards        
    col3, col4 = st.columns(2)
    with col3:
        #st.success("### 🛡️ Segurança")
        #if st.button("Ver análise de segurança", key="btn_seguranca"):
        #    st.session_state['pagina'] = "🛡️ Segurança"
        #    st.rerun()
        pass

    with col4:
        st.info("### 🎓 Educação")
        if st.button("Ver análise de educação", key="btn_educacao"):
            st.session_state['pagina'] = "🎓 Educação"
            st.rerun()
                

# -----------------------------------
# 🔹 Verificar se a página deve ser alterada com base na session_state
# -----------------------------------
if 'pagina' in st.session_state:
    pagina = st.session_state['pagina']
    # Limpar a variável de sessão para evitar loops
    del st.session_state['pagina']

# -----------------------------------
# 🔹 Roteamento para a página correta
# -----------------------------------
#if pagina == "🏥 Saúde":
#    exibir_analise("saude")
#    
#elif pagina == "👶 Desenvolvimento Infantil":
#    exibir_analise("infancia")
#    
#elif pagina == "🛡️ Segurança":
#    exibir_analise("seguranca")
#    
if pagina == "🎓 Educação":
    exibir_analise("educacao")
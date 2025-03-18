import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da página
st.set_page_config(page_title="Análise Multidimensional por Clusters", layout="wide")

# Configurações por tipo de análise
CONFIG = {
    "saneamento": {
        # Configurações de saneamento mantidas inalteradas...
        "titulo": "Análise de Saneamento Municipal por Clusters",
        "descricao": "Este dashboard apresenta uma análise das condições de saneamento dos municípios utilizando a técnica de K-Means.",
        "arquivos": {
            "medias": "output/medias_clusters_saneamento.csv",
            "diagnostico": "output/diagnostico_clusters_saneamento.csv",
            "cidades": "output/municipios_clusters_saneamento.csv",
            "representativos": "output/municipios_representativos_saneamento.csv",
            "mapa": "output/mapa_interativo_4clusters_saneamento.html"
        },
        "colunas_cluster": {
            "df_medias": "cluster",
            "df_diagnostico": "cluster", 
            "df_cidades": "cluster"
        },
        "rotulos_cluster": {
            "0": "Boa infraestrutura básica sem tratamento",
            "1": "Infraestrutura completa com tratamento de esgoto",
            "2": "Infraestrutura deficiente, baixo acesso à água",
            "3": "Infraestrutura intermediária em desenvolvimento"
        },
        "indicadores": """
        - **Acesso à Água**: Taxa de acesso à água pela rede geral.
        - **Tratamento de Esgoto**: Taxa de tratamento de esgoto.
        - **Coleta de Resíduos**: Taxa de cobertura de coleta de resíduos sólidos.
        - **Destino Correto**: Destinação adequada dos resíduos sólidos (0 = não, 1 = sim).
        - **Banheiros no Domicílio**: Percentual de domicílios com banheiro.
        - **Drenagem Pluvial**: Existência de sistema de drenagem e manejo de águas pluviais (0 = não, 1 = sim).
        - **Política Municipal**: Existência de política municipal de saneamento básico (0 = não, 1 = sim).
        """,
        "perfis": """
        Através da análise estatística, identificamos 4 perfis distintos de municípios com base em seus indicadores de saneamento:

        1. **Boa infraestrutura básica sem tratamento**: Municípios com bom acesso à água e coleta de resíduos, mas deficientes em tratamento de esgoto e destinação final adequada.

        2. **Infraestrutura completa com tratamento de esgoto**: Municípios mais desenvolvidos em saneamento, com destaque para o tratamento de esgoto e melhores indicadores gerais.

        3. **Infraestrutura deficiente, baixo acesso à água**: Municípios com graves deficiências no acesso à água e outros serviços básicos, apesar de terem políticas municipais estabelecidas.

        4. **Infraestrutura intermediária em desenvolvimento**: Municípios com indicadores medianos de saneamento, sem grandes destaques ou deficiências extremas.
        """,
        "colunas_selecionadas": ["Perfil do Cluster", "Número de Municípios", "Acesso à Água (%)", 
                                "Tratamento de Esgoto (%)", "Cobertura de Coleta de Resíduos (%)",
                                "Destino Correto de Resíduos (%)", "Banheiros nos Domicílios (%)",
                                "Drenagem Pluvial (%)", "Política Municipal (%)"],
        "colunas_diagnostico": ["Perfil", "Pontos Fortes", "Pontos Fracos", "Recomendações"],
        "coluna_busca": "Cidades",
        "cor_grafico": {
            "Boa infraestrutura básica sem tratamento": "#9467bd",
            "Infraestrutura completa com tratamento de esgoto": "#1f77b4",
            "Infraestrutura deficiente, baixo acesso à água": "#2ca02c",
            "Infraestrutura intermediária em desenvolvimento": "#ffeb3b"
        },
        "metodologia": """
        ### Processamento dos Dados
        
        1. **Pré-processamento**: 
           - Tratamento adequado para variáveis binárias e taxas
           - Preenchimento de valores ausentes (média para taxas, moda para binárias)
           - Transformação arcoseno para variáveis com assimetria significativa
           - Normalização seletiva (StandardScaler para taxas, preservação de variáveis binárias)
        
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
    "saude": {
        "titulo": "Análise de Saúde Municipal por Clusters",
        "descricao": "Este dashboard apresenta uma análise das condições de saúde dos municípios utilizando a técnica de K-Means.",
        "arquivos": {
            "medias": "output/medias_clusters_saude.csv",
            "diagnostico": "output/diagnostico_clusters_saude.csv",
            "cidades": "output/municipios_clusters_saude.csv",
            "mapa": "output/mapa_interativo_5clusters_saude.html"
        },
        "colunas_cluster": {
            "df_medias": "cluster",
            "df_diagnostico": "cluster", 
            "df_cidades": "cluster"
        },
        "rotulos_cluster": {
            "0": "Baixa vulnerabilidade geral",
            "1": "Alta mortalidade precoce",
            "2": "Alta mortalidade infantil",
            "3": "Crítico em mortalidade materna",
            "4": "Alta dependência de APS"
        },
        "indicadores": """
        - **Mortalidade Materna**: Taxa de mortalidade materna por habitante (2023).
        - **Mortalidade Infantil**: Taxa de mortalidade na infância por habitante (2023).
        - **Mortalidade Precoce**: Taxa de mortalidade precoce por habitante (2023).
        - **Internações Sensíveis**: Percentual de internações por condições sensíveis à atenção primária (2024).
        """,
        "perfis": """
        Através da análise estatística, identificamos 5 perfis distintos de municípios com base em seus indicadores de saúde:

        1. **Baixa vulnerabilidade geral (65 municípios)**: Municípios sem mortalidade materna, com baixas taxas de mortalidade infantil e precoce e menor taxa de internações por condições sensíveis à APS (19.72%).

        2. **Alta mortalidade precoce (40 municípios)**: Municípios com baixa mortalidade materna, porém com a maior taxa de mortalidade precoce (0.000515) e internações APS moderadas (24.54%).

        3. **Alta mortalidade infantil (27 municípios)**: Municípios sem mortalidade materna, mas com a maior taxa de mortalidade infantil (0.000773) e internações APS moderadas (24.35%).

        4. **Crítico em mortalidade materna (11 municípios)**: Municípios com mortalidade materna extremamente alta (8.83), mortalidade precoce moderada-alta (0.000308) e internações APS moderadas (21.77%).

        5. **Alta dependência de APS (81 municípios)**: Municípios sem mortalidade materna, com indicadores de mortalidade moderados, mas com a maior taxa de internações por condições sensíveis à APS (32.34%).
        """,
        "colunas_selecionadas": ["Nome do Cluster", "Mortalidade Materna", "Mortalidade Infantil", 
                                "Mortalidade Precoce", "Internações Sensíveis (%)"],
        "colunas_diagnostico": ["Nome do Cluster", "Pontos Fortes", "Pontos Fracos", "Recomendações"],
        "coluna_busca": "Cidades",
        "metodologia": """
        ### Processamento dos Dados
        
        1. **Pré-processamento**: 
           - Remoção de valores ausentes
           - Normalização das taxas por população
           - Transformação logarítmica para corrigir assimetria
           - Padronização usando StandardScaler
        
        2. **Clustering**:
           - Algoritmo K-Means 
           - Número ideal de clusters determinado pelo método da silhueta
           - Validação por PCA (Análise de Componentes Principais)
        
        3. **Interpretação**:
           - Análise das médias dos indicadores por cluster
           - Diagnóstico de pontos fortes e fracos
           - Elaboração de recomendações específicas
        """
    },
    "educacao": {
        "titulo": "Análise Educacional Municipal por Clusters",
        "descricao": "Este dashboard apresenta uma análise das condições educacionais dos municípios utilizando a técnica de K-Means.",
        "arquivos": {
            "medias": "output/medias_clusters_educ.csv",
            "diagnostico": "output/diagnostico_clusters_educ.csv",
            "cidades": "output/cidades_clusterizadas_educ.csv",
            "mapa": "output/mapa_interativo_clusters_educacao.html"
        },
        "colunas_cluster": {
            "df_medias": "Cluster",
            "df_diagnostico": "Cluster", 
            "df_cidades": "Cluster"
        },
        "rotulos_cluster": {
            "0": "Emergência Educacional",
            "1": "Pouca infraestrutura",
            "2": "Contradição Educacional"
        },
        "indicadores": """
        - **Taxa de Distorção Idade-Série (tx_distorcao_fundamental)**: Percentual de alunos com idade acima da esperada para a série.
        - **Taxa de Escolas por Habitante (taxa_escolas_por_habitante)**: Número de escolas proporcional à população.
        - **IDEB Anos Iniciais (ideb_ano_inicial)**: Índice de Desenvolvimento da Educação Básica para os anos iniciais do ensino fundamental.
        - **Total de Alfabetização (Total_alfabetização)**: Percentual da população alfabetizada.
        - **Taxa de Abandono Escolar (Taxa de abandonos EF)**: Percentual de alunos que deixaram a escola no Ensino Fundamental.
        """,
        "perfis": """
        Através da análise estatística, identificamos 3 perfis distintos de municípios com base em seus indicadores educacionais:

        1. **Emergência Educacional**: Municípios com indicadores educacionais críticos que necessitam de intervenção imediata.

        2. **Pouca infraestrutura**: Municípios com déficit de escolas e estrutura educacional, apesar de alguns indicadores de desempenho razoáveis.

        3. **Contradição Educacional**: Municípios com bons indicadores em algumas áreas, mas com deficiências significativas em outras, apresentando um perfil contraditório.
        """,
        "colunas_diagnostico": ["Perfil", "Pontos Fortes", "Pontos Fracos", "Recomendações"],
        "coluna_busca": "Cidades",
        "colunas_selecionadas": ["Nome do Cluster", "tx_distorcao_fundamental", "taxa_escolas_por_habitante", "ideb_ano_inicial", "Total_alfabetização", "Taxa de abandonos EF"],
        "cor_grafico": {
            "Emergência Educacional": "#d32f2f",
            "Pouca infraestrutura": "#ffa000",
            "Contradição Educacional": "#388e3c"
        },
        "metodologia": """
        ### Processamento dos Dados
        
        1. **Pré-processamento**: 
           - Tratamento de valores ausentes
           - Padronização das variáveis
           - Análise de correlação entre indicadores
        
        2. **Clustering**:
           - Algoritmo K-Means com 3 clusters
           - Número ideal de clusters determinado por métodos estatísticos
           - Visualização por PCA (Análise de Componentes Principais)
        
        3. **Interpretação**:
           - Análise das médias dos indicadores por cluster
           - Diagnóstico de pontos fortes e fracos
           - Elaboração de recomendações específicas por perfil
        """
    },
    "infancia": {
    "titulo": "Análise de Infância Municipal por Clusters",
    "descricao": "Este dashboard apresenta uma análise dos indicadores de infância dos municípios utilizando a técnica de K-Means.",
    "arquivos": {
        "medias": "output/medias_clusters_infancia.csv",
        "diagnostico": "output/diagnostico_clusters_infancia.csv",
        "cidades": "output/municipios_clusters_infancia.csv",
        "mapa": "output/mapa_interativo_5clusters_infancia.html"
    },
    "colunas_cluster": {
        "df_medias": "cluster",
        "df_diagnostico": "cluster", 
        "df_cidades": "cluster"
    },
    "rotulos_cluster": {
        "0": "Municípios com Equilíbrio Relativo",
        "1": "Crise na Saúde Infantil",
        "2": "Desnutrição Crítica com Boa Educação",
        "3": "Déficit Educacional Crítico",
        "4": "Vulnerabilidade Nutricional com Educação Precária"
    },
    "indicadores": """
    - **Mortalidade Infantil**: Taxa de mortalidade na infância por habitante (2023).
    - **Atendimento Ensino Infantil**: Taxa de atendimento do ensino infantil (%).
    - **Desnutrição Infantil**: Taxa de desnutrição na infância (2024).
    """,
    "perfis": """
    Através da análise estatística, identificamos 5 perfis distintos de municípios com base em seus indicadores relacionados à infância:

    1. **Municípios com Equilíbrio Relativo (71 municípios)**: Baixa mortalidade infantil (0,000135), cobertura educacional intermediária (57,67%), baixa desnutrição infantil (0,25%).

    2. **Crise na Saúde Infantil (23 municípios)**: Alta mortalidade infantil (0,000819), baixa cobertura educacional (53,83%), desnutrição infantil elevada (0,70%).

    3. **Desnutrição Crítica com Boa Educação (28 municípios)**: Baixa mortalidade infantil (0,000118), melhor cobertura educacional (63,03%), desnutrição infantil extremamente alta (1,60%).

    4. **Déficit Educacional Crítico (35 municípios)**: Mortalidade infantil moderada (0,000227), déficit crítico na educação infantil (39,54%), desnutrição moderada (0,39%).

    5. **Vulnerabilidade Nutricional com Educação Precária (67 municípios)**: Mortalidade infantil moderada (0,000181), baixa cobertura educacional (47,61%), desnutrição infantil muito alta (1,19%).
    """,
    "colunas_selecionadas": ["Nome do Cluster", "Mortalidade Infantil", 
                            "Atendimento Ensino Infantil", "Desnutrição Infantil"],
    "colunas_diagnostico": ["Perfil", "Pontos Fortes", "Pontos Fracos", "Recomendações"],
    "coluna_busca": "Cidades",
    "cor_grafico": {
        "0": "#1f77b4",  # Azul - Equilíbrio Relativo
        "1": "#d62728",  # Vermelho - Crise na Saúde Infantil
        "2": "#ff7f0e",  # Laranja - Desnutrição Crítica
        "3": "#2ca02c",  # Verde - Déficit Educacional
        "4": "#9467bd"   # Roxo - Vulnerabilidade Nutricional
    },
    "metodologia": """
    ### Processamento dos Dados
    
    1. **Pré-processamento**: 
       - Tratamento de valores problemáticos (#VALUE!, vírgulas em números)
       - Normalização das taxas por população
       - Transformação logarítmica para corrigir assimetria
       - Padronização usando StandardScaler
       - Tratamento de outliers
    
    2. **Clustering**:
       - Algoritmo K-Means com 5 clusters
       - Número ideal de clusters determinado pelos métodos do cotovelo e silhueta
       - Visualização por PCA (Análise de Componentes Principais)
    
    3. **Interpretação**:
       - Análise das médias dos indicadores por cluster
       - Diagnóstico de pontos fortes e fracos
       - Elaboração de recomendações específicas para cada grupo
    """
    }
}

# -----------------------------------
# 🔹 Menu de Navegação
# -----------------------------------
st.sidebar.title("📊 Navegação")
# Usando radio ao invés de selectbox para evitar a edição de texto
pagina = st.sidebar.radio(
    "Escolha o tipo de análise:",
    ["🏠 Página Inicial", "💧 Saneamento", "🏥 Saúde", "🎓 Educação", "👶 Infância"]
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
        
        if "representativos" in config["arquivos"]:
            caminho_arquivo = config["arquivos"]["representativos"]
            if os.path.exists(caminho_arquivo):
                dados["df_representativos"] = pd.read_csv(caminho_arquivo)
            else:
                caminho_alt = f"output/{caminho_arquivo}"
                if os.path.exists(caminho_alt):
                    dados["df_representativos"] = pd.read_csv(caminho_alt)
                else:
                    st.warning(f"Arquivo de municípios representativos não encontrado: {caminho_arquivo}")
        
        # Preparar rótulos de cluster
        col_cluster_medias = config["colunas_cluster"]["df_medias"]
        col_cluster_diagnostico = config["colunas_cluster"]["df_diagnostico"]
        col_cluster_cidades = config["colunas_cluster"]["df_cidades"]
        rotulos = config["rotulos_cluster"]
        
        # Função para criar rótulos com número do cluster
        def get_cluster_label_with_number(cluster_id, description):
            # Converter para string caso não seja
            cluster_id = str(cluster_id)
            # Calcular o número de exibição (cluster 0 -> 1, cluster 1 -> 2, etc.)
            try:
                display_num = str(int(cluster_id) + 1)
            except (ValueError, TypeError):
                # Se não for possível converter para int, usar o valor original
                display_num = cluster_id
            return f"Cluster {display_num}: {description}"
        
        # Adicionar nomes descritivos aos DataFrames COM número do cluster
        if "df_medias" in dados:
            if col_cluster_medias in dados["df_medias"].columns:
                # Adicionar coluna de número do cluster que começa em 1 (com tratamento de erro)
                try:
                    dados["df_medias"]["Número do Cluster"] = dados["df_medias"][col_cluster_medias].astype(int) + 1
                except (ValueError, TypeError):
                    # Se não for possível converter para int, usar um índice baseado na ordem
                    unique_clusters = dados["df_medias"][col_cluster_medias].unique()
                    cluster_map = {c: i+1 for i, c in enumerate(unique_clusters)}
                    dados["df_medias"]["Número do Cluster"] = dados["df_medias"][col_cluster_medias].map(cluster_map)
                
                if tipo == "saneamento":
                    nome_coluna = "Perfil do Cluster"
                else:
                    nome_coluna = "Nome do Cluster"
                
                # Criar rótulos que incluem o número do cluster
                dados["df_medias"][nome_coluna] = dados["df_medias"].apply(
                    lambda row: get_cluster_label_with_number(
                        row[col_cluster_medias], 
                        rotulos.get(str(row[col_cluster_medias]), f"Cluster {row['Número do Cluster']}")
                    ), 
                    axis=1
                )
        
        if "df_diagnostico" in dados:
            if col_cluster_diagnostico in dados["df_diagnostico"].columns:
                # Adicionar coluna de número do cluster que começa em 1 (com tratamento de erro)
                try:
                    dados["df_diagnostico"]["Número do Cluster"] = dados["df_diagnostico"][col_cluster_diagnostico].astype(int) + 1
                except (ValueError, TypeError):
                    # Se não for possível converter para int, usar um índice baseado na ordem
                    unique_clusters = dados["df_diagnostico"][col_cluster_diagnostico].unique()
                    cluster_map = {c: i+1 for i, c in enumerate(unique_clusters)}
                    dados["df_diagnostico"]["Número do Cluster"] = dados["df_diagnostico"][col_cluster_diagnostico].map(cluster_map)
                
                if tipo == "saneamento":
                    nome_coluna = "Perfil"
                elif tipo == "educacao":
                    nome_coluna = "Perfil"
                else:
                    nome_coluna = "Nome do Cluster"
                
                # Criar rótulos que incluem o número do cluster
                dados["df_diagnostico"][nome_coluna] = dados["df_diagnostico"].apply(
                    lambda row: get_cluster_label_with_number(
                        row[col_cluster_diagnostico], 
                        rotulos.get(str(row[col_cluster_diagnostico]), f"Cluster {row['Número do Cluster']}")
                    ), 
                    axis=1
                )
        
        if "df_cidades" in dados:
            if col_cluster_cidades in dados["df_cidades"].columns:
                # Adicionar coluna de número do cluster que começa em 1 (com tratamento de erro)
                try:
                    dados["df_cidades"]["Número do Cluster"] = dados["df_cidades"][col_cluster_cidades].astype(int) + 1
                except (ValueError, TypeError):
                    # Se não for possível converter para int, usar um índice baseado na ordem
                    unique_clusters = dados["df_cidades"][col_cluster_cidades].unique()
                    cluster_map = {c: i+1 for i, c in enumerate(unique_clusters)}
                    dados["df_cidades"]["Número do Cluster"] = dados["df_cidades"][col_cluster_cidades].map(cluster_map)
                
                if tipo == "saneamento":
                    nome_coluna = "Perfil do Cluster"
                else:
                    nome_coluna = "Nome do Cluster"
                
                if nome_coluna not in dados["df_cidades"].columns:
                    # Criar rótulos que incluem o número do cluster
                    dados["df_cidades"][nome_coluna] = dados["df_cidades"].apply(
                        lambda row: get_cluster_label_with_number(
                            row[col_cluster_cidades], 
                            rotulos.get(str(row[col_cluster_cidades]), f"Cluster {row['Número do Cluster']}")
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
        if tipo == "educacao":
            # Tratamento especial para educação
            try:
                df_display = dados["df_medias"].copy()
                
                # Verificar e mapear colunas se existirem
                cols_map = {
                    "tx_distorcao_fundamental": "Taxa de Distorção (%)",
                    "taxa_escolas_por_habitante": "Taxa de Escolas",
                    "ideb_ano_inicial": "IDEB Anos Iniciais",
                    "Total_alfabetização": "Alfabetização (%)",
                    "Taxa de abandonos EF": "Taxa de Abandono (%)"
                }
                
                # Colunas que vamos exibir
                columns_to_display = ["Número do Cluster", "Nome do Cluster"]
                
                # Adicionar apenas as colunas que realmente existem no dataframe
                for original_col, display_col in cols_map.items():
                    if original_col in df_display.columns:
                        df_display.rename(columns={original_col: display_col}, inplace=True)
                        columns_to_display.append(display_col)
                
                # Exibir o dataframe com as colunas selecionadas que existem
                st.dataframe(df_display[columns_to_display], use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao processar dados de educação: {e}")
                # Exibição de fallback: mostrar todas as colunas
                st.dataframe(dados["df_medias"], use_container_width=True)
        else:
            # Para outros casos
            if "colunas_selecionadas" in config:
                # Garantir que as colunas selecionadas incluam o Número do Cluster
                if "Número do Cluster" not in config["colunas_selecionadas"]:
                    colunas = ["Número do Cluster"] + config["colunas_selecionadas"]
                else:
                    colunas = config["colunas_selecionadas"]
                
                # Verificar quais colunas existem no dataframe
                colunas_existentes = [col for col in colunas if col in dados["df_medias"].columns]
                
                st.dataframe(dados["df_medias"][colunas_existentes], use_container_width=True)
            else:
                # Para outros casos, selecionamos todas exceto a coluna original do cluster
                col_cluster = config["colunas_cluster"]["df_medias"]
                colunas = ["Número do Cluster", "Nome do Cluster"] + [col for col in dados["df_medias"].columns if col != col_cluster and col != "Nome do Cluster" and col != "Número do Cluster"]
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
        # Adicionar coluna de número do cluster ao diagnóstico
        if "Número do Cluster" not in config["colunas_diagnostico"]:
            colunas_diagnostico = ["Número do Cluster"] + config["colunas_diagnostico"]
        else:
            colunas_diagnostico = config["colunas_diagnostico"]
        
        # Verificar quais colunas existem no dataframe
        colunas_existentes = [col for col in colunas_diagnostico if col in dados["df_diagnostico"].columns]
        
        st.dataframe(dados["df_diagnostico"][colunas_existentes], use_container_width=True)
    else:
        st.warning(f"Dados de diagnóstico não disponíveis para {tipo}.")

    # -----------------------------------
    # 🔹 Seção 6 - Municípios Representativos (apenas para saneamento)
    # -----------------------------------
    if tipo == "saneamento" and "df_representativos" in dados:
        st.header("🏙️ Municípios Representativos por Cluster")
        st.dataframe(dados["df_representativos"], use_container_width=True)

    # -----------------------------------
    # 🔹 Seção 7 - Distribuição dos Municípios
    # -----------------------------------
    st.header("📊 Distribuição dos Municípios por Cluster")
    if "df_cidades" in dados:
        try:
            # Definir qual coluna contém o nome do cluster
            if tipo == "saneamento":
                nome_coluna = "Perfil do Cluster"
            else:
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
    # 🔹 Seção 8 - Dados Detalhados (Expansível)
    # -----------------------------------
    with st.expander("🔍 Ver Dados Completos por Município"):
        if "df_cidades" in dados:
            # Adicionar campo de busca
            search = st.text_input("Buscar município:", key=f"search_{tipo}")
            
            # Definir coluna para busca
            coluna_busca = config.get("coluna_busca", "Cidades")
            
            # Para educação, usar sempre a coluna Cidades
            if tipo == "educacao":
                coluna_busca = "Cidades"
            
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
    # 🔹 Seção 9 - Metodologia
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
    
    Esta ferramenta proporciona uma visão integrada de três dimensões fundamentais para o desenvolvimento municipal:
    
    ### 💧 **Saneamento** 
    Análise dos indicadores de saneamento básico, incluindo acesso à água, coleta e tratamento de esgoto, gerenciamento de resíduos sólidos e drenagem urbana.
    
    ### 🏥 **Saúde** 
    Avaliação dos indicadores de saúde pública, focando em mortalidade materna, infantil, precoce e internações sensíveis à atenção primária.
    
    ### 🎓 **Educação** 
    Diagnóstico das condições educacionais, considerando fatores como distorção idade-série, infraestrutura escolar, qualidade do ensino e alfabetização.
    
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
    # Exibir mini-cards para navegação alternativa
st.markdown("## Escolha uma dimensão para analisar:")

# Primeira linha com 2 cards
col1, col2 = st.columns(2)
with col1:
    st.info("### 💧 Saneamento")
    if st.button("Ver análise de saneamento", key="btn_saneamento"):
        st.session_state['pagina'] = "💧 Saneamento"
        st.rerun()
        
with col2:
    st.warning("### 🏥 Saúde")
    if st.button("Ver análise de saúde", key="btn_saude"):
        st.session_state['pagina'] = "🏥 Saúde"
        st.rerun()

# Segunda linha com 2 cards        
col3, col4 = st.columns(2)
with col3:
    st.success("### 🎓 Educação")
    if st.button("Ver análise de educação", key="btn_educacao"):
        st.session_state['pagina'] = "🎓 Educação"
        st.rerun()

with col4:
    st.info("### 👶 Infância")
    if st.button("Ver análise de infância", key="btn_infancia"):
        st.session_state['pagina'] = "👶 Infância"
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
if pagina == "💧 Saneamento":
    exibir_analise("saneamento")
    
elif pagina == "🏥 Saúde":
    exibir_analise("saude")
    
elif pagina == "🎓 Educação":
    exibir_analise("educacao")
    
elif pagina == "👶 Infância":
    exibir_analise("infancia")
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da página
st.set_page_config(page_title="Análise Multidimensional por Clusters", layout="wide")

# Configurações por tipo de análise
CONFIG = {
    "saneamento": {
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
            "0": "Alta demanda em atenção primária",
            "1": "Vulnerabilidade materna",
            "2": "Mortalidade precoce elevada",
            "3": "Vulnerabilidade infantil",
            "4": "Melhores indicadores gerais"
        },
        "indicadores": """
        - **Mortalidade Materna**: Taxa de mortalidade materna por habitante (2023).
        - **Mortalidade Infantil**: Taxa de mortalidade na infância por habitante (2023).
        - **Mortalidade Precoce**: Taxa de mortalidade precoce por habitante (2023).
        - **Internações Sensíveis**: Percentual de internações por condições sensíveis à atenção primária (2024).
        """,
        "perfis": """
        Através da análise estatística, identificamos 5 perfis distintos de municípios com base em seus indicadores de saúde:

        1. **Alta demanda em atenção primária**: Municípios com taxas elevadas de internações que poderiam ser evitadas com atenção primária eficaz.

        2. **Vulnerabilidade materna**: Municípios com altas taxas de mortalidade materna, indicando problemas na assistência ao pré-natal e parto.

        3. **Mortalidade precoce elevada**: Municípios com alta mortalidade precoce, sugerindo desafios no tratamento de doenças crônicas.

        4. **Vulnerabilidade infantil**: Municípios com altas taxas de mortalidade infantil, indicando deficiências nos cuidados pediátricos.

        5. **Melhores indicadores gerais**: Municípios com bom desempenho em todos os indicadores analisados.
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
    }
}

# -----------------------------------
# 🔹 Menu de Navegação
# -----------------------------------
st.sidebar.title("📊 Navegação")
# Usando radio ao invés de selectbox para evitar a edição de texto
pagina = st.sidebar.radio(
    "Escolha o tipo de análise:",
    ["🏠 Página Inicial", "💧 Saneamento", "🏥 Saúde", "🎓 Educação"]
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
        
        # Adicionar nomes descritivos aos DataFrames
        if "df_medias" in dados:
            if col_cluster_medias in dados["df_medias"].columns:
                if tipo == "saneamento":
                    nome_coluna = "Perfil do Cluster"
                else:
                    nome_coluna = "Nome do Cluster"
                
                dados["df_medias"][nome_coluna] = dados["df_medias"][col_cluster_medias].astype(str).map(rotulos)
        
        if "df_diagnostico" in dados:
            if col_cluster_diagnostico in dados["df_diagnostico"].columns:
                if tipo == "saneamento":
                    nome_coluna = "Perfil"
                elif tipo == "educacao":
                    nome_coluna = "Perfil"
                else:
                    nome_coluna = "Nome do Cluster"
                
                dados["df_diagnostico"][nome_coluna] = dados["df_diagnostico"][col_cluster_diagnostico].astype(str).map(rotulos)
        
        if "df_cidades" in dados:
            if col_cluster_cidades in dados["df_cidades"].columns:
                if tipo == "saneamento":
                    nome_coluna = "Perfil do Cluster"
                else:
                    nome_coluna = "Nome do Cluster"
                
                if nome_coluna not in dados["df_cidades"].columns:
                    dados["df_cidades"][nome_coluna] = dados["df_cidades"][col_cluster_cidades].astype(str).map(rotulos)
        
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
            if tipo == "educacao":
                # Para educação, criamos um DataFrame com nomes mais amigáveis para exibição
                df_display = dados["df_medias"].copy()
                # Mapear os nomes técnicos para nomes amigáveis
                cols_map = {
                    "tx_distorcao_fundamental": "Taxa de Distorção (%)",
                    "taxa_escolas_por_habitante": "Taxa de Escolas",
                    "ideb_ano_inicial": "IDEB Anos Iniciais",
                    "Total_alfabetização": "Alfabetização (%)",
                    "Taxa de abandonos EF": "Taxa de Abandono (%)"
                }
                for old_col, new_col in cols_map.items():
                    if old_col in df_display.columns:
                        df_display = df_display.rename(columns={old_col: new_col})
                
                # Adicionar coluna de Nome do Cluster se não existir
                if "Nome do Cluster" not in df_display.columns:
                    col_cluster = config["colunas_cluster"]["df_medias"]
                    df_display["Nome do Cluster"] = df_display[col_cluster].astype(str).map(config["rotulos_cluster"])
                
                # Selecionar colunas para exibição
                friendly_cols = ["Nome do Cluster"]
                for col in config["colunas_selecionadas"][1:]:
                    if col in cols_map:
                        friendly_cols.append(cols_map[col])
                
                st.dataframe(df_display[friendly_cols], use_container_width=True)
            else:
                colunas = config["colunas_selecionadas"]
                st.dataframe(dados["df_medias"][colunas], use_container_width=True)
        else:
            # Para outros casos, selecionamos todas exceto a coluna original do cluster
            col_cluster = config["colunas_cluster"]["df_medias"]
            colunas = ["Nome do Cluster"] + [col for col in dados["df_medias"].columns if col != col_cluster and col != "Nome do Cluster"]
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
        st.dataframe(dados["df_diagnostico"][config["colunas_diagnostico"]], use_container_width=True)
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
        # Definir qual coluna contém o nome do cluster
        if tipo == "saneamento":
            nome_coluna = "Perfil do Cluster"
        else:
            nome_coluna = "Nome do Cluster"
            
        # Criar dataframe de contagem
        df_contagem = dados["df_cidades"][nome_coluna].value_counts().reset_index()
        df_contagem.columns = ["Perfil", "Quantidade de Municípios"]
        
        # Exibir contagem
        col1, col2 = st.columns([2, 3])
        with col1:
            st.dataframe(df_contagem, use_container_width=True)
        
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
            
            # Exibir dados
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
    st.markdown("## Escolha uma dimensão para analisar:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 💧 Saneamento")
        if st.button("Ver análise de saneamento", key="btn_saneamento"):
            # Usar session_state para armazenar a nova página e depois usar rerun
            st.session_state['pagina'] = "💧 Saneamento"
            st.rerun()
            
    with col2:
        st.warning("### 🏥 Saúde")
        if st.button("Ver análise de saúde", key="btn_saude"):
            st.session_state['pagina'] = "🏥 Saúde"
            st.rerun()
            
    with col3:
        st.success("### 🎓 Educação")
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
if pagina == "💧 Saneamento":
    exibir_analise("saneamento")
    
elif pagina == "🏥 Saúde":
    exibir_analise("saude")
    
elif pagina == "🎓 Educação":
    exibir_analise("educacao")
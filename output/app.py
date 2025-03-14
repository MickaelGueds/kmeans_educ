import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# Configuração da página
st.set_page_config(page_title="Análise Multidimensional por Clusters", layout="wide")

# CSS personalizado para melhorar a interface
def aplicar_css():
    st.markdown("""
    <style>
    /* Estilo para os cartões de navegação */
    .dimensao-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        flex-wrap: wrap;
        gap: 16px;
    }
    
    .dimensao-box {
        border-radius: 10px;
        padding: 30px 20px;
        width: 32%;
        min-width: 250px;
        transition: transform 0.3s, box-shadow 0.3s;
        margin-bottom: 10px;
        cursor: pointer;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .dimensao-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .saneamento {
        background-color: #1e3a8a;
    }
    
    .saude {
        background-color: #6b6302;
    }
    
    .educacao {
        background-color: #185d27;
    }
    
    .dimensao-icon {
        font-size: 36px;
        margin-bottom: 15px;
    }
    
    .dimensao-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .dimensao-desc {
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Esconder botões do Streamlit usados para navegação */
    .stButton {
        display: none;
    }
    
    /* Estilo para o botão voltar */
    .voltar-link {
        display: inline-flex;
        align-items: center;
        color: #4B9EFF;
        font-weight: 500;
        margin-bottom: 20px;
        cursor: pointer;
        text-decoration: none;
        padding: 5px 0;
    }
    
    .voltar-link:hover {
        text-decoration: underline;
    }
    
    /* Melhorias gerais de UI */
    h1 {
        margin-bottom: 20px;
    }
    
    .highlight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #4B9EFF;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    
    .footer {
        margin-top: 30px;
        padding-top: 10px;
        border-top: 1px solid #e6e6e6;
        text-align: center;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

# Aplicar CSS personalizado
aplicar_css()

# Configurações por tipo de análise
CONFIG = {
    "inicial": {
        "titulo": "Análise Multidimensional Municipal por Clusters",
        "descricao": """
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
        """
    },
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
            "diagnostico": "diagnostico_clusters_saude.csv",
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
            "medias": "medias_clusters.csv",
            "diagnostico": "diagnostico_clusters_3.csv",
            "cidades": "cidades_clusterizadas.csv",
            "mapa": "mapa_interativo.html"
        },
        "colunas_cluster": {
            "df_medias": "Cluster",
            "df_diagnostico": "Cluster", 
            "df_cidades": "Cluster"
        },
        "rotulos_cluster": {
            0: "Emergência Educacional",
            1: "Pouca infraestrutura",
            2: "Contradição Educacional"
        },
        "indicadores": """
        - **Taxa de Distorção Idade-Série**: Percentual de alunos com idade acima da esperada para a série.
        - **Taxa de Escolas por Habitante**: Número de escolas proporcional à população.
        - **IDEB (Índice de Desenvolvimento da Educação Básica)**: Mede a qualidade do ensino.
        - **Total de Alfabetização**: Percentual da população alfabetizada.
        - **Taxa de Abandono Escolar**: Percentual de alunos que deixaram a escola.
        """,
        "perfis": """
        Através da análise estatística, identificamos 3 perfis distintos de municípios com base em seus indicadores educacionais:

        1. **Emergência Educacional**: Municípios com indicadores educacionais críticos que necessitam de intervenção imediata.

        2. **Pouca infraestrutura**: Municípios com déficit de escolas e estrutura educacional, apesar de alguns indicadores de desempenho razoáveis.

        3. **Contradição Educacional**: Municípios com bons indicadores em algumas áreas, mas com deficiências significativas em outras, apresentando um perfil contraditório.
        """,
        "colunas_diagnostico": ["Nome do Cluster", "Pontos Fortes", "Pontos Fracos", "Recomendações"],
        "coluna_busca": "Cidade",
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
# 🔹 Inicialização do estado da sessão
# -----------------------------------
# Inicializar estado da sessão para a página selecionada se não existir
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = "🏠 Página Inicial"

# -----------------------------------
# 🔹 Funções para os cartões de navegação - COMPATÍVEL
# -----------------------------------
def aplicar_css_navegacao():
    """Aplica estilos CSS para os cartões de navegação"""
    st.markdown("""
    <style>
    .dimensao-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        flex-wrap: wrap;
        gap: 16px;
    }
    
    .dimensao-box {
        border-radius: 10px;
        padding: 30px 20px;
        width: 32%;
        min-width: 250px;
        transition: transform 0.3s, box-shadow 0.3s;
        margin-bottom: 10px;
        cursor: pointer;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .dimensao-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .saneamento {
        background-color: #1e3a8a;
    }
    
    .saude {
        background-color: #6b6302;
    }
    
    .educacao {
        background-color: #185d27;
    }
    
    .dimensao-icon {
        font-size: 36px;
        margin-bottom: 15px;
    }
    
    .dimensao-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .dimensao-desc {
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Esconder completamente os botões do Streamlit */
    .botoes-ocultos {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Função para ser compatível com diferentes versões do Streamlit
def rerun_streamlit():
    """Compatibilidade entre versões do Streamlit para rerun"""
    try:
        # Tenta o método mais recente primeiro
        st.rerun()
    except:
        # Se falhar, usa o método legado
        st.experimental_rerun()

def exibir_cartoes_dimensao():
    """
    Exibe os três cartões para seleção de dimensão com navegação intuitiva.
    """
    # Aplicar CSS para os cartões
    aplicar_css_navegacao()
    
    st.header("Escolha uma dimensão para analisar:")
    
    # Usar HTML para criar cartões clicáveis mais bonitos
    html_cards = f"""
    <div class="dimensao-container">
        <div class="dimensao-box saneamento" onclick="document.getElementById('btn_saneamento').click()">
            <div class="dimensao-icon">💧</div>
            <div class="dimensao-title">Saneamento</div>
            <div class="dimensao-desc">Análise de acesso à água, esgoto, coleta de resíduos e drenagem urbana</div>
        </div>
        
        <div class="dimensao-box saude" onclick="document.getElementById('btn_saude').click()">
            <div class="dimensao-icon">🏥</div>
            <div class="dimensao-title">Saúde</div>
            <div class="dimensao-desc">Análise de mortalidade materna, infantil, precoce e internações sensíveis</div>
        </div>
        
        <div class="dimensao-box educacao" onclick="document.getElementById('btn_educacao').click()">
            <div class="dimensao-icon">🎓</div>
            <div class="dimensao-title">Educação</div>
            <div class="dimensao-desc">Análise de distorção idade-série, infraestrutura escolar e alfabetização</div>
        </div>
    </div>
    """
    
    st.markdown(html_cards, unsafe_allow_html=True)
    
    # Botões escondidos em um container com classe CSS que os oculta
    st.markdown('<div class="botoes-ocultos">', unsafe_allow_html=True)
    if st.button("Saneamento", key="btn_saneamento"):
        st.session_state.pagina_atual = "💧 Saneamento"
        rerun_streamlit()
    
    if st.button("Saúde", key="btn_saude"):
        st.session_state.pagina_atual = "🏥 Saúde"
        rerun_streamlit()
    
    if st.button("Educação", key="btn_educacao"):
        st.session_state.pagina_atual = "🎓 Educação"
        rerun_streamlit()
    st.markdown('</div>', unsafe_allow_html=True)

# Também é necessário atualizar a função mudar_pagina
def mudar_pagina(nova_pagina):
    """Função para mudar de página usando estado da sessão"""
    st.session_state.pagina_atual = nova_pagina
    rerun_streamlit()  # Usando a função compatível

def exibir_botao_voltar():
    """Exibe um botão de voltar elegante"""
    voltar_html = """
    <div class="voltar-link" onclick="document.getElementById('btn_voltar').click()">
        ← Voltar para a página inicial
    </div>
    """
    st.markdown(voltar_html, unsafe_allow_html=True)
    
    if st.button("Voltar", key="btn_voltar"):
        mudar_pagina("🏠 Página Inicial")

# -----------------------------------
# 🔹 Menu lateral - MELHORADO
# -----------------------------------
with st.sidebar:
    st.title("📊 Navegação")
    
    # Menu com botões estilizados
    opcoes_menu = {
        "🏠 Página Inicial": "Visão geral do projeto", 
        "💧 Saneamento": "Análise de saneamento básico", 
        "🏥 Saúde": "Análise de indicadores de saúde", 
        "🎓 Educação": "Análise de indicadores educacionais"
    }
    
    for opcao, descricao in opcoes_menu.items():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(opcao.split()[0])  # Emoji
        with col2:
            if st.button(opcao.split(" ", 1)[1], help=descricao, key=f"sidebar_{opcao}"):
                mudar_pagina(opcao)

    st.markdown("---")
    st.caption("© Diretoria de Monitoramento de Políticas Públicas")

# -----------------------------------
# 🔹 Função para carregar dados
# -----------------------------------
def carregar_dados(tipo):
    config = CONFIG[tipo]
    dados = {}
    
    try:
        # Carregar arquivos conforme disponibilidade
        if "arquivos" in config:
            if "medias" in config["arquivos"]:
                try:
                    dados["df_medias"] = pd.read_csv(config["arquivos"]["medias"])
                except:
                    st.warning(f"Não foi possível carregar o arquivo {config['arquivos']['medias']}")
            
            if "diagnostico" in config["arquivos"]:
                try:
                    dados["df_diagnostico"] = pd.read_csv(config["arquivos"]["diagnostico"])
                except:
                    st.warning(f"Não foi possível carregar o arquivo {config['arquivos']['diagnostico']}")
            
            if "cidades" in config["arquivos"]:
                try:
                    dados["df_cidades"] = pd.read_csv(config["arquivos"]["cidades"])
                except:
                    st.warning(f"Não foi possível carregar o arquivo {config['arquivos']['cidades']}")
            
            if "representativos" in config["arquivos"]:
                try:
                    dados["df_representativos"] = pd.read_csv(config["arquivos"]["representativos"])
                except:
                    st.warning(f"Não foi possível carregar o arquivo {config['arquivos']['representativos']}")
            
            # Carregar mapa HTML se existir
            if "mapa" in config["arquivos"]:
                try:
                    with open(config["arquivos"]["mapa"], "r", encoding="utf-8") as file:
                        dados["html_mapa"] = file.read()
                except:
                    st.warning(f"Não foi possível carregar o arquivo do mapa {config['arquivos']['mapa']}")
        
        # Adicionar rótulos aos clusters se os DataFrames foram carregados com sucesso
        if "colunas_cluster" in config and "rotulos_cluster" in config:
            # Adicionar nomes aos DataFrames
            if "df_medias" in dados and "df_medias" in config["colunas_cluster"]:
                col = config["colunas_cluster"]["df_medias"]
                if col in dados["df_medias"].columns:
                    nome_coluna = "Perfil do Cluster" if tipo == "saneamento" else "Nome do Cluster"
                    dados["df_medias"][nome_coluna] = dados["df_medias"][col].astype(str).map(config["rotulos_cluster"])
            
            if "df_diagnostico" in dados and "df_diagnostico" in config["colunas_cluster"]:
                col = config["colunas_cluster"]["df_diagnostico"]
                if col in dados["df_diagnostico"].columns:
                    nome_coluna = "Perfil" if tipo == "saneamento" else "Nome do Cluster"
                    dados["df_diagnostico"][nome_coluna] = dados["df_diagnostico"][col].astype(str).map(config["rotulos_cluster"])
            
            if "df_cidades" in dados and "df_cidades" in config["colunas_cluster"]:
                col = config["colunas_cluster"]["df_cidades"]
                if col in dados["df_cidades"].columns:
                    nome_coluna = "Perfil do Cluster" if tipo == "saneamento" else "Nome do Cluster"
                    if nome_coluna not in dados["df_cidades"].columns:
                        dados["df_cidades"][nome_coluna] = dados["df_cidades"][col].astype(str).map(config["rotulos_cluster"])
        
        return dados
    
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return {}

# -----------------------------------
# 🔹 Função para exibir análise
# -----------------------------------
def exibir_analise(tipo):
    if tipo not in CONFIG:
        st.error(f"Tipo de análise '{tipo}' não configurado.")
        return
    
    config = CONFIG[tipo]
    
    # Título e descrição
    st.title(config["titulo"])
    
    if tipo == "inicial":
        # Para a página inicial, a descrição é o conteúdo principal
        st.markdown(config["descricao"])
        
        # Adicionar cartões de navegação na página inicial
        exibir_cartoes_dimensao()
        
        return
    
    # Exibir botão de voltar nas páginas de análise
    exibir_botao_voltar()
    
    # Descrição da análise atual
    st.markdown(f'<div class="highlight-box">{config["descricao"]}</div>', unsafe_allow_html=True)
    
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
            colunas = config["colunas_selecionadas"]
        else:
            # Para educação, selecionamos todas exceto a coluna original do cluster
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
        st.error(f"Arquivo de mapa não encontrado para {tipo}.")

    # -----------------------------------
    # 🔹 Seção 5 - Diagnóstico dos Clusters
    # -----------------------------------
    st.header("📋 Diagnóstico dos Clusters")
    if "df_diagnostico" in dados and "colunas_diagnostico" in config:
        st.dataframe(dados["df_diagnostico"][config["colunas_diagnostico"]], use_container_width=True)

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
        nome_coluna = "Perfil do Cluster" if tipo == "saneamento" else "Nome do Cluster"
        
        # Verificar se a coluna existe
        if nome_coluna in dados["df_cidades"].columns:
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

    # -----------------------------------
    # 🔹 Seção 8 - Dados Detalhados (Expansível)
    # -----------------------------------
    with st.expander("🔍 Ver Dados Completos por Município"):
        if "df_cidades" in dados:
            # Adicionar campo de busca
            search = st.text_input("Buscar município:", key=f"search_{tipo}")
            
            # Definir coluna para busca
            coluna_busca = config.get("coluna_busca", "Cidades")
            
            # Tentar diferentes nomes de coluna para busca se necessário
            if coluna_busca not in dados["df_cidades"].columns and tipo == "educacao":
                alternativas = ["Cidades", "Cidade", "Municipio", "Município"]
                for alt in alternativas:
                    if alt in dados["df_cidades"].columns:
                        coluna_busca = alt
                        break
            
            # Filtrar dados se houver busca
            if search and coluna_busca in dados["df_cidades"].columns:
                filtered_df = dados["df_cidades"][dados["df_cidades"][coluna_busca].str.contains(search, case=False)]
            else:
                filtered_df = dados["df_cidades"]
            
            # Exibir dados
            st.dataframe(filtered_df, use_container_width=True)

    # -----------------------------------
    # 🔹 Seção 9 - Metodologia
    # -----------------------------------
    with st.expander("📓 Metodologia"):
        st.markdown(config["metodologia"])

    # -----------------------------------
    # 🔹 Rodapé
    # -----------------------------------
    st.markdown('<div class="footer">Diretoria de Monitoramento de Políticas Públicas - DMP</div>', unsafe_allow_html=True)

# -----------------------------------
# 🔹 Verificar parâmetros de URL para navegação direta
# -----------------------------------
query_params = st.experimental_get_query_params()
if "page" in query_params:
    page = query_params["page"][0]
    if page in ["saneamento", "saude", "educacao"]:
        emoji_map = {"saneamento": "💧", "saude": "🏥", "educacao": "🎓"}
        title_map = {"saneamento": "Saneamento", "saude": "Saúde", "educacao": "Educação"}
        st.session_state.pagina_atual = f"{emoji_map[page]} {title_map[page]}"

# -----------------------------------
# 🔹 Roteamento com base na seleção do menu
# -----------------------------------
pagina = st.session_state.pagina_atual

if pagina == "🏠 Página Inicial":
    exibir_analise("inicial")
elif pagina == "💧 Saneamento":
    exibir_analise("saneamento")
elif pagina == "🏥 Saúde":
    exibir_analise("saude")
elif pagina == "🎓 Educação":
    exibir_analise("educacao")
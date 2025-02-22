# 📊 Clusterização de Municípios do Piauí com K-Means

Este projeto utiliza técnicas de aprendizado não supervisionado para agrupar municípios do Piauí com base em indicadores educacionais. A metodologia aplicada envolve normalização dos dados, redução de dimensionalidade (PCA) e clusterização (K-Means).

## 📌 Metodologia

### 🔹 1. Preparação dos Dados

O objetivo é agrupar municípios do Piauí considerando qualidade educacional (IDEB) e volume educacional (número de matrículas e docentes).

No entanto, as métricas utilizadas possuem escalas diferentes e outliers, o que pode afetar o modelo de clusterização. Para evitar distorções, aplicamos técnicas de normalização e transformação dos dados.

### 🔹 2. Variáveis Utilizadas

Foram consideradas as seguintes métricas para a clusterização:

- **Indicador de Desenvolvimento da Educação Básica (IDEB)** - Ensino Fundamental
- **Número de matrículas no ensino fundamental**
- **Número de matrículas no ensino médio**
- **Número de docentes no ensino fundamental**
- **Número de docentes no ensino médio**

## ⚙️ Transformação das Variáveis

### 📈 2.1 Normalização do IDEB (IDEB Escalonado)

O IDEB foi padronizado utilizando o `RobustScaler`, que transforma os valores em relação à mediana e intervalo interquartil (IQR).

**Fórmula aplicada:**

IDEB Escalonado = (IDEB − Mediana(IDEB)) / IQR(IDEB)


**Por que usar essa normalização?**

- O IDEB pode ter valores com baixa variação, mas conter outliers.
- O escalonamento robusto reduz o impacto de valores extremos, mantendo a estrutura original dos dados.

### 🏫 2.2 Construção do Índice de Volume (PCA)

As métricas de volume (matrículas e docentes) possuem escalas muito diferentes. Para garantir comparabilidade, aplicamos três etapas:

1. **Transformação Logarítmica (log1p)**
   - Reduz grandes variações entre municípios grandes e pequenos.
   - **Fórmula aplicada:**
     ```
     x′ = log(1 + x)
     ```

2. **Escalonamento Robusto (RobustScaler)**
   - Normaliza os valores das métricas de matrícula/docentes com base na mediana e IQR.

3. **Redução de Dimensionalidade (PCA - Principal Component Analysis)**
   - O PCA combina variáveis correlacionadas em um único índice, chamado **Índice de Volume**, que representa a variação conjunta das métricas educacionais.
   - A primeira componente principal (PC1) captura a maior variação dos dados.

**Por que usar PCA?**
- ✅ Matrículas e docentes são altamente correlacionados.
- ✅ O PCA reduz redundância e melhora a eficiência do modelo.

## 🏷️ Clusterização com K-Means

Com as variáveis transformadas, aplicamos o algoritmo K-Means para segmentar os municípios.

**Variáveis utilizadas na clusterização:**
- **IDEB Escalonado** (qualidade da educação).
- **Índice de Volume** (PCA das matrículas e docentes) (tamanho do sistema educacional).

**Por que usar apenas essas duas variáveis?**
- ✅ Evita aumento desnecessário da complexidade do modelo.
- ✅ Mantém um equilíbrio entre qualidade (IDEB) e quantidade (Volume Index).

### 📌 Escolha do número ideal de clusters (k)

Utilizamos o método do cotovelo, que analisa a variação intra-cluster para determinar o valor ideal de `k`. O número de clusters foi definido conforme a melhor separação dos dados.

## 📊 Resultados

Após a clusterização:

- Criamos um arquivo CSV contendo:
  - ✅ Município
  - ✅ Cluster atribuído
  - ✅ Proximidade ao centro do cluster (distância euclidiana ao centróide)

A proximidade mede quão representativo um município é dentro do seu cluster.

## 4. Interpretação dos Resultados

Após a clusterização, é importante interpretar a saída do modelo. A interpretação envolve compreender as características médias de cada cluster e analisar a proximidade dos municípios aos centros dos clusters.

### 4.1 Características Médias por Cluster

Uma forma de interpretar os clusters é visualizar as médias das variáveis dentro de cada cluster. Através da análise das médias, podemos identificar a principal diferença entre os clusters. Por exemplo, se um cluster tem um IDEB muito alto e um Índice de Volume grande, ele pode representar municípios com boa educação e grande sistema educacional.

**Exemplo de tabelas de médias por cluster:**

| Cluster | IDEB_scaled | Volume_index |
|---------|-------------|--------------|
| 0       | 0.516239    | -1.319312    |
| 1       | 0.141026    | 3.433563     |
| 2       | -0.028736   | 0.846913     |
| 3       | 1.111111    | 9.729542     |
| 4       | -0.626126   | -0.842809    |

**Interpretação:**
- **Cluster 0:** Desempenho educacional moderado, sistema educacional pequeno.
- **Cluster 1:** Desempenho educacional abaixo da média, sistema educacional grande.
- **Cluster 2:** Desempenho educacional ligeiramente abaixo da média, sistema educacional médio.
- **Cluster 3:** Desempenho educacional alto, sistema educacional muito grande.
- **Cluster 4:** Desempenho educacional baixo, sistema educacional pequeno.

### 4.2 Proximidade dos Clusters (Distância ao Centro)

A proximidade de um município ao centro do seu cluster pode ser calculada utilizando a distância euclidiana. Quanto menor a distância, mais representativo o município é dentro do seu cluster.

**A proximidade pode ser interpretada da seguinte forma:**
- Municípios próximos ao centro de um cluster são mais representativos daquele grupo.
- Municípios mais distantes podem ser considerados outliers ou casos marginais.

### 4.3 Ajustando o Número de Clusters (k)

Decidir o número ideal de clusters é uma parte crucial da análise de K-Means. O Método do Cotovelo já é uma técnica que você usou para escolher o valor de `k`, mas como ajustar esse número?

- **Aumentar k:** Se você aumentar o número de clusters, você pode obter grupos menores e mais específicos, mas o modelo pode se tornar mais complexo e pode sobreajustar os dados (overfitting). Além disso, a interpretação de clusters menores pode ser mais difícil.
- **Diminuir k:** Se você diminuir o número de clusters, o modelo pode começar a generalizar mais, criando grupos mais amplos. Isso pode ser bom para uma visão mais macro dos dados, mas pode perder nuances importantes dentro dos grupos.

**Quando ajustar k?**
- Se você notar que os clusters resultantes não fazem sentido ou não são representativos, talvez seja hora de ajustar o número de clusters.
- Aumentar `k` pode gerar divisões mais específicas, mas também mais complexas e com menor generalização.

## 📚 Referências

- 📖 Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
- 📖 Johnson, R. A., & Wichern, D. W. (2007). *Applied Multivariate Statistical Analysis* (6ª ed.). Pearson.
- 📄 Medium – Towards Data Science:
  - 🔗 Artigos sobre `RobustScaler`, transformação logarítmica (`log1p`) e clusterização com K-Means.

## Sugestões
- Mais variaveis que demonstrem a qualidade educacional como taxa de aprovação do enem
- Talvez uma proporção de matriculas/docentes o que resulta em uma variavel que demonstr a carga dos professores nas escolas

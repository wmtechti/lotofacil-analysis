# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-01-03

### ✨ Adicionado

#### 🎯 Análise Espacial
- Implementação completa do sistema de análise espacial do grid 5×5 da Lotofácil
- Mapeamento de números para coordenadas (linha, coluna) no volante
- Heatmap de frequências por célula, linha e coluna do grid
- Análise de co-ocorrência entre números (matriz 25×25)
- Detecção de clusters espaciais usando DBSCAN com distância Manhattan
- Métricas espaciais: centroide, dispersão, distância entre pares
- Análise de bias borda vs centro

#### 🌡️ Análise de Padrões
- Classificação de números em quentes, médios e frios (baseado em desvio estatístico)
- Análise de tendências temporais com janela móvel de 500 sorteios
- Identificação de 43 super pares com força > 95%
- Micro-clusters com 3 algoritmos diferentes (DBSCAN eps=1.0, eps=1.5, K-Means)
- Análise de força de pares de números

#### 🎲 Monte Carlo e Simulação
- Gerador inteligente de jogos com 6 estratégias diferentes:
  - Pesos (Quente + Tendência)
  - Números Quentes
  - Super Pares
  - Balanceamento Espacial
  - Coluna 5 (Mais Quente)
  - Tendência Alta
- Simulação Monte Carlo completa (10.000 iterações)
- Validação histórica de estratégias contra 3.575 sorteios
- Ranking de estratégias por performance
- Cálculo de probabilidades empíricas de acerto

#### 🎨 Visualizações
- Heatmap colorido do grid 5×5 com números
- Gráfico de barras de frequência (colorido por temperatura)
- Comparação visual de linhas e colunas
- Grafo de rede de co-ocorrência (top 30 pares)
- Distribuições de métricas espaciais (5 gráficos)
- Gráficos de tendências temporais
- Gráficos de desvios (quente/frio)

#### 📊 Relatórios e Exportações
- Relatório resumo em texto com estatísticas principais
- 15+ arquivos CSV com dados estruturados
- 5 imagens PNG em alta resolução (300 DPI)
- Arquivo JSON com estatísticas de Monte Carlo
- Exportação de melhores jogos e comparação de estratégias

#### 📚 Documentação
- README.md completo com instruções de uso
- GUIA_DE_USO.md com exemplos práticos e estratégias
- Docstrings em todos os módulos
- Comentários explicativos no código
- Notebook Jupyter interativo para análise exploratória

### 🔧 Módulos Desenvolvidos

- `grid_mapping.py` - Mapeamento número ↔ coordenada
- `io_data.py` - Carregamento e validação de dados
- `heatmap_analysis.py` - Análise de frequências espaciais
- `spatial_metrics.py` - Métricas de dispersão e padrões
- `cooccurrence.py` - Análise de co-ocorrência
- `cluster_analysis.py` - Detecção de clusters (DBSCAN)
- `advanced_analysis.py` - Análises avançadas (quente/frio, tendências)
- `visualizations.py` - Geração de gráficos e imagens
- `game_generator.py` - Gerador inteligente de jogos
- `monte_carlo.py` - Simulação e validação histórica
- `main.py` - Pipeline principal de análise
- `advanced_main.py` - Pipeline de análises avançadas
- `simulation_main.py` - Pipeline de simulação Monte Carlo

### 📈 Resultados Principais

- **Dataset**: 3.575 sorteios analisados (29/09/2003 até 01/01/2026)
- **Número mais quente**: 20 (+4.06% acima do esperado)
- **Número mais frio**: 16 (-4.62% abaixo do esperado)
- **Melhor par**: [11+20] - 1.362 vezes (38.1% dos sorteios)
- **Coluna mais quente**: Coluna 5 (números 5,10,15,20,25)
- **Melhor estratégia**: Tendência Alta (12.42% taxa de prêmio)
- **Ganho vs aleatório**: +1.08% de chance de prêmio

### 🛠️ Tecnologias

- Python 3.11+
- pandas >= 2.0
- numpy >= 1.24
- scikit-learn >= 1.3 (DBSCAN, K-Means)
- matplotlib >= 3.7
- seaborn >= 0.12
- networkx >= 3.0 (grafos de co-ocorrência)
- openpyxl >= 3.1
- tqdm >= 4.66 (progress bars)

### 🔒 Arquivos de Configuração

- `.gitignore` - Ignora arquivos temporários e resultados
- `requirements.txt` - Dependências do projeto
- `VERSION` - Versionamento semântico
- `CHANGELOG.md` - Este arquivo

### 📝 Formato de Dados

- Entrada: CSV/XLSX com 15 colunas de números sorteados
- Validação automática de intervalo (1-25) e duplicatas
- Suporte a múltiplos formatos de coluna (Bola1..15, b1..15)

---

## Tipos de Mudanças

- `✨ Adicionado` - Para novas funcionalidades
- `🔧 Modificado` - Para mudanças em funcionalidades existentes
- `🗑️ Depreciado` - Para funcionalidades que serão removidas
- `🚫 Removido` - Para funcionalidades removidas
- `🐛 Corrigido` - Para correção de bugs
- `🔒 Segurança` - Para correções de vulnerabilidades

---

## Versionamento Semântico

Formato: `MAJOR.MINOR.PATCH`

- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Novas funcionalidades (compatível com versões anteriores)
- **PATCH**: Correções de bugs (compatível com versões anteriores)

---

[1.0.0]: https://github.com/wmtechti/lotofacil-analysis/releases/tag/v1.0.0

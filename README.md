# 🎯 Análise Espacial da Lotofácil

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/wmtechti/lotofacil-analysis/releases/tag/v1.0.0)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

Projeto de análise estatística e espacial da Lotofácil usando o grid 5×5 do volante como domínio geoespacial abstrato.

## 📋 Sobre o Projeto

Este projeto trata o volante da Lotofácil (25 números dispostos em grid 5×5) como um espaço geográfico para análise de padrões espaciais. Utilizamos técnicas de análise espacial, clustering e co-ocorrência para identificar padrões nos sorteios históricos.

### Layout do Volante

```
 1   2   3   4   5
 6   7   8   9  10
11  12  13  14  15
16  17  18  19  20
21  22  23  24  25
```

## 🎲 Como Funciona a Lotofácil

- **Escolha**: marque entre 15 e 20 números dentre os 25 disponíveis
- **Prêmios**: ganhe ao acertar 11, 12, 13, 14 ou 15 números
- **Sorteio**: 15 números são sorteados

## 🔬 Análises Implementadas

### 1. **Heatmap de Frequência**
Calcula quantas vezes cada número (célula do grid) foi sorteado e agrega por:
- Frequência por célula individual
- Frequência por linha (1 a 5)
- Frequência por coluna (1 a 5)

### 2. **Métricas Espaciais**
Para cada sorteio, calcula:
- **Centroide**: ponto médio das coordenadas dos números sorteados
- **Dispersão**: distância média e máxima ao centroide
- **Distância entre pares**: média de distância Manhattan entre todos os números
- **Bias borda/centro**: proporção de números nas bordas vs centro

### 3. **Co-ocorrência**
Identifica pares de números que saem juntos com frequência:
- Matriz 25×25 de co-ocorrências
- Ranking dos top pares mais frequentes

### 4. **Clusters Espaciais (DBSCAN)**
Detecta agrupamentos de números no grid usando:
- **Algoritmo**: DBSCAN (Density-Based Spatial Clustering)
- **Métrica**: Distância de Manhattan
- **Parâmetros ajustáveis**:
  - `eps=1.0`: vizinhos imediatos (horizontal/vertical)
  - `eps=1.5`: inclui diagonais
  - `eps=2.0`: vizinhança 2×2

## 📁 Estrutura do Projeto

```
lotofacil-analysis/
├── data/
│   └── lotofacil_sorteios.csv    # histórico de sorteios
├── out/                           # resultados gerados
│   ├── heatmap_5x5.csv
│   ├── freq_linhas.csv
│   ├── freq_colunas.csv
│   ├── metrics_por_sorteio.csv
│   ├── top_pares_coocorrencia.csv
│   ├── clusters_dbscan_manhattan.csv
│   └── summary.json
├── src/
│   ├── __init__.py
│   ├── grid_mapping.py            # mapeamento número ↔ coordenada
│   ├── io_data.py                 # carregamento de dados
│   ├── heatmap_analysis.py        # análise de frequência
│   ├── spatial_metrics.py         # métricas espaciais
│   ├── cooccurrence.py            # análise de co-ocorrência
│   ├── cluster_analysis.py        # detecção de clusters
│   └── main.py                    # script principal
├── notebooks/                     # análises exploratórias
├── requirements.txt
└── README.md
```

## 🚀 Como Usar

### 1. Instalação

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente (Windows)
.venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Preparar os Dados

Crie o arquivo `data/lotofacil_sorteios.csv` com o seguinte formato:

```csv
concurso,data,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15
3200,2025-12-30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
3199,2025-12-29,2,3,5,7,8,10,11,13,15,17,19,21,22,24,25
```

**Requisitos do CSV:**
- Cabeçalho obrigatório
- 15 colunas com os números sorteados (b1 a b15)
- Números devem estar entre 1 e 25
- Sem duplicatas dentro de cada sorteio

### 3. Executar a Análise

```bash
python src/main.py
```

## 📊 Saídas Geradas

### `heatmap_5x5.csv`
Matriz 5×5 mostrando frequência de cada número:
```
       col_1  col_2  col_3  col_4  col_5
linha_1    150    142    138    145    140
linha_2    148    151    149    143    147
...
```

### `metrics_por_sorteio.csv`
Métricas espaciais de cada sorteio:
- `mean_to_centroid`: dispersão média
- `mean_pair_dist`: distância média entre números
- `edge_count`: números nas bordas
- `center_count`: números no centro

### `top_pares_coocorrencia.csv`
Pares que mais saem juntos:
```
a,b,count
2,3,85
5,7,82
...
```

### `clusters_dbscan_manhattan.csv`
Clusters identificados no grid:
```
number,freq,row,col,cluster
13,152,3,3,0
14,150,3,4,0
7,148,2,2,1
...
```
- `cluster=-1`: número não pertence a nenhum cluster (ruído)
- `cluster>=0`: ID do cluster

## 🎲 Ferramentas de Análise de Apostas

O projeto agora inclui ferramentas para analisar suas apostas:

### 📱 Análise Rápida de Apostas

- **`analisar_concurso_3610.py`**: Analise rapidamente seus jogos contra o resultado do concurso 3610
- **`analisar_apostas_imagem.py`**: Extraia números de imagens usando OCR e analise contra qualquer concurso

Veja o [Guia de Análise de Apostas](GUIA_ANALISE_APOSTAS.md) para instruções detalhadas.

#### Exemplo de Uso Rápido:

```bash
# Análise rápida do concurso 3610
python analisar_concurso_3610.py

# Análise com extração de imagem
python analisar_apostas_imagem.py minha_aposta.jpg 3610 "01,03,05,07,08,10,13,14,17,20,21,22,23,24,25"
```

## 🎯 Próximos Passos

- [ ] Gerador inteligente de apostas baseado em clusters
- [ ] Simulador histórico de apostas
- [ ] Análise temporal (tendências por período)
- [ ] Visualizações interativas (heatmaps, grafos)
- [ ] Detecção de padrões temporais (sazonalidade)
- [ ] Análise de redes de co-ocorrência

## 📚 Dependências

- **pandas**: manipulação de dados
- **numpy**: computação numérica
- **scikit-learn**: algoritmos de clustering
- **matplotlib**: visualizações (opcional)
- **seaborn**: visualizações estatísticas (opcional)
- **networkx**: grafos de co-ocorrência
- **tqdm**: barras de progresso
- **Pillow**: processamento de imagens (para análise de apostas)
- **pytesseract**: OCR para extração de números de imagens (para análise de apostas)

## 🤝 Contribuindo

Este é um projeto de análise estatística. Contribuições são bem-vindas!

## 📋 Changelog

Veja [CHANGELOG.md](CHANGELOG.md) para histórico detalhado de mudanças.

## ⚠️ Aviso Legal

Este projeto é apenas para fins educacionais e de análise estatística. Não garante resultados em apostas reais. Jogue com responsabilidade.

## 📝 Licença

Projeto de uso educacional e pessoal.

---

**Tag do projeto**: `#lotofacil`

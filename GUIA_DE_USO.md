# 📊 Guia Completo de Uso - Análise da Lotofácil

## ✅ O que foi criado:

### 📂 Estrutura do Projeto
```
lotofacil/
├── data/
│   └── lotofacil_sorteios.csv          # 3.575 sorteios
├── out/                                  # Resultados das análises
│   ├── heatmap_grid.png                 # 🎨 Heatmap visual do grid 5×5
│   ├── freq_barras.png                  # 📊 Frequência por número
│   ├── linhas_colunas.png               # 📐 Comparação linhas/colunas
│   ├── rede_coocorrencia.png            # 🔗 Grafo de pares
│   ├── metricas_espaciais.png           # 📈 Distribuições
│   ├── relatorio_resumo.txt             # 📄 Relatório completo
│   ├── numeros_quentes_frios.csv        # 🌡️ Classificação quente/frio
│   ├── tendencias_temporais.csv         # 📈 Tendências ao longo do tempo
│   ├── pares_forca.csv                  # ⭐ Super pares (força > 95%)
│   ├── clusters_*.csv                   # 🎯 Diferentes análises de clusters
│   └── bias_borda_centro.json           # 📐 Análise borda vs centro
├── src/
│   ├── main.py                          # Script principal
│   ├── advanced_main.py                 # Análises avançadas
│   └── visualizations.py                # Módulo de gráficos
└── notebooks/
    └── analise_lotofacil.ipynb          # Notebook interativo
```

## 🚀 Como Usar

### 1️⃣ Análise Completa (Padrão)
```powershell
.venv\Scripts\activate
python src/main.py
```

**Gera**:
- ✅ Heatmap do grid 5×5
- ✅ Frequências por número
- ✅ Comparação linhas/colunas
- ✅ Rede de co-ocorrência (top 30 pares)
- ✅ Métricas espaciais
- ✅ Relatório em texto

### 2️⃣ Análises Avançadas
```powershell
.venv\Scripts\activate
python src/advanced_main.py
```

**Gera**:
- ✅ Classificação quente/frio/médio
- ✅ Tendências temporais (janela de 500 sorteios)
- ✅ Micro-clusters (3 algoritmos diferentes)
- ✅ Super pares (força > 95%)
- ✅ Análise de bias borda/centro

### 3️⃣ Notebook Jupyter (Interativo)
```powershell
.venv\Scripts\activate
jupyter notebook notebooks/analise_lotofacil.ipynb
```

Ou abra direto no VS Code e execute célula por célula!

## 📊 Principais Resultados

### 🔥 Números Mais Quentes
| # | Número | Frequência | Desvio |
|---|--------|------------|--------|
| 1 | **20** | 2.232 | +4.06% |
| 2 | **10** | 2.219 | +3.45% |
| 3 | **25** | 2.219 | +3.45% |
| 4 | **11** | 2.199 | +2.52% |
| 5 | **13** | 2.178 | +1.54% |

### ❄️ Números Mais Frios
| # | Número | Frequência | Desvio |
|---|--------|------------|--------|
| 1 | **16** | 2.046 | -4.62% |
| 2 | **8**  | 2.072 | -3.40% |
| 3 | **23** | 2.088 | -2.66% |
| 4 | **6**  | 2.095 | -2.33% |
| 5 | **17** | 2.108 | -1.72% |

### ⭐ Top 5 Super Pares (Força > 95%)
1. **[11 + 20]**: 1.362 vezes (100.0%)
2. **[10 + 25]**: 1.355 vezes (99.5%)
3. **[13 + 20]**: 1.351 vezes (99.2%)
4. **[10 + 20]**: 1.348 vezes (99.0%)
5. **[20 + 25]**: 1.341 vezes (98.5%)

### 📈 Tendências Atuais
**Em Alta** (últimos 500 sorteios):
- 📈 20: +8.14%
- 📈 8: +6.75%
- 📈 10: +6.19%
- 📈 25: +6.17%

**Em Baixa**:
- 📉 11: -6.12%
- 📉 19: -5.62%
- 📉 23: -5.33%

### 📐 Padrões Espaciais
- **Coluna 5** (números 5, 10, 15, 20, 25): **MAIS QUENTE** (10.948 aparições)
- **Linha 3** (números 11-15): **MAIS QUENTE** (10.839 aparições)
- **Linha 4** (números 16-20): **MAIS FRIA** (10.648 aparições)
- **Bias borda**: +0.21% (ligeiramente acima do esperado)

## 💡 Insights e Estratégias

### ✅ Recomendações Baseadas em Dados:

1. **Priorize a Coluna 5**
   - Números: 5, 10, 15, 20, 25
   - Especialmente: 10, 20, 25 (os 3 estão no top 5 quentes E em alta)

2. **Use Super Pares**
   - Combine [11+20], [10+25], [13+20]
   - 43 pares têm força > 95%

3. **Balanceamento Espacial**
   - 9-10 números nas bordas (média: 9.63)
   - 5-6 números no centro (média: 5.37)

4. **Evite Concentração na Linha 4**
   - Números 16-20 são menos frequentes
   - Exceto o 20 (que é outlier positivo)

5. **Aproveite Tendências**
   - Números em alta: 20, 8, 10, 25
   - Evite números em queda: 11, 19, 23

### 📋 Exemplo de Jogo Otimizado (15 números):
```
Baseado na análise:
1, 3, 4, 5, 8, 10, 11, 13, 14, 20, 22, 24, 25

Características:
- 5 números da coluna 5 ✓
- Inclui os top 3 mais quentes (20, 10, 25) ✓
- Contém 3 super pares ([11+20], [10+25], [13+20]) ✓
- Balanceado: 9 bordas, 6 centro ✓
- Evita linha 4 (exceto 20) ✓
```

## 🔄 Atualizando a Análise

Quando tiver novos sorteios:

1. Atualize o arquivo `data/lotofacil_sorteios.csv` (ou `.xlsx`)
2. Rode novamente:
```powershell
.venv\Scripts\activate
python src/main.py
python src/advanced_main.py
```

## 📸 Visualizações Geradas

Todas as imagens estão em `out/`:
- **heatmap_grid.png** - Mapa de calor 5×5 com números
- **freq_barras.png** - Barras coloridas (verde=quente, vermelho=frio)
- **linhas_colunas.png** - Comparação de linhas e colunas
- **rede_coocorrencia.png** - Grafo com os 30 pares mais fortes
- **metricas_espaciais.png** - 5 distribuições estatísticas

## ⚠️ Aviso Legal

Esta é uma **análise estatística para fins educacionais**. Não há garantia de resultados em apostas reais. A Lotofácil é um jogo de sorte e os resultados passados não garantem resultados futuros.

**Jogue com responsabilidade!**

---

## 🆘 Precisa de Ajuda?

Se encontrar algum problema:
1. Verifique se o ambiente virtual está ativado
2. Confirme que todas as dependências estão instaladas: `pip install -r requirements.txt`
3. Veja os logs de erro para identificar o problema

**Divirta-se analisando! 🎯**

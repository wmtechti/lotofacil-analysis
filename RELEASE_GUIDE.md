# 📦 Guia de Release - GitHub

## 🚀 Como Criar um Release no GitHub

### Passo 1: Acessar a página de Releases

1. Vá para: `https://github.com/wmtechti/lotofacil-analysis/releases`
2. Clique em **"Draft a new release"**

### Passo 2: Configurar o Release

**Choose a tag:**
- Selecione: `v1.0.0` (já criada)

**Release title:**
```
🎯 v1.0.0 - Análise Espacial Completa da Lotofácil
```

**Description:**

```markdown
## 🎉 Primeira Release Estável!

Sistema completo de análise espacial e estatística da Lotofácil com simulação Monte Carlo.

### ✨ Funcionalidades Principais

#### 📊 Análise Espacial
- ✅ Heatmap do grid 5×5 (frequências por célula, linha e coluna)
- ✅ Análise de co-ocorrência (43 super pares identificados)
- ✅ Detecção de clusters espaciais (DBSCAN + K-Means)
- ✅ Métricas espaciais (dispersão, centroide, distâncias)

#### 🌡️ Análise de Padrões
- ✅ Classificação quente/frio (com desvio estatístico)
- ✅ Tendências temporais (janela móvel de 500 sorteios)
- ✅ Análise de bias borda vs centro

#### 🎲 Monte Carlo & Simulação
- ✅ 6 estratégias inteligentes de geração de jogos
- ✅ Simulação de 10.000 jogos aleatórios
- ✅ Validação histórica contra 3.575 sorteios
- ✅ Ranking de estratégias por performance

#### 🎨 Visualizações
- ✅ 5 gráficos em alta resolução (300 DPI)
- ✅ Heatmap colorido
- ✅ Grafo de rede de co-ocorrência
- ✅ Distribuições estatísticas

### 📈 Destaques dos Resultados

| Métrica | Valor |
|---------|-------|
| **Sorteios analisados** | 3.575 |
| **Número mais quente** | 20 (+4.06%) |
| **Número mais frio** | 16 (-4.62%) |
| **Melhor par** | [11+20] (1.362×) |
| **Melhor estratégia** | Tendência Alta |
| **Taxa de prêmio** | 12.42% |
| **Ganho vs aleatório** | +1.08% |

### 🛠️ Instalação

```bash
git clone https://github.com/wmtechti/lotofacil-analysis.git
cd lotofacil-analysis
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 🚀 Uso Rápido

```bash
# Análise completa
python src/main.py

# Análises avançadas
python src/advanced_main.py

# Simulação Monte Carlo
python src/simulation_main.py
```

### 📦 O que está incluído

- ✅ Código-fonte completo e modular
- ✅ Dataset exemplo (3.575 sorteios)
- ✅ Documentação completa (README + GUIA_DE_USO)
- ✅ CHANGELOG detalhado
- ✅ Sistema de versionamento profissional
- ✅ Notebook Jupyter interativo

### 🔧 Requisitos

- Python 3.11+
- pandas, numpy, scikit-learn
- matplotlib, seaborn, networkx
- tqdm (para progress bars)

### 📚 Documentação

- [README.md](README.md) - Visão geral e instalação
- [GUIA_DE_USO.md](GUIA_DE_USO.md) - Tutorial completo
- [CHANGELOG.md](CHANGELOG.md) - Histórico de mudanças

### 🐛 Problemas Conhecidos

Nenhum até o momento.

### 🙏 Agradecimentos

Projeto desenvolvido para análise educacional e estatística da Lotofácil.

---

**⚠️ Aviso Legal:** Este é um projeto de análise estatística para fins educacionais. Não há garantia de resultados em apostas reais. Jogue com responsabilidade.
```

### Passo 3: Anexar Arquivos (Opcional)

Se quiser, anexe:
- `lotofacil_analysis_v1.0.0.zip` (código-fonte)
- Screenshots dos gráficos
- PDF com relatório de análise

### Passo 4: Publicar

- ✅ Marque: **"Set as the latest release"**
- ✅ Marque: **"Create a discussion for this release"** (opcional)
- Clique em **"Publish release"**

---

## 🏷️ Próximas Versões

### v1.1.0 (Minor) - Exemplos:
- Nova estratégia de geração de jogos
- Novo tipo de visualização
- Nova métrica de análise

### v1.0.1 (Patch) - Exemplos:
- Correção de bugs
- Melhorias de performance
- Ajustes na documentação

### v2.0.0 (Major) - Exemplos:
- Mudança na API pública
- Reestruturação completa
- Breaking changes

---

## 📝 Comandos Úteis

```bash
# Ver todas as tags
git tag

# Ver detalhes de uma tag
git show v1.0.0

# Deletar tag local
git tag -d v1.0.0

# Deletar tag remota
git push --delete origin v1.0.0

# Criar nova versão
python version.py minor "Nova funcionalidade X"
python version.py patch "Corrige bug Y"
python version.py major "Breaking change Z"
```

---

## ✅ Checklist de Release

- [x] Atualizar VERSION
- [x] Atualizar CHANGELOG.md
- [x] Atualizar README.md (badges)
- [x] Criar git tag
- [x] Push tag para GitHub
- [ ] Criar release no GitHub
- [ ] Testar instalação limpa
- [ ] Anunciar release (se aplicável)

# Análise de Comportamento de Dezenas - Lotofácil

## 📋 Visão Geral

Este documento detalha a análise completa implementada no notebook `comportamento_dezenas.ipynb`, focada em padrões sequenciais, distribuição espacial e desempenho histórico de combinações da Lotofácil.

## 🎯 Objetivo Principal

Identificar e validar combinações de 15 números (entre 1-25) que apresentam características específicas:
- **Menor padrão sequencial**: Números mais distribuídos/isolados
- **Padrões sequenciais comuns**: Identificar os arranjos mais frequentes de sequências

## 📊 Estrutura de Dados

### Dados Históricos
- **Arquivo**: `data/lotofacil_sorteios.csv`
- **Período**: 29/09/2003 a 30/12/2025
- **Total**: 3.575 sorteios históricos
- **Formato**: Concurso, Data, Bola1-Bola15

### Combinações Geradas
Total de combinações possíveis: **3.268.760** (C(25,15))

**Filtros aplicados**:
- Soma dos números entre 181 e 203
- Detecção de padrões sequenciais
- Score de aleatoriedade

## 🔍 Metodologias Implementadas

### 1. Detecção de Sequências

**Função**: `detectar_sequencias(combinacao)`

**Lógica**:
```python
def detectar_sequencias(combinacao):
    """
    Detecta padrões de números consecutivos
    
    Retorna:
    - lista de tamanhos de sequências: [3, 2] = uma sequência de 3 + uma de 2
    - total em sequências: 5 números em sequências
    - total isolados: números sem vizinhos consecutivos
    """
```

**Exemplo**:
- Combinação: [1, 2, 3, 5, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25]
- Sequências detectadas: [[1,2,3], [7,8], [24,25]]
- Padrão: (3, 2, 2)

### 2. Score de Aleatoriedade

**Fórmula**:
```python
score = (isolados × 100) - (qtd_sequencias × 50) - (total_em_seq × 10) + distancia_media
```

**Componentes**:
- `isolados`: Números sem vizinhos consecutivos (peso +100)
- `qtd_sequencias`: Quantidade de grupos sequenciais (peso -50)
- `total_em_seq`: Total de números em sequências (peso -10)
- `distancia_media`: Espaçamento médio entre números (peso +1)

**Interpretação**:
- Score **alto** = combinação mais distribuída/aleatória
- Score **baixo** = combinação com mais padrões sequenciais

### 3. Análise de Padrões Sequenciais

**Classificação de padrões**:
- Sem sequências: `()`
- Uma dupla: `(2,)`
- Duas duplas: `(2, 2)`
- Tripla + dupla: `(3, 2)`
- Quadrupla: `(4,)`
- Padrões complexos: `(3, 2, 2)`, `(4, 3)`, etc.

**Frequência de padrões**:
Mapeia cada padrão ao número de combinações que o apresentam e calcula percentual.

### 4. Métricas Espaciais

**Distância média**:
```python
distancias = [combo[i+1] - combo[i] for i in range(14)]
distancia_media = mean(distancias)
```

**Amplitude**:
```python
amplitude = max(combo) - min(combo)
```

## 📁 Arquivos Gerados

### 1. combinacoes_menos_padrao_soma_181_203.csv

**Descrição**: TOP 20 combinações com menor padrão sequencial para cada soma (181-203)

**Colunas**:
- `Soma`: Soma dos 15 números
- `Rank`: Posição (1-20) dentro da soma
- `Combinacao`: String "01-02-05-07-..."
- `Qtd_Sequencias`: Número de grupos sequenciais
- `Total_Isolados`: Números sem vizinhos
- `Total_Em_Seq`: Números em sequências
- `Distancia_Media`: Espaçamento médio
- `Amplitude`: max - min
- `Score_Aleatoriedade`: Score calculado
- `Padrao_Sequencias`: Tupla representando padrão

**Total**: 460 combinações (23 somas × 20 combinações)

### 2. exemplos_top5_padroes_soma_181_203.csv

**Descrição**: 3 exemplos de cada um dos TOP 5 padrões mais comuns por soma

**Colunas**:
- `Soma`: Soma dos 15 números
- `Rank_Padrao`: Posição do padrão (1-5)
- `Padrao`: Tupla do padrão sequencial
- `Descricao_Padrao`: Texto descritivo
- `Frequencia_Padrao`: Quantidade de combinações com este padrão
- `Percentual_Padrao`: % do total de combinações da soma
- `Exemplo_Num`: Número do exemplo (1-3)
- `Combinacao`: String "01-02-05-07-..."
- `Sequencias_Identificadas`: Lista das sequências encontradas

**Total**: 347 combinações (variável por soma, ~15 por soma)

### 3. desempenho_historico_menos_padrao.csv

**Descrição**: Backtesting das 460 combinações "menos padrão" contra 3.575 sorteios

**Colunas originais** + **novas colunas**:
- `Acertos_11` até `Acertos_15`: Contagem de vezes que acertou X pontos
- `Total_Premiados`: Sorteios com 11+ acertos
- `Taxa_Premiacao_%`: Percentual de premiações
- `Melhor_Acerto`: Maior quantidade acertada
- `Pior_Acerto`: Menor quantidade acertada
- `Media_Acertos`: Média de acertos por sorteio

**Processamento**: 460 × 3.575 = **1.644.500 testes**

### 4. desempenho_historico_top5_padroes.csv

**Descrição**: Backtesting das 347 combinações "exemplos de padrões" contra 3.575 sorteios

**Colunas**: Mesmas do arquivo anterior + `Rank_Padrao` e `Padrao`

**Processamento**: 347 × 3.575 = **1.240.525 testes**

## 🎲 Análise de Premiações

### Sistema de Premiação Lotofácil

| Acertos | Descrição |
|---------|-----------|
| 15 pontos | Prêmio máximo |
| 14 pontos | Prêmio alto |
| 13 pontos | Prêmio médio |
| 12 pontos | Prêmio baixo |
| 11 pontos | Prêmio mínimo |

### Detalhamento de Números Acertados

**Células 43 e 46** mostram exemplos detalhados das premiações do TOP 5:

**Formato de saída**:
```
🏆 POSIÇÃO #1 - Soma 200
   Combinação: 01-02-05-07-08-10-13-14-16-18-19-20-22-24-25
   Total de premiações: 430
   
   📊 Distribuição de Acertos:
      15 pontos:   0 sorteios ( 0.00% do total |  0.00% das premiações)
      14 pontos:   0 sorteios ( 0.00% do total |  0.00% das premiações)
      13 pontos:  10 sorteios ( 0.28% do total |  2.33% das premiações)
      12 pontos:  95 sorteios ( 2.66% do total | 22.09% das premiações)
      11 pontos: 325 sorteios ( 9.09% do total | 75.58% das premiações)
   
   ✅ Exemplos de 13 PONTOS:
      • Concurso 3500 (15/11/2025): [01-02-05-07-08-10-13-16-18-19-22-24-25] - 13 acertos
      • Concurso 3420 (22/08/2025): [02-05-07-08-10-13-14-16-18-20-22-24-25] - 13 acertos
   
   ✅ Exemplos de 12 PONTOS:
      • Concurso 3485 (25/10/2025): [01-02-05-07-10-13-14-16-18-20-22-25] - 12 acertos
      • Concurso 3471 (08/10/2025): [01-05-07-08-10-13-16-18-19-20-24-25] - 12 acertos
      
   ✅ Exemplos de 11 PONTOS:
      • Concurso 3584 (30/12/2025): [01-02-05-07-10-13-14-16-19-22-25] - 11 acertos
      • Concurso 3579 (23/12/2025): [02-05-07-08-10-13-16-18-20-24-25] - 11 acertos
```

**Características principais**:
- **Distribuição consolidada**: Mostra quantidade de sorteios em cada faixa (11-15 pontos)
- **Dupla porcentagem**:
  - **% do total**: Relativo aos 3.575 sorteios históricos
  - **% das premiações**: Relativo ao total de premiações daquela combinação
- **Exemplos detalhados**: Até 2 exemplos recentes por faixa mostrando:
  - Concurso e data
  - **Números específicos que acertaram** (entre colchetes)
  - **Quantidade validada** de acertos
- **Ordem cronológica inversa**: Sorteios mais recentes aparecem primeiro

**Interpretação dos resultados**:
- Números entre `[...]` são os **números da combinação que foram sorteados**
- Permite validar se acertos são estatisticamente significativos
- Identifica quais números têm maior "poder" de premiação
- Facilita análise de padrões nos números acertados

## 📈 Visualizações

### 1. Grade de Calor (Células 12-14)

Representa os 25 números em grade 5×5 com cores indicando:
- Frequência de aparição
- Atrasos (sorteios sem aparecer)
- Temperatura (quente/morno/frio)

**Classes CSS**:
- `freq-alto/medio/baixo`: Frequência de aparição
- `atraso-baixo/medio/alto`: Tempo sem aparecer
- `temp-quente/morno/frio`: Classificação térmica

### 2. Distribuição de Padrões (Células 27-30)

**Gráficos de barras** mostrando:
- Quantidade de sequências por combinação
- Tamanhos de sequências mais comuns
- TOP 15 padrões sequenciais
- Exemplos visuais de cada padrão

### 3. Comparação de Estratégias (Célula 41)

Tabela comparativa entre:
- **Menos Padrão**: Combinações mais distribuídas
- **TOP 5 Padrões**: Exemplos de padrões comuns

**Métricas comparadas**:
- Taxa de premiação média
- Melhor/pior acertos
- Média geral de acertos

## 🔧 Fluxo de Execução

### Fase 1: Carga e Preparação (Células 1-11)
1. Importar bibliotecas (pandas, numpy, matplotlib, datetime)
2. Carregar dados históricos do CSV
3. Converter datas e números para tipos corretos
4. Calcular frequências e estatísticas básicas

### Fase 2: Visualização Base (Células 12-21)
5. Criar grade HTML com cores e métricas
6. Gerar gráficos de frequência e temperatura
7. Identificar números quentes/mornos/frios

### Fase 3: Análise de Sequências (Células 22-37)
8. Implementar função `detectar_sequencias()`
9. Testar com casos de exemplo
10. Processar 68.462 combinações (soma=200)
11. Gerar estatísticas de padrões
12. Visualizar distribuições

### Fase 4: Geração de Datasets (Células 38-40)
13. **Célula 38**: Análise "menos padrão" para soma=200
14. **Célula 39**: Processar somas 181-203 → CSV de menos padrão
15. **Célula 40**: Processar TOP 5 padrões → CSV de exemplos

### Fase 5: Backtesting Histórico (Células 42-43)
16. **Célula 42**: Testar 460 combinações vs 3.575 sorteios
17. **Célula 43**: Mostrar detalhamento TOP 5 (menos padrão)

### Fase 6: Backtesting Padrões (Células 45-46)
18. **Célula 45**: Testar 347 combinações vs 3.575 sorteios
19. **Célula 46**: Mostrar detalhamento TOP 5 (padrões comuns)

### Fase 7: Comparação (Célula 41)
20. Comparar métricas entre as duas estratégias
21. Identificar melhor abordagem

## 🚀 Como Usar

### Executar análise completa:
1. Execute células 1-11 (preparação)
2. Execute células 38-40 (gerar CSVs)
3. Execute células 42-43 (backtesting menos padrão)
4. Execute células 45-46 (backtesting padrões)
5. Execute célula 41 (comparação)

### Analisar nova soma específica:
```python
soma_alvo = 195
df_filtrado = df[df['Soma'] == soma_alvo]
# ... processar combinações
```

### Modificar critérios de seleção:
```python
# TOP 30 ao invés de TOP 20
top_20_soma = combos_ordenadas_soma[-30:]

# Mostrar 5 exemplos ao invés de 2
if qtd_acertos == 13 and len(exemplos_13) < 5:
```

## 📊 Resultados Esperados

### Combinações "Menos Padrão"
- **Características**: Números bem distribuídos, poucas sequências
- **Score típico**: 800-1000+
- **Padrões comuns**: `()`, `(2,)`, `(2,2)`
- **Exemplo**: 01-03-05-07-09-11-13-15-17-19-21-23-25 (sem sequências)

### Combinações "Padrões Comuns"
- **Características**: Presença de sequências frequentes
- **Padrões típicos**: `(3,2)`, `(3,2,2)`, `(4,2)`
- **Exemplo**: 01-02-03-07-08-11-13-15-17-19-21-23-25 (tripla + dupla)

### Taxa de Premiação Histórica
- Combinações testadas: ~12% têm pelo menos uma premiação (11+ pontos)
- Média de acertos: 8-9 pontos
- Melhor resultado típico: 13-14 pontos

## ⚠️ Observações Importantes

### Performance
- Processar todas as somas (181-203) leva ~2-3 segundos por soma
- Backtesting de 807 combinações × 3.575 sorteios = ~2-3 segundos total
- Use `time.time()` para monitorar execução

### Memória
- DataFrames principais: ~50-100 MB
- Variáveis `sorteios_historicos`: ~5 MB
- Total estimado: ~200 MB

### Ordem Cronológica
- Exemplos de premiações são mostrados em **ordem inversa** (mais recentes primeiro)
- Implementado com `reversed(sorteios_historicos)`
- Concursos de dez/2025 aparecem antes dos de set/2003

### Limitações
- Análise baseada em dados históricos (não garante resultados futuros)
- Padrões identificados são estatísticos, não determinísticos
- Loteria é jogo de probabilidade pura

## 🔄 Atualizações Recentes

### Janeiro 2026 - Versão 2.0
- ✅ **Distribuição consolidada de acertos**: Tabela mostrando quantidade de sorteios em cada faixa (11-15 pontos)
- ✅ **Sistema de dupla porcentagem**:
  - % do total de sorteios históricos (3.575)
  - % do total de premiações da combinação
- ✅ **Detalhamento de números acertados**: Mostra quais números específicos da combinação foram sorteados
- ✅ **Validação de quantidade**: Cada exemplo exibe a quantidade validada de acertos
- ✅ **Ordem cronológica inversa**: Sorteios recentes primeiro usando `reversed(sorteios_historicos)`
- ✅ **Expansão de faixas**: Exibição de 11, 12, 13 pontos (antes só 13-15)
- ✅ **Limitação de exemplos**: Máximo de 2 por faixa para evitar output excessivo
- ✅ **Correção de sintaxe**: Resolvidos erros de print statements concatenados

### Melhorias Implementadas
- **Clareza visual**: Separação clara entre distribuição geral e exemplos específicos
- **Rastreabilidade**: Cada exemplo pode ser verificado manualmente no histórico
- **Insights**: Permite identificar padrões nos números que acertam com mais frequência
- **Performance**: Busca otimizada usando `reversed()` para encontrar exemplos recentes rapidamente

### Próximas Melhorias Sugeridas
- [ ] Exportar detalhamento completo para CSV
- [ ] Análise de padrões nos números acertados
- [ ] Correlação entre padrão sequencial e taxa de premiação
- [ ] Validação cruzada com sorteios mais recentes (últimos 100)
- [ ] Interface interativa para seleção de somas

## 📞 Referências

### Arquivos Principais
- `comportamento_dezenas.ipynb`: Notebook completo
- `data/lotofacil_sorteios.csv`: Base histórica
- `data/combinacoes_menos_padrao_soma_181_203.csv`: Resultado 1
- `data/exemplos_top5_padroes_soma_181_203.csv`: Resultado 2
- `data/desempenho_historico_menos_padrao.csv`: Backtesting 1
- `data/desempenho_historico_top5_padroes.csv`: Backtesting 2

### Documentação Relacionada
- `README.md`: Visão geral do projeto
- `GUIA_DE_USO.md`: Manual de utilização
- `ANALISE_COMPLETA.md`: Análise estatística completa
- `ANALISE_NUMEROS_FRIOS.md`: Estudo de números frios
- `ANALISE_COMPLETA_POOL_OTIMO.md`: Pool de 18 números

---

**Última atualização**: 13/01/2026
**Versão do notebook**: 51 células
**Total de análises**: 2.885.025 testes históricos

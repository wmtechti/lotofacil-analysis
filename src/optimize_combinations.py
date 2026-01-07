"""
Otimizador de Combinações - 18 Números Mais Quentes

Gera combinações otimizadas dos 18 números que mais saíram,
removendo jogos improváveis e mantendo custo abaixo de R$ 1.000.
"""

import pandas as pd
import numpy as np
from itertools import combinations
from pathlib import Path
import json


class CombinationOptimizer:
    """Otimizador de combinações para reduzir custo"""
    
    def __init__(self, budget=1000, price_per_game=3.50):
        self.budget = budget
        self.price_per_game = price_per_game
        self.max_games = int(budget / price_per_game)
        self.hot_numbers = []
        self.super_pairs = []
        self.all_combinations = []
        self.optimized_games = []
        
    def load_hot_numbers(self, top_n=18):
        """Carregar os N números mais quentes"""
        print("=" * 80)
        print(f"🔥 OTIMIZADOR DE COMBINAÇÕES - {top_n} NÚMEROS MAIS QUENTES")
        print("=" * 80)
        
        df = pd.read_csv('out/lotofacil/numeros_quentes_frios.csv')
        df_sorted = df.sort_values('freq', ascending=False)
        
        self.hot_numbers = list(df_sorted.head(top_n)['numero'].values)
        
        print(f"\n📊 OS {top_n} NÚMEROS MAIS QUENTES:")
        print("-" * 80)
        for idx, row in df_sorted.head(top_n).iterrows():
            print(f"  {row['numero']:2d} - Freq: {row['freq']:4d} | Desvio: {row['desvio_%']:+6.2f}% | {row['categoria']}")
        
        # Calcular todas as combinações possíveis
        total_combinations = self._calculate_combinations(top_n, 15)
        total_cost = total_combinations * self.price_per_game
        
        print(f"\n💰 ANÁLISE DE CUSTO:")
        print(f"  • Total de combinações possíveis: {total_combinations:,}")
        print(f"  • Custo total (fechar): R$ {total_cost:,.2f}")
        print(f"  • Orçamento disponível: R$ {self.budget:,.2f}")
        print(f"  • Máximo de jogos: {self.max_games}")
        print(f"  • Redução necessária: {(1 - self.max_games/total_combinations)*100:.1f}%")
        
    def _calculate_combinations(self, n, r):
        """Calcular C(n, r) - combinações"""
        from math import factorial
        return factorial(n) // (factorial(r) * factorial(n - r))
    
    def load_super_pairs(self):
        """Carregar super pares para filtro de qualidade"""
        df_pairs = pd.read_csv('out/lotofacil/pares_forca.csv')
        super_pairs_df = df_pairs[df_pairs['categoria'] == '⭐⭐⭐ Super Par']
        
        self.super_pairs = [
            (int(row['a']), int(row['b'])) 
            for _, row in super_pairs_df.iterrows()
            if int(row['a']) in self.hot_numbers and int(row['b']) in self.hot_numbers
        ]
        
        print(f"\n🔗 Super pares disponíveis entre os 18 números: {len(self.super_pairs)}")
        if len(self.super_pairs) > 0:
            print(f"  Top 5: {self.super_pairs[:5]}")
    
    def number_to_coord(self, num):
        """Converter número para coordenada no grid 5×5"""
        num = num - 1
        linha = num // 5
        coluna = num % 5
        return (linha, coluna)
    
    def calculate_dispersion(self, numbers):
        """Calcular dispersão espacial"""
        coords = [self.number_to_coord(n) for n in numbers]
        
        centroid_row = np.mean([c[0] for c in coords])
        centroid_col = np.mean([c[1] for c in coords])
        
        distances = [
            np.sqrt((c[0] - centroid_row)**2 + (c[1] - centroid_col)**2) 
            for c in coords
        ]
        
        return np.mean(distances)
    
    def count_adjacent_pairs(self, numbers):
        """Contar pares adjacentes"""
        coords = set(self.number_to_coord(n) for n in numbers)
        adjacent_count = 0
        
        for linha, coluna in coords:
            neighbors = [
                (linha - 1, coluna),
                (linha + 1, coluna),
                (linha, coluna - 1),
                (linha, coluna + 1)
            ]
            
            for neighbor in neighbors:
                if neighbor in coords:
                    adjacent_count += 1
        
        return adjacent_count // 2
    
    def has_super_pair(self, numbers):
        """Verificar se contém pelo menos 1 super par"""
        numbers_set = set(numbers)
        for a, b in self.super_pairs:
            if a in numbers_set and b in numbers_set:
                return True
        return False
    
    def check_regional_balance(self, numbers):
        """Verificar equilíbrio regional (linhas e colunas)"""
        coords = [self.number_to_coord(n) for n in numbers]
        
        line_counts = [0] * 5
        for linha, _ in coords:
            line_counts[linha] += 1
        
        col_counts = [0] * 5
        for _, coluna in coords:
            col_counts[coluna] += 1
        
        # Verificar se distribuição é razoável (não concentrado)
        line_balanced = all(1 <= count <= 5 for count in line_counts)
        col_balanced = all(1 <= count <= 5 for count in col_counts)
        
        return line_balanced and col_balanced
    
    def score_game(self, numbers):
        """Pontuar jogo baseado em critérios de qualidade"""
        score = 0
        
        # Critério 1: Dispersão espacial (0-3 pontos)
        dispersion = self.calculate_dispersion(numbers)
        if dispersion >= 2.2:
            score += 3
        elif dispersion >= 1.8:
            score += 2
        elif dispersion >= 1.5:
            score += 1
        
        # Critério 2: Baixa contiguidade (0-3 pontos)
        adjacent = self.count_adjacent_pairs(numbers)
        if adjacent <= 1:
            score += 3
        elif adjacent <= 2:
            score += 2
        elif adjacent <= 3:
            score += 1
        
        # Critério 3: Super par presente (0-2 pontos)
        if self.has_super_pair(numbers):
            score += 2
        
        # Critério 4: Equilíbrio regional (0-2 pontos)
        if self.check_regional_balance(numbers):
            score += 2
        
        return score
    
    def filter_and_rank_combinations(self):
        """Filtrar e rankear combinações"""
        print(f"\n🔬 FILTRANDO E RANQUEANDO COMBINAÇÕES...")
        print(f"  Gerando todas as {self._calculate_combinations(18, 15):,} combinações...")
        
        # Gerar todas as combinações
        all_combos = list(combinations(self.hot_numbers, 15))
        
        print(f"  Pontuando {len(all_combos):,} jogos...")
        
        # Pontuar cada combinação
        scored_games = []
        for i, combo in enumerate(all_combos):
            if i % 100 == 0:
                print(f"    Processando: {i:,} / {len(all_combos):,} ({i/len(all_combos)*100:.1f}%)", end='\r')
            
            score = self.score_game(combo)
            
            # Filtro mínimo: score >= 5 (pelo menos metade dos pontos)
            if score >= 5:
                scored_games.append({
                    'numbers': sorted(combo),
                    'score': score,
                    'dispersion': self.calculate_dispersion(combo),
                    'adjacent_pairs': self.count_adjacent_pairs(combo),
                    'has_super_pair': self.has_super_pair(combo)
                })
        
        print(f"\n  ✅ Jogos aprovados (score ≥ 5): {len(scored_games):,}")
        
        # Ordenar por score (maior para menor)
        scored_games.sort(key=lambda x: x['score'], reverse=True)
        
        # Selecionar os melhores jogos dentro do orçamento
        self.optimized_games = scored_games[:self.max_games]
        
        print(f"\n📊 RESULTADO DA OTIMIZAÇÃO:")
        print(f"  • Jogos selecionados: {len(self.optimized_games)}")
        print(f"  • Custo total: R$ {len(self.optimized_games) * self.price_per_game:.2f}")
        print(f"  • Economia: R$ {(len(all_combos) - len(self.optimized_games)) * self.price_per_game:,.2f}")
        print(f"  • Score médio: {np.mean([g['score'] for g in self.optimized_games]):.2f} / 10")
        
        # Estatísticas
        print(f"\n📈 ESTATÍSTICAS DOS JOGOS SELECIONADOS:")
        print(f"  • Score mínimo: {min(g['score'] for g in self.optimized_games)}")
        print(f"  • Score máximo: {max(g['score'] for g in self.optimized_games)}")
        print(f"  • Dispersão média: {np.mean([g['dispersion'] for g in self.optimized_games]):.2f}")
        print(f"  • Jogos com super par: {sum(1 for g in self.optimized_games if g['has_super_pair'])}")
        
    def save_optimized_games(self):
        """Salvar jogos otimizados"""
        print(f"\n💾 Salvando jogos otimizados...")
        
        Path('out/optimized').mkdir(exist_ok=True)
        
        # Criar DataFrame
        games_data = []
        for i, game in enumerate(self.optimized_games, 1):
            games_data.append({
                'jogo_id': i,
                'numeros': ','.join(map(str, game['numbers'])),
                'score': game['score'],
                'dispersao': round(game['dispersion'], 2),
                'pares_adjacentes': game['adjacent_pairs'],
                'tem_super_par': 'Sim' if game['has_super_pair'] else 'Não'
            })
        
        df = pd.DataFrame(games_data)
        df.to_csv('out/optimized/jogos_18_quentes_otimizados.csv', index=False)
        
        print(f"  ✅ Salvos em: out/optimized/jogos_18_quentes_otimizados.csv")
        
        # Criar relatório
        report = f"""
RELATÓRIO: COMBINAÇÕES OTIMIZADAS - 18 NÚMEROS MAIS QUENTES
{'=' * 80}

🔥 NÚMEROS UTILIZADOS:
{self.hot_numbers}

💰 ANÁLISE FINANCEIRA:
  • Orçamento disponível: R$ {self.budget:,.2f}
  • Preço por jogo: R$ {self.price_per_game:.2f}
  • Máximo de jogos possíveis: {self.max_games}
  • Jogos gerados: {len(self.optimized_games)}
  • Custo total: R$ {len(self.optimized_games) * self.price_per_game:.2f}
  • Saldo restante: R$ {self.budget - (len(self.optimized_games) * self.price_per_game):.2f}

📊 COMPARAÇÃO:
  • Total de combinações (fechar): {self._calculate_combinations(18, 15):,}
  • Custo total (fechar): R$ {self._calculate_combinations(18, 15) * self.price_per_game:,.2f}
  • Economia obtida: R$ {(self._calculate_combinations(18, 15) - len(self.optimized_games)) * self.price_per_game:,.2f}
  • Redução de custo: {(1 - len(self.optimized_games)/self._calculate_combinations(18, 15))*100:.1f}%

🎯 CRITÉRIOS DE OTIMIZAÇÃO:
  1. Dispersão Espacial (até 3 pontos)
     - Números espalhados pelo grid 5×5
  
  2. Baixa Contiguidade (até 3 pontos)
     - Evitar números adjacentes
  
  3. Super Pares (até 2 pontos)
     - Incluir pares com histórico forte
  
  4. Equilíbrio Regional (até 2 pontos)
     - Distribuição balanceada por linhas/colunas

📈 QUALIDADE DOS JOGOS:
  • Score mínimo: {min(g['score'] for g in self.optimized_games)} / 10
  • Score máximo: {max(g['score'] for g in self.optimized_games)} / 10
  • Score médio: {np.mean([g['score'] for g in self.optimized_games]):.2f} / 10
  • Dispersão média: {np.mean([g['dispersion'] for g in self.optimized_games]):.2f}
  • Jogos com super par: {sum(1 for g in self.optimized_games if g['has_super_pair'])} ({sum(1 for g in self.optimized_games if g['has_super_pair'])/len(self.optimized_games)*100:.1f}%)

✅ RECOMENDAÇÕES:
  • Todos os jogos têm score ≥ 5/10 (mínimo de qualidade)
  • Jogos estão ordenados por score (melhores primeiro)
  • Combine estes jogos com sua análise pessoal
  • Jogue com responsabilidade

Arquivos gerados:
  • out/optimized/jogos_18_quentes_otimizados.csv
  • out/optimized/relatorio_otimizacao.txt
"""
        
        with open('out/optimized/relatorio_otimizacao.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"  ✅ Relatório salvo em: out/optimized/relatorio_otimizacao.txt")
        
        # Exibir top 10 jogos
        print(f"\n🏆 TOP 10 MELHORES JOGOS:")
        print("-" * 80)
        for i, game in enumerate(self.optimized_games[:10], 1):
            nums_str = ','.join(map(str, game['numbers']))
            print(f"  {i:2d}. Score: {game['score']}/10 | Dispersão: {game['dispersion']:.2f} | "
                  f"Adjacentes: {game['adjacent_pairs']} | Super par: {'✓' if game['has_super_pair'] else '✗'}")
            print(f"      Números: {nums_str}")


def main():
    """Executar otimização"""
    optimizer = CombinationOptimizer(budget=1000, price_per_game=3.00)
    
    # Carregar dados
    optimizer.load_hot_numbers(top_n=18)
    optimizer.load_super_pairs()
    
    # Filtrar e rankear
    optimizer.filter_and_rank_combinations()
    
    # Salvar resultados
    optimizer.save_optimized_games()
    
    print("\n" + "=" * 80)
    print("✅ OTIMIZAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print(f"\n💡 Você pode jogar {optimizer.max_games} jogos otimizados por R$ {optimizer.budget:.2f}")
    print(f"   Economia de R$ {optimizer._calculate_combinations(18, 15) * 3.00 - optimizer.budget:,.2f} vs fechar!")


if __name__ == '__main__':
    main()

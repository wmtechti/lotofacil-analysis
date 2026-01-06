"""
Backtesting: Validação dos jogos otimizados contra sorteios históricos

Este script testa os 30 jogos gerados pela análise combinada contra todos os
sorteios históricos da Lotofácil para avaliar a eficácia das estratégias.
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from collections import defaultdict

class BacktestingEngine:
    """Motor de backtesting para validar estratégias de loteria"""
    
    def __init__(self):
        self.historical_draws = []
        self.optimized_games = []
        self.results = defaultdict(list)
        
    def load_historical_data(self):
        """Carregar sorteios históricos da Lotofácil"""
        print("📂 Carregando sorteios históricos da Lotofácil...")
        
        # Carregar do CSV convertido
        df = pd.read_csv('data/lotofacil_sorteios.csv')
        
        for _, row in df.iterrows():
            numbers = sorted([int(row[f'Bola{i}']) for i in range(1, 16)])
            self.historical_draws.append({
                'concurso': int(row['Concurso']),
                'numbers': numbers
            })
        
        print(f"✅ {len(self.historical_draws)} sorteios históricos carregados")
        
    def load_optimized_games(self):
        """Carregar jogos otimizados gerados"""
        print("\n📂 Carregando jogos otimizados...")
        
        df = pd.read_csv('out/jogos_otimizados_combined.csv')
        
        for _, row in df.iterrows():
            # Parse da string de números
            nums_str = row['numeros_str']
            numbers = sorted([int(x) for x in nums_str.split(',')])
            
            self.optimized_games.append({
                'jogo_id': row['jogo_id'],
                'numbers': numbers,
                'strategy': row['estrategia']
            })
        
        print(f"✅ {len(self.optimized_games)} jogos otimizados carregados")
        
    def calculate_matches(self, game_numbers, draw_numbers):
        """Calcular quantos números acertados"""
        return len(set(game_numbers) & set(draw_numbers))
    
    def classify_prize(self, matches):
        """Classificar prêmio baseado em acertos (Lotofácil)"""
        if matches == 15:
            return '15 acertos (SENA)'
        elif matches == 14:
            return '14 acertos (QUINA)'
        elif matches == 13:
            return '13 acertos (QUADRA)'
        elif matches == 12:
            return '12 acertos (TERNO)'
        elif matches == 11:
            return '11 acertos'
        else:
            return 'Sem prêmio'
    
    def run_backtest(self):
        """Executar backtesting completo"""
        print("\n" + "=" * 80)
        print("🔬 EXECUTANDO BACKTESTING")
        print("=" * 80)
        
        total_games = len(self.optimized_games)
        total_draws = len(self.historical_draws)
        total_tests = total_games * total_draws
        
        print(f"\n📊 Parâmetros:")
        print(f"   • Jogos otimizados: {total_games}")
        print(f"   • Sorteios históricos: {total_draws}")
        print(f"   • Total de testes: {total_tests:,}")
        
        # Estatísticas por jogo
        game_stats = []
        
        # Estatísticas por estratégia
        strategy_stats = defaultdict(lambda: {
            'total_matches': 0,
            'prizes': defaultdict(int),
            'games_count': 0,
            'best_match': 0
        })
        
        print("\n🔄 Processando backtesting...")
        
        for game in self.optimized_games:
            game_id = game['jogo_id']
            game_nums = game['numbers']
            strategy = game['strategy']
            
            matches_distribution = defaultdict(int)
            prizes_won = defaultdict(int)
            total_matches = 0
            best_match = 0
            
            for draw in self.historical_draws:
                draw_nums = draw['numbers']
                matches = self.calculate_matches(game_nums, draw_nums)
                
                matches_distribution[matches] += 1
                total_matches += matches
                
                if matches > best_match:
                    best_match = matches
                
                prize = self.classify_prize(matches)
                if prize != 'Sem prêmio':
                    prizes_won[prize] += 1
            
            # Estatísticas do jogo
            avg_matches = total_matches / len(self.historical_draws)
            prize_rate = sum(prizes_won.values()) / len(self.historical_draws) * 100
            
            game_stats.append({
                'jogo_id': game_id,
                'strategy': strategy,
                'avg_matches': avg_matches,
                'best_match': best_match,
                'prize_rate': prize_rate,
                'prizes_11': prizes_won.get('11 acertos', 0),
                'prizes_12': prizes_won.get('12 acertos (TERNO)', 0),
                'prizes_13': prizes_won.get('13 acertos (QUADRA)', 0),
                'prizes_14': prizes_won.get('14 acertos (QUINA)', 0),
                'prizes_15': prizes_won.get('15 acertos (SENA)', 0),
                'numbers': ','.join(map(str, game_nums))
            })
            
            # Acumular por estratégia
            strategy_stats[strategy]['total_matches'] += total_matches
            strategy_stats[strategy]['games_count'] += 1
            strategy_stats[strategy]['best_match'] = max(strategy_stats[strategy]['best_match'], best_match)
            for prize, count in prizes_won.items():
                strategy_stats[strategy]['prizes'][prize] += count
        
        print("✅ Backtesting concluído!")
        
        # Salvar resultados
        self.save_results(game_stats, strategy_stats)
        
        # Exibir resultados
        self.display_results(game_stats, strategy_stats)
    
    def save_results(self, game_stats, strategy_stats):
        """Salvar resultados do backtesting"""
        print("\n💾 Salvando resultados...")
        
        # Criar diretório
        Path('out/backtesting').mkdir(exist_ok=True)
        
        # Salvar estatísticas por jogo
        df_games = pd.DataFrame(game_stats)
        df_games.to_csv('out/backtesting/resultados_por_jogo.csv', index=False)
        
        # Salvar estatísticas por estratégia
        strategy_rows = []
        for strategy, stats in strategy_stats.items():
            avg_matches = stats['total_matches'] / (stats['games_count'] * len(self.historical_draws))
            total_prizes = sum(stats['prizes'].values())
            prize_rate = (total_prizes / (stats['games_count'] * len(self.historical_draws))) * 100
            
            strategy_rows.append({
                'estrategia': strategy,
                'jogos_count': stats['games_count'],
                'avg_matches': avg_matches,
                'best_match': stats['best_match'],
                'prize_rate_%': prize_rate,
                'prizes_11': stats['prizes'].get('11 acertos', 0),
                'prizes_12': stats['prizes'].get('12 acertos (TERNO)', 0),
                'prizes_13': stats['prizes'].get('13 acertos (QUADRA)', 0),
                'prizes_14': stats['prizes'].get('14 acertos (QUINA)', 0),
                'prizes_15': stats['prizes'].get('15 acertos (SENA)', 0)
            })
        
        df_strategies = pd.DataFrame(strategy_rows)
        df_strategies = df_strategies.sort_values('prize_rate_%', ascending=False)
        df_strategies.to_csv('out/backtesting/resultados_por_estrategia.csv', index=False)
        
        print("✅ Resultados salvos em: out/backtesting/")
    
    def display_results(self, game_stats, strategy_stats):
        """Exibir resultados formatados"""
        print("\n" + "=" * 80)
        print("📊 RESULTADOS DO BACKTESTING")
        print("=" * 80)
        
        # Estatísticas gerais
        df_games = pd.DataFrame(game_stats)
        
        print(f"\n📈 ESTATÍSTICAS GERAIS:")
        print(f"   • Média de acertos (todos os jogos): {df_games['avg_matches'].mean():.2f}")
        print(f"   • Melhor jogo (média): {df_games['avg_matches'].max():.2f} acertos")
        print(f"   • Pior jogo (média): {df_games['avg_matches'].min():.2f} acertos")
        print(f"   • Taxa média de prêmio: {df_games['prize_rate'].mean():.2f}%")
        
        # Top 5 jogos
        print(f"\n🏆 TOP 5 JOGOS (por taxa de prêmio):")
        top_games = df_games.nlargest(5, 'prize_rate')[['jogo_id', 'strategy', 'avg_matches', 'prize_rate', 'numbers']]
        for idx, row in top_games.iterrows():
            print(f"   {row['jogo_id']}. {row['strategy']:30s} | Média: {row['avg_matches']:.2f} | Taxa: {row['prize_rate']:.2f}%")
            print(f"      Números: {row['numbers']}")
        
        # Comparação por estratégia
        print(f"\n📊 COMPARAÇÃO POR ESTRATÉGIA:")
        print(f"{'Estratégia':30s} {'Jogos':>6s} {'Média':>8s} {'Melhor':>8s} {'Taxa %':>8s}")
        print("-" * 80)
        
        for strategy, stats in sorted(strategy_stats.items(), 
                                     key=lambda x: x[1]['total_matches'] / (x[1]['games_count'] * len(self.historical_draws)),
                                     reverse=True):
            avg_matches = stats['total_matches'] / (stats['games_count'] * len(self.historical_draws))
            total_prizes = sum(stats['prizes'].values())
            prize_rate = (total_prizes / (stats['games_count'] * len(self.historical_draws))) * 100
            
            print(f"{strategy:30s} {stats['games_count']:6d} {avg_matches:8.2f} {stats['best_match']:8d} {prize_rate:8.2f}")
        
        # Distribuição de prêmios
        print(f"\n🎁 DISTRIBUIÇÃO DE PRÊMIOS (todos os jogos):")
        total_11 = df_games['prizes_11'].sum()
        total_12 = df_games['prizes_12'].sum()
        total_13 = df_games['prizes_13'].sum()
        total_14 = df_games['prizes_14'].sum()
        total_15 = df_games['prizes_15'].sum()
        
        print(f"   • 11 acertos: {total_11:,}")
        print(f"   • 12 acertos (TERNO): {total_12:,}")
        print(f"   • 13 acertos (QUADRA): {total_13:,}")
        print(f"   • 14 acertos (QUINA): {total_14:,}")
        print(f"   • 15 acertos (SENA): {total_15:,}")
        
        # Baseline aleatório (esperado)
        print(f"\n📊 COMPARAÇÃO COM BASELINE ALEATÓRIO:")
        expected_11 = len(self.historical_draws) * 0.1134  # ~11.34% para 11+ acertos
        actual_avg = df_games['prize_rate'].mean() / 100 * len(self.historical_draws)
        
        print(f"   • Esperado (aleatório): ~{expected_11:.1f} prêmios por jogo")
        print(f"   • Obtido (otimizado): ~{actual_avg:.1f} prêmios por jogo")
        improvement = ((actual_avg - expected_11) / expected_11) * 100
        print(f"   • Melhoria: {improvement:+.2f}%")
        
        print("\n" + "=" * 80)
        print("✅ BACKTESTING COMPLETO!")
        print("=" * 80)


def main():
    """Executar backtesting"""
    engine = BacktestingEngine()
    
    # Carregar dados
    engine.load_historical_data()
    engine.load_optimized_games()
    
    # Executar backtesting
    engine.run_backtest()


if __name__ == '__main__':
    main()

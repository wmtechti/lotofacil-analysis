"""
Módulo de simulação Monte Carlo para Lotofácil.
Testa estratégias contra o histórico de sorteios.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from tqdm import tqdm


class MonteCarloSimulator:
    """Simulador Monte Carlo para testar estratégias da Lotofácil."""
    
    def __init__(self, historical_draws: pd.DataFrame, ball_cols: List[str]):
        """
        Inicializa o simulador.
        
        Args:
            historical_draws: DataFrame com sorteios históricos
            ball_cols: Colunas com os números sorteados
        """
        self.draws = historical_draws
        self.ball_cols = ball_cols
        
        # Converte sorteios para sets para comparação rápida
        self.draw_sets = []
        for _, row in self.draws.iterrows():
            self.draw_sets.append(set(row[ball_cols].tolist()))
    
    def count_matches(self, game: List[int], draw: set) -> int:
        """
        Conta quantos números do jogo acertaram no sorteio.
        
        Args:
            game: Lista de números apostados
            draw: Set de números sorteados
            
        Returns:
            Quantidade de acertos
        """
        return len(set(game) & draw)
    
    def simulate_game_history(self, game: List[int]) -> Dict[str, any]:
        """
        Simula um jogo contra todo o histórico.
        
        Args:
            game: Lista de números do jogo
            
        Returns:
            Dicionário com estatísticas de acertos
        """
        matches = []
        prizes = {11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        
        for draw in self.draw_sets:
            n_matches = self.count_matches(game, draw)
            matches.append(n_matches)
            
            if n_matches >= 11:
                prizes[n_matches] += 1
        
        return {
            'acertos': matches,
            'media_acertos': np.mean(matches),
            'max_acertos': max(matches),
            'premios_11': prizes[11],
            'premios_12': prizes[12],
            'premios_13': prizes[13],
            'premios_14': prizes[14],
            'premios_15': prizes[15],
            'total_premios': sum(prizes.values()),
            'taxa_premio_%': (sum(prizes.values()) / len(self.draws)) * 100
        }
    
    def simulate_strategy(self, games: List[List[int]], 
                         strategy_name: str = "Estratégia") -> pd.DataFrame:
        """
        Simula múltiplos jogos de uma estratégia.
        
        Args:
            games: Lista de jogos gerados
            strategy_name: Nome da estratégia
            
        Returns:
            DataFrame com resultados por jogo
        """
        results = []
        
        for i, game in enumerate(games, 1):
            stats = self.simulate_game_history(game)
            results.append({
                'estrategia': strategy_name,
                'jogo_id': i,
                'numeros': str(sorted(game)),
                'media_acertos': stats['media_acertos'],
                'max_acertos': stats['max_acertos'],
                'premios_11': stats['premios_11'],
                'premios_12': stats['premios_12'],
                'premios_13': stats['premios_13'],
                'premios_14': stats['premios_14'],
                'premios_15': stats['premios_15'],
                'total_premios': stats['total_premios'],
                'taxa_premio_%': stats['taxa_premio_%']
            })
        
        return pd.DataFrame(results)
    
    def simulate_all_strategies(self, strategy_games: Dict[str, List[List[int]]]) -> pd.DataFrame:
        """
        Simula todas as estratégias.
        
        Args:
            strategy_games: Dicionário estratégia -> lista de jogos
            
        Returns:
            DataFrame consolidado com todos os resultados
        """
        all_results = []
        
        print("🎲 Simulando estratégias contra histórico...")
        for strategy_name, games in strategy_games.items():
            print(f"   Testando: {strategy_name} ({len(games)} jogos)...")
            df = self.simulate_strategy(games, strategy_name)
            all_results.append(df)
        
        return pd.concat(all_results, ignore_index=True)
    
    def compare_strategies(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Compara performance de diferentes estratégias.
        
        Args:
            results_df: DataFrame com resultados das simulações
            
        Returns:
            DataFrame com comparação agregada
        """
        comparison = results_df.groupby('estrategia').agg({
            'media_acertos': 'mean',
            'max_acertos': 'max',
            'premios_11': 'sum',
            'premios_12': 'sum',
            'premios_13': 'sum',
            'premios_14': 'sum',
            'premios_15': 'sum',
            'total_premios': 'sum',
            'taxa_premio_%': 'mean'
        }).round(2)
        
        comparison = comparison.sort_values('total_premios', ascending=False)
        return comparison
    
    def monte_carlo_random(self, n_simulations: int = 10000, 
                          n_numbers: int = 15) -> Dict[str, any]:
        """
        Simulação Monte Carlo pura (jogos completamente aleatórios).
        
        Args:
            n_simulations: Número de simulações
            n_numbers: Quantidade de números por jogo
            
        Returns:
            Estatísticas agregadas
        """
        print(f"🎰 Executando Monte Carlo: {n_simulations:,} simulações...")
        
        all_matches = []
        prizes = {11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        
        for _ in tqdm(range(n_simulations), desc="Simulações"):
            # Gera jogo aleatório
            game = sorted(np.random.choice(range(1, 26), size=n_numbers, replace=False).tolist())
            
            # Testa contra um sorteio aleatório do histórico
            draw = self.draw_sets[np.random.randint(0, len(self.draw_sets))]
            
            n_matches = self.count_matches(game, draw)
            all_matches.append(n_matches)
            
            if n_matches >= 11:
                prizes[n_matches] += 1
        
        return {
            'n_simulacoes': n_simulations,
            'media_acertos': np.mean(all_matches),
            'desvio_acertos': np.std(all_matches),
            'min_acertos': min(all_matches),
            'max_acertos': max(all_matches),
            'premios_11': prizes[11],
            'premios_12': prizes[12],
            'premios_13': prizes[13],
            'premios_14': prizes[14],
            'premios_15': prizes[15],
            'total_premios': sum(prizes.values()),
            'prob_11_acertos_%': (prizes[11] / n_simulations) * 100,
            'prob_12_acertos_%': (prizes[12] / n_simulations) * 100,
            'prob_13_acertos_%': (prizes[13] / n_simulations) * 100,
            'prob_14_acertos_%': (prizes[14] / n_simulations) * 100,
            'prob_15_acertos_%': (prizes[15] / n_simulations) * 100,
            'prob_qualquer_premio_%': (sum(prizes.values()) / n_simulations) * 100
        }
    
    def validate_best_games(self, results_df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        """
        Retorna os melhores jogos encontrados.
        
        Args:
            results_df: DataFrame com resultados
            top_n: Quantidade de melhores jogos
            
        Returns:
            DataFrame com top jogos
        """
        best = results_df.nlargest(top_n, 'total_premios')
        return best[['estrategia', 'numeros', 'media_acertos', 'max_acertos', 
                     'total_premios', 'taxa_premio_%']]

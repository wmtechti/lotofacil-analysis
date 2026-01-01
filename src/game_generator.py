"""
Módulo de geração de jogos otimizados para Lotofácil.
Usa as análises espaciais, pares fortes e tendências para gerar combinações.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import List, Set, Tuple, Dict
from .grid_mapping import build_number_coord_map, GridSpec


class LotofacilGameGenerator:
    """Gerador inteligente de jogos da Lotofácil."""
    
    def __init__(self, hot_cold_df: pd.DataFrame, pairs_df: pd.DataFrame, 
                 trends_df: pd.DataFrame, bias: Dict):
        """
        Inicializa o gerador com dados das análises.
        
        Args:
            hot_cold_df: DataFrame com classificação quente/frio
            pairs_df: DataFrame com pares fortes
            trends_df: DataFrame com tendências
            bias: Dicionário com bias borda/centro
        """
        self.hot_cold = hot_cold_df
        self.pairs = pairs_df
        self.trends = trends_df
        self.bias = bias
        self.n2c = build_number_coord_map()
        
        # Pré-processa dados para otimização
        self._build_weights()
    
    def _build_weights(self):
        """Constrói pesos para cada número baseado nas análises."""
        self.weights = {}
        
        for _, row in self.hot_cold.iterrows():
            num = row['numero']
            base_weight = 1.0
            
            # Ajusta por temperatura (quente/frio)
            if row['categoria'] == '🔥 Quente':
                base_weight *= 1.3
            elif row['categoria'] == '❄️ Frio':
                base_weight *= 0.7
            
            # Ajusta por tendência
            trend_row = self.trends[self.trends['numero'] == num]
            if not trend_row.empty:
                trend = trend_row.iloc[0]['tendencia_%']
                if trend > 5:
                    base_weight *= 1.2
                elif trend < -5:
                    base_weight *= 0.8
            
            self.weights[num] = base_weight
        
        # Normaliza pesos
        total = sum(self.weights.values())
        self.weights = {k: v/total for k, v in self.weights.items()}
    
    def generate_random_weighted(self, n_numbers: int = 15) -> List[int]:
        """
        Gera um jogo usando pesos baseados nas análises.
        
        Args:
            n_numbers: Quantidade de números (15-20)
            
        Returns:
            Lista de números sorteados
        """
        numbers = list(range(1, 26))
        weights = [self.weights[n] for n in numbers]
        
        selected = np.random.choice(numbers, size=n_numbers, replace=False, p=weights)
        return sorted(selected.tolist())
    
    def generate_hot_strategy(self, n_numbers: int = 15) -> List[int]:
        """
        Estratégia: prioriza números quentes.
        
        Args:
            n_numbers: Quantidade de números
            
        Returns:
            Lista de números
        """
        # Pega 70% dos mais quentes
        hot_count = int(n_numbers * 0.7)
        hot_numbers = self.hot_cold.head(hot_count)['numero'].tolist()
        
        # Completa com números médios aleatórios
        medium = self.hot_cold[
            (self.hot_cold['categoria'] == '🌡️ Médio')
        ]['numero'].tolist()
        
        remaining = n_numbers - len(hot_numbers)
        if remaining > 0:
            selected_medium = np.random.choice(medium, size=remaining, replace=False)
            hot_numbers.extend(selected_medium.tolist())
        
        return sorted(hot_numbers)
    
    def generate_pairs_strategy(self, n_numbers: int = 15) -> List[int]:
        """
        Estratégia: maximiza super pares.
        
        Args:
            n_numbers: Quantidade de números
            
        Returns:
            Lista de números
        """
        selected = set()
        
        # Adiciona números dos top pares
        for _, row in self.pairs.head(20).iterrows():
            if len(selected) >= n_numbers:
                break
            selected.add(row['a'])
            selected.add(row['b'])
        
        # Se faltam números, completa com quentes
        if len(selected) < n_numbers:
            hot = self.hot_cold[
                ~self.hot_cold['numero'].isin(selected)
            ]['numero'].tolist()
            
            remaining = n_numbers - len(selected)
            selected.update(hot[:remaining])
        
        # Se ainda falta, remove excesso
        if len(selected) > n_numbers:
            # Remove os menos quentes
            to_remove = len(selected) - n_numbers
            cold_in_selected = [
                n for n in selected 
                if self.hot_cold[self.hot_cold['numero'] == n]['categoria'].iloc[0] == '❄️ Frio'
            ]
            for n in cold_in_selected[:to_remove]:
                selected.remove(n)
        
        return sorted(list(selected))[:n_numbers]
    
    def generate_spatial_balanced(self, n_numbers: int = 15) -> List[int]:
        """
        Estratégia: balanceamento espacial (bordas vs centro).
        
        Args:
            n_numbers: Quantidade de números
            
        Returns:
            Lista de números
        """
        # Calcula proporção ideal (baseado no bias observado)
        edge_target = int(n_numbers * 0.64)  # 64% bordas (baseado na análise)
        center_target = n_numbers - edge_target
        
        # Separa números em bordas e centro
        edge_nums = []
        center_nums = []
        
        for num in range(1, 26):
            r, c = self.n2c[num]
            if r == 0 or r == 4 or c == 0 or c == 4:
                edge_nums.append(num)
            else:
                center_nums.append(num)
        
        # Seleciona baseado em peso
        edge_weights = [self.weights[n] for n in edge_nums]
        center_weights = [self.weights[n] for n in center_nums]
        
        # Normaliza
        edge_weights = np.array(edge_weights) / sum(edge_weights)
        center_weights = np.array(center_weights) / sum(center_weights)
        
        selected_edge = np.random.choice(edge_nums, size=edge_target, replace=False, p=edge_weights)
        selected_center = np.random.choice(center_nums, size=center_target, replace=False, p=center_weights)
        
        return sorted(selected_edge.tolist() + selected_center.tolist())
    
    def generate_column5_strategy(self, n_numbers: int = 15) -> List[int]:
        """
        Estratégia: prioriza coluna 5 (mais quente).
        
        Args:
            n_numbers: Quantidade de números
            
        Returns:
            Lista de números
        """
        # Coluna 5: 5, 10, 15, 20, 25
        col5 = [5, 10, 15, 20, 25]
        
        # Inclui 4 números da coluna 5 (80%)
        selected = set(col5[:4])
        
        # Completa com números quentes de outras colunas
        remaining = n_numbers - len(selected)
        other_hot = [
            n for n in self.hot_cold.head(20)['numero'].tolist()
            if n not in selected
        ]
        
        selected.update(other_hot[:remaining])
        
        return sorted(list(selected))[:n_numbers]
    
    def generate_trending_strategy(self, n_numbers: int = 15) -> List[int]:
        """
        Estratégia: foca em números em alta.
        
        Args:
            n_numbers: Quantidade de números
            
        Returns:
            Lista de números
        """
        # Pega números com tendência positiva
        trending_up = self.trends[
            self.trends['tendencia_%'] > 0
        ].sort_values('tendencia_%', ascending=False)
        
        selected = set(trending_up.head(n_numbers)['numero'].tolist())
        
        # Se não tem suficientes, completa com quentes
        if len(selected) < n_numbers:
            hot = self.hot_cold['numero'].tolist()
            for n in hot:
                if len(selected) >= n_numbers:
                    break
                selected.add(n)
        
        return sorted(list(selected))[:n_numbers]
    
    def generate_all_strategies(self, n_numbers: int = 15, 
                                games_per_strategy: int = 3) -> Dict[str, List[List[int]]]:
        """
        Gera jogos com todas as estratégias.
        
        Args:
            n_numbers: Quantidade de números por jogo
            games_per_strategy: Jogos por estratégia
            
        Returns:
            Dicionário com estratégia -> lista de jogos
        """
        strategies = {
            'Pesos (Quente+Tendência)': lambda: self.generate_random_weighted(n_numbers),
            'Números Quentes': lambda: self.generate_hot_strategy(n_numbers),
            'Super Pares': lambda: self.generate_pairs_strategy(n_numbers),
            'Balanceamento Espacial': lambda: self.generate_spatial_balanced(n_numbers),
            'Coluna 5 (Mais Quente)': lambda: self.generate_column5_strategy(n_numbers),
            'Tendência Alta': lambda: self.generate_trending_strategy(n_numbers),
        }
        
        results = {}
        for name, strategy_func in strategies.items():
            games = []
            for _ in range(games_per_strategy):
                games.append(strategy_func())
            results[name] = games
        
        return results

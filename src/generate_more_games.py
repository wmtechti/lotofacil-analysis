"""
Gerador de Jogos Otimizados - Lotofácil

Gera jogos adicionais usando as melhores estratégias identificadas no backtesting:
- Dispersão Máxima (melhor desempenho: 10.55%)
- Equilíbrio Regional (segundo melhor: 10.43%)
"""

import pandas as pd
import numpy as np
import random
from pathlib import Path


class OptimizedGameGenerator:
    """Gerador de jogos otimizados para Lotofácil"""
    
    def __init__(self):
        self.grid_size = (5, 5)  # Grid 5×5 da Lotofácil
        self.numbers_per_game = 15
        self.super_pairs = []
        self.hot_numbers = []
        
    def load_analysis_data(self):
        """Carregar dados das análises para geração inteligente"""
        print("📂 Carregando dados das análises...")
        
        # Carregar super pares
        pares_df = pd.read_csv('out/lotofacil/pares_forca.csv')
        super_pares = pares_df[pares_df['categoria'] == '⭐⭐⭐ Super Par']
        self.super_pairs = [(int(row['a']), int(row['b'])) for _, row in super_pares.iterrows()]
        
        # Carregar números quentes
        hot_cold_df = pd.read_csv('out/lotofacil/numeros_quentes_frios.csv')
        self.hot_numbers = list(hot_cold_df.nlargest(15, 'freq')['numero'].values)
        
        print(f"✅ {len(self.super_pairs)} super pares carregados")
        print(f"✅ {len(self.hot_numbers)} números quentes identificados")
        
    def number_to_coord(self, num):
        """Converter número (1-25) para coordenadas (linha, coluna)"""
        num = num - 1  # Ajustar para índice 0
        linha = num // 5
        coluna = num % 5
        return (linha, coluna)
    
    def coord_to_number(self, linha, coluna):
        """Converter coordenadas para número"""
        return linha * 5 + coluna + 1
    
    def calculate_dispersion(self, numbers):
        """Calcular dispersão espacial do jogo"""
        coords = [self.number_to_coord(n) for n in numbers]
        
        # Calcular centróide
        centroid_row = np.mean([c[0] for c in coords])
        centroid_col = np.mean([c[1] for c in coords])
        
        # Distância média ao centróide
        distances = [np.sqrt((c[0] - centroid_row)**2 + (c[1] - centroid_col)**2) 
                    for c in coords]
        
        return np.mean(distances)
    
    def check_regional_balance(self, numbers):
        """Verificar equilíbrio por linhas e colunas"""
        coords = [self.number_to_coord(n) for n in numbers]
        
        # Contar por linha
        line_counts = [0] * 5
        for linha, _ in coords:
            line_counts[linha] += 1
        
        # Contar por coluna
        col_counts = [0] * 5
        for _, coluna in coords:
            col_counts[coluna] += 1
        
        # Verificar se está balanceado (3 números por linha idealmente)
        line_balanced = all(2 <= count <= 4 for count in line_counts)
        col_balanced = all(2 <= count <= 4 for count in col_counts)
        
        return line_balanced and col_balanced
    
    def count_adjacent_pairs(self, numbers):
        """Contar pares de números adjacentes"""
        coords = set(self.number_to_coord(n) for n in numbers)
        adjacent_count = 0
        
        for linha, coluna in coords:
            # Verificar vizinhos (cima, baixo, esquerda, direita)
            neighbors = [
                (linha - 1, coluna),
                (linha + 1, coluna),
                (linha, coluna - 1),
                (linha, coluna + 1)
            ]
            
            for neighbor in neighbors:
                if neighbor in coords:
                    adjacent_count += 1
        
        # Cada par é contado duas vezes
        return adjacent_count // 2
    
    def generate_dispersed_game(self):
        """Estratégia 1: Dispersão Máxima"""
        max_attempts = 1000
        best_game = None
        best_dispersion = 0
        
        for _ in range(max_attempts):
            # Gerar jogo aleatório
            game = sorted(random.sample(range(1, 26), self.numbers_per_game))
            
            # Calcular dispersão
            dispersion = self.calculate_dispersion(game)
            
            # Verificar se tem poucos adjacentes
            adjacent = self.count_adjacent_pairs(game)
            
            if dispersion > best_dispersion and adjacent <= 2:
                best_dispersion = dispersion
                best_game = game
        
        # Se não encontrou um ótimo, retornar o melhor encontrado
        if best_game is None:
            best_game = sorted(random.sample(range(1, 26), self.numbers_per_game))
        
        return best_game, 'Dispersão Máxima'
    
    def generate_balanced_game(self):
        """Estratégia 2: Equilíbrio Regional"""
        max_attempts = 1000
        
        for _ in range(max_attempts):
            game = []
            
            # Selecionar 3 números por linha (totalizando 15)
            for linha in range(5):
                # Escolher 3 colunas aleatórias
                cols = random.sample(range(5), 3)
                for col in cols:
                    num = self.coord_to_number(linha, col)
                    game.append(num)
            
            game = sorted(game)
            
            # Verificar equilíbrio
            if self.check_regional_balance(game):
                # Verificar dispersão razoável
                if self.calculate_dispersion(game) >= 1.8:
                    return game, 'Equilíbrio Regional'
        
        # Fallback: gerar aleatório balanceado
        game = []
        for linha in range(5):
            cols = random.sample(range(5), 3)
            for col in cols:
                game.append(self.coord_to_number(linha, col))
        
        return sorted(game), 'Equilíbrio Regional'
    
    def generate_cooccurrence_game(self):
        """Estratégia 3: Co-ocorrência + Dispersão"""
        # Selecionar 2 super pares aleatórios
        selected_pairs = random.sample(self.super_pairs[:20], 2)
        
        game = []
        for a, b in selected_pairs:
            game.append(a)
            game.append(b)
        
        # Completar com números dispersos (evitando duplicatas)
        remaining = [n for n in range(1, 26) if n not in game]
        
        # Selecionar números adicionais para maximizar dispersão
        while len(game) < self.numbers_per_game:
            best_num = None
            best_dispersion = 0
            
            for num in remaining:
                temp_game = game + [num]
                dispersion = self.calculate_dispersion(temp_game)
                
                if dispersion > best_dispersion:
                    best_dispersion = dispersion
                    best_num = num
            
            if best_num:
                game.append(best_num)
                remaining.remove(best_num)
        
        return sorted(game), 'Co-ocorrência + Dispersão'
    
    def generate_games(self, total_games=100):
        """Gerar conjunto de jogos otimizados"""
        print(f"\n🎮 Gerando {total_games} jogos otimizados...")
        
        games = []
        
        # Distribuição: 50% Dispersão, 30% Equilíbrio, 20% Co-ocorrência
        dispersed_count = int(total_games * 0.5)
        balanced_count = int(total_games * 0.3)
        cooccurrence_count = total_games - dispersed_count - balanced_count
        
        # Gerar jogos de Dispersão Máxima
        print(f"  Gerando {dispersed_count} jogos - Dispersão Máxima...")
        for i in range(dispersed_count):
            game, strategy = self.generate_dispersed_game()
            games.append({
                'jogo_id': i + 1,
                'numeros': game,
                'estrategia': strategy,
                'numeros_str': ','.join(map(str, game))
            })
        
        # Gerar jogos de Equilíbrio Regional
        print(f"  Gerando {balanced_count} jogos - Equilíbrio Regional...")
        for i in range(balanced_count):
            game, strategy = self.generate_balanced_game()
            games.append({
                'jogo_id': dispersed_count + i + 1,
                'numeros': game,
                'estrategia': strategy,
                'numeros_str': ','.join(map(str, game))
            })
        
        # Gerar jogos de Co-ocorrência + Dispersão
        print(f"  Gerando {cooccurrence_count} jogos - Co-ocorrência + Dispersão...")
        for i in range(cooccurrence_count):
            game, strategy = self.generate_cooccurrence_game()
            games.append({
                'jogo_id': dispersed_count + balanced_count + i + 1,
                'numeros': game,
                'estrategia': strategy,
                'numeros_str': ','.join(map(str, game))
            })
        
        return games
    
    def save_games(self, games, filename='jogos_otimizados_100.csv'):
        """Salvar jogos em CSV"""
        df = pd.DataFrame(games)
        
        output_path = f'out/{filename}'
        df.to_csv(output_path, index=False)
        
        print(f"\n✅ {len(games)} jogos salvos em: {output_path}")
        
        # Estatísticas
        print(f"\n📊 Distribuição por estratégia:")
        for strategy, count in df['estrategia'].value_counts().items():
            print(f"   • {strategy}: {count} jogos")


def main():
    """Executar geração de jogos"""
    generator = OptimizedGameGenerator()
    
    # Carregar dados
    generator.load_analysis_data()
    
    # Gerar jogos
    games = generator.generate_games(total_games=100)
    
    # Salvar
    generator.save_games(games)
    
    print("\n" + "=" * 80)
    print("✅ GERAÇÃO DE JOGOS CONCLUÍDA!")
    print("=" * 80)


if __name__ == '__main__':
    main()

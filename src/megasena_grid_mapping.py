"""
Mapeamento de números da Mega-Sena para grid 6×10 (estilo Batalha Naval).

Grid Layout:
Colunas:  1   2   3   4   5   6   7   8   9  10
Linha 1: [01][02][03][04][05][06][07][08][09][10]
Linha 2: [11][12][13][14][15][16][17][18][19][20]
Linha 3: [21][22][23][24][25][26][27][28][29][30]
Linha 4: [31][32][33][34][35][36][37][38][39][40]
Linha 5: [41][42][43][44][45][46][47][48][49][50]
Linha 6: [51][52][53][54][55][56][57][58][59][60]
"""

import numpy as np
from typing import Tuple, List


def number_to_coord(numero: int) -> Tuple[int, int]:
    """
    Converte um número (1-60) para coordenadas (linha, coluna) no grid 6×10.
    
    Args:
        numero: Número entre 1 e 60
        
    Returns:
        Tupla (linha, coluna) onde linha ∈ [0,5] e coluna ∈ [0,9]
        
    Examples:
        >>> number_to_coord(1)
        (0, 0)  # Linha 1, Coluna 1
        >>> number_to_coord(10)
        (0, 9)  # Linha 1, Coluna 10
        >>> number_to_coord(11)
        (1, 0)  # Linha 2, Coluna 1
        >>> number_to_coord(60)
        (5, 9)  # Linha 6, Coluna 10
    """
    if not 1 <= numero <= 60:
        raise ValueError(f"Número {numero} fora do intervalo [1, 60]")
    
    # Ajusta para índice 0-based
    idx = numero - 1
    linha = idx // 10
    coluna = idx % 10
    
    return (linha, coluna)


def coord_to_number(linha: int, coluna: int) -> int:
    """
    Converte coordenadas (linha, coluna) para número (1-60).
    
    Args:
        linha: Linha do grid [0-5]
        coluna: Coluna do grid [0-9]
        
    Returns:
        Número correspondente [1-60]
        
    Examples:
        >>> coord_to_number(0, 0)
        1
        >>> coord_to_number(5, 9)
        60
    """
    if not (0 <= linha <= 5 and 0 <= coluna <= 9):
        raise ValueError(f"Coordenadas ({linha}, {coluna}) fora do grid 6×10")
    
    return linha * 10 + coluna + 1


def create_grid_from_numbers(numeros: List[int]) -> np.ndarray:
    """
    Cria um grid 6×10 marcando as posições dos números sorteados.
    
    Args:
        numeros: Lista de números sorteados (ex: [4, 5, 30, 33, 41, 52])
        
    Returns:
        Array numpy 6×10 com 1 nas posições sorteadas e 0 nas demais
        
    Example:
        >>> grid = create_grid_from_numbers([1, 2, 3, 4, 5, 6])
        >>> grid[0, :6]  # Primeira linha, primeiras 6 colunas
        array([1, 1, 1, 1, 1, 1])
    """
    grid = np.zeros((6, 10), dtype=int)
    
    for num in numeros:
        linha, coluna = number_to_coord(num)
        grid[linha, coluna] = 1
    
    return grid


def get_neighbors(linha: int, coluna: int, include_diagonal: bool = False) -> List[Tuple[int, int]]:
    """
    Retorna vizinhos válidos de uma célula no grid.
    
    Args:
        linha: Linha da célula [0-5]
        coluna: Coluna da célula [0-9]
        include_diagonal: Se True, inclui vizinhos diagonais (8 vizinhos)
                         Se False, apenas ortogonais (4 vizinhos)
        
    Returns:
        Lista de tuplas (linha, coluna) dos vizinhos válidos
    """
    neighbors = []
    
    # Vizinhos ortogonais (cima, baixo, esquerda, direita)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    if include_diagonal:
        # Adiciona diagonais
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for dl, dc in directions:
        nl, nc = linha + dl, coluna + dc
        # Verifica se está dentro dos limites do grid
        if 0 <= nl <= 5 and 0 <= nc <= 9:
            neighbors.append((nl, nc))
    
    return neighbors


def build_number_coord_map():
    """
    Constrói dicionários de mapeamento bidirecional.
    
    Returns:
        Tupla (num_to_coord, coord_to_num) com os dois dicionários
    """
    num_to_coord = {num: number_to_coord(num) for num in range(1, 61)}
    coord_to_num = {(l, c): coord_to_number(l, c) for l in range(6) for c in range(10)}
    
    return num_to_coord, coord_to_num


def print_grid(grid: np.ndarray, numbers: List[int] = None):
    """
    Imprime o grid de forma visual.
    
    Args:
        grid: Array 6×10 com 0s e 1s
        numbers: Lista opcional dos números sorteados (para exibição)
    """
    print("\n" + "="*52)
    print("   ", end="")
    for col in range(1, 11):
        print(f"{col:4}", end="")
    print()
    print("   " + "-" * 44)
    
    for linha in range(6):
        print(f"{linha+1} |", end="")
        for coluna in range(10):
            numero = coord_to_number(linha, coluna)
            if grid[linha, coluna] == 1:
                print(f" {numero:2}*", end="")
            else:
                print(f" {numero:2} ", end="")
        print(" |")
    
    print("   " + "-" * 44)
    if numbers:
        print(f"Números sorteados: {sorted(numbers)}")
    print("="*52)


if __name__ == "__main__":
    # Teste com primeiro sorteio
    numeros_teste = [4, 5, 30, 33, 41, 52]
    
    print("🎯 Sistema de Mapeamento Mega-Sena 6×10")
    print(f"\nTestando com sorteio: {numeros_teste}")
    
    # Criar grid
    grid = create_grid_from_numbers(numeros_teste)
    print_grid(grid, numeros_teste)
    
    # Testar conversões
    print("\n✅ Testes de conversão:")
    for num in [1, 10, 11, 60]:
        coord = number_to_coord(num)
        back = coord_to_number(*coord)
        print(f"  {num:2} → {coord} → {back:2}")

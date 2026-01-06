"""
Análise de padrões geométricos dos sorteios da Mega-Sena no grid 6×10.

Análises implementadas:
1. Contiguidade - números adjacentes
2. Dispersão espacial - distâncias entre números
3. Classificação de padrões - linear, cluster, disperso, etc.
4. Simetria - vertical, horizontal, central
5. Concentração por regiões do grid
"""

import numpy as np
from typing import List, Tuple, Dict
from collections import Counter
from megasena_grid_mapping import (
    number_to_coord, create_grid_from_numbers, get_neighbors
)


def analyze_contiguity(numeros: List[int], include_diagonal: bool = False) -> Dict:
    """
    Analisa a contiguidade dos números sorteados.
    
    Args:
        numeros: Lista de 6 números sorteados
        include_diagonal: Se True, considera vizinhos diagonais
        
    Returns:
        Dicionário com métricas de contiguidade:
        - connected_pairs: número de pares adjacentes
        - connected_components: número de componentes conectados
        - largest_component_size: tamanho do maior componente
        - adjacency_ratio: proporção de números conectados
    """
    grid = create_grid_from_numbers(numeros)
    coords = [number_to_coord(n) for n in numeros]
    
    # Conta pares adjacentes
    connected_pairs = 0
    adjacency_matrix = np.zeros((len(numeros), len(numeros)), dtype=int)
    
    for i, (l1, c1) in enumerate(coords):
        neighbors = get_neighbors(l1, c1, include_diagonal)
        for j, (l2, c2) in enumerate(coords):
            if i != j and (l2, c2) in neighbors:
                connected_pairs += 1
                adjacency_matrix[i, j] = 1
    
    # Conta pares únicos (evita contagem dupla)
    connected_pairs = connected_pairs // 2
    
    # Detecta componentes conectados usando DFS
    visited = set()
    components = []
    
    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in range(len(numeros)):
            if neighbor not in visited and adjacency_matrix[node, neighbor]:
                dfs(neighbor, component)
    
    for i in range(len(numeros)):
        if i not in visited:
            component = []
            dfs(i, component)
            components.append(component)
    
    largest_component_size = max(len(c) for c in components)
    num_components = len(components)
    
    # Razão de adjacência: quantos números têm pelo menos um vizinho
    nums_with_neighbors = sum(1 for i in range(len(numeros)) if adjacency_matrix[i].sum() > 0)
    adjacency_ratio = nums_with_neighbors / len(numeros)
    
    return {
        'connected_pairs': connected_pairs,
        'connected_components': num_components,
        'largest_component_size': largest_component_size,
        'adjacency_ratio': adjacency_ratio,
        'is_fully_connected': num_components == 1,
        'is_fully_dispersed': num_components == 6
    }


def analyze_spatial_dispersion(numeros: List[int]) -> Dict:
    """
    Analisa a dispersão espacial dos números no grid.
    
    Returns:
        Dicionário com métricas de dispersão:
        - centroid: coordenadas do centroide
        - mean_distance_to_centroid: distância média ao centroide
        - mean_pairwise_distance: distância média entre todos os pares
        - max_distance: maior distância entre 2 números
        - min_distance: menor distância entre 2 números
        - std_distance: desvio padrão das distâncias
    """
    coords = np.array([number_to_coord(n) for n in numeros])
    
    # Centroide
    centroid = coords.mean(axis=0)
    
    # Distâncias ao centroide (Manhattan)
    distances_to_centroid = np.abs(coords - centroid).sum(axis=1)
    mean_dist_centroid = distances_to_centroid.mean()
    
    # Distâncias par-a-par (Manhattan)
    pairwise_distances = []
    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            dist = np.abs(coords[i] - coords[j]).sum()
            pairwise_distances.append(dist)
    
    return {
        'centroid': tuple(centroid),
        'mean_distance_to_centroid': mean_dist_centroid,
        'mean_pairwise_distance': np.mean(pairwise_distances),
        'max_distance': np.max(pairwise_distances),
        'min_distance': np.min(pairwise_distances),
        'std_distance': np.std(pairwise_distances),
        'spread_row': coords[:, 0].max() - coords[:, 0].min(),
        'spread_col': coords[:, 1].max() - coords[:, 1].min()
    }


def classify_pattern(numeros: List[int]) -> str:
    """
    Classifica o padrão geométrico formado pelos números.
    
    Categorias:
    - LINHA_HORIZONTAL: todos na mesma linha
    - LINHA_VERTICAL: todos na mesma coluna
    - DIAGONAL: padrão diagonal
    - CLUSTER: agrupamento denso (componente único, alta adjacência)
    - SEMI_CLUSTER: agrupamento parcial
    - DISPERSO: números espalhados sem conexão
    - L_SHAPE: formato em L
    - T_SHAPE: formato em T
    """
    coords = np.array([number_to_coord(n) for n in numeros])
    contiguity = analyze_contiguity(numeros, include_diagonal=False)
    
    # Verifica linha horizontal (todos na mesma linha)
    if len(set(coords[:, 0])) == 1:
        return "LINHA_HORIZONTAL"
    
    # Verifica linha vertical (todos na mesma coluna)
    if len(set(coords[:, 1])) == 1:
        return "LINHA_VERTICAL"
    
    # Verifica diagonal
    # Diagonal principal: linha - coluna constante
    # Diagonal secundária: linha + coluna constante
    diff = coords[:, 0] - coords[:, 1]
    soma = coords[:, 0] + coords[:, 1]
    if len(set(diff)) <= 2 or len(set(soma)) <= 2:
        return "DIAGONAL"
    
    # Cluster: componente único e alta adjacência
    if contiguity['is_fully_connected'] and contiguity['adjacency_ratio'] >= 0.67:
        return "CLUSTER"
    
    # Semi-cluster: 2-3 componentes
    if contiguity['connected_components'] <= 3:
        return "SEMI_CLUSTER"
    
    # Disperso: muitos componentes ou baixa adjacência
    if contiguity['is_fully_dispersed'] or contiguity['adjacency_ratio'] < 0.4:
        return "DISPERSO"
    
    # Formas específicas (L, T, etc.) - análise mais complexa
    # Simplificação: se não se encaixou acima, é "IRREGULAR"
    return "IRREGULAR"


def analyze_symmetry(numeros: List[int]) -> Dict:
    """
    Analisa simetrias no padrão.
    
    Returns:
        - vertical_symmetry: score de simetria vertical (0-1)
        - horizontal_symmetry: score de simetria horizontal (0-1)
        - central_symmetry: score de simetria central (0-1)
    """
    grid = create_grid_from_numbers(numeros)
    
    # Simetria vertical (espelho no eixo vertical central)
    grid_v_flip = np.fliplr(grid)
    vertical_symmetry = (grid == grid_v_flip).sum() / grid.size
    
    # Simetria horizontal (espelho no eixo horizontal central)
    grid_h_flip = np.flipud(grid)
    horizontal_symmetry = (grid == grid_h_flip).sum() / grid.size
    
    # Simetria central (rotação 180°)
    grid_c_flip = np.rot90(grid, 2)
    central_symmetry = (grid == grid_c_flip).sum() / grid.size
    
    return {
        'vertical_symmetry': vertical_symmetry,
        'horizontal_symmetry': horizontal_symmetry,
        'central_symmetry': central_symmetry
    }


def analyze_region_distribution(numeros: List[int]) -> Dict:
    """
    Analisa distribuição por regiões do grid.
    
    Divide o grid em:
    - Quadrantes: Superior Esquerdo, Superior Direito, Inferior Esquerdo, Inferior Direito
    - Zonas: Topo (linhas 1-2), Meio (linhas 3-4), Base (linhas 5-6)
    - Laterais: Esquerda (colunas 1-3), Centro (colunas 4-7), Direita (colunas 8-10)
    """
    coords = [number_to_coord(n) for n in numeros]
    
    # Quadrantes (3 linhas × 5 colunas)
    quadrants = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0}
    for linha, coluna in coords:
        if linha < 3 and coluna < 5:
            quadrants['Q1'] += 1  # Superior Esquerdo
        elif linha < 3 and coluna >= 5:
            quadrants['Q2'] += 1  # Superior Direito
        elif linha >= 3 and coluna < 5:
            quadrants['Q3'] += 1  # Inferior Esquerdo
        else:
            quadrants['Q4'] += 1  # Inferior Direito
    
    # Zonas horizontais
    zones_h = {'TOPO': 0, 'MEIO': 0, 'BASE': 0}
    for linha, _ in coords:
        if linha < 2:
            zones_h['TOPO'] += 1
        elif linha < 4:
            zones_h['MEIO'] += 1
        else:
            zones_h['BASE'] += 1
    
    # Zonas verticais
    zones_v = {'ESQUERDA': 0, 'CENTRO': 0, 'DIREITA': 0}
    for _, coluna in coords:
        if coluna < 3:
            zones_v['ESQUERDA'] += 1
        elif coluna < 7:
            zones_v['CENTRO'] += 1
        else:
            zones_v['DIREITA'] += 1
    
    return {
        'quadrants': quadrants,
        'zones_horizontal': zones_h,
        'zones_vertical': zones_v
    }


def full_geometric_analysis(numeros: List[int]) -> Dict:
    """
    Análise geométrica completa de um sorteio.
    
    Args:
        numeros: Lista de 6 números sorteados
        
    Returns:
        Dicionário com todas as métricas e classificações
    """
    return {
        'numeros': sorted(numeros),
        'contiguity': analyze_contiguity(numeros, include_diagonal=False),
        'contiguity_diagonal': analyze_contiguity(numeros, include_diagonal=True),
        'dispersion': analyze_spatial_dispersion(numeros),
        'pattern': classify_pattern(numeros),
        'symmetry': analyze_symmetry(numeros),
        'regions': analyze_region_distribution(numeros)
    }


if __name__ == "__main__":
    # Testes com exemplos variados
    test_cases = [
        ([1, 2, 3, 4, 5, 6], "Linha horizontal"),
        ([1, 11, 21, 31, 41, 51], "Linha vertical"),
        ([4, 5, 30, 33, 41, 52], "Primeiro sorteio real"),
        ([1, 12, 23, 34, 45, 56], "Diagonal"),
        ([5, 10, 25, 40, 55, 60], "Disperso")
    ]
    
    print("🔍 Análise de Padrões Geométricos - Mega-Sena\n")
    
    for numeros, descricao in test_cases:
        print(f"\n{'='*60}")
        print(f"Teste: {descricao}")
        print(f"Números: {numeros}")
        
        analysis = full_geometric_analysis(numeros)
        
        print(f"\n📐 Padrão: {analysis['pattern']}")
        print(f"🔗 Pares conectados: {analysis['contiguity']['connected_pairs']}")
        print(f"📊 Componentes: {analysis['contiguity']['connected_components']}")
        print(f"📏 Dispersão média: {analysis['dispersion']['mean_pairwise_distance']:.2f}")
        print(f"🎯 Centroide: {analysis['dispersion']['centroid']}")

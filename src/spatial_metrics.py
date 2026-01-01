"""
Módulo de métricas espaciais para sorteios da Lotofácil.
Calcula dispersão, centroide e padrões de distribuição espacial.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import List
from .grid_mapping import build_number_coord_map, GridSpec


def manhattan(a: np.ndarray, b: np.ndarray) -> int:
    """
    Calcula a distância de Manhattan entre dois pontos.
    
    Args:
        a: Primeiro ponto (array de 2 elementos)
        b: Segundo ponto (array de 2 elementos)
        
    Returns:
        Distância de Manhattan (soma das diferenças absolutas)
    """
    return int(abs(a[0] - b[0]) + abs(a[1] - b[1]))


def draw_spatial_metrics(df: pd.DataFrame, ball_cols: List[str], spec: GridSpec = GridSpec()) -> pd.DataFrame:
    """
    Calcula métricas espaciais para cada sorteio.
    
    Para cada sorteio, calcula:
    - Centroide (ponto médio das coordenadas)
    - Dispersão em relação ao centroide
    - Distância média e máxima entre pares de números
    - Contagem de números nas bordas vs centro do grid
    
    Args:
        df: DataFrame com os sorteios
        ball_cols: Lista de colunas contendo os números sorteados
        spec: Especificação do grid
        
    Returns:
        DataFrame com uma linha por sorteio e colunas:
        - row_index: índice do sorteio original
        - mean_to_centroid: distância média ao centroide
        - max_to_centroid: distância máxima ao centroide
        - mean_pair_dist: distância média entre todos os pares
        - max_pair_dist: distância máxima entre pares
        - edge_count: quantidade de números nas bordas
        - center_count: quantidade de números no centro
    """
    n2c = build_number_coord_map(spec)

    rows = []
    for idx, row in df.iterrows():
        nums = row[ball_cols].tolist()
        coords = np.array([n2c[int(n)] for n in nums], dtype=int)  # shape (15,2)

        # centroide (média) e dispersão
        centroid = coords.mean(axis=0)
        dists_to_centroid = np.abs(coords - centroid).sum(axis=1)  # manhattan para centroid "real"
        mean_to_centroid = float(dists_to_centroid.mean())
        max_to_centroid = float(dists_to_centroid.max())

        # distância média entre todos os pares
        pair_dists = []
        for i in range(len(coords)):
            for j in range(i+1, len(coords)):
                pair_dists.append(manhattan(coords[i], coords[j]))
        mean_pair_dist = float(np.mean(pair_dists))
        max_pair_dist = float(np.max(pair_dists))

        # bias borda/centro: borda = r=0/4 ou c=0/4
        edge = int(((coords[:, 0] == 0) | (coords[:, 0] == spec.rows-1) |
                    (coords[:, 1] == 0) | (coords[:, 1] == spec.cols-1)).sum())
        center = 15 - edge

        rows.append({
            "row_index": int(idx),
            "mean_to_centroid": mean_to_centroid,
            "max_to_centroid": max_to_centroid,
            "mean_pair_dist": mean_pair_dist,
            "max_pair_dist": max_pair_dist,
            "edge_count": edge,
            "center_count": center,
        })

    return pd.DataFrame(rows)

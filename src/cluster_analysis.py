"""
Módulo de análise de clusters espaciais.
Detecta agrupamentos de números no grid usando DBSCAN com distância Manhattan.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sklearn.cluster import DBSCAN

from .grid_mapping import build_number_coord_map, GridSpec


def _pairwise_manhattan(coords: np.ndarray) -> np.ndarray:
    """
    Calcula matriz de distâncias de Manhattan entre todos os pontos.
    
    Args:
        coords: Array (N, 2) com coordenadas dos pontos
        
    Returns:
        Matriz (N, N) com distâncias de Manhattan
    """
    N = coords.shape[0]
    D = np.zeros((N, N), dtype=float)
    for i in range(N):
        for j in range(i+1, N):
            d = abs(coords[i, 0] - coords[j, 0]) + abs(coords[i, 1] - coords[j, 1])
            D[i, j] = D[j, i] = d
    return D


def cluster_numbers_dbscan(
    freq_by_number: np.ndarray,
    spec: GridSpec = GridSpec(),
    eps: float = 1.0,
    min_samples: int = 2,
    top_n: int = 25,
) -> pd.DataFrame:
    """
    Clusteriza os números mais frequentes usando DBSCAN com distância Manhattan.
    
    O algoritmo DBSCAN agrupa números que estão próximos no grid (vizinhos)
    e que aparecem com frequência similar.
    
    Args:
        freq_by_number: Array com frequência de cada número (índice 1..25)
        spec: Especificação do grid
        eps: Raio de vizinhança (padrão 1.0 = vizinhos imediatos)
        min_samples: Mínimo de pontos para formar um cluster
        top_n: Quantidade de números mais frequentes a considerar
        
    Returns:
        DataFrame com colunas:
        - number: número da lotofácil
        - freq: frequência do número
        - row: linha no grid (1-based)
        - col: coluna no grid (1-based)
        - cluster: ID do cluster (-1 = ruído/sem cluster)
        
    Notas:
        - eps=1.0: apenas vizinhos diretos (horizontal/vertical)
        - eps=1.5: inclui diagonais
        - eps=2.0: vizinhança 2x2
    """
    # seleciona os top_n números mais frequentes
    nums = [(n, int(freq_by_number[n])) for n in range(1, spec.n_max + 1)]
    nums.sort(key=lambda x: x[1], reverse=True)
    nums = nums[:top_n]

    # mapeia para coordenadas
    n2c = build_number_coord_map(spec)
    selected_numbers = [n for n, _ in nums]
    coords = np.array([n2c[n] for n in selected_numbers], dtype=int)

    # calcula matriz de distâncias Manhattan
    D = _pairwise_manhattan(coords)

    # aplica DBSCAN
    model = DBSCAN(eps=eps, min_samples=min_samples, metric="precomputed")
    labels = model.fit_predict(D)

    # monta resultado
    out = pd.DataFrame({
        "number": selected_numbers,
        "freq": [f for _, f in nums],
        "row": coords[:, 0] + 1,  # converte para 1-based
        "col": coords[:, 1] + 1,  # converte para 1-based
        "cluster": labels,
    }).sort_values(["cluster", "freq"], ascending=[True, False])

    return out

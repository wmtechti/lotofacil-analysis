"""
Módulo de análise de heatmap (mapa de calor) do grid da Lotofácil.
Calcula frequências de números por célula, linha e coluna.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import List, Dict
from .grid_mapping import build_number_coord_map, GridSpec


def compute_heatmap(df: pd.DataFrame, ball_cols: List[str], spec: GridSpec = GridSpec()) -> Dict[str, object]:
    """
    Calcula o heatmap de frequências no grid 5x5.
    
    Conta quantas vezes cada número (célula do grid) foi sorteado e agrega
    por linhas e colunas.
    
    Args:
        df: DataFrame com os sorteios
        ball_cols: Lista de colunas contendo os números sorteados
        spec: Especificação do grid
        
    Returns:
        Dicionário contendo:
        - heatmap_matrix: matriz numpy (5x5) com contagens
        - heatmap_df: DataFrame formatado do heatmap
        - row_df: DataFrame com frequência por linha
        - col_df: DataFrame com frequência por coluna
    """
    n2c = build_number_coord_map(spec)
    heat = np.zeros((spec.rows, spec.cols), dtype=int)

    # conta ocorrências de cada número
    for n in df[ball_cols].to_numpy().ravel():
        r, c = n2c[int(n)]
        heat[r, c] += 1

    # agrega por linha e coluna
    row_sum = heat.sum(axis=1)
    col_sum = heat.sum(axis=0)

    # cria DataFrames formatados
    heat_df = pd.DataFrame(
        heat, 
        index=[f"linha_{i+1}" for i in range(spec.rows)],
        columns=[f"col_{j+1}" for j in range(spec.cols)]
    )
    
    row_df = pd.DataFrame({
        "linha": [i+1 for i in range(spec.rows)], 
        "freq": row_sum
    })
    
    col_df = pd.DataFrame({
        "coluna": [j+1 for j in range(spec.cols)], 
        "freq": col_sum
    })

    return {
        "heatmap_matrix": heat,
        "heatmap_df": heat_df,
        "row_df": row_df,
        "col_df": col_df,
    }

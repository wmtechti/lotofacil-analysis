"""
Módulo de análise de co-ocorrência de números.
Calcula quais números tendem a sair juntos nos sorteios.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import List


def cooccurrence_matrix(df: pd.DataFrame, ball_cols: List[str], n_max: int = 25) -> np.ndarray:
    """
    Calcula a matriz de co-ocorrência de números.
    
    Para cada par de números, conta quantas vezes eles aparecem juntos
    no mesmo sorteio.
    
    Args:
        df: DataFrame com os sorteios
        ball_cols: Lista de colunas contendo os números sorteados
        n_max: Número máximo (25 para Lotofácil)
        
    Returns:
        Matriz numpy (26x26) onde mat[a][b] = quantas vezes os números a e b
        saíram juntos. Índice 0 não é usado.
    """
    mat = np.zeros((n_max + 1, n_max + 1), dtype=int)  # 1..25 (ignorando 0)
    
    for nums in df[ball_cols].to_numpy():
        nums = list(map(int, nums))
        # conta todas as combinações de pares
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                a, b = nums[i], nums[j]
                mat[a, b] += 1
                mat[b, a] += 1  # matriz simétrica
                
    return mat


def top_pairs(mat: np.ndarray, top_k: int = 50) -> pd.DataFrame:
    """
    Retorna os top K pares de números que mais saem juntos.
    
    Args:
        mat: Matriz de co-ocorrência
        top_k: Quantidade de pares a retornar
        
    Returns:
        DataFrame com colunas: a, b, count (ordenado por count decrescente)
    """
    pairs = []
    n = mat.shape[0] - 1
    
    # percorre apenas triângulo superior para evitar duplicatas
    for a in range(1, n+1):
        for b in range(a+1, n+1):
            pairs.append((a, b, int(mat[a, b])))
    
    # ordena por contagem decrescente
    pairs.sort(key=lambda x: x[2], reverse=True)
    pairs = pairs[:top_k]
    
    return pd.DataFrame(pairs, columns=["a", "b", "count"])

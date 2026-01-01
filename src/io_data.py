"""
Módulo de I/O para carregar sorteios da Lotofácil.
Lê arquivos CSV e valida os dados.
"""
from __future__ import annotations

import pandas as pd
from typing import List, Tuple

DEFAULT_BALL_COLS = [f"b{i}" for i in range(1, 16)]  # b1..b15


def load_draws_csv(path: str, ball_cols: List[str] | None = None) -> Tuple[pd.DataFrame, List[str]]:
    """
    Carrega sorteios da Lotofácil de um arquivo CSV.
    
    Formato esperado:
    - CSV com cabeçalho
    - 15 colunas de bolas (números sorteados)
    - Colunas padrão: b1, b2, ..., b15
    - Pode conter outras colunas (concurso, data, etc.)
    
    Args:
        path: Caminho do arquivo CSV
        ball_cols: Lista de nomes das colunas de bolas. Se None, tenta detectar automaticamente.
        
    Returns:
        Tupla (DataFrame completo, lista de colunas de bolas)
        
    Raises:
        ValueError: Se houver números fora do intervalo 1-25 ou duplicados no sorteio
    """
    df = pd.read_csv(path)

    if ball_cols is None:
        # tenta detectar colunas b1..b15
        ball_cols = [c for c in DEFAULT_BALL_COLS if c in df.columns]
        if len(ball_cols) != 15:
            # fallback: últimas 15 colunas
            ball_cols = list(df.columns[-15:])

    # garante int
    df[ball_cols] = df[ball_cols].astype(int)

    # valida faixas 1..25
    bad = (df[ball_cols] < 1).any(axis=1) | (df[ball_cols] > 25).any(axis=1)
    if bad.any():
        idxs = df.index[bad].tolist()[:10]
        raise ValueError(f"Encontrados números fora de 1..25 nas linhas: {idxs} (mostrando até 10)")

    # valida duplicidade dentro do sorteio
    dup = df[ball_cols].apply(lambda row: len(set(row.tolist())) != len(row.tolist()), axis=1)
    if dup.any():
        idxs = df.index[dup].tolist()[:10]
        raise ValueError(f"Encontradas duplicidades dentro do sorteio nas linhas: {idxs} (mostrando até 10)")

    return df, ball_cols

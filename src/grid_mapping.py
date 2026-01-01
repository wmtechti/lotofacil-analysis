"""
Módulo de mapeamento do grid 5x5 da Lotofácil.
Converte números (1..25) em coordenadas (linha, coluna) e vice-versa.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

GridCoord = Tuple[int, int]  # (row, col) 0-based


@dataclass(frozen=True)
class GridSpec:
    """Especificação do grid da Lotofácil."""
    rows: int = 5
    cols: int = 5
    n_min: int = 1
    n_max: int = 25


def number_to_coord(n: int, spec: GridSpec = GridSpec()) -> GridCoord:
    """
    Converte um número (1..25) para coordenada (linha, coluna) no grid 5x5.
    
    Layout do volante:
    1  2  3  4  5
    6  7  8  9  10
    11 12 13 14 15
    16 17 18 19 20
    21 22 23 24 25
    
    Args:
        n: Número de 1 a 25
        spec: Especificação do grid
        
    Returns:
        Tupla (row, col) com índices baseados em 0
        
    Raises:
        ValueError: Se o número estiver fora do intervalo válido
    """
    if not (spec.n_min <= n <= spec.n_max):
        raise ValueError(f"Número fora do intervalo: {n}")
    idx = n - spec.n_min  # 0..24
    r = idx // spec.cols
    c = idx % spec.cols
    return r, c


def coord_to_number(r: int, c: int, spec: GridSpec = GridSpec()) -> int:
    """
    Converte coordenada (linha, coluna) de volta para número (1..25).
    
    Args:
        r: Linha (0-based)
        c: Coluna (0-based)
        spec: Especificação do grid
        
    Returns:
        Número de 1 a 25
        
    Raises:
        ValueError: Se a coordenada for inválida
    """
    if not (0 <= r < spec.rows and 0 <= c < spec.cols):
        raise ValueError(f"Coord inválida: {(r,c)}")
    idx = r * spec.cols + c
    return spec.n_min + idx


def build_number_coord_map(spec: GridSpec = GridSpec()) -> Dict[int, GridCoord]:
    """
    Constrói um dicionário mapeando todos os números para suas coordenadas.
    
    Args:
        spec: Especificação do grid
        
    Returns:
        Dicionário {número: (linha, coluna)}
    """
    return {n: number_to_coord(n, spec) for n in range(spec.n_min, spec.n_max + 1)}

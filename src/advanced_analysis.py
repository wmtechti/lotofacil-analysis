"""
Módulo de análise de padrões avançados da Lotofácil.
Números quentes/frios, análise temporal e micro-clusters.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sklearn.cluster import DBSCAN, KMeans
from .grid_mapping import build_number_coord_map, GridSpec


def hot_cold_analysis(freq_by_number: np.ndarray, n_sorteios: int, 
                     spec: GridSpec = GridSpec()) -> pd.DataFrame:
    """
    Classifica números em quentes, médios e frios.
    
    Args:
        freq_by_number: Array com frequência de cada número
        n_sorteios: Total de sorteios
        spec: Especificação do grid
        
    Returns:
        DataFrame com classificação de cada número
    """
    expected_freq = (n_sorteios * 15) / 25  # frequência esperada (distribuição uniforme)
    
    results = []
    for n in range(1, spec.n_max + 1):
        freq = freq_by_number[n]
        deviation = ((freq - expected_freq) / expected_freq) * 100
        
        # Classificação
        if deviation > 1.5:
            category = "🔥 Quente"
        elif deviation < -1.5:
            category = "❄️ Frio"
        else:
            category = "🌡️ Médio"
        
        results.append({
            "numero": n,
            "freq": int(freq),
            "esperado": int(expected_freq),
            "desvio_%": round(deviation, 2),
            "categoria": category
        })
    
    df = pd.DataFrame(results)
    df = df.sort_values("desvio_%", ascending=False)
    return df


def temporal_trend_analysis(df: pd.DataFrame, ball_cols: List[str], 
                            window_size: int = 500) -> pd.DataFrame:
    """
    Analisa tendências temporais dos números mais quentes.
    
    Args:
        df: DataFrame com sorteios
        ball_cols: Colunas com números sorteados
        window_size: Tamanho da janela móvel
        
    Returns:
        DataFrame com tendências
    """
    trends = []
    
    for n in range(1, 26):
        # Conta em janelas móveis
        freq_over_time = []
        for i in range(0, len(df) - window_size, window_size // 2):
            window = df.iloc[i:i+window_size]
            count = (window[ball_cols] == n).sum().sum()
            freq_over_time.append(count)
        
        if len(freq_over_time) >= 2:
            # Tendência: últimas janelas vs primeiras
            recent = np.mean(freq_over_time[-3:]) if len(freq_over_time) >= 3 else freq_over_time[-1]
            old = np.mean(freq_over_time[:3]) if len(freq_over_time) >= 3 else freq_over_time[0]
            
            trend = ((recent - old) / old * 100) if old > 0 else 0
            
            trends.append({
                "numero": n,
                "tendencia_%": round(trend, 2),
                "status": "📈 Subindo" if trend > 5 else "📉 Caindo" if trend < -5 else "➡️ Estável"
            })
    
    return pd.DataFrame(trends).sort_values("tendencia_%", ascending=False)


def micro_clusters_analysis(freq_by_number: np.ndarray, 
                            spec: GridSpec = GridSpec()) -> Dict[str, pd.DataFrame]:
    """
    Detecta micro-clusters usando diferentes parâmetros.
    
    Args:
        freq_by_number: Array com frequência de cada número
        spec: Especificação do grid
        
    Returns:
        Dicionário com diferentes análises de clusters
    """
    from .cluster_analysis import _pairwise_manhattan
    
    n2c = build_number_coord_map(spec)
    numbers = list(range(1, spec.n_max + 1))
    coords = np.array([n2c[n] for n in numbers], dtype=int)
    
    # Matriz de distâncias
    D = _pairwise_manhattan(coords)
    
    results = {}
    
    # DBSCAN com eps menor (vizinhos imediatos)
    model1 = DBSCAN(eps=1.0, min_samples=3, metric="precomputed")
    labels1 = model1.fit_predict(D)
    
    results["vizinhos_imediatos"] = pd.DataFrame({
        "numero": numbers,
        "freq": [int(freq_by_number[n]) for n in numbers],
        "cluster": labels1
    }).sort_values(["cluster", "freq"], ascending=[True, False])
    
    # DBSCAN com eps médio (inclui diagonais)
    model2 = DBSCAN(eps=1.5, min_samples=3, metric="precomputed")
    labels2 = model2.fit_predict(D)
    
    results["com_diagonais"] = pd.DataFrame({
        "numero": numbers,
        "freq": [int(freq_by_number[n]) for n in numbers],
        "cluster": labels2
    }).sort_values(["cluster", "freq"], ascending=[True, False])
    
    # K-Means espacial (força 4 quadrantes)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels3 = kmeans.fit_predict(coords)
    
    results["quadrantes"] = pd.DataFrame({
        "numero": numbers,
        "freq": [int(freq_by_number[n]) for n in numbers],
        "quadrante": labels3
    }).sort_values(["quadrante", "freq"], ascending=[True, False])
    
    return results


def pair_strength_analysis(co_matrix: np.ndarray, top_n: int = 100) -> pd.DataFrame:
    """
    Analisa força de ligação entre pares e identifica super-pares.
    
    Args:
        co_matrix: Matriz de co-ocorrência
        top_n: Quantidade de pares a analisar
        
    Returns:
        DataFrame com análise de força dos pares
    """
    pairs = []
    
    for a in range(1, 26):
        for b in range(a+1, 26):
            count = int(co_matrix[a, b])
            
            # Força relativa (normalizada pelo máximo)
            pairs.append({
                "a": a,
                "b": b,
                "count": count,
            })
    
    df = pd.DataFrame(pairs).sort_values("count", ascending=False).head(top_n)
    
    # Adiciona força normalizada
    max_count = df['count'].max()
    df['forca_%'] = (df['count'] / max_count * 100).round(2)
    
    # Classifica
    df['categoria'] = df['forca_%'].apply(
        lambda x: "⭐⭐⭐ Super Par" if x >= 95 
        else "⭐⭐ Par Forte" if x >= 85 
        else "⭐ Par Médio"
    )
    
    return df


def edge_center_bias(df: pd.DataFrame, ball_cols: List[str], 
                     spec: GridSpec = GridSpec()) -> Dict[str, float]:
    """
    Calcula bias geral entre bordas e centro.
    
    Args:
        df: DataFrame com sorteios
        ball_cols: Colunas com números
        spec: Especificação do grid
        
    Returns:
        Dicionário com estatísticas de bias
    """
    n2c = build_number_coord_map(spec)
    
    edge_count = 0
    center_count = 0
    total_numbers = 0
    
    for nums in df[ball_cols].to_numpy():
        for n in nums:
            total_numbers += 1
            r, c = n2c[int(n)]
            
            # Borda: linha/coluna 0 ou 4
            if r == 0 or r == 4 or c == 0 or c == 4:
                edge_count += 1
            else:
                center_count += 1
    
    edge_percent = (edge_count / total_numbers) * 100
    center_percent = (center_count / total_numbers) * 100
    
    # Total de números possíveis nas bordas vs centro
    edge_positions = 16  # bordas do grid 5x5
    center_positions = 9  # centro
    
    expected_edge = (edge_positions / 25) * 100
    expected_center = (center_positions / 25) * 100
    
    return {
        "borda_%_real": round(edge_percent, 2),
        "centro_%_real": round(center_percent, 2),
        "borda_%_esperado": round(expected_edge, 2),
        "centro_%_esperado": round(expected_center, 2),
        "bias_borda": round(edge_percent - expected_edge, 2),
        "bias_centro": round(center_percent - expected_center, 2),
    }

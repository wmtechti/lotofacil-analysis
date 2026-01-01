"""
Script de análises avançadas da Lotofácil.
Executa análises de padrões, tendências e micro-clusters.
"""
from __future__ import annotations

import os
import sys
import json
import numpy as np

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.io_data import load_draws_csv
from src.cooccurrence import cooccurrence_matrix
from src.advanced_analysis import (
    hot_cold_analysis, temporal_trend_analysis, micro_clusters_analysis,
    pair_strength_analysis, edge_center_bias
)


def main():
    """Executa análises avançadas."""
    print("🔬 Iniciando análises avançadas da Lotofácil...")
    
    os.makedirs("out", exist_ok=True)
    
    # 1. Carrega dados
    print("📂 Carregando dados...")
    df, ball_cols = load_draws_csv("data/lotofacil_sorteios.csv")
    print(f"   ✓ {len(df)} sorteios carregados")
    
    # Calcula frequências
    freq_by_number = np.zeros(26, dtype=int)
    for n in df[ball_cols].to_numpy().ravel():
        freq_by_number[int(n)] += 1
    
    # 2. Análise Quente/Frio
    print("\n🌡️  Análise de números quentes/frios...")
    hot_cold_df = hot_cold_analysis(freq_by_number, len(df))
    hot_cold_df.to_csv("out/numeros_quentes_frios.csv", index=False)
    print("   ✓ Arquivo salvo: out/numeros_quentes_frios.csv")
    
    print("\n📊 Top 5 Mais Quentes:")
    for idx, row in hot_cold_df.head(5).iterrows():
        print(f"   {row['categoria']} Número {row['numero']:2d}: " +
              f"{row['freq']:,} vezes (desvio: {row['desvio_%']:+.2f}%)")
    
    print("\n📊 Top 5 Mais Frios:")
    for idx, row in hot_cold_df.tail(5).iterrows():
        print(f"   {row['categoria']} Número {row['numero']:2d}: " +
              f"{row['freq']:,} vezes (desvio: {row['desvio_%']:+.2f}%)")
    
    # 3. Tendências temporais
    print("\n📈 Análise de tendências temporais...")
    trends_df = temporal_trend_analysis(df, ball_cols, window_size=500)
    trends_df.to_csv("out/tendencias_temporais.csv", index=False)
    print("   ✓ Arquivo salvo: out/tendencias_temporais.csv")
    
    print("\n   Top 5 em alta:")
    for idx, row in trends_df.head(5).iterrows():
        print(f"   {row['status']} Número {row['numero']:2d}: {row['tendencia_%']:+.2f}%")
    
    print("\n   Top 5 em baixa:")
    for idx, row in trends_df.tail(5).iterrows():
        print(f"   {row['status']} Número {row['numero']:2d}: {row['tendencia_%']:+.2f}%")
    
    # 4. Micro-clusters
    print("\n🎯 Detectando micro-clusters...")
    clusters = micro_clusters_analysis(freq_by_number)
    
    for name, cluster_df in clusters.items():
        filename = f"out/clusters_{name}.csv"
        cluster_df.to_csv(filename, index=False)
        
        n_clusters = len(cluster_df[cluster_df.iloc[:, -1] >= 0].iloc[:, -1].unique())
        print(f"   ✓ {name}: {n_clusters} clusters identificados")
    
    # 5. Análise de força de pares
    print("\n🔗 Analisando força de pares...")
    co_matrix = cooccurrence_matrix(df, ball_cols, n_max=25)
    pairs_strength = pair_strength_analysis(co_matrix, top_n=50)
    pairs_strength.to_csv("out/pares_forca.csv", index=False)
    print("   ✓ Arquivo salvo: out/pares_forca.csv")
    
    print("\n   Super Pares (força > 95%):")
    super_pairs = pairs_strength[pairs_strength['forca_%'] >= 95]
    for idx, row in super_pairs.iterrows():
        print(f"   {row['categoria']} [{row['a']:2d} + {row['b']:2d}]: " +
              f"{row['count']:,} vezes ({row['forca_%']:.1f}%)")
    
    # 6. Bias borda/centro
    print("\n📐 Análise de bias borda/centro...")
    bias = edge_center_bias(df, ball_cols)
    
    with open("out/bias_borda_centro.json", "w", encoding="utf-8") as f:
        json.dump(bias, f, ensure_ascii=False, indent=2)
    
    print(f"   Bordas: {bias['borda_%_real']:.2f}% (esperado: {bias['borda_%_esperado']:.2f}%)")
    print(f"   Centro: {bias['centro_%_real']:.2f}% (esperado: {bias['centro_%_esperado']:.2f}%)")
    print(f"   Bias borda: {bias['bias_borda']:+.2f}%")
    print(f"   Bias centro: {bias['bias_centro']:+.2f}%")
    
    print("\n✅ Análises avançadas concluídas!")
    print("📁 Arquivos em: out/")


if __name__ == "__main__":
    main()

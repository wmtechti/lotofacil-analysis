"""
Script principal de análise da Lotofácil.
Executa todas as análises e gera os arquivos de saída.
"""
from __future__ import annotations

import os
import json
import numpy as np

from src.io_data import load_draws_csv
from src.heatmap_analysis import compute_heatmap
from src.spatial_metrics import draw_spatial_metrics
from src.cooccurrence import cooccurrence_matrix, top_pairs
from src.cluster_analysis import cluster_numbers_dbscan


def ensure_out_dir():
    """Cria o diretório de saída se não existir."""
    os.makedirs("out", exist_ok=True)


def main():
    """
    Executa o pipeline completo de análise.
    
    Passos:
    1. Carrega sorteios do CSV
    2. Gera heatmap do grid 5x5
    3. Calcula métricas espaciais por sorteio
    4. Calcula co-ocorrência de números
    5. Detecta clusters usando DBSCAN
    6. Salva todos os resultados em out/
    """
    print("🎯 Iniciando análise da Lotofácil...")
    ensure_out_dir()

    # 1. Carrega dados
    print("📂 Carregando sorteios...")
    df, ball_cols = load_draws_csv("data/lotofacil_sorteios.csv")
    print(f"   ✓ {len(df)} sorteios carregados")

    # 2. Heatmap
    print("🔥 Calculando heatmap do grid 5x5...")
    hm = compute_heatmap(df, ball_cols)
    hm["heatmap_df"].to_csv("out/heatmap_5x5.csv", index=True)
    hm["row_df"].to_csv("out/freq_linhas.csv", index=False)
    hm["col_df"].to_csv("out/freq_colunas.csv", index=False)
    print("   ✓ Heatmap gerado")

    # 3. Frequência por número (1..25)
    print("📊 Calculando frequências...")
    freq_by_number = np.zeros(26, dtype=int)
    for n in df[ball_cols].to_numpy().ravel():
        freq_by_number[int(n)] += 1

    # 4. Métricas espaciais por sorteio
    print("📐 Calculando métricas espaciais...")
    metrics_df = draw_spatial_metrics(df, ball_cols)
    metrics_df.to_csv("out/metrics_por_sorteio.csv", index=False)
    print("   ✓ Métricas calculadas")

    # 5. Co-ocorrência
    print("🔗 Analisando co-ocorrência de números...")
    co = cooccurrence_matrix(df, ball_cols, n_max=25)
    pairs_df = top_pairs(co, top_k=80)
    pairs_df.to_csv("out/top_pares_coocorrencia.csv", index=False)
    print(f"   ✓ Top 80 pares identificados")

    # 6. Clusters (DBSCAN Manhattan) nos números mais frequentes
    print("🎯 Detectando clusters espaciais (DBSCAN)...")
    clusters_df = cluster_numbers_dbscan(
        freq_by_number=freq_by_number,
        eps=1.0,          # vizinhança imediata (Manhattan <= 1)
        min_samples=2,
        top_n=25
    )
    clusters_df.to_csv("out/clusters_dbscan_manhattan.csv", index=False)
    n_clusters = len(clusters_df[clusters_df['cluster'] >= 0]['cluster'].unique())
    print(f"   ✓ {n_clusters} clusters identificados")

    # 7. Resumo em JSON
    print("💾 Salvando resumo...")
    summary = {
        "n_sorteios": int(len(df)),
        "heatmap_path": "out/heatmap_5x5.csv",
        "metrics_path": "out/metrics_por_sorteio.csv",
        "top_pairs_path": "out/top_pares_coocorrencia.csv",
        "clusters_path": "out/clusters_dbscan_manhattan.csv",
        "ball_cols_used": ball_cols,
        "n_clusters": n_clusters,
    }
    with open("out/summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n✅ Análise concluída!")
    print(f"📁 Arquivos gerados em: out/")
    print(f"📊 Total de sorteios analisados: {len(df)}")
    print(f"🎯 Total de clusters identificados: {n_clusters}")


if __name__ == "__main__":
    main()

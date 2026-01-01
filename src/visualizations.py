"""
Módulo de visualizações para análise da Lotofácil.
Gera gráficos, heatmaps e grafos de co-ocorrência.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import networkx as nx
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


def plot_heatmap_grid(heatmap_matrix: np.ndarray, output_path: str = "out/heatmap_grid.png"):
    """
    Cria heatmap visual do grid 5x5 com números da Lotofácil.
    
    Args:
        heatmap_matrix: Matriz 5x5 com frequências
        output_path: Caminho para salvar a imagem
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Cria o heatmap
    sns.heatmap(heatmap_matrix, 
                annot=True, 
                fmt='d', 
                cmap='YlOrRd',
                cbar_kws={'label': 'Frequência'},
                linewidths=2,
                linecolor='white',
                ax=ax)
    
    # Adiciona os números da lotofácil em cada célula
    for i in range(5):
        for j in range(5):
            number = i * 5 + j + 1
            freq = heatmap_matrix[i, j]
            ax.text(j + 0.5, i + 0.2, f'#{number}', 
                   ha='center', va='center', 
                   fontsize=14, fontweight='bold', color='darkblue')
    
    ax.set_xlabel('Coluna', fontsize=12, fontweight='bold')
    ax.set_ylabel('Linha', fontsize=12, fontweight='bold')
    ax.set_title('Heatmap do Grid 5×5 da Lotofácil\nFrequência de Sorteios por Número', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Heatmap salvo em: {output_path}")
    plt.close()


def plot_frequency_bars(freq_by_number: np.ndarray, output_path: str = "out/freq_barras.png"):
    """
    Gráfico de barras da frequência de cada número.
    
    Args:
        freq_by_number: Array com frequência de cada número (índice 1..25)
        output_path: Caminho para salvar a imagem
    """
    numbers = list(range(1, 26))
    freqs = [freq_by_number[n] for n in numbers]
    
    # Identifica os 5 mais e menos sorteados
    top5_idx = np.argsort(freqs)[-5:]
    bottom5_idx = np.argsort(freqs)[:5]
    
    colors = ['#ff4444' if i in bottom5_idx else '#44ff44' if i in top5_idx else '#4488ff' 
              for i in range(25)]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(numbers, freqs, color=colors, edgecolor='black', linewidth=0.7)
    
    ax.set_xlabel('Número', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequência', fontsize=12, fontweight='bold')
    ax.set_title('Frequência de Sorteio por Número\n🟢 Top 5 | 🔵 Médio | 🔴 Bottom 5', 
                fontsize=14, fontweight='bold')
    ax.set_xticks(numbers)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adiciona valores nas barras mais altas
    for i in top5_idx:
        ax.text(numbers[i], freqs[i], f'{freqs[i]}', 
               ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico de barras salvo em: {output_path}")
    plt.close()


def plot_row_col_comparison(row_df: pd.DataFrame, col_df: pd.DataFrame, 
                            output_path: str = "out/linhas_colunas.png"):
    """
    Compara frequências por linha e coluna.
    
    Args:
        row_df: DataFrame com frequências por linha
        col_df: DataFrame com frequências por coluna
        output_path: Caminho para salvar a imagem
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Linhas
    colors_row = ['#ff6b6b' if f == row_df['freq'].max() else 
                  '#4ecdc4' if f == row_df['freq'].min() else '#95e1d3' 
                  for f in row_df['freq']]
    ax1.bar(row_df['linha'], row_df['freq'], color=colors_row, edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('Linha (1-5)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Frequência Total', fontsize=11, fontweight='bold')
    ax1.set_title('Frequência por Linha do Grid', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    for i, (linha, freq) in enumerate(zip(row_df['linha'], row_df['freq'])):
        ax1.text(linha, freq, f'{freq}', ha='center', va='bottom', fontweight='bold')
    
    # Colunas
    colors_col = ['#ff6b6b' if f == col_df['freq'].max() else 
                  '#4ecdc4' if f == col_df['freq'].min() else '#95e1d3' 
                  for f in col_df['freq']]
    ax2.bar(col_df['coluna'], col_df['freq'], color=colors_col, edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Coluna (1-5)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Frequência Total', fontsize=11, fontweight='bold')
    ax2.set_title('Frequência por Coluna do Grid', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    for i, (col, freq) in enumerate(zip(col_df['coluna'], col_df['freq'])):
        ax2.text(col, freq, f'{freq}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Comparação linhas/colunas salva em: {output_path}")
    plt.close()


def plot_cooccurrence_network(pairs_df: pd.DataFrame, top_n: int = 30, 
                              output_path: str = "out/rede_coocorrencia.png"):
    """
    Cria grafo de rede mostrando co-ocorrência entre números.
    
    Args:
        pairs_df: DataFrame com pares e suas contagens
        top_n: Quantidade de pares a mostrar
        output_path: Caminho para salvar a imagem
    """
    G = nx.Graph()
    
    # Adiciona arestas (top N pares)
    top_pairs = pairs_df.head(top_n)
    for _, row in top_pairs.iterrows():
        G.add_edge(row['a'], row['b'], weight=row['count'])
    
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Layout circular
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Tamanho dos nós baseado no grau (quantas conexões)
    node_sizes = [G.degree(n) * 200 for n in G.nodes()]
    
    # Espessura das arestas baseada no peso
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights)
    edge_widths = [5 * (w / max_weight) for w in weights]
    
    # Desenha a rede
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                          node_color='#3498db', alpha=0.8, ax=ax)
    nx.draw_networkx_edges(G, pos, width=edge_widths, 
                          alpha=0.5, edge_color='#e74c3c', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, 
                           font_weight='bold', font_color='white', ax=ax)
    
    ax.set_title(f'Rede de Co-ocorrência - Top {top_n} Pares Mais Frequentes\n' +
                'Espessura da linha = Frequência de saída conjunta', 
                fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Rede de co-ocorrência salva em: {output_path}")
    plt.close()


def plot_spatial_metrics_distribution(metrics_df: pd.DataFrame, 
                                      output_path: str = "out/metricas_espaciais.png"):
    """
    Distribui as métricas espaciais dos sorteios.
    
    Args:
        metrics_df: DataFrame com métricas por sorteio
        output_path: Caminho para salvar a imagem
    """
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    metrics = [
        ('mean_to_centroid', 'Distância Média ao Centroide'),
        ('mean_pair_dist', 'Distância Média Entre Pares'),
        ('max_pair_dist', 'Distância Máxima Entre Pares'),
        ('edge_count', 'Números nas Bordas'),
        ('center_count', 'Números no Centro'),
    ]
    
    for idx, (metric, title) in enumerate(metrics):
        row = idx // 3
        col = idx % 3
        ax = axes[row, col]
        
        ax.hist(metrics_df[metric], bins=30, color='#3498db', 
               edgecolor='black', alpha=0.7)
        ax.axvline(metrics_df[metric].mean(), color='red', 
                  linestyle='--', linewidth=2, label=f'Média: {metrics_df[metric].mean():.2f}')
        ax.set_xlabel(title, fontsize=10, fontweight='bold')
        ax.set_ylabel('Frequência', fontsize=10)
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
    
    # Remove último subplot se não usado
    if len(metrics) < 6:
        fig.delaxes(axes[1, 2])
    
    fig.suptitle('Distribuição das Métricas Espaciais dos Sorteios', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Métricas espaciais salvas em: {output_path}")
    plt.close()


def create_summary_report(freq_by_number: np.ndarray, pairs_df: pd.DataFrame,
                         metrics_df: pd.DataFrame, n_sorteios: int,
                         output_path: str = "out/relatorio_resumo.txt"):
    """
    Cria relatório em texto com resumo das análises.
    
    Args:
        freq_by_number: Array com frequência de cada número
        pairs_df: DataFrame com pares mais frequentes
        metrics_df: DataFrame com métricas espaciais
        n_sorteios: Número total de sorteios
        output_path: Caminho para salvar o relatório
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RELATÓRIO DE ANÁLISE ESPACIAL - LOTOFÁCIL\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"📊 Total de sorteios analisados: {n_sorteios:,}\n")
        f.write(f"📅 Período: 29/09/2003 até presente\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("🔥 TOP 10 NÚMEROS MAIS SORTEADOS\n")
        f.write("-" * 80 + "\n")
        nums_sorted = [(n, freq_by_number[n]) for n in range(1, 26)]
        nums_sorted.sort(key=lambda x: x[1], reverse=True)
        for i, (num, freq) in enumerate(nums_sorted[:10], 1):
            percent = (freq / (n_sorteios * 15)) * 100
            f.write(f"{i:2d}. Número {num:2d}: {freq:,} vezes ({percent:.2f}%)\n")
        
        f.write("\n" + "-" * 80 + "\n")
        f.write("❄️  TOP 10 NÚMEROS MENOS SORTEADOS\n")
        f.write("-" * 80 + "\n")
        for i, (num, freq) in enumerate(nums_sorted[-10:][::-1], 1):
            percent = (freq / (n_sorteios * 15)) * 100
            f.write(f"{i:2d}. Número {num:2d}: {freq:,} vezes ({percent:.2f}%)\n")
        
        f.write("\n" + "-" * 80 + "\n")
        f.write("🔗 TOP 15 PARES QUE MAIS SAEM JUNTOS\n")
        f.write("-" * 80 + "\n")
        for i, row in pairs_df.head(15).iterrows():
            percent = (row['count'] / n_sorteios) * 100
            f.write(f"{i+1:2d}. [{row['a']:2d} + {row['b']:2d}]: {row['count']:,} vezes ({percent:.2f}%)\n")
        
        f.write("\n" + "-" * 80 + "\n")
        f.write("📐 MÉTRICAS ESPACIAIS MÉDIAS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Distância média ao centroide: {metrics_df['mean_to_centroid'].mean():.2f}\n")
        f.write(f"Distância média entre pares: {metrics_df['mean_pair_dist'].mean():.2f}\n")
        f.write(f"Números nas bordas (média): {metrics_df['edge_count'].mean():.2f}\n")
        f.write(f"Números no centro (média): {metrics_df['center_count'].mean():.2f}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("Análise gerada pelo sistema de análise espacial da Lotofácil\n")
        f.write("=" * 80 + "\n")
    
    print(f"✓ Relatório resumo salvo em: {output_path}")

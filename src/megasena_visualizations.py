"""
Visualizações dos padrões geométricos da Mega-Sena no grid 6×10.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from typing import List, Dict
from megasena_grid_mapping import number_to_coord, create_grid_from_numbers


def plot_single_draw_grid(numeros: List[int], concurso: int = None, 
                          save_path: str = None, show_numbers: bool = True):
    """
    Visualiza um único sorteio no grid 6×10.
    
    Args:
        numeros: Lista de 6 números sorteados
        concurso: Número do concurso (opcional)
        save_path: Caminho para salvar a imagem
        show_numbers: Se True, mostra os números nas células
    """
    grid = create_grid_from_numbers(numeros)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Criar grid visual
    for linha in range(6):
        for coluna in range(10):
            numero = linha * 10 + coluna + 1
            
            # Cor de fundo
            if grid[linha, coluna] == 1:
                color = '#FF6B6B'  # Vermelho para sorteados
                edge_color = '#C92A2A'
                edge_width = 3
            else:
                color = '#E9ECEF'  # Cinza claro
                edge_color = '#ADB5BD'
                edge_width = 1
            
            # Desenhar célula
            rect = patches.Rectangle(
                (coluna, 5-linha), 1, 1,
                linewidth=edge_width,
                edgecolor=edge_color,
                facecolor=color
            )
            ax.add_patch(rect)
            
            # Adicionar número
            if show_numbers:
                text_color = 'white' if grid[linha, coluna] == 1 else '#495057'
                weight = 'bold' if grid[linha, coluna] == 1 else 'normal'
                ax.text(
                    coluna + 0.5, 5-linha + 0.5, str(numero),
                    ha='center', va='center',
                    fontsize=11, color=text_color, weight=weight
                )
    
    # Configurações do plot
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Título
    title = f"Mega-Sena - Concurso {concurso}" if concurso else "Mega-Sena - Grid 6×10"
    subtitle = f"Números sorteados: {sorted(numeros)}"
    fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    ax.text(5, -0.5, subtitle, ha='center', fontsize=12, color='#495057')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Salvo: {save_path}")
    
    plt.close()


def plot_heatmap_frequency(all_draws: List[List[int]], save_path: str = None):
    """
    Heatmap de frequência: quantas vezes cada número foi sorteado.
    
    Args:
        all_draws: Lista de sorteios, cada um com 6 números
        save_path: Caminho para salvar
    """
    # Criar grid de frequências
    freq_grid = np.zeros((6, 10))
    
    for draw in all_draws:
        for numero in draw:
            linha, coluna = number_to_coord(numero)
            freq_grid[linha, coluna] += 1
    
    # Plot
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Heatmap
    im = ax.imshow(freq_grid, cmap='YlOrRd', aspect='auto')
    
    # Adicionar valores nas células
    for linha in range(6):
        for coluna in range(10):
            numero = linha * 10 + coluna + 1
            freq = int(freq_grid[linha, coluna])
            
            text = ax.text(
                coluna, linha, f"{numero}\n({freq})",
                ha='center', va='center',
                color='white' if freq > freq_grid.mean() else 'black',
                fontsize=9, weight='bold'
            )
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Frequência de Sorteios', fontsize=12)
    
    # Configurações
    ax.set_xticks(range(10))
    ax.set_xticklabels([f'Col {i+1}' for i in range(10)])
    ax.set_yticks(range(6))
    ax.set_yticklabels([f'Linha {i+1}' for i in range(6)])
    
    ax.set_title(
        f'Heatmap de Frequências - Mega-Sena\n{len(all_draws)} sorteios analisados',
        fontsize=16, fontweight='bold', pad=20
    )
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Salvo: {save_path}")
    
    plt.close()


def plot_pattern_distribution(patterns: List[str], save_path: str = None):
    """
    Gráfico de distribuição dos padrões geométricos.
    
    Args:
        patterns: Lista de classificações de padrões
        save_path: Caminho para salvar
    """
    from collections import Counter
    
    pattern_counts = Counter(patterns)
    
    # Ordenar por frequência
    patterns_sorted = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
    labels = [p[0] for p in patterns_sorted]
    values = [p[1] for p in patterns_sorted]
    percentages = [100 * v / len(patterns) for v in values]
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = sns.color_palette("husl", len(labels))
    bars = ax.barh(labels, values, color=colors, edgecolor='black', linewidth=1.5)
    
    # Adicionar valores nas barras
    for i, (bar, val, pct) in enumerate(zip(bars, values, percentages)):
        ax.text(
            val + max(values)*0.01, bar.get_y() + bar.get_height()/2,
            f'{val} ({pct:.1f}%)',
            va='center', fontsize=11, weight='bold'
        )
    
    ax.set_xlabel('Quantidade de Sorteios', fontsize=12, weight='bold')
    ax.set_ylabel('Padrão Geométrico', fontsize=12, weight='bold')
    ax.set_title(
        f'Distribuição de Padrões Geométricos - Mega-Sena\n{len(patterns)} sorteios',
        fontsize=16, fontweight='bold', pad=20
    )
    
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Salvo: {save_path}")
    
    plt.close()


def plot_contiguity_scatter(contiguity_data: List[Dict], save_path: str = None):
    """
    Scatter plot: pares conectados vs componentes conectados.
    
    Args:
        contiguity_data: Lista de dicionários de análise de contiguidade
        save_path: Caminho para salvar
    """
    connected_pairs = [d['connected_pairs'] for d in contiguity_data]
    components = [d['connected_components'] for d in contiguity_data]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Scatter
    scatter = ax.scatter(
        connected_pairs, components,
        alpha=0.5, s=50, c=connected_pairs,
        cmap='viridis', edgecolors='black', linewidth=0.5
    )
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Pares Conectados', fontsize=11)
    
    # Estatísticas
    from scipy import stats
    correlation = stats.pearsonr(connected_pairs, components)[0]
    
    ax.text(
        0.05, 0.95,
        f'Correlação: {correlation:.3f}\nN = {len(contiguity_data)}',
        transform=ax.transAxes,
        fontsize=11, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )
    
    ax.set_xlabel('Pares Conectados (adjacentes)', fontsize=12, weight='bold')
    ax.set_ylabel('Componentes Conectados', fontsize=12, weight='bold')
    ax.set_title(
        'Análise de Contiguidade - Mega-Sena',
        fontsize=16, fontweight='bold', pad=20
    )
    
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Salvo: {save_path}")
    
    plt.close()


def plot_dispersion_distribution(dispersion_data: List[Dict], save_path: str = None):
    """
    Distribuição das métricas de dispersão espacial.
    
    Args:
        dispersion_data: Lista de dicionários de análise de dispersão
        save_path: Caminho para salvar
    """
    mean_dists = [d['mean_pairwise_distance'] for d in dispersion_data]
    max_dists = [d['max_distance'] for d in dispersion_data]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histograma distância média
    axes[0].hist(mean_dists, bins=30, color='#4ECDC4', edgecolor='black', alpha=0.7)
    axes[0].axvline(np.mean(mean_dists), color='red', linestyle='--', linewidth=2,
                    label=f'Média: {np.mean(mean_dists):.2f}')
    axes[0].set_xlabel('Distância Média Entre Números', fontsize=11, weight='bold')
    axes[0].set_ylabel('Frequência', fontsize=11, weight='bold')
    axes[0].set_title('Distribuição da Dispersão Média', fontsize=13, weight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Histograma distância máxima
    axes[1].hist(max_dists, bins=30, color='#FF6B6B', edgecolor='black', alpha=0.7)
    axes[1].axvline(np.mean(max_dists), color='blue', linestyle='--', linewidth=2,
                    label=f'Média: {np.mean(max_dists):.2f}')
    axes[1].set_xlabel('Distância Máxima', fontsize=11, weight='bold')
    axes[1].set_ylabel('Frequência', fontsize=11, weight='bold')
    axes[1].set_title('Distribuição da Dispersão Máxima', fontsize=13, weight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    fig.suptitle('Análise de Dispersão Espacial - Mega-Sena', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Salvo: {save_path}")
    
    plt.close()


def plot_region_heatmap(region_data: List[Dict], save_path: str = None):
    """
    Heatmap de concentração por quadrantes.
    
    Args:
        region_data: Lista de dicionários de análise regional
        save_path: Caminho para salvar
    """
    # Agregar dados de quadrantes
    quadrant_totals = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0}
    
    for data in region_data:
        for q, count in data['quadrants'].items():
            quadrant_totals[q] += count
    
    # Converter para matriz 2×2
    quad_matrix = np.array([
        [quadrant_totals['Q1'], quadrant_totals['Q2']],
        [quadrant_totals['Q3'], quadrant_totals['Q4']]
    ])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    im = ax.imshow(quad_matrix, cmap='Oranges', aspect='auto')
    
    # Adicionar valores
    for i in range(2):
        for j in range(2):
            q_name = ['Q1', 'Q2', 'Q3', 'Q4'][i*2 + j]
            pct = 100 * quad_matrix[i, j] / quad_matrix.sum()
            text = ax.text(
                j, i, f'{q_name}\n{int(quad_matrix[i, j])}\n({pct:.1f}%)',
                ha='center', va='center',
                color='white' if quad_matrix[i, j] > quad_matrix.mean() else 'black',
                fontsize=14, weight='bold'
            )
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Frequência Total', fontsize=12)
    
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Esquerda', 'Direita'], fontsize=12)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Superior', 'Inferior'], fontsize=12)
    
    ax.set_title(
        f'Concentração por Quadrantes - Mega-Sena\n{len(region_data)} sorteios',
        fontsize=16, fontweight='bold', pad=20
    )
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Salvo: {save_path}")
    
    plt.close()


if __name__ == "__main__":
    # Teste visual com primeiro sorteio
    test_draw = [4, 5, 30, 33, 41, 52]
    
    print("🎨 Criando visualização de teste...")
    plot_single_draw_grid(test_draw, concurso=1, save_path="out/test_draw.png")

"""
Pipeline principal de análise geométrica da Mega-Sena.

Processa todos os sorteios e gera:
1. Análise estatística de padrões geométricos
2. Visualizações
3. Relatório de insights
"""

import sys
import os
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
import numpy as np
from tqdm import tqdm
from collections import Counter
import json

from megasena_grid_mapping import number_to_coord, create_grid_from_numbers, print_grid
from megasena_geometric_analysis import full_geometric_analysis
from megasena_visualizations import (
    plot_single_draw_grid,
    plot_heatmap_frequency,
    plot_pattern_distribution,
    plot_contiguity_scatter,
    plot_dispersion_distribution,
    plot_region_heatmap
)


def load_megasena_data(csv_path: str = "data/mega-sena.csv") -> pd.DataFrame:
    """
    Carrega dados da Mega-Sena do CSV.
    
    Returns:
        DataFrame com colunas Concurso e Bola1-Bola6
    """
    print(f"📂 Carregando dados: {csv_path}")
    
    df = pd.read_csv(csv_path, encoding='utf-8')
    
    # Verificar colunas esperadas
    ball_cols = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    
    if not all(col in df.columns for col in ball_cols):
        raise ValueError(f"CSV deve conter colunas: {ball_cols}")
    
    # Validação
    for col in ball_cols:
        if df[col].min() < 1 or df[col].max() > 60:
            raise ValueError(f"Números devem estar entre 1 e 60. Encontrado: {df[col].min()}-{df[col].max()}")
    
    print(f"✅ {len(df)} sorteios carregados")
    
    return df


def analyze_all_draws(df: pd.DataFrame) -> list:
    """
    Analisa todos os sorteios e retorna lista de análises.
    
    Args:
        df: DataFrame com sorteios
        
    Returns:
        Lista de dicionários com análise completa de cada sorteio
    """
    print("\n🔍 Analisando padrões geométricos...")
    
    ball_cols = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    results = []
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processando"):
        numeros = row[ball_cols].tolist()
        concurso = row['Concurso'] if 'Concurso' in df.columns else idx + 1
        
        analysis = full_geometric_analysis(numeros)
        analysis['concurso'] = concurso
        
        results.append(analysis)
    
    print(f"✅ {len(results)} sorteios analisados")
    
    return results


def generate_summary_report(analyses: list, output_path: str = "out/megasena_geometric_report.txt"):
    """
    Gera relatório em texto com estatísticas agregadas.
    
    Args:
        analyses: Lista de análises de sorteios
        output_path: Caminho para salvar relatório
    """
    print("\n📊 Gerando relatório estatístico...")
    
    # Coletar métricas
    patterns = [a['pattern'] for a in analyses]
    connected_pairs = [a['contiguity']['connected_pairs'] for a in analyses]
    components = [a['contiguity']['connected_components'] for a in analyses]
    adjacency_ratios = [a['contiguity']['adjacency_ratio'] for a in analyses]
    mean_distances = [a['dispersion']['mean_pairwise_distance'] for a in analyses]
    max_distances = [a['dispersion']['max_distance'] for a in analyses]
    
    # Contadores
    pattern_counts = Counter(patterns)
    fully_connected = sum(1 for a in analyses if a['contiguity']['is_fully_connected'])
    fully_dispersed = sum(1 for a in analyses if a['contiguity']['is_fully_dispersed'])
    
    # Criar relatório
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("RELATÓRIO DE ANÁLISE GEOMÉTRICA - MEGA-SENA")
    report_lines.append("Grid 6×10 (Números 1-60)")
    report_lines.append("=" * 80)
    report_lines.append(f"\n📊 ESTATÍSTICAS GERAIS")
    report_lines.append(f"  Total de sorteios analisados: {len(analyses)}")
    report_lines.append(f"  Período: Concurso {analyses[0]['concurso']} até {analyses[-1]['concurso']}")
    
    report_lines.append(f"\n📐 DISTRIBUIÇÃO DE PADRÕES GEOMÉTRICOS")
    for pattern, count in pattern_counts.most_common():
        percentage = 100 * count / len(analyses)
        report_lines.append(f"  {pattern:20s}: {count:4d} sorteios ({percentage:5.2f}%)")
    
    report_lines.append(f"\n🔗 ANÁLISE DE CONTIGUIDADE")
    report_lines.append(f"  Pares conectados (média): {np.mean(connected_pairs):.2f}")
    report_lines.append(f"  Pares conectados (mín-máx): {np.min(connected_pairs)}-{np.max(connected_pairs)}")
    report_lines.append(f"  Componentes conectados (média): {np.mean(components):.2f}")
    report_lines.append(f"  Razão de adjacência (média): {np.mean(adjacency_ratios):.2%}")
    report_lines.append(f"  Sorteios totalmente conectados: {fully_connected} ({100*fully_connected/len(analyses):.2f}%)")
    report_lines.append(f"  Sorteios totalmente dispersos: {fully_dispersed} ({100*fully_dispersed/len(analyses):.2f}%)")
    
    report_lines.append(f"\n📏 ANÁLISE DE DISPERSÃO ESPACIAL")
    report_lines.append(f"  Distância média (média): {np.mean(mean_distances):.2f}")
    report_lines.append(f"  Distância média (mín-máx): {np.min(mean_distances):.2f}-{np.max(mean_distances):.2f}")
    report_lines.append(f"  Distância máxima (média): {np.mean(max_distances):.2f}")
    report_lines.append(f"  Distância máxima (mín-máx): {np.min(max_distances):.2f}-{np.max(max_distances):.2f}")
    
    # Análise regional
    report_lines.append(f"\n🗺️  ANÁLISE REGIONAL (Quadrantes)")
    quadrant_totals = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0}
    for a in analyses:
        for q, count in a['regions']['quadrants'].items():
            quadrant_totals[q] += count
    
    total_numbers = sum(quadrant_totals.values())
    report_lines.append(f"  Q1 (Superior Esquerdo): {quadrant_totals['Q1']:5d} ({100*quadrant_totals['Q1']/total_numbers:.2f}%)")
    report_lines.append(f"  Q2 (Superior Direito):  {quadrant_totals['Q2']:5d} ({100*quadrant_totals['Q2']/total_numbers:.2f}%)")
    report_lines.append(f"  Q3 (Inferior Esquerdo): {quadrant_totals['Q3']:5d} ({100*quadrant_totals['Q3']/total_numbers:.2f}%)")
    report_lines.append(f"  Q4 (Inferior Direito):  {quadrant_totals['Q4']:5d} ({100*quadrant_totals['Q4']/total_numbers:.2f}%)")
    
    # Top 5 sorteios mais conectados
    report_lines.append(f"\n🏆 TOP 5 SORTEIOS MAIS CONECTADOS")
    sorted_by_pairs = sorted(analyses, key=lambda x: x['contiguity']['connected_pairs'], reverse=True)
    for i, a in enumerate(sorted_by_pairs[:5], 1):
        nums = sorted(a['numeros'])
        pairs = a['contiguity']['connected_pairs']
        pattern = a['pattern']
        report_lines.append(f"  {i}. Concurso {a['concurso']}: {nums} - {pairs} pares ({pattern})")
    
    # Top 5 sorteios mais dispersos
    report_lines.append(f"\n🌐 TOP 5 SORTEIOS MAIS DISPERSOS")
    sorted_by_dist = sorted(analyses, key=lambda x: x['dispersion']['mean_pairwise_distance'], reverse=True)
    for i, a in enumerate(sorted_by_dist[:5], 1):
        nums = sorted(a['numeros'])
        dist = a['dispersion']['mean_pairwise_distance']
        pattern = a['pattern']
        report_lines.append(f"  {i}. Concurso {a['concurso']}: {nums} - Dist {dist:.2f} ({pattern})")
    
    report_lines.append("\n" + "=" * 80)
    
    # Salvar relatório
    report_text = "\n".join(report_lines)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"✅ Relatório salvo: {output_path}")
    print("\n" + report_text)


def generate_visualizations(df: pd.DataFrame, analyses: list):
    """
    Gera todas as visualizações.
    
    Args:
        df: DataFrame com sorteios
        analyses: Lista de análises
    """
    print("\n🎨 Gerando visualizações...")
    
    os.makedirs("out", exist_ok=True)
    
    # 1. Heatmap de frequências
    ball_cols = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    all_draws = df[ball_cols].values.tolist()
    plot_heatmap_frequency(all_draws, save_path="out/megasena_heatmap_frequency.png")
    
    # 2. Distribuição de padrões
    patterns = [a['pattern'] for a in analyses]
    plot_pattern_distribution(patterns, save_path="out/megasena_pattern_distribution.png")
    
    # 3. Scatter de contiguidade
    contiguity_data = [a['contiguity'] for a in analyses]
    plot_contiguity_scatter(contiguity_data, save_path="out/megasena_contiguity_scatter.png")
    
    # 4. Distribuição de dispersão
    dispersion_data = [a['dispersion'] for a in analyses]
    plot_dispersion_distribution(dispersion_data, save_path="out/megasena_dispersion_dist.png")
    
    # 5. Heatmap regional
    region_data = [a['regions'] for a in analyses]
    plot_region_heatmap(region_data, save_path="out/megasena_region_heatmap.png")
    
    # 6. Exemplos de sorteios (primeiros 10 e alguns padrões específicos)
    print("  Criando grids de exemplo...")
    
    for idx in range(min(10, len(df))):
        numeros = df.iloc[idx][ball_cols].tolist()
        concurso = df.iloc[idx]['Concurso'] if 'Concurso' in df.columns else idx + 1
        plot_single_draw_grid(
            numeros, concurso=concurso,
            save_path=f"out/draw_examples/concurso_{concurso:04d}.png"
        )
    
    print("✅ Todas as visualizações geradas!")


def save_json_results(analyses: list, output_path: str = "out/megasena_analyses.json"):
    """
    Salva resultados completos em JSON.
    
    Args:
        analyses: Lista de análises
        output_path: Caminho para salvar JSON
    """
    print(f"\n💾 Salvando resultados em JSON: {output_path}")
    
    # Converter numpy types para tipos nativos Python
    def convert_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(convert_types(item) for item in obj)
        else:
            return obj
    
    analyses_clean = convert_types(analyses)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analyses_clean, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON salvo com {len(analyses)} análises")


def main():
    """Pipeline principal."""
    print("🎯 ANÁLISE GEOMÉTRICA DA MEGA-SENA")
    print("Grid 6×10 - Padrões tipo Batalha Naval")
    print("=" * 60)
    
    # 1. Carregar dados
    df = load_megasena_data()
    
    # 2. Analisar todos os sorteios
    analyses = analyze_all_draws(df)
    
    # 3. Gerar relatório
    generate_summary_report(analyses)
    
    # 4. Gerar visualizações
    generate_visualizations(df, analyses)
    
    # 5. Salvar JSON
    save_json_results(analyses)
    
    print("\n" + "=" * 60)
    print("✅ ANÁLISE COMPLETA!")
    print(f"📁 Resultados salvos em: out/")
    print("=" * 60)


if __name__ == "__main__":
    main()

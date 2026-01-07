"""
Otimiza a proporção de números quentes e frios em apostas de 18 números
"""

import pandas as pd
from pathlib import Path
from itertools import combinations
import numpy as np

def load_hot_cold_numbers():
    """Carrega números quentes e frios"""
    file_path = Path('out/lotofacil/numeros_quentes_frios.csv')
    df = pd.read_csv(file_path)
    
    # Ordena por frequência
    df_sorted = df.sort_values('freq', ascending=False)
    
    # 15 mais frios (os últimos)
    cold_numbers = set(df_sorted.tail(15)['numero'].tolist())
    
    # Todos os outros são considerados quentes/médios
    hot_numbers = set(df_sorted.head(10)['numero'].tolist())
    
    return hot_numbers, cold_numbers, df_sorted

def load_recent_draws(n=20):
    """Carrega os últimos N sorteios"""
    draws_file = Path('data/lotofacil_sorteios.csv')
    df = pd.read_csv(draws_file)
    
    recent = df.tail(n)
    
    draws = []
    for _, row in recent.iterrows():
        numbers = set()
        for i in range(1, 16):
            numbers.add(int(row[f'Bola{i}']))
        
        draws.append({
            'concurso': int(row['Concurso']),
            'data': row['Data Sorteio'],
            'numbers': numbers
        })
    
    return draws

def simulate_strategy(num_cold, num_games=100):
    """Simula uma estratégia com N números frios"""
    hot_numbers, cold_numbers, df_sorted = load_hot_cold_numbers()
    draws = load_recent_draws(20)
    
    # Seleciona os números
    num_hot = 18 - num_cold
    
    # Pega os N mais quentes
    top_hot = df_sorted.head(num_hot)['numero'].tolist()
    
    # Pega os N frios mais "importantes" (os menos frios entre os frios)
    # Inverte a lógica: pega os frios que aparecem MAIS entre os frios
    cold_df = df_sorted.tail(15).sort_values('freq', ascending=False)
    top_cold = cold_df.head(num_cold)['numero'].tolist() if num_cold > 0 else []
    
    selected_18 = top_hot + top_cold
    
    # Gera algumas combinações para testar
    # Limita a 500 combinações para não demorar muito
    total_combinations = 1
    for i in range(15):
        total_combinations = total_combinations * (18 - i) // (i + 1)
    
    num_samples = min(num_games, total_combinations)
    
    # Gera combinações de 15 dos 18
    all_combos = list(combinations(selected_18, 15))
    
    # Se houver muitas, amostra aleatoriamente
    if len(all_combos) > num_samples:
        import random
        random.seed(42)
        sampled_combos = random.sample(all_combos, num_samples)
    else:
        sampled_combos = all_combos[:num_samples]
    
    # Testa cada combinação contra os sorteios
    total_hits = {11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
    
    for combo in sampled_combos:
        combo_set = set(combo)
        for draw in draws:
            matches = len(combo_set & draw['numbers'])
            if matches >= 11:
                total_hits[matches] += 1
    
    # Calcula estatísticas
    total_tests = len(sampled_combos) * len(draws)
    hit_rate = sum(total_hits.values()) / total_tests * 100 if total_tests > 0 else 0
    
    return {
        'num_cold': num_cold,
        'num_hot': num_hot,
        'selected_18': sorted(selected_18),
        'hot_selected': sorted(top_hot),
        'cold_selected': sorted(top_cold) if top_cold else [],
        'num_games_tested': len(sampled_combos),
        'total_hits': total_hits,
        'total_tests': total_tests,
        'hit_rate': hit_rate,
        'avg_prize_per_game': sum(total_hits.values()) / len(sampled_combos) if sampled_combos else 0
    }

def main():
    print("="*80)
    print("🎯 OTIMIZAÇÃO DA PROPORÇÃO QUENTES × FRIOS")
    print("="*80)
    print()
    
    print("📊 Testando diferentes proporções de números frios em 18 números...")
    print()
    
    # Testa diferentes quantidades de números frios (0 a 8)
    results = []
    
    for num_cold in range(0, 9):
        print(f"⏳ Testando: {18-num_cold} quentes + {num_cold} frios...")
        result = simulate_strategy(num_cold, num_games=200)
        results.append(result)
    
    print()
    print("="*80)
    print("📊 RESULTADOS DA SIMULAÇÃO (últimos 20 sorteios)")
    print("="*80)
    print()
    
    # Cabeçalho
    print(f"{'Frios':<6} {'Quentes':<8} {'11 acertos':<12} {'12 acertos':<12} {'13 acertos':<12} {'14 acertos':<12} {'15 acertos':<12} {'Taxa %':<10} {'Média/Jogo'}")
    print("-"*130)
    
    # Resultados
    for result in results:
        print(f"{result['num_cold']:<6} {result['num_hot']:<8} "
              f"{result['total_hits'][11]:<12} {result['total_hits'][12]:<12} "
              f"{result['total_hits'][13]:<12} {result['total_hits'][14]:<12} "
              f"{result['total_hits'][15]:<12} {result['hit_rate']:<10.2f} "
              f"{result['avg_prize_per_game']:.2f}")
    
    print()
    
    # Encontra a melhor estratégia
    best_by_rate = max(results, key=lambda x: x['hit_rate'])
    best_by_14_15 = max(results, key=lambda x: x['total_hits'][14] + x['total_hits'][15])
    best_by_avg = max(results, key=lambda x: x['avg_prize_per_game'])
    
    print("="*80)
    print("🏆 MELHORES ESTRATÉGIAS")
    print("="*80)
    print()
    
    print(f"✨ Melhor Taxa de Premiação: {best_by_rate['num_hot']} quentes + {best_by_rate['num_cold']} frios")
    print(f"   Taxa: {best_by_rate['hit_rate']:.2f}% | Média/jogo: {best_by_rate['avg_prize_per_game']:.2f}")
    print()
    
    print(f"💎 Melhor para 14+ acertos: {best_by_14_15['num_hot']} quentes + {best_by_14_15['num_cold']} frios")
    print(f"   14 acertos: {best_by_14_15['total_hits'][14]} | 15 acertos: {best_by_14_15['total_hits'][15]}")
    print()
    
    print(f"📈 Melhor Média por Jogo: {best_by_avg['num_hot']} quentes + {best_by_avg['num_cold']} frios")
    print(f"   Média: {best_by_avg['avg_prize_per_game']:.2f} prêmios/jogo")
    print()
    
    # Detalhamento da melhor estratégia
    print("="*80)
    print("🎯 RECOMENDAÇÃO FINAL")
    print("="*80)
    print()
    
    recommended = best_by_avg
    
    print(f"Proporção Recomendada: {recommended['num_hot']} QUENTES + {recommended['num_cold']} FRIOS")
    print()
    print(f"Números Quentes Selecionados ({len(recommended['hot_selected'])}):")
    print(f"  {', '.join(map(str, recommended['hot_selected']))}")
    print()
    
    if recommended['cold_selected']:
        print(f"Números Frios Selecionados ({len(recommended['cold_selected'])}):")
        print(f"  {', '.join(map(str, recommended['cold_selected']))}")
        print()
    
    print(f"Total de 18 números:")
    print(f"  {', '.join(map(str, recommended['selected_18']))}")
    print()
    
    print("Desempenho nos últimos 20 sorteios:")
    print(f"  15 acertos: {recommended['total_hits'][15]}")
    print(f"  14 acertos: {recommended['total_hits'][14]}")
    print(f"  13 acertos: {recommended['total_hits'][13]}")
    print(f"  12 acertos: {recommended['total_hits'][12]}")
    print(f"  11 acertos: {recommended['total_hits'][11]}")
    print(f"  Total de prêmios: {sum(recommended['total_hits'].values())}")
    print(f"  Média por jogo: {recommended['avg_prize_per_game']:.2f}")
    print()
    
    # Comparação com estratégia atual (0 frios)
    current_strategy = results[0]  # 0 frios = estratégia atual
    
    print("="*80)
    print("📊 COMPARAÇÃO: NOVA ESTRATÉGIA vs ATUAL")
    print("="*80)
    print()
    
    print(f"{'Métrica':<25} {'Atual (0 frios)':<20} {'Recomendada ({} frios)'.format(recommended['num_cold']):<25}")
    print("-"*80)
    print(f"{'15 acertos':<25} {current_strategy['total_hits'][15]:<20} {recommended['total_hits'][15]:<25}")
    print(f"{'14 acertos':<25} {current_strategy['total_hits'][14]:<20} {recommended['total_hits'][14]:<25}")
    print(f"{'13 acertos':<25} {current_strategy['total_hits'][13]:<20} {recommended['total_hits'][13]:<25}")
    print(f"{'12 acertos':<25} {current_strategy['total_hits'][12]:<20} {recommended['total_hits'][12]:<25}")
    print(f"{'11 acertos':<25} {current_strategy['total_hits'][11]:<20} {recommended['total_hits'][11]:<25}")
    print(f"{'Total de prêmios':<25} {sum(current_strategy['total_hits'].values()):<20} {sum(recommended['total_hits'].values()):<25}")
    print(f"{'Média por jogo':<25} {current_strategy['avg_prize_per_game']:<20.2f} {recommended['avg_prize_per_game']:<25.2f}")
    print()
    
    improvement = ((recommended['avg_prize_per_game'] - current_strategy['avg_prize_per_game']) / 
                   current_strategy['avg_prize_per_game'] * 100) if current_strategy['avg_prize_per_game'] > 0 else 0
    
    if improvement > 0:
        print(f"✅ Melhoria: +{improvement:.1f}% na média de prêmios por jogo")
    elif improvement < 0:
        print(f"⚠️ Redução: {improvement:.1f}% na média de prêmios por jogo")
    else:
        print("➡️ Desempenho equivalente")
    
    print()
    
    # Salva relatório
    output_dir = Path('out/optimized')
    output_dir.mkdir(exist_ok=True, parents=True)
    
    report_file = output_dir / 'analise_proporcao_quentes_frios.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("ANÁLISE DE PROPORÇÃO QUENTES × FRIOS\n")
        f.write("="*80 + "\n\n")
        
        f.write("RESULTADOS DA SIMULAÇÃO:\n")
        f.write("-"*80 + "\n")
        for result in results:
            f.write(f"\n{result['num_hot']} quentes + {result['num_cold']} frios:\n")
            f.write(f"  15 acertos: {result['total_hits'][15]}\n")
            f.write(f"  14 acertos: {result['total_hits'][14]}\n")
            f.write(f"  13 acertos: {result['total_hits'][13]}\n")
            f.write(f"  12 acertos: {result['total_hits'][12]}\n")
            f.write(f"  11 acertos: {result['total_hits'][11]}\n")
            f.write(f"  Taxa: {result['hit_rate']:.2f}%\n")
            f.write(f"  Média/jogo: {result['avg_prize_per_game']:.2f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("RECOMENDAÇÃO FINAL:\n")
        f.write("-"*80 + "\n")
        f.write(f"{recommended['num_hot']} QUENTES + {recommended['num_cold']} FRIOS\n\n")
        f.write(f"Números selecionados: {', '.join(map(str, recommended['selected_18']))}\n")
        f.write(f"Quentes: {', '.join(map(str, recommended['hot_selected']))}\n")
        if recommended['cold_selected']:
            f.write(f"Frios: {', '.join(map(str, recommended['cold_selected']))}\n")
    
    print(f"💾 Relatório salvo em: {report_file}")
    print()

if __name__ == '__main__':
    main()

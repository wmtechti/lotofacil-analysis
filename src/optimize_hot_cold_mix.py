"""
Otimiza a proporção de números quentes e frios em apostas de 18 números
baseado em análises históricas
"""

import pandas as pd
from pathlib import Path
from itertools import combinations
import numpy as np

def load_hot_and_cold_numbers():
    """Carrega números quentes e frios"""
    df = pd.read_csv('out/lotofacil/numeros_quentes_frios.csv')
    
    # 15 mais frios
    cold_numbers = [16, 8, 23, 6, 17, 7, 21, 18, 9, 19, 15, 2, 22, 5, 12]
    
    # 18 mais quentes (complemento)
    all_numbers = set(range(1, 26))
    hot_numbers = sorted(all_numbers - set(cold_numbers))
    
    # Dados detalhados
    hot_data = df[df['numero'].isin(hot_numbers)].sort_values('freq', ascending=False)
    cold_data = df[df['numero'].isin(cold_numbers)].sort_values('freq', ascending=False)
    
    return hot_numbers, cold_numbers, hot_data, cold_data

def load_recent_draws(n=20):
    """Carrega os últimos N sorteios"""
    df = pd.read_csv('data/lotofacil_sorteios.csv')
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

def simulate_mix_strategy(hot_count, cold_count, hot_numbers, cold_numbers, draws):
    """
    Simula uma estratégia com X quentes + Y frios
    Retorna estatísticas de acertos
    """
    # Seleciona os top hot_count quentes e top cold_count frios "mais quentes entre os frios"
    df = pd.read_csv('out/lotofacil/numeros_quentes_frios.csv')
    
    # Pega os mais quentes
    top_hot = df[df['numero'].isin(hot_numbers)].nlargest(hot_count, 'freq')['numero'].tolist()
    
    # Pega os frios mais "quentes" (menor desvio negativo)
    top_cold = df[df['numero'].isin(cold_numbers)].nlargest(cold_count, 'freq')['numero'].tolist()
    
    # Combinação
    game_numbers = set(top_hot + top_cold)
    
    # Testa contra os sorteios
    results = {
        'strategy': f"{hot_count} quentes + {cold_count} frios",
        'numbers': sorted(game_numbers),
        'hits_15': 0,
        'hits_14': 0,
        'hits_13': 0,
        'hits_12': 0,
        'hits_11': 0,
        'total_hits': 0
    }
    
    for draw in draws:
        matches = len(game_numbers & draw['numbers'])
        if matches == 15:
            results['hits_15'] += 1
        elif matches == 14:
            results['hits_14'] += 1
        elif matches == 13:
            results['hits_13'] += 1
        elif matches == 12:
            results['hits_12'] += 1
        elif matches == 11:
            results['hits_11'] += 1
        
        if matches >= 11:
            results['total_hits'] += 1
    
    # Score ponderado: 15=100, 14=20, 13=5, 12=2, 11=1
    results['weighted_score'] = (
        results['hits_15'] * 100 +
        results['hits_14'] * 20 +
        results['hits_13'] * 5 +
        results['hits_12'] * 2 +
        results['hits_11'] * 1
    )
    
    return results

def main():
    print("="*80)
    print("🔬 OTIMIZAÇÃO DA MIX QUENTES + FRIOS")
    print("="*80)
    print()
    
    # Carrega dados
    hot_numbers, cold_numbers, hot_data, cold_data = load_hot_and_cold_numbers()
    draws = load_recent_draws(20)
    
    print(f"📊 Base de análise:")
    print(f"   • 10 números quentes: {hot_numbers}")
    print(f"   • 15 números frios: {cold_numbers}")
    print(f"   • Últimos 20 sorteios (concursos {draws[-1]['concurso']} a {draws[0]['concurso']})")
    print()
    
    print("="*80)
    print("🧪 TESTANDO DIFERENTES PROPORÇÕES")
    print("="*80)
    print()
    
    # Testa diferentes combinações
    strategies = []
    
    # 18 quentes puro (atual) - não é possível pois só temos 10 quentes
    # Então vamos testar com os números disponíveis
    
    # Como só temos 10 quentes puros, vamos pegar os números "menos frios"
    # Redefinindo: vamos considerar como "quentes" os top 18 por frequência
    
    df = pd.read_csv('out/lotofacil/numeros_quentes_frios.csv')
    top_18 = df.nlargest(18, 'freq')['numero'].tolist()
    top_17 = df.nlargest(17, 'freq')['numero'].tolist()
    top_16 = df.nlargest(16, 'freq')['numero'].tolist()
    top_15 = df.nlargest(15, 'freq')['numero'].tolist()
    
    # Números frios mais críticos (que mais aparecem)
    critical_cold = [8, 6, 21, 7, 9]  # Top 5 frios que mais impediram vitórias
    
    # Estratégia 1: 18 mais quentes (atual)
    result1 = simulate_mix_strategy(18, 0, top_18, [], draws)
    result1['strategy'] = "18 mais quentes (atual)"
    result1['numbers'] = top_18
    strategies.append(result1)
    
    # Estratégia 2: 17 quentes + 1 frio crítico (8)
    game2 = top_17 + [8]
    result2 = {
        'strategy': "17 quentes + 1 frio (8)",
        'numbers': game2,
        'hits_15': 0, 'hits_14': 0, 'hits_13': 0, 'hits_12': 0, 'hits_11': 0, 'total_hits': 0
    }
    for draw in draws:
        matches = len(set(game2) & draw['numbers'])
        if matches == 15: result2['hits_15'] += 1
        elif matches == 14: result2['hits_14'] += 1
        elif matches == 13: result2['hits_13'] += 1
        elif matches == 12: result2['hits_12'] += 1
        elif matches == 11: result2['hits_11'] += 1
        if matches >= 11: result2['total_hits'] += 1
    result2['weighted_score'] = (result2['hits_15']*100 + result2['hits_14']*20 + 
                                  result2['hits_13']*5 + result2['hits_12']*2 + result2['hits_11']*1)
    strategies.append(result2)
    
    # Estratégia 3: 16 quentes + 2 frios (8, 6)
    game3 = top_16 + [8, 6]
    result3 = {
        'strategy': "16 quentes + 2 frios (8, 6)",
        'numbers': game3,
        'hits_15': 0, 'hits_14': 0, 'hits_13': 0, 'hits_12': 0, 'hits_11': 0, 'total_hits': 0
    }
    for draw in draws:
        matches = len(set(game3) & draw['numbers'])
        if matches == 15: result3['hits_15'] += 1
        elif matches == 14: result3['hits_14'] += 1
        elif matches == 13: result3['hits_13'] += 1
        elif matches == 12: result3['hits_12'] += 1
        elif matches == 11: result3['hits_11'] += 1
        if matches >= 11: result3['total_hits'] += 1
    result3['weighted_score'] = (result3['hits_15']*100 + result3['hits_14']*20 + 
                                  result3['hits_13']*5 + result3['hits_12']*2 + result3['hits_11']*1)
    strategies.append(result3)
    
    # Estratégia 4: 15 quentes + 3 frios (8, 6, 9)
    game4 = top_15 + [8, 6, 9]
    result4 = {
        'strategy': "15 quentes + 3 frios (8, 6, 9)",
        'numbers': game4,
        'hits_15': 0, 'hits_14': 0, 'hits_13': 0, 'hits_12': 0, 'hits_11': 0, 'total_hits': 0
    }
    for draw in draws:
        matches = len(set(game4) & draw['numbers'])
        if matches == 15: result4['hits_15'] += 1
        elif matches == 14: result4['hits_14'] += 1
        elif matches == 13: result4['hits_13'] += 1
        elif matches == 12: result4['hits_12'] += 1
        elif matches == 11: result4['hits_11'] += 1
        if matches >= 11: result4['total_hits'] += 1
    result4['weighted_score'] = (result4['hits_15']*100 + result4['hits_14']*20 + 
                                  result4['hits_13']*5 + result4['hits_12']*2 + result4['hits_11']*1)
    strategies.append(result4)
    
    # Exibe resultados
    print(f"{'Estratégia':<30} {'15':<5} {'14':<5} {'13':<5} {'12':<5} {'11':<5} {'Score':<8} {'Total'}")
    print("-"*80)
    
    for s in strategies:
        print(f"{s['strategy']:<30} {s['hits_15']:<5} {s['hits_14']:<5} {s['hits_13']:<5} "
              f"{s['hits_12']:<5} {s['hits_11']:<5} {s['weighted_score']:<8} {s['total_hits']}")
    
    print()
    
    # Melhor estratégia
    best = max(strategies, key=lambda x: x['weighted_score'])
    
    print("="*80)
    print("🏆 ESTRATÉGIA RECOMENDADA")
    print("="*80)
    print()
    print(f"✅ {best['strategy']}")
    print(f"   Números: {', '.join(map(str, sorted(best['numbers'])))}")
    print()
    print(f"   Performance nos últimos 20 sorteios:")
    print(f"   • 15 acertos: {best['hits_15']}")
    print(f"   • 14 acertos: {best['hits_14']}")
    print(f"   • 13 acertos: {best['hits_13']}")
    print(f"   • 12 acertos: {best['hits_12']}")
    print(f"   • 11 acertos: {best['hits_11']}")
    print(f"   • Score ponderado: {best['weighted_score']}")
    print()
    
    # Análise dos números frios críticos
    print("="*80)
    print("📊 NÚMEROS FRIOS CRÍTICOS (que mais aparecem impedindo vitórias)")
    print("="*80)
    print()
    print("Baseado nas análises de 14 e 13 acertos:")
    print()
    print("  Número  8: Apareceu em 36/36 casos de 13 acertos no concurso 3567")
    print("  Número  6: Apareceu em 9/9 casos de 13 acertos no concurso 3570")
    print("  Número 21: Apareceu em 9/9 casos de 13 acertos no concurso 3570")
    print("  Número  7: Número mais frio depois de 8 e 16")
    print("  Número  9: Frequentemente aparece nos sorteios")
    print()
    
    # Comparação com estratégia atual
    print("="*80)
    print("📈 COMPARAÇÃO COM ESTRATÉGIA ATUAL")
    print("="*80)
    print()
    
    current_strategy = strategies[0]
    
    if best != current_strategy:
        improvement = best['weighted_score'] - current_strategy['weighted_score']
        pct_improvement = (improvement / current_strategy['weighted_score'] * 100) if current_strategy['weighted_score'] > 0 else 0
        
        print(f"Estratégia atual (18 quentes):")
        print(f"  Score: {current_strategy['weighted_score']}")
        print()
        print(f"Estratégia recomendada ({best['strategy']}):")
        print(f"  Score: {best['weighted_score']}")
        print(f"  Melhoria: +{improvement} pontos ({pct_improvement:+.1f}%)")
    else:
        print("✅ A estratégia atual já é a melhor!")
    
    print()
    
    # Salva relatório
    output_dir = Path('out/optimized')
    report_file = output_dir / 'otimizacao_mix_quentes_frios.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("OTIMIZAÇÃO DA MIX QUENTES + FRIOS\n")
        f.write("="*80 + "\n\n")
        
        f.write("ESTRATÉGIAS TESTADAS:\n")
        f.write("-"*80 + "\n")
        for s in strategies:
            f.write(f"\n{s['strategy']}\n")
            f.write(f"  Números: {', '.join(map(str, sorted(s['numbers'])))}\n")
            f.write(f"  15 acertos: {s['hits_15']}\n")
            f.write(f"  14 acertos: {s['hits_14']}\n")
            f.write(f"  13 acertos: {s['hits_13']}\n")
            f.write(f"  12 acertos: {s['hits_12']}\n")
            f.write(f"  11 acertos: {s['hits_11']}\n")
            f.write(f"  Score: {s['weighted_score']}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("RECOMENDAÇÃO:\n")
        f.write(f"{best['strategy']}\n")
        f.write(f"Números: {', '.join(map(str, sorted(best['numbers'])))}\n")
    
    print(f"💾 Relatório salvo em: {report_file}")
    print()

if __name__ == '__main__':
    main()

"""
Testa diferentes estratégias e identifica a melhor
"""

import pandas as pd
from pathlib import Path

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

def test_strategy(pool_numbers, strategy_name, draws):
    """Testa uma estratégia contra os últimos sorteios"""
    
    results = {
        'strategy': strategy_name,
        'pool': sorted(pool_numbers),
        'hits_15': 0,
        'hits_14': 0,
        'hits_13': 0,
        'hits_12': 0,
        'hits_11': 0
    }
    
    for draw in draws:
        matches = len(pool_numbers & draw['numbers'])
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
    
    # Score ponderado: 15=100, 14=20, 13=5, 12=2, 11=1
    results['score'] = (
        results['hits_15'] * 100 +
        results['hits_14'] * 20 +
        results['hits_13'] * 5 +
        results['hits_12'] * 2 +
        results['hits_11'] * 1
    )
    
    results['total_hits'] = (results['hits_15'] + results['hits_14'] + 
                             results['hits_13'] + results['hits_12'] + results['hits_11'])
    
    return results

def main():
    print("="*80)
    print("🔬 TESTE COMPARATIVO DE ESTRATÉGIAS")
    print("="*80)
    print()
    
    draws = load_recent_draws(20)
    df = pd.read_csv('out/lotofacil/numeros_quentes_frios.csv')
    
    # Definir estratégias
    strategies = []
    
    # 1. Estratégia ORIGINAL (18 mais quentes)
    top18 = set(df.nlargest(18, 'freq')['numero'].tolist())
    strategies.append(test_strategy(top18, "18 mais quentes (ORIGINAL)", draws))
    
    # 2. Nova combinação testada (16 quentes + 6, 8)
    top16 = set(df.nlargest(16, 'freq')['numero'].tolist())
    new_combo = top16 | {6, 8}
    strategies.append(test_strategy(new_combo, "16 quentes + 2 frios (6, 8)", draws))
    
    # 3. Alternativa: 17 quentes + 8 (mantém 19)
    top17 = set(df.nlargest(17, 'freq')['numero'].tolist())
    alt1 = top17 | {8}
    strategies.append(test_strategy(alt1, "17 quentes + 1 frio (8)", draws))
    
    # 4. Alternativa: 17 quentes + 6 (mantém 19)
    alt2 = top17 | {6}
    strategies.append(test_strategy(alt2, "17 quentes + 1 frio (6)", draws))
    
    # 5. 15 quentes + 3 frios críticos (6, 8, 21)
    top15 = set(df.nlargest(15, 'freq')['numero'].tolist())
    alt3 = top15 | {6, 8, 21}
    strategies.append(test_strategy(alt3, "15 quentes + 3 frios (6, 8, 21)", draws))
    
    # Exibe resultados
    print(f"{'Estratégia':<35} {'15':<5} {'14':<5} {'13':<5} {'12':<5} {'11':<5} {'Score':<7} {'Total'}")
    print("-"*80)
    
    for s in strategies:
        print(f"{s['strategy']:<35} {s['hits_15']:<5} {s['hits_14']:<5} {s['hits_13']:<5} "
              f"{s['hits_12']:<5} {s['hits_11']:<5} {s['score']:<7} {s['total_hits']}")
    
    print()
    
    # Melhor estratégia
    best = max(strategies, key=lambda x: x['score'])
    
    print("="*80)
    print("🏆 MELHOR ESTRATÉGIA")
    print("="*80)
    print()
    print(f"✅ {best['strategy']}")
    print(f"   Score: {best['score']} pontos")
    print()
    print(f"   Números: {', '.join(map(str, best['pool']))}")
    print()
    print(f"   Performance nos últimos 20 sorteios:")
    print(f"   • 15 acertos: {best['hits_15']}")
    print(f"   • 14 acertos: {best['hits_14']}")
    print(f"   • 13 acertos: {best['hits_13']}")
    print(f"   • 12 acertos: {best['hits_12']}")
    print(f"   • 11 acertos: {best['hits_11']}")
    print(f"   • Total de acertos: {best['total_hits']}")
    print()
    
    # Comparação com segunda melhor
    sorted_strategies = sorted(strategies, key=lambda x: x['score'], reverse=True)
    second_best = sorted_strategies[1]
    
    print("="*80)
    print("📊 COMPARAÇÃO COM 2ª MELHOR")
    print("="*80)
    print()
    print(f"1ª: {best['strategy']}")
    print(f"    Score: {best['score']}")
    print()
    print(f"2ª: {second_best['strategy']}")
    print(f"    Score: {second_best['score']}")
    print(f"    Diferença: {best['score'] - second_best['score']} pontos")
    print()
    
    # Análise dos números
    print("="*80)
    print("🔍 COMPOSIÇÃO DA MELHOR ESTRATÉGIA")
    print("="*80)
    print()
    
    # Verifica quais são frios
    cold_numbers = {16, 8, 23, 6, 17, 7, 21, 18, 9, 19, 15, 2, 22, 5, 12}
    best_pool_set = set(best['pool'])
    
    quentes_na_pool = best_pool_set - cold_numbers
    frios_na_pool = best_pool_set & cold_numbers
    
    print(f"Números QUENTES ({len(quentes_na_pool)}):")
    print(f"   {', '.join(map(str, sorted(quentes_na_pool)))}")
    print()
    
    if frios_na_pool:
        print(f"Números FRIOS incluídos ({len(frios_na_pool)}):")
        for num in sorted(frios_na_pool):
            row = df[df['numero'] == num].iloc[0]
            print(f"   {num}: Freq {int(row['freq'])}, Desvio {row['desvio_%']:+.2f}%")
    
    print()
    
    # Salva relatório
    output_dir = Path('out/optimized')
    report_file = output_dir / 'comparacao_estrategias_final.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("TESTE COMPARATIVO DE ESTRATÉGIAS\n")
        f.write("="*80 + "\n\n")
        
        f.write("RESULTADOS:\n")
        f.write("-"*80 + "\n")
        for s in sorted(strategies, key=lambda x: x['score'], reverse=True):
            f.write(f"\n{s['strategy']}\n")
            f.write(f"  Pool: {', '.join(map(str, s['pool']))}\n")
            f.write(f"  15: {s['hits_15']}, 14: {s['hits_14']}, 13: {s['hits_13']}, ")
            f.write(f"12: {s['hits_12']}, 11: {s['hits_11']}\n")
            f.write(f"  Score: {s['score']}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write(f"VENCEDOR: {best['strategy']}\n")
        f.write(f"Pool: {', '.join(map(str, best['pool']))}\n")
    
    print(f"💾 Relatório salvo em: {report_file}")
    print()
    
    # Salva a melhor pool
    best_pool_file = output_dir / 'melhor_pool_18_numeros.txt'
    with open(best_pool_file, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, sorted(best['pool']))))
    
    print(f"💾 Pool otimizada salva em: {best_pool_file}")
    print()

if __name__ == '__main__':
    main()

"""
Analisa os acertos de 14 e 13 com a NOVA combinação otimizada (16 quentes + 2 frios)
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
            'numbers': numbers,
            'numbers_list': sorted(numbers)
        })
    
    return draws

def analyze_hits(target_hits=14):
    """Analisa jogos com N acertos"""
    
    # NOVA COMBINAÇÃO OTIMIZADA (16 quentes + 2 frios)
    our_pool = set([1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25])
    
    draws = load_recent_draws(20)
    
    results = []
    
    for draw in draws:
        # Conta quantos números do sorteio estão na nossa pool
        matches = len(draw['numbers'] & our_pool)
        
        if matches == target_hits:
            # Números que estão na nossa pool mas NÃO saíram no sorteio
            missing_from_draw = our_pool - draw['numbers']
            # Números que saíram mas NÃO estão na nossa pool
            extra_in_draw = draw['numbers'] - our_pool
            
            results.append({
                'concurso': draw['concurso'],
                'data': draw['data'],
                'numeros_sorteio': draw['numbers_list'],
                'numeros_nossa_pool': sorted(our_pool),
                'numeros_que_faltaram': sorted(missing_from_draw),
                'numeros_extras_sorteio': sorted(extra_in_draw)
            })
    
    return results, our_pool

def main():
    print("="*80)
    print("🎯 ANÁLISE COM NOVA COMBINAÇÃO OTIMIZADA")
    print("="*80)
    print()
    
    our_pool = set([1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25])
    
    print("Nova Combinação (18 números):")
    print(f"   {', '.join(map(str, sorted(our_pool)))}")
    print()
    print("Composição: 16 quentes + 2 frios (6, 8)")
    print()
    
    # Análise de 14 acertos
    print("="*80)
    print("📊 ANÁLISE DE 14 ACERTOS (últimos 20 sorteios)")
    print("="*80)
    print()
    
    results_14, _ = analyze_hits(14)
    
    if results_14:
        print(f"✅ Encontrados {len(results_14)} caso(s) de 14 acertos\n")
        
        print(f"{'Concurso':<10} {'Data':<15} {'Números que Faltaram':<30} {'Números Extras'}")
        print("-"*80)
        
        for result in sorted(results_14, key=lambda x: x['concurso'], reverse=True):
            concurso = str(result['concurso'])
            data = result['data']
            faltaram = ', '.join(map(str, result['numeros_que_faltaram']))
            extras = ', '.join(map(str, result['numeros_extras_sorteio']))
            print(f"{concurso:<10} {data:<15} {faltaram:<30} {extras}")
        
        print()
        print("DETALHES:")
        print("-"*80)
        
        for i, result in enumerate(sorted(results_14, key=lambda x: x['concurso'], reverse=True), 1):
            print(f"\n{i}. Concurso {result['concurso']} ({result['data']})")
            print(f"   Números sorteados: {', '.join(map(str, result['numeros_sorteio']))}")
            print(f"   ❌ Faltaram da pool: {', '.join(map(str, result['numeros_que_faltaram']))}")
            print(f"   ✅ Extras no sorteio: {', '.join(map(str, result['numeros_extras_sorteio']))}")
        
        # Estatísticas
        all_missing = []
        all_extra = []
        for result in results_14:
            all_missing.extend(result['numeros_que_faltaram'])
            all_extra.extend(result['numeros_extras_sorteio'])
        
        print("\n" + "="*80)
        print("📈 ESTATÍSTICAS - 14 ACERTOS")
        print("="*80)
        print()
        
        if all_missing:
            missing_count = {}
            for num in all_missing:
                missing_count[num] = missing_count.get(num, 0) + 1
            
            print("Números da nossa pool que NÃO saíram:")
            for num, count in sorted(missing_count.items(), key=lambda x: x[1], reverse=True):
                print(f"  Número {num:2d}: {count} vez(es)")
        
        print()
        
        if all_extra:
            extra_count = {}
            for num in all_extra:
                extra_count[num] = extra_count.get(num, 0) + 1
            
            print("Números que saíram mas NÃO estão na pool:")
            for num, count in sorted(extra_count.items(), key=lambda x: x[1], reverse=True):
                print(f"  Número {num:2d}: {count} vez(es)")
        
    else:
        print("❌ Nenhum caso de 14 acertos nos últimos 20 sorteios")
    
    print()
    
    # Análise de 13 acertos
    print("="*80)
    print("📊 ANÁLISE DE 13 ACERTOS (últimos 20 sorteios)")
    print("="*80)
    print()
    
    results_13, _ = analyze_hits(13)
    
    if results_13:
        print(f"✅ Encontrados {len(results_13)} caso(s) de 13 acertos\n")
        
        # Agrupa por concurso
        by_concurso = {}
        for result in results_13:
            concurso = result['concurso']
            if concurso not in by_concurso:
                by_concurso[concurso] = []
            by_concurso[concurso].append(result)
        
        print(f"{'Concurso':<10} {'Data':<15} {'Qtd':<5} {'Números Extras Mais Comuns'}")
        print("-"*80)
        
        for concurso in sorted(by_concurso.keys(), reverse=True):
            cases = by_concurso[concurso]
            data = cases[0]['data']
            
            # Conta números extras
            extras_concurso = []
            for case in cases:
                extras_concurso.extend(case['numeros_extras_sorteio'])
            
            extras_count = {}
            for num in extras_concurso:
                extras_count[num] = extras_count.get(num, 0) + 1
            
            top_extras = sorted(extras_count.items(), key=lambda x: x[1], reverse=True)[:3]
            extras_str = ', '.join([f"{num}({cnt}x)" for num, cnt in top_extras])
            
            print(f"{concurso:<10} {data:<15} {len(cases):<5} {extras_str}")
        
        # Estatísticas detalhadas
        all_missing_13 = []
        all_extra_13 = []
        for result in results_13:
            all_missing_13.extend(result['numeros_que_faltaram'])
            all_extra_13.extend(result['numeros_extras_sorteio'])
        
        print("\n" + "="*80)
        print("📈 ESTATÍSTICAS - 13 ACERTOS")
        print("="*80)
        print()
        
        if all_missing_13:
            missing_count_13 = {}
            for num in all_missing_13:
                missing_count_13[num] = missing_count_13.get(num, 0) + 1
            
            print("Números da nossa pool que NÃO saíram (impediram 14+ acertos):")
            for num, count in sorted(missing_count_13.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  Número {num:2d}: {count:3d} vez(es)")
        
        print()
        
        if all_extra_13:
            extra_count_13 = {}
            for num in all_extra_13:
                extra_count_13[num] = extra_count_13.get(num, 0) + 1
            
            print("Números que saíram mas NÃO estão na pool:")
            for num, count in sorted(extra_count_13.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  Número {num:2d}: {count:3d} vez(es)")
        
    else:
        print("❌ Nenhum caso de 13 acertos nos últimos 20 sorteios")
    
    print()
    
    # Salva relatório
    output_dir = Path('out/optimized')
    report_file = output_dir / 'analise_nova_combinacao.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("ANÁLISE COM NOVA COMBINAÇÃO OTIMIZADA\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Combinação: {', '.join(map(str, sorted(our_pool)))}\n")
        f.write("Composição: 16 quentes + 2 frios (6, 8)\n\n")
        
        f.write(f"14 ACERTOS: {len(results_14)} caso(s)\n")
        f.write(f"13 ACERTOS: {len(results_13)} caso(s)\n\n")
        
        if results_14:
            f.write("\n14 ACERTOS - DETALHES:\n")
            f.write("-"*80 + "\n")
            for result in results_14:
                f.write(f"\nConcurso {result['concurso']} ({result['data']})\n")
                f.write(f"  Sorteados: {', '.join(map(str, result['numeros_sorteio']))}\n")
                f.write(f"  Faltaram: {', '.join(map(str, result['numeros_que_faltaram']))}\n")
                f.write(f"  Extras: {', '.join(map(str, result['numeros_extras_sorteio']))}\n")
        
        if results_13:
            f.write("\n13 ACERTOS - RESUMO POR CONCURSO:\n")
            f.write("-"*80 + "\n")
            for concurso in sorted(by_concurso.keys(), reverse=True):
                cases = by_concurso[concurso]
                f.write(f"\nConcurso {concurso} ({cases[0]['data']}): {len(cases)} caso(s)\n")
    
    print(f"💾 Relatório salvo em: {report_file}")
    print()

if __name__ == '__main__':
    main()

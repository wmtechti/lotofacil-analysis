"""
Analisa os jogos que fizeram 13 acertos e identifica os números que faltaram
"""

import pandas as pd
from pathlib import Path

def load_optimized_games():
    """Carrega os jogos otimizados"""
    games_file = Path('out/optimized/jogos_18_quentes_otimizados.csv')
    df = pd.read_csv(games_file)
    
    games = {}
    for _, row in df.iterrows():
        numbers = [int(x) for x in row['numeros'].split(',')]
        games[row['jogo_id']] = {
            'numbers': set(numbers),
            'numbers_list': sorted(numbers),
            'score': row['score']
        }
    
    return games

def load_recent_draws(n=20):
    """Carrega os últimos N sorteios"""
    draws_file = Path('data/lotofacil_sorteios.csv')
    df = pd.read_csv(draws_file)
    
    # Pega os últimos N sorteios
    recent = df.tail(n)
    
    draws = {}
    for _, row in recent.iterrows():
        numbers = set()
        for i in range(1, 16):
            numbers.add(int(row[f'Bola{i}']))
        
        draws[int(row['Concurso'])] = {
            'data': row['Data Sorteio'],
            'numbers': numbers,
            'numbers_list': sorted(numbers)
        }
    
    return draws

def find_13_hits():
    """Encontra os jogos que fizeram 13 acertos nos últimos 20 sorteios"""
    games = load_optimized_games()
    draws = load_recent_draws(20)
    
    results = []
    
    for game_id, game_data in games.items():
        for concurso, draw_data in draws.items():
            # Conta quantos números coincidem
            matches = len(game_data['numbers'] & draw_data['numbers'])
            
            if matches == 13:
                # Encontra os números que estavam no jogo mas NÃO no sorteio (2 números)
                missing_from_draw = game_data['numbers'] - draw_data['numbers']
                # Encontra os números que estavam no sorteio mas NÃO no jogo (2 números)
                extra_in_draw = draw_data['numbers'] - game_data['numbers']
                
                results.append({
                    'jogo_id': game_id,
                    'concurso': concurso,
                    'data': draw_data['data'],
                    'numeros_jogo': game_data['numbers_list'],
                    'numeros_sorteio': draw_data['numbers_list'],
                    'numeros_que_faltaram': sorted(missing_from_draw),  # 2 números do jogo que não saíram
                    'numeros_extras_sorteio': sorted(extra_in_draw)  # 2 números que saíram mas não estavam no jogo
                })
    
    return results

def main():
    print("="*80)
    print("🎯 ANÁLISE DOS 13 ACERTOS - NÚMEROS QUE FALTARAM (ÚLTIMOS 20 SORTEIOS)")
    print("="*80)
    print()
    
    results = find_13_hits()
    
    if not results:
        print("❌ Nenhum jogo fez 13 acertos nos últimos 20 sorteios")
        return
    
    print(f"📊 Encontrados {len(results)} casos de 13 acertos nos últimos 20 sorteios\n")
    
    # Agrupa por concurso para melhor visualização
    by_concurso = {}
    for result in results:
        concurso = result['concurso']
        if concurso not in by_concurso:
            by_concurso[concurso] = []
        by_concurso[concurso].append(result)
    
    # Exibe por concurso
    for concurso in sorted(by_concurso.keys(), reverse=True):
        cases = by_concurso[concurso]
        print("="*80)
        print(f"CONCURSO {concurso} ({cases[0]['data']}) - {len(cases)} jogo(s) com 13 acertos")
        print("="*80)
        print(f"Números sorteados: {', '.join(map(str, cases[0]['numeros_sorteio']))}")
        print()
        
        for i, result in enumerate(cases, 1):
            print(f"{i}. Jogo #{result['jogo_id']}")
            print(f"   Números do jogo: {', '.join(map(str, result['numeros_jogo']))}")
            print(f"   ❌ Faltaram: {', '.join(map(str, result['numeros_que_faltaram']))}")
            print(f"   ✅ Extras no sorteio: {', '.join(map(str, result['numeros_extras_sorteio']))}")
            print()
    
    # Cria tabela resumo
    print("="*80)
    print("📋 TABELA RESUMO - TODOS OS 13 ACERTOS")
    print("="*80)
    print()
    print(f"{'Jogo':<7} {'Concurso':<10} {'Data':<12} {'Números que Faltaram':<22} {'Números Extras no Sorteio':<25}")
    print("-"*80)
    
    for result in sorted(results, key=lambda x: (x['concurso'], x['jogo_id']), reverse=True):
        jogo = f"#{result['jogo_id']}"
        concurso = str(result['concurso'])
        data = result['data']
        faltaram = ', '.join(map(str, result['numeros_que_faltaram']))
        extras = ', '.join(map(str, result['numeros_extras_sorteio']))
        
        print(f"{jogo:<7} {concurso:<10} {data:<12} {faltaram:<22} {extras:<25}")
    
    print()
    
    # Análise dos números que mais faltaram
    print("="*80)
    print("📊 ANÁLISE: Números que mais impediram os 14+ acertos")
    print("="*80)
    print()
    
    all_missing = []
    all_extra = []
    
    for result in results:
        all_missing.extend(result['numeros_que_faltaram'])
        all_extra.extend(result['numeros_extras_sorteio'])
    
    if all_missing:
        missing_count = {}
        for num in all_missing:
            missing_count[num] = missing_count.get(num, 0) + 1
        
        print("Números do jogo que NÃO saíram (impediram 14+ acertos):")
        for num, count in sorted(missing_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  Número {num:2d}: apareceu {count:3d} vez(es)")
        print()
    
    if all_extra:
        extra_count = {}
        for num in all_extra:
            extra_count[num] = extra_count.get(num, 0) + 1
        
        print("Números que saíram mas NÃO estavam nos jogos:")
        for num, count in sorted(extra_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  Número {num:2d}: apareceu {count:3d} vez(es)")
    
    print()
    
    # Estatísticas por concurso
    print("="*80)
    print("📊 ESTATÍSTICAS POR CONCURSO")
    print("="*80)
    print()
    print(f"{'Concurso':<10} {'Data':<12} {'Jogos com 13':<15} {'Números Extras Mais Comuns'}")
    print("-"*80)
    
    for concurso in sorted(by_concurso.keys(), reverse=True):
        cases = by_concurso[concurso]
        data = cases[0]['data']
        num_jogos = len(cases)
        
        # Conta números extras mais comuns neste concurso
        extras_concurso = []
        for case in cases:
            extras_concurso.extend(case['numeros_extras_sorteio'])
        
        extras_count = {}
        for num in extras_concurso:
            extras_count[num] = extras_count.get(num, 0) + 1
        
        top_extras = sorted(extras_count.items(), key=lambda x: x[1], reverse=True)[:3]
        extras_str = ', '.join([f"{num}({cnt}x)" for num, cnt in top_extras])
        
        print(f"{concurso:<10} {data:<12} {num_jogos:<15} {extras_str}")
    
    print()
    
    # Salva relatório
    output_dir = Path('out/optimized')
    report_file = output_dir / 'analise_13_acertos.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("ANÁLISE DOS 13 ACERTOS - ÚLTIMOS 20 SORTEIOS\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Total de casos: {len(results)}\n\n")
        
        for concurso in sorted(by_concurso.keys(), reverse=True):
            cases = by_concurso[concurso]
            f.write(f"\nCONCURSO {concurso} ({cases[0]['data']}) - {len(cases)} caso(s)\n")
            f.write("-"*80 + "\n")
            f.write(f"Números sorteados: {', '.join(map(str, cases[0]['numeros_sorteio']))}\n\n")
            
            for result in cases:
                f.write(f"Jogo #{result['jogo_id']}\n")
                f.write(f"  Números do jogo: {', '.join(map(str, result['numeros_jogo']))}\n")
                f.write(f"  Faltaram: {', '.join(map(str, result['numeros_que_faltaram']))}\n")
                f.write(f"  Extras: {', '.join(map(str, result['numeros_extras_sorteio']))}\n\n")
    
    print(f"💾 Relatório salvo em: {report_file}")
    print()

if __name__ == '__main__':
    main()

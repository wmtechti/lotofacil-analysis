"""
Analisa os jogos que fizeram 14 acertos e identifica os números que faltaram
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

def load_draws():
    """Carrega todos os sorteios"""
    draws_file = Path('data/lotofacil_sorteios.csv')
    df = pd.read_csv(draws_file)
    
    draws = {}
    for _, row in df.iterrows():
        numbers = set()
        for i in range(1, 16):
            numbers.add(int(row[f'Bola{i}']))
        
        draws[int(row['Concurso'])] = {
            'data': row['Data Sorteio'],
            'numbers': numbers,
            'numbers_list': sorted(numbers)
        }
    
    return draws

def find_14_hits():
    """Encontra os jogos que fizeram 14 acertos"""
    games = load_optimized_games()
    draws = load_draws()
    
    results = []
    
    for game_id, game_data in games.items():
        for concurso, draw_data in draws.items():
            # Conta quantos números coincidem
            matches = len(game_data['numbers'] & draw_data['numbers'])
            
            if matches == 14:
                # Encontra os números que estavam no jogo mas NÃO no sorteio
                missing_from_draw = game_data['numbers'] - draw_data['numbers']
                # Encontra os números que estavam no sorteio mas NÃO no jogo
                extra_in_draw = draw_data['numbers'] - game_data['numbers']
                
                results.append({
                    'jogo_id': game_id,
                    'concurso': concurso,
                    'data': draw_data['data'],
                    'numeros_jogo': game_data['numbers_list'],
                    'numeros_sorteio': draw_data['numbers_list'],
                    'numeros_que_faltaram': sorted(missing_from_draw),  # Números do jogo que não saíram
                    'numeros_extras_sorteio': sorted(extra_in_draw)  # Números que saíram mas não estavam no jogo
                })
    
    return results

def main():
    print("="*80)
    print("🎯 ANÁLISE DOS 14 ACERTOS - NÚMEROS QUE FALTARAM")
    print("="*80)
    print()
    
    results = find_14_hits()
    
    if not results:
        print("❌ Nenhum jogo fez 14 acertos")
        return
    
    print(f"📊 Encontrados {len(results)} casos de 14 acertos\n")
    
    # Exibe cada caso
    for i, result in enumerate(results, 1):
        print("="*80)
        print(f"CASO {i}: Jogo #{result['jogo_id']} × Concurso {result['concurso']} ({result['data']})")
        print("="*80)
        print()
        
        print(f"🎲 Números do Jogo #{result['jogo_id']}:")
        print(f"   {', '.join(map(str, result['numeros_jogo']))}")
        print()
        
        print(f"🎰 Números Sorteados no Concurso {result['concurso']}:")
        print(f"   {', '.join(map(str, result['numeros_sorteio']))}")
        print()
        
        print(f"❌ Número que estava no JOGO mas NÃO SAIU no sorteio:")
        print(f"   {', '.join(map(str, result['numeros_que_faltaram']))} ← Este número impediu os 15 acertos")
        print()
        
        print(f"✅ Número que SAIU no sorteio mas NÃO estava no jogo:")
        print(f"   {', '.join(map(str, result['numeros_extras_sorteio']))}")
        print()
    
    # Cria tabela resumo
    print("="*80)
    print("📋 TABELA RESUMO - NÚMEROS QUE FALTARAM PARA 15 ACERTOS")
    print("="*80)
    print()
    print(f"{'Jogo':<6} {'Concurso':<10} {'Data':<12} {'Número que Faltou':<20} {'Número Extra no Sorteio':<25}")
    print("-"*80)
    
    for result in results:
        jogo = f"#{result['jogo_id']}"
        concurso = str(result['concurso'])
        data = result['data']
        faltou = ', '.join(map(str, result['numeros_que_faltaram']))
        extra = ', '.join(map(str, result['numeros_extras_sorteio']))
        
        print(f"{jogo:<6} {concurso:<10} {data:<12} {faltou:<20} {extra:<25}")
    
    print()
    
    # Análise dos números que mais faltaram
    print("="*80)
    print("📊 ANÁLISE: Números que mais impediram os 15 acertos")
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
        
        print("Números do jogo que NÃO saíram (impediram 15 acertos):")
        for num, count in sorted(missing_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  Número {num:2d}: apareceu {count} vez(es)")
        print()
    
    if all_extra:
        extra_count = {}
        for num in all_extra:
            extra_count[num] = extra_count.get(num, 0) + 1
        
        print("Números que saíram mas NÃO estavam nos jogos:")
        for num, count in sorted(extra_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  Número {num:2d}: apareceu {count} vez(es)")
    
    print()
    
    # Salva relatório
    output_dir = Path('out/optimized')
    report_file = output_dir / 'analise_14_acertos.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("ANÁLISE DOS 14 ACERTOS - NÚMEROS QUE FALTARAM\n")
        f.write("="*80 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"CASO {i}: Jogo #{result['jogo_id']} × Concurso {result['concurso']} ({result['data']})\n")
            f.write("-"*80 + "\n")
            f.write(f"Números do Jogo: {', '.join(map(str, result['numeros_jogo']))}\n")
            f.write(f"Números Sorteados: {', '.join(map(str, result['numeros_sorteio']))}\n")
            f.write(f"Faltou no sorteio: {', '.join(map(str, result['numeros_que_faltaram']))}\n")
            f.write(f"Extra no sorteio: {', '.join(map(str, result['numeros_extras_sorteio']))}\n")
            f.write("\n")
    
    print(f"💾 Relatório salvo em: {report_file}")
    print()

if __name__ == '__main__':
    main()

"""
Verifica se a nova combinação (16 quentes + 2 frios) já fez 15 acertos
"""

import pandas as pd
from pathlib import Path
from itertools import combinations

def load_all_draws():
    """Carrega todos os sorteios"""
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    draws = []
    for _, row in df.iterrows():
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

def check_15_hits():
    """Verifica se algum sorteio teve 15 números da nossa combinação"""
    
    # Nossa combinação otimizada (18 números)
    our_numbers = set([1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25])
    
    draws = load_all_draws()
    
    perfect_matches = []
    
    for draw in draws:
        # Conta quantos números do sorteio estão na nossa combinação
        matches = len(draw['numbers'] & our_numbers)
        
        if matches == 15:
            # TODOS os 15 números do sorteio estão na nossa combinação de 18!
            # Isso significa que qualquer jogo de 15 números dentro dos nossos 18
            # que contenha esses 15 específicos teria ganhado
            perfect_matches.append({
                'concurso': draw['concurso'],
                'data': draw['data'],
                'numbers': draw['numbers_list'],
                'missing_from_our_pool': sorted(our_numbers - draw['numbers'])
            })
    
    return perfect_matches, our_numbers

def main():
    print("="*80)
    print("🎰 VERIFICAÇÃO DE 15 ACERTOS - COMBINAÇÃO OTIMIZADA")
    print("="*80)
    print()
    
    perfect_matches, our_numbers = check_15_hits()
    
    print("Nossa combinação (18 números):")
    print(f"   {', '.join(map(str, sorted(our_numbers)))}")
    print()
    
    total_draws = len(load_all_draws())
    
    if perfect_matches:
        print(f"✅ SIM! Encontrados {len(perfect_matches)} sorteios onde TODOS os 15 números")
        print(f"   saíram dentro da nossa pool de 18 números!")
        print()
        print(f"   Isso representa {len(perfect_matches)/total_draws*100:.2f}% de {total_draws} sorteios")
        print()
        
        print("="*80)
        print("LISTA DE SORTEIOS COM 15 ACERTOS POSSÍVEIS")
        print("="*80)
        print()
        print(f"{'Concurso':<10} {'Data':<15} {'Números Sorteados':<50} {'Faltaram'}")
        print("-"*80)
        
        for match in perfect_matches:
            concurso = str(match['concurso'])
            data = match['data']
            numbers = ', '.join(map(str, match['numbers']))
            missing = ', '.join(map(str, match['missing_from_our_pool']))
            print(f"{concurso:<10} {data:<15} {numbers:<50} {missing}")
        
        print()
        print("="*80)
        print("💡 IMPORTANTE:")
        print("="*80)
        print()
        print("Estes sorteios representam oportunidades onde:")
        print("  • TODOS os 15 números sorteados estavam na nossa pool de 18")
        print("  • Qualquer combinação de 15 números que incluísse esses 15 teria GANHADO")
        print(f"  • Com C(18,15) = 816 jogos, você teria pelo menos {len(perfect_matches)} vitórias garantidas")
        print()
        
        # Análise dos números que faltaram
        all_missing = []
        for match in perfect_matches:
            all_missing.extend(match['missing_from_our_pool'])
        
        missing_count = {}
        for num in all_missing:
            missing_count[num] = missing_count.get(num, 0) + 1
        
        print("Números da nossa pool que NÃO saíram (dos 3 restantes):")
        for num, count in sorted(missing_count.items(), key=lambda x: x[1], reverse=True):
            pct = count / len(perfect_matches) * 100
            print(f"  Número {num:2d}: ficou de fora em {count:3d} sorteios ({pct:5.1f}%)")
        
    else:
        print(f"❌ NÃO. Nenhum sorteio teve todos os 15 números dentro da nossa pool de 18.")
        print()
        print("Isso significa que sempre houve pelo menos 1 número sorteado fora dos nossos 18.")
    
    print()
    
    # Salva relatório
    output_dir = Path('out/optimized')
    report_file = output_dir / 'verificacao_15_acertos.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("VERIFICAÇÃO DE 15 ACERTOS - COMBINAÇÃO OTIMIZADA\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Combinação: {', '.join(map(str, sorted(our_numbers)))}\n\n")
        f.write(f"Total de sorteios analisados: {total_draws}\n")
        f.write(f"Sorteios com 15 acertos possíveis: {len(perfect_matches)}\n\n")
        
        if perfect_matches:
            f.write("LISTA DE SORTEIOS:\n")
            f.write("-"*80 + "\n")
            for match in perfect_matches:
                f.write(f"\nConcurso {match['concurso']} ({match['data']})\n")
                f.write(f"  Números sorteados: {', '.join(map(str, match['numbers']))}\n")
                f.write(f"  Não saíram da pool: {', '.join(map(str, match['missing_from_our_pool']))}\n")
    
    print(f"💾 Relatório salvo em: {report_file}")
    print()

if __name__ == '__main__':
    main()

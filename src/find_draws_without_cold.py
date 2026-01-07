"""
Identifica sorteios que não tiveram nenhum número frio
"""

import pandas as pd
from pathlib import Path

def load_cold_numbers():
    """Carrega os números frios"""
    # Os 15 números mais frios identificados anteriormente
    cold_numbers = [16, 8, 23, 6, 17, 7, 21, 18, 9, 19, 15, 2, 22, 5, 12]
    return set(cold_numbers)

def load_all_draws():
    """Carrega todos os sorteios"""
    draws_file = Path('data/lotofacil_sorteios.csv')
    df = pd.read_csv(draws_file)
    
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

def find_draws_without_cold():
    """Encontra sorteios sem números frios"""
    cold_numbers = load_cold_numbers()
    draws = load_all_draws()
    
    draws_without_cold = []
    
    for draw in draws:
        # Verifica se há interseção entre os números do sorteio e os números frios
        has_cold = bool(draw['numbers'] & cold_numbers)
        
        if not has_cold:
            # Este sorteio não tem nenhum número frio
            draws_without_cold.append(draw)
    
    return draws_without_cold, cold_numbers

def main():
    print("="*80)
    print("❄️ SORTEIOS SEM NÚMEROS FRIOS")
    print("="*80)
    print()
    
    draws_without_cold, cold_numbers = find_draws_without_cold()
    
    print(f"📊 Números Frios Analisados (15 mais frios):")
    print(f"   {', '.join(map(str, sorted(cold_numbers)))}")
    print()
    
    total_draws = len(load_all_draws())
    
    if not draws_without_cold:
        print("✅ RESULTADO: TODOS os sorteios tiveram pelo menos 1 número frio!")
        print(f"   Total de sorteios analisados: {total_draws}")
    else:
        print(f"❌ RESULTADO: Encontrados {len(draws_without_cold)} sorteios SEM números frios")
        print(f"   Percentual: {len(draws_without_cold)/total_draws*100:.2f}% de {total_draws} sorteios")
        print()
        print("="*80)
        print("LISTA DE SORTEIOS SEM NÚMEROS FRIOS")
        print("="*80)
        print()
        print(f"{'Concurso':<10} {'Data':<15} {'Números Sorteados'}")
        print("-"*80)
        
        for draw in draws_without_cold:
            concurso = str(draw['concurso'])
            data = draw['data']
            numbers = ', '.join(map(str, draw['numbers_list']))
            print(f"{concurso:<10} {data:<15} {numbers}")
    
    print()
    print("="*80)
    print("📊 ESTATÍSTICAS")
    print("="*80)
    print()
    
    # Estatísticas sobre presença de números frios
    all_draws = load_all_draws()
    
    # Conta quantos números frios em cada sorteio
    cold_count_distribution = {}
    
    for draw in all_draws:
        cold_count = len(draw['numbers'] & cold_numbers)
        cold_count_distribution[cold_count] = cold_count_distribution.get(cold_count, 0) + 1
    
    print("Distribuição de Números Frios por Sorteio:")
    print("-"*80)
    for count in sorted(cold_count_distribution.keys()):
        freq = cold_count_distribution[count]
        pct = freq / len(all_draws) * 100
        bar = "█" * int(pct / 2)
        print(f"{count:2d} números frios: {freq:4d} sorteios ({pct:5.2f}%) {bar}")
    
    print()
    
    # Mínimo e máximo de números frios
    min_cold = min(cold_count_distribution.keys())
    max_cold = max(cold_count_distribution.keys())
    avg_cold = sum(count * freq for count, freq in cold_count_distribution.items()) / len(all_draws)
    
    print(f"Mínimo de números frios em um sorteio: {min_cold}")
    print(f"Máximo de números frios em um sorteio: {max_cold}")
    print(f"Média de números frios por sorteio: {avg_cold:.2f}")
    print()
    
    # Salva relatório
    output_dir = Path('out/cold_analysis')
    output_dir.mkdir(exist_ok=True, parents=True)
    
    report_file = output_dir / 'sorteios_sem_frios.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("SORTEIOS SEM NÚMEROS FRIOS\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Números Frios (15 mais frios): {', '.join(map(str, sorted(cold_numbers)))}\n\n")
        f.write(f"Total de sorteios analisados: {total_draws}\n")
        f.write(f"Sorteios sem números frios: {len(draws_without_cold)}\n\n")
        
        if draws_without_cold:
            f.write("LISTA DE SORTEIOS SEM NÚMEROS FRIOS:\n")
            f.write("-"*80 + "\n")
            for draw in draws_without_cold:
                f.write(f"Concurso {draw['concurso']} ({draw['data']})\n")
                f.write(f"  Números: {', '.join(map(str, draw['numbers_list']))}\n\n")
        else:
            f.write("TODOS os sorteios tiveram pelo menos 1 número frio!\n")
        
        f.write("\nDISTRIBUIÇÃO DE NÚMEROS FRIOS POR SORTEIO:\n")
        f.write("-"*80 + "\n")
        for count in sorted(cold_count_distribution.keys()):
            freq = cold_count_distribution[count]
            pct = freq / len(all_draws) * 100
            f.write(f"{count:2d} números frios: {freq:4d} sorteios ({pct:5.2f}%)\n")
    
    print(f"💾 Relatório salvo em: {report_file}")
    print()

if __name__ == '__main__':
    main()

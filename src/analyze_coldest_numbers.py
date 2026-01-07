import pandas as pd
from pathlib import Path

def analyze_coldest_numbers():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Contar frequência de cada número
    frequencia = {}
    for numero in range(1, 26):
        count = 0
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                count += 1
        frequencia[numero] = count
    
    # Calcular desvio percentual
    total_sorteios = len(df)
    frequencia_esperada = total_sorteios * (15/25)  # Cada número deveria aparecer em 60% dos sorteios
    
    print("=" * 100)
    print("ANÁLISE DOS NÚMEROS MAIS FRIOS")
    print("=" * 100)
    print(f"\nTotal de sorteios analisados: {total_sorteios}")
    print(f"Frequência esperada por número: {frequencia_esperada:.2f} aparições ({(15/25)*100:.1f}%)")
    print("\n" + "=" * 100)
    
    # Números que nunca saíram
    nunca_sairam = [num for num, freq in frequencia.items() if freq == 0]
    
    print("\nNÚMEROS QUE NUNCA SAÍRAM:")
    print("-" * 100)
    if nunca_sairam:
        print(f"  {nunca_sairam}")
    else:
        print("  ✓ TODOS os números de 1 a 25 já saíram pelo menos uma vez!")
    
    # Ordenar por frequência (do menor para o maior)
    sorted_freq = sorted(frequencia.items(), key=lambda x: x[1])
    
    print("\n" + "=" * 100)
    print("RANKING DOS NÚMEROS MAIS FRIOS (que menos saíram):")
    print("-" * 100)
    print(f"{'Rank':>5} | {'Número':>7} | {'Aparições':>11} | {'Freq %':>9} | {'Desvio':>10} | {'Status':>15}")
    print("-" * 100)
    
    for rank, (numero, freq) in enumerate(sorted_freq, 1):
        freq_pct = (freq / total_sorteios) * 100
        desvio_pct = ((freq - frequencia_esperada) / frequencia_esperada) * 100
        
        if desvio_pct <= -3:
            status = "❄️❄️❄️ Muito Frio"
        elif desvio_pct <= -2:
            status = "❄️❄️ Frio"
        elif desvio_pct <= -1:
            status = "❄️ Frio"
        else:
            status = "Normal"
        
        print(f"{rank:5d} | {numero:7d} | {freq:11d} | {freq_pct:8.2f}% | {desvio_pct:9.2f}% | {status:>15}")
    
    # Selecionar os 18 mais frios que saíram ao menos 1 vez
    numeros_validos = [(num, freq) for num, freq in sorted_freq if freq > 0]
    top_18_frios = [num for num, freq in numeros_validos[:18]]
    
    print("\n" + "=" * 100)
    print("TOP 18 NÚMEROS MAIS FRIOS (para estratégia contrária):")
    print("-" * 100)
    print(f"\nNúmeros selecionados: {sorted(top_18_frios)}")
    
    # Estatísticas dos 18 selecionados
    print("\nEstatísticas dos 18 selecionados:")
    total_aparicoes = sum(frequencia[num] for num in top_18_frios)
    media_aparicoes = total_aparicoes / 18
    
    print(f"  Total de aparições combinadas: {total_aparicoes}")
    print(f"  Média de aparições: {media_aparicoes:.2f}")
    print(f"  Mínimo: {min(frequencia[num] for num in top_18_frios)}")
    print(f"  Máximo: {max(frequencia[num] for num in top_18_frios)}")
    
    # Comparação com os 18 mais quentes
    top_18_quentes = [num for num, freq in sorted(frequencia.items(), key=lambda x: x[1], reverse=True)[:18]]
    total_quentes = sum(frequencia[num] for num in top_18_quentes)
    
    print("\n" + "=" * 100)
    print("COMPARAÇÃO: 18 MAIS FRIOS vs 18 MAIS QUENTES:")
    print("-" * 100)
    
    print(f"\n18 Mais FRIOS: {sorted(top_18_frios)}")
    print(f"  Total de aparições: {total_aparicoes}")
    print(f"  Média por número: {total_aparicoes/18:.2f}")
    
    print(f"\n18 Mais QUENTES: {sorted(top_18_quentes)}")
    print(f"  Total de aparições: {total_quentes}")
    print(f"  Média por número: {total_quentes/18:.2f}")
    
    print(f"\nDiferença: {total_quentes - total_aparicoes} aparições ({((total_quentes - total_aparicoes)/total_quentes)*100:.1f}%)")
    
    # Análise de paridade
    pares_frios = sum(1 for n in top_18_frios if n % 2 == 0)
    impares_frios = 18 - pares_frios
    
    pares_quentes = sum(1 for n in top_18_quentes if n % 2 == 0)
    impares_quentes = 18 - pares_quentes
    
    print("\n" + "=" * 100)
    print("ANÁLISE DE PARIDADE:")
    print("-" * 100)
    print(f"\n18 Mais FRIOS:")
    print(f"  Pares: {pares_frios} → {[n for n in top_18_frios if n % 2 == 0]}")
    print(f"  Ímpares: {impares_frios} → {[n for n in top_18_frios if n % 2 != 0]}")
    
    print(f"\n18 Mais QUENTES:")
    print(f"  Pares: {pares_quentes} → {[n for n in top_18_quentes if n % 2 == 0]}")
    print(f"  Ímpares: {impares_quentes} → {[n for n in top_18_quentes if n % 2 != 0]}")
    
    # Últimos 50 sorteios - performance
    ultimos_50 = df.tail(50)
    
    aparicoes_frios_50 = {}
    aparicoes_quentes_50 = {}
    
    for numero in top_18_frios:
        count = 0
        for idx, row in ultimos_50.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                count += 1
        aparicoes_frios_50[numero] = count
    
    for numero in top_18_quentes:
        count = 0
        for idx, row in ultimos_50.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                count += 1
        aparicoes_quentes_50[numero] = count
    
    print("\n" + "=" * 100)
    print("PERFORMANCE NOS ÚLTIMOS 50 SORTEIOS:")
    print("-" * 100)
    
    total_frios_50 = sum(aparicoes_frios_50.values())
    total_quentes_50 = sum(aparicoes_quentes_50.values())
    
    print(f"\n18 Mais FRIOS:")
    print(f"  Total de aparições: {total_frios_50}")
    print(f"  Média por número: {total_frios_50/18:.2f}")
    print(f"  Frequência média: {(total_frios_50/18/50)*100:.1f}%")
    
    print(f"\n18 Mais QUENTES:")
    print(f"  Total de aparições: {total_quentes_50}")
    print(f"  Média por número: {total_quentes_50/18:.2f}")
    print(f"  Frequência média: {(total_quentes_50/18/50)*100:.1f}%")
    
    print(f"\nDiferença últimos 50: {total_quentes_50 - total_frios_50} aparições")
    
    # Salvar resultados
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvar pool de 18 frios
    pool_path = output_dir / 'pool_18_mais_frios.txt'
    with open(pool_path, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, sorted(top_18_frios))))
    
    print(f"\n✓ Pool salva em: {pool_path}")
    
    # Salvar relatório completo
    report_path = output_dir / 'analise_numeros_frios.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("ANÁLISE DOS NÚMEROS MAIS FRIOS\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"Total de sorteios: {total_sorteios}\n\n")
        
        f.write("TOP 18 MAIS FRIOS:\n")
        f.write(f"{sorted(top_18_frios)}\n\n")
        
        f.write("RANKING COMPLETO:\n")
        f.write("-" * 100 + "\n")
        for rank, (numero, freq) in enumerate(sorted_freq, 1):
            freq_pct = (freq / total_sorteios) * 100
            desvio_pct = ((freq - frequencia_esperada) / frequencia_esperada) * 100
            f.write(f"{rank:2d}. Número {numero:2d}: {freq:4d} aparições ({freq_pct:5.2f}%, {desvio_pct:+6.2f}%)\n")
    
    print(f"✓ Relatório salvo em: {report_path}")
    
    return {
        'top_18_frios': sorted(top_18_frios),
        'top_18_quentes': sorted(top_18_quentes),
        'nunca_sairam': nunca_sairam,
        'total_frios': total_aparicoes,
        'total_quentes': total_quentes
    }

if __name__ == "__main__":
    result = analyze_coldest_numbers()
    
    print("\n" + "=" * 100)
    print("RESUMO:")
    print("-" * 100)
    print(f"✓ Pool de 18 mais frios: {result['top_18_frios']}")
    print(f"✓ Números que nunca saíram: {result['nunca_sairam'] if result['nunca_sairam'] else 'Nenhum'}")
    print(f"✓ Próximos passos: Gerar combinações otimizadas e testar contra histórico")

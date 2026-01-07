import pandas as pd
from pathlib import Path

def analyze_coldest_in_last_50():
    # Pool de 18 números mais frios
    pool_frios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16, 17, 18, 19, 21, 22, 23]
    
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Pegar últimos 50 sorteios
    ultimos_50 = df.tail(50).copy()
    
    print("=" * 120)
    print("ANÁLISE: NÚMEROS FRIOS NOS ÚLTIMOS 50 SORTEIOS")
    print("=" * 120)
    print(f"\nPool de 18 Números Frios: {pool_frios}")
    print("\n" + "=" * 120)
    print(f"{'Concurso':>10} | {'Números Sorteados':^60} | {'Frios':>6} | {'Números Frios Sorteados':^30}")
    print("-" * 120)
    
    resultados = []
    
    for idx, row in ultimos_50.iterrows():
        concurso = row['Concurso']
        numeros_sorteados = sorted([row[f'Bola{i}'] for i in range(1, 16)])
        
        # Identificar quais números frios saíram
        frios_sorteados = [num for num in numeros_sorteados if num in pool_frios]
        qtd_frios = len(frios_sorteados)
        
        # Formatar números sorteados com destaque para frios
        nums_str = ', '.join([f"**{n:02d}**" if n in pool_frios else f"{n:02d}" for n in numeros_sorteados])
        frios_str = ', '.join([f"{n:02d}" for n in frios_sorteados])
        
        print(f"{concurso:10d} | {str(numeros_sorteados):60} | {qtd_frios:6d} | {frios_str:30}")
        
        resultados.append({
            'Concurso': concurso,
            'Numeros_Sorteados': numeros_sorteados,
            'Qtd_Frios': qtd_frios,
            'Frios_Sorteados': frios_sorteados
        })
    
    # Estatísticas
    qtds_frios = [r['Qtd_Frios'] for r in resultados]
    
    print("\n" + "=" * 120)
    print("ESTATÍSTICAS DOS ÚLTIMOS 50 SORTEIOS")
    print("=" * 120)
    
    print(f"\nQuantidade de números frios por sorteio:")
    print(f"  Mínimo: {min(qtds_frios)} números frios")
    print(f"  Máximo: {max(qtds_frios)} números frios")
    print(f"  Média: {sum(qtds_frios)/len(qtds_frios):.2f} números frios por sorteio")
    print(f"  Mediana: {sorted(qtds_frios)[len(qtds_frios)//2]} números frios")
    
    # Distribuição
    print("\nDistribuição de frequência:")
    from collections import Counter
    distribuicao = Counter(qtds_frios)
    
    print(f"{'Qtd Frios':>12} | {'Sorteios':>10} | {'Percentual':>12} | {'Barra':^40}")
    print("-" * 80)
    for qtd in sorted(distribuicao.keys()):
        count = distribuicao[qtd]
        pct = (count / 50) * 100
        barra = "█" * int(pct / 2.5)
        print(f"{qtd:12d} | {count:10d} | {pct:11.1f}% | {barra:40}")
    
    # Análise de padrões
    print("\n" + "=" * 120)
    print("ANÁLISE DE PADRÕES")
    print("=" * 120)
    
    # Sorteios com mais frios
    top_frios = sorted(resultados, key=lambda x: x['Qtd_Frios'], reverse=True)[:5]
    print("\n🔵 Top 5 Sorteios com MAIS números frios:")
    for r in top_frios:
        print(f"  Concurso {r['Concurso']:5d}: {r['Qtd_Frios']:2d} frios → {r['Frios_Sorteados']}")
    
    # Sorteios com menos frios
    bottom_frios = sorted(resultados, key=lambda x: x['Qtd_Frios'])[:5]
    print("\n🔴 Top 5 Sorteios com MENOS números frios:")
    for r in bottom_frios:
        print(f"  Concurso {r['Concurso']:5d}: {r['Qtd_Frios']:2d} frios → {r['Frios_Sorteados']}")
    
    # Números frios mais frequentes nos últimos 50
    todos_frios_sorteados = []
    for r in resultados:
        todos_frios_sorteados.extend(r['Frios_Sorteados'])
    
    freq_frios = Counter(todos_frios_sorteados)
    
    print("\n" + "=" * 120)
    print("FREQUÊNCIA DOS NÚMEROS FRIOS NOS ÚLTIMOS 50 SORTEIOS")
    print("=" * 120)
    print(f"{'Número':>8} | {'Aparições':>11} | {'Freq %':>9} | {'Status':>20} | {'Barra':^40}")
    print("-" * 100)
    
    for numero in sorted(pool_frios):
        freq = freq_frios.get(numero, 0)
        freq_pct = (freq / 50) * 100
        
        if freq_pct >= 70:
            status = "🔥🔥 Muito Quente"
        elif freq_pct >= 60:
            status = "🔥 Quente"
        elif freq_pct >= 50:
            status = "😐 Normal"
        elif freq_pct >= 40:
            status = "❄️ Frio"
        else:
            status = "❄️❄️ Muito Frio"
        
        barra = "█" * int(freq_pct / 2.5)
        print(f"{numero:8d} | {freq:11d} | {freq_pct:8.1f}% | {status:>20} | {barra:40}")
    
    # Análise de cobertura
    print("\n" + "=" * 120)
    print("ANÁLISE DE COBERTURA")
    print("=" * 120)
    
    sorteios_9_ou_mais = sum(1 for q in qtds_frios if q >= 9)
    sorteios_10_ou_mais = sum(1 for q in qtds_frios if q >= 10)
    sorteios_8_ou_menos = sum(1 for q in qtds_frios if q <= 8)
    
    print(f"\nSorteios com 10+ números frios: {sorteios_10_ou_mais} ({(sorteios_10_ou_mais/50)*100:.1f}%)")
    print(f"Sorteios com 9+ números frios: {sorteios_9_ou_mais} ({(sorteios_9_ou_mais/50)*100:.1f}%)")
    print(f"Sorteios com 8- números frios: {sorteios_8_ou_menos} ({(sorteios_8_ou_menos/50)*100:.1f}%)")
    
    # Potencial de acerto
    media_frios = sum(qtds_frios) / len(qtds_frios)
    print(f"\nMédia de acertos esperada com estratégia de 18 frios: {media_frios:.2f} de 15")
    print(f"Taxa de cobertura média: {(media_frios/15)*100:.1f}%")
    
    # Salvar relatório
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'analise_frios_ultimos_50.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("ANÁLISE: NÚMEROS FRIOS NOS ÚLTIMOS 50 SORTEIOS\n")
        f.write("=" * 120 + "\n\n")
        f.write(f"Pool de 18 Números Frios: {pool_frios}\n\n")
        
        f.write("DETALHAMENTO POR CONCURSO:\n")
        f.write("-" * 120 + "\n")
        for r in resultados:
            f.write(f"Concurso {r['Concurso']:5d}: {r['Qtd_Frios']:2d} frios → {r['Frios_Sorteados']}\n")
        
        f.write("\n" + "=" * 120 + "\n")
        f.write("ESTATÍSTICAS:\n")
        f.write("-" * 120 + "\n")
        f.write(f"Mínimo: {min(qtds_frios)} números frios\n")
        f.write(f"Máximo: {max(qtds_frios)} números frios\n")
        f.write(f"Média: {sum(qtds_frios)/len(qtds_frios):.2f} números frios por sorteio\n")
        f.write(f"Mediana: {sorted(qtds_frios)[len(qtds_frios)//2]} números frios\n")
        
        f.write("\n" + "=" * 120 + "\n")
        f.write("DISTRIBUIÇÃO:\n")
        f.write("-" * 120 + "\n")
        for qtd in sorted(distribuicao.keys()):
            count = distribuicao[qtd]
            pct = (count / 50) * 100
            f.write(f"{qtd:2d} frios: {count:2d} sorteios ({pct:5.1f}%)\n")
    
    print(f"\n✓ Relatório detalhado salvo em: {report_path}")
    
    return {
        'resultados': resultados,
        'media': media_frios,
        'minimo': min(qtds_frios),
        'maximo': max(qtds_frios),
        'distribuicao': distribuicao
    }

if __name__ == "__main__":
    stats = analyze_coldest_in_last_50()
    
    print("\n" + "=" * 120)
    print("CONCLUSÃO")
    print("=" * 120)
    print(f"\n✓ Em média, {stats['media']:.2f} dos 15 números sorteados pertencem ao pool de 18 frios")
    print(f"✓ Isso representa {(stats['media']/15)*100:.1f}% de cobertura média")
    print(f"✓ Variação: {stats['minimo']} a {stats['maximo']} números frios por sorteio")

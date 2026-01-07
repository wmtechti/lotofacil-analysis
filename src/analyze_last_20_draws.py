import pandas as pd
from pathlib import Path

def analyze_last_20_draws():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Pegar últimos 20
    ultimos_20 = df.tail(20)
    
    print("=" * 140)
    print("ANÁLISE: NÚMEROS QUE SE REPETIRAM NOS ÚLTIMOS 20 SORTEIOS")
    print("=" * 140)
    
    primeiro_concurso = ultimos_20.iloc[0]['Concurso']
    ultimo_concurso = ultimos_20.iloc[-1]['Concurso']
    
    print(f"\nPeríodo analisado: Concurso {primeiro_concurso} a {ultimo_concurso}")
    print(f"Total de sorteios: 20\n")
    
    # Contar frequência de cada número
    frequencia = {i: 0 for i in range(1, 26)}
    
    # Lista de todos os sorteios
    sorteios_detalhados = []
    
    for idx, row in ultimos_20.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        
        sorteios_detalhados.append({
            'Concurso': row['Concurso'],
            'Data': row['Data Sorteio'],
            'Numeros': numeros_sorteados
        })
        
        for numero in numeros_sorteados:
            frequencia[numero] += 1
    
    # Ordenar por frequência
    freq_ordenada = sorted(frequencia.items(), key=lambda x: x[1], reverse=True)
    
    # Estatísticas
    print("=" * 140)
    print("FREQUÊNCIA DE CADA NÚMERO NOS ÚLTIMOS 20 SORTEIOS")
    print("=" * 140)
    
    print(f"\n{'Rank':>5} | {'Número':>8} | {'Aparições':>12} | {'%':>10} | {'Status':>20} | {'Barra Visual':>30}")
    print("-" * 100)
    
    for rank, (numero, count) in enumerate(freq_ordenada, 1):
        pct = (count / 20) * 100
        
        # Status
        if count >= 16:
            status = "🔥 MUITO QUENTE"
            emoji = "🔥"
        elif count >= 13:
            status = "🌡️  QUENTE"
            emoji = "🌡️"
        elif count >= 10:
            status = "➡️  NORMAL"
            emoji = "➡️"
        elif count >= 7:
            status = "❄️  FRIO"
            emoji = "❄️"
        else:
            status = "🧊 MUITO FRIO"
            emoji = "🧊"
        
        # Barra visual
        barra = "█" * count + "░" * (20 - count)
        
        print(f"{emoji}{rank:4d} | {numero:8d} | {count:12d} | {pct:9.1f}% | {status:>20} | {barra}")
    
    # Grupos de análise
    print("\n" + "=" * 140)
    print("📊 GRUPOS DE ANÁLISE")
    print("=" * 140)
    
    muito_quentes = [num for num, count in freq_ordenada if count >= 16]
    quentes = [num for num, count in freq_ordenada if 13 <= count < 16]
    normais = [num for num, count in freq_ordenada if 10 <= count < 13]
    frios = [num for num, count in freq_ordenada if 7 <= count < 10]
    muito_frios = [num for num, count in freq_ordenada if count < 7]
    
    print(f"\n🔥 MUITO QUENTES (16+ aparições): {len(muito_quentes)}")
    if muito_quentes:
        for num in muito_quentes:
            count = frequencia[num]
            print(f"   • {num:2d}: {count:2d} aparições ({(count/20)*100:.1f}%)")
    
    print(f"\n🌡️  QUENTES (13-15 aparições): {len(quentes)}")
    if quentes:
        for num in quentes:
            count = frequencia[num]
            print(f"   • {num:2d}: {count:2d} aparições ({(count/20)*100:.1f}%)")
    
    print(f"\n➡️  NORMAIS (10-12 aparições): {len(normais)}")
    if normais:
        for num in normais:
            count = frequencia[num]
            print(f"   • {num:2d}: {count:2d} aparições ({(count/20)*100:.1f}%)")
    
    print(f"\n❄️  FRIOS (7-9 aparições): {len(frios)}")
    if frios:
        for num in frios:
            count = frequencia[num]
            print(f"   • {num:2d}: {count:2d} aparições ({(count/20)*100:.1f}%)")
    
    print(f"\n🧊 MUITO FRIOS (0-6 aparições): {len(muito_frios)}")
    if muito_frios:
        for num in muito_frios:
            count = frequencia[num]
            print(f"   • {num:2d}: {count:2d} aparições ({(count/20)*100:.1f}%)")
    
    # Lista detalhada dos 20 sorteios
    print("\n" + "=" * 140)
    print("📋 DETALHAMENTO DOS ÚLTIMOS 20 SORTEIOS")
    print("=" * 140)
    
    for i, sorteio in enumerate(reversed(sorteios_detalhados), 1):
        numeros_str = ','.join([f"{n:02d}" for n in sorteio['Numeros']])
        print(f"\n{i:2d}. Concurso {sorteio['Concurso']} - {sorteio['Data']}")
        print(f"    {numeros_str}")
    
    # Números que aparecem em TODOS os 20 sorteios
    print("\n" + "=" * 140)
    print("🎯 ANÁLISE ESPECIAL")
    print("=" * 140)
    
    sempre_presente = [num for num, count in frequencia.items() if count == 20]
    
    if sempre_presente:
        print(f"\n✅ Números que apareceram em TODOS os 20 sorteios: {len(sempre_presente)}")
        print(f"   {sempre_presente}")
    else:
        print(f"\n❌ Nenhum número apareceu em todos os 20 sorteios")
    
    # Números que NÃO apareceram
    nao_apareceram = [num for num, count in frequencia.items() if count == 0]
    
    if nao_apareceram:
        print(f"\n❌ Números que NÃO apareceram em nenhum dos 20 sorteios: {len(nao_apareceram)}")
        print(f"   {nao_apareceram}")
    else:
        print(f"\n✅ Todos os 25 números apareceram pelo menos 1 vez")
    
    # Comparar com nossos pools
    print("\n" + "=" * 140)
    print("📦 COMPARAÇÃO COM NOSSOS POOLS")
    print("=" * 140)
    
    pool_otimo = [1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20, 22, 24, 25]
    pool_13_21 = [1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 15, 16, 18, 19, 20, 21, 23, 25]
    pool_original = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    
    pools = [
        ('Pool Ótimo (18)', pool_otimo),
        ('Pool com 13,21 (19)', pool_13_21),
        ('Pool Original (19)', pool_original)
    ]
    
    print(f"\n{'Pool':<30} | {'Números':>10} | {'Aparições':>15} | {'Média':>10}")
    print("-" * 70)
    
    for nome, pool in pools:
        total_aparicoes = sum(frequencia[num] for num in pool)
        media = total_aparicoes / 20
        
        print(f"{nome:<30} | {len(pool):>10} | {total_aparicoes:>15} | {media:>9.2f}/15")
    
    # Top 18 números mais frequentes nos últimos 20
    top_18_ultimos_20 = [num for num, _ in freq_ordenada[:18]]
    top_18_ultimos_20.sort()
    
    print(f"\n📊 TOP 18 MAIS FREQUENTES NOS ÚLTIMOS 20:")
    print(f"   {top_18_ultimos_20}")
    
    # Comparar com pool ótimo
    numeros_diferentes = set(pool_otimo) ^ set(top_18_ultimos_20)
    
    if numeros_diferentes:
        print(f"\n⚠️  Diferenças entre Pool Ótimo e Top 18 últimos 20:")
        
        no_otimo_nao_top = set(pool_otimo) - set(top_18_ultimos_20)
        no_top_nao_otimo = set(top_18_ultimos_20) - set(pool_otimo)
        
        if no_otimo_nao_top:
            print(f"   No Pool Ótimo mas não no Top 18 recente: {sorted(no_otimo_nao_top)}")
            for num in sorted(no_otimo_nao_top):
                print(f"      • {num:2d}: {frequencia[num]:2d} aparições nos últimos 20")
        
        if no_top_nao_otimo:
            print(f"   No Top 18 recente mas não no Pool Ótimo: {sorted(no_top_nao_otimo)}")
            for num in sorted(no_top_nao_otimo):
                print(f"      • {num:2d}: {frequencia[num]:2d} aparições nos últimos 20")
    else:
        print(f"\n✅ Pool Ótimo e Top 18 últimos 20 são IDÊNTICOS!")
    
    # Salvar relatório
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'analise_ultimos_20_sorteios.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("ANÁLISE DOS ÚLTIMOS 20 SORTEIOS\n")
        f.write("=" * 100 + "\n\n")
        
        f.write(f"Período: Concurso {primeiro_concurso} a {ultimo_concurso}\n\n")
        
        f.write("FREQUÊNCIA:\n\n")
        for rank, (numero, count) in enumerate(freq_ordenada, 1):
            pct = (count / 20) * 100
            f.write(f"{rank:2d}. Número {numero:2d}: {count:2d} aparições ({pct:5.1f}%)\n")
        
        f.write(f"\n\nMUITO QUENTES (16+): {muito_quentes}\n")
        f.write(f"QUENTES (13-15): {quentes}\n")
        f.write(f"NORMAIS (10-12): {normais}\n")
        f.write(f"FRIOS (7-9): {frios}\n")
        f.write(f"MUITO FRIOS (0-6): {muito_frios}\n")
        
        f.write(f"\n\nTop 18 mais frequentes: {top_18_ultimos_20}\n")
    
    print(f"\n✓ Relatório salvo em: {report_path}")
    
    print("\n" + "=" * 140)
    
    return {
        'frequencia': frequencia,
        'muito_quentes': muito_quentes,
        'top_18': top_18_ultimos_20
    }

if __name__ == "__main__":
    resultado = analyze_last_20_draws()
    
    print(f"\n✅ Análise dos últimos 20 sorteios concluída!")
    print(f"✅ {len(resultado['muito_quentes'])} números muito quentes (16+ aparições)")
    print(f"✅ Top 18: {resultado['top_18']}")

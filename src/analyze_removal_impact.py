import pandas as pd
from pathlib import Path

def analyze_impact_of_removing_each():
    # Pool atual de 19 números
    pool_19 = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    ultimos_50 = df.tail(50)
    
    print("=" * 120)
    print("ANÁLISE DE IMPACTO: REMOVER 1 NÚMERO DO POOL DE 19")
    print("=" * 120)
    print(f"\nPool atual: {pool_19}")
    print(f"\nAnalisando impacto de remover cada número individualmente...\n")
    
    # Para cada número, calcular impacto de sua remoção
    resultados = []
    
    for numero_remover in pool_19:
        # Pool sem este número (18 números)
        pool_18_teste = [n for n in pool_19 if n != numero_remover]
        
        # Contar jogos perfeitos perdidos (15 acertos que viram 14)
        jogos_perfeitos_perdidos = 0
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            acertos_com_19 = len([n for n in numeros_sorteados if n in pool_19])
            acertos_com_18 = len([n for n in numeros_sorteados if n in pool_18_teste])
            
            if acertos_com_19 == 15 and acertos_com_18 == 14:
                jogos_perfeitos_perdidos += 1
        
        # Performance nos últimos 50
        total_acertos_19 = 0
        total_acertos_18 = 0
        
        for idx, row in ultimos_50.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            total_acertos_19 += len([n for n in numeros_sorteados if n in pool_19])
            total_acertos_18 += len([n for n in numeros_sorteados if n in pool_18_teste])
        
        media_19 = total_acertos_19 / 50
        media_18 = total_acertos_18 / 50
        perda_acertos = media_19 - media_18
        
        # Frequência do número nos últimos 50
        freq_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                     if numero_remover in [row[f'Bola{i}'] for i in range(1, 16)])
        
        # Frequência histórica
        freq_hist = sum(1 for idx, row in df.iterrows() 
                       if numero_remover in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_hist_pct = (freq_hist / len(df)) * 100
        
        # Distribuição de acertos com pool de 18
        dist_13_plus = 0
        dist_14_plus = 0
        dist_15 = 0
        
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            acertos = len([n for n in numeros_sorteados if n in pool_18_teste])
            if acertos >= 13:
                dist_13_plus += 1
            if acertos >= 14:
                dist_14_plus += 1
            if acertos == 15:
                dist_15 += 1
        
        resultados.append({
            'Numero': numero_remover,
            'Perf_Perdidos': jogos_perfeitos_perdidos,
            'Media_18': media_18,
            'Perda_Acertos': perda_acertos,
            'Freq_50': freq_50,
            'Freq_Hist_Pct': freq_hist_pct,
            'Dist_15': dist_15,
            'Dist_14_Plus': dist_14_plus,
            'Dist_13_Plus': dist_13_plus
        })
    
    # Ordenar por menor impacto (menor perda de acertos)
    resultados_sorted = sorted(resultados, key=lambda x: x['Perda_Acertos'])
    
    print("=" * 120)
    print("RANKING: NÚMEROS COM MENOR IMPACTO SE REMOVIDOS")
    print("-" * 120)
    print(f"{'Rank':>5} | {'Nº':>4} | {'15-Acertos':>11} | {'Perda':>8} | {'Média18':>9} | {'Freq50':>8} | {'HistPct':>9} | {'15s':>5} | {'14+':>6} | {'13+':>6}")
    print(f"{'':>5} | {'':>4} | {'Perdidos':>11} | {'Últimos':>8} | {'Últimos50':>9} | {'(de 50)':>8} | {'':>9} | {'Total':>5} | {'Total':>6} | {'Total':>6}")
    print("-" * 120)
    
    for rank, r in enumerate(resultados_sorted, 1):
        # Destacar os 3 melhores para remover
        destaque = "👉 " if rank <= 3 else "   "
        
        print(f"{destaque}{rank:2d} | {r['Numero']:4d} | {r['Perf_Perdidos']:11d} | {r['Perda_Acertos']:7.2f} | {r['Media_18']:9.2f} | {r['Freq_50']:8d} | {r['Freq_Hist_Pct']:8.2f}% | {r['Dist_15']:5d} | {r['Dist_14_Plus']:6d} | {r['Dist_13_Plus']:6d}")
    
    # Análise dos 3 melhores candidatos para remoção
    print("\n" + "=" * 120)
    print("TOP 3 NÚMEROS CANDIDATOS À REMOÇÃO (MENOR IMPACTO)")
    print("=" * 120)
    
    for i, r in enumerate(resultados_sorted[:3], 1):
        numero = r['Numero']
        
        # Classificação
        numeros_base = [1, 2, 3, 4, 5, 9, 12, 15, 18, 19, 22]
        frios_exclusivos = [6, 7, 8, 16, 17, 21, 23]
        quentes_exclusivos = [10, 11, 13, 14, 20, 24, 25]
        
        if numero in numeros_base:
            classif = "BASE"
        elif numero in frios_exclusivos:
            classif = "FRIO EXCLUSIVO"
        elif numero in quentes_exclusivos:
            classif = "QUENTE EXCLUSIVO"
        else:
            classif = "Outro"
        
        print(f"\n{i}º LUGAR: NÚMERO {numero} ({classif})")
        print("-" * 120)
        print(f"   Jogos perfeitos perdidos: {r['Perf_Perdidos']} de 6")
        print(f"   Perda média nos últimos 50: {r['Perda_Acertos']:.2f} acertos por sorteio")
        print(f"   Média com pool de 18 (sem {numero}): {r['Media_18']:.2f} de 15")
        print(f"   Frequência últimos 50: {r['Freq_50']} aparições ({(r['Freq_50']/50)*100:.1f}%)")
        print(f"   Frequência histórica: {r['Freq_Hist_Pct']:.2f}%")
        print(f"   Pool de 18 teria: {r['Dist_15']} jogos perfeitos, {r['Dist_14_Plus']} com 14+, {r['Dist_13_Plus']} com 13+")
        
        # Recomendação
        if r['Perf_Perdidos'] == 0:
            print(f"   ✅ EXCELENTE: Não perde NENHUM jogo perfeito!")
        elif r['Perf_Perdidos'] == 1:
            print(f"   ✅ BOM: Perde apenas 1 jogo perfeito")
        else:
            print(f"   ⚠️ Perde {r['Perf_Perdidos']} jogos perfeitos")
    
    # Análise dos 3 piores para remover
    print("\n" + "=" * 120)
    print("⚠️ TOP 3 NÚMEROS QUE NÃO DEVEM SER REMOVIDOS (MAIOR IMPACTO)")
    print("=" * 120)
    
    for i, r in enumerate(reversed(resultados_sorted[-3:]), 1):
        numero = r['Numero']
        
        if numero in numeros_base:
            classif = "BASE"
        elif numero in frios_exclusivos:
            classif = "FRIO EXCLUSIVO"
        elif numero in quentes_exclusivos:
            classif = "QUENTE EXCLUSIVO"
        else:
            classif = "Outro"
        
        print(f"\n{i}º: NÚMERO {numero} ({classif})")
        print(f"   ❌ Jogos perfeitos perdidos: {r['Perf_Perdidos']} de 6")
        print(f"   ❌ Perda média: {r['Perda_Acertos']:.2f} acertos/sorteio")
        print(f"   ❌ Frequência últimos 50: {r['Freq_50']} ({(r['Freq_50']/50)*100:.1f}%)")
    
    # Recomendação final
    melhor = resultados_sorted[0]
    
    print("\n" + "=" * 120)
    print("🎯 RECOMENDAÇÃO FINAL")
    print("=" * 120)
    
    print(f"\n✅ REMOVER: Número {melhor['Numero']}")
    print(f"\n   Motivos:")
    print(f"   • Menor impacto: perda de apenas {melhor['Perda_Acertos']:.2f} acertos/sorteio")
    print(f"   • Jogos perfeitos perdidos: {melhor['Perf_Perdidos']} de 6")
    print(f"   • Pool de 18 resultante terá {melhor['Dist_15']} jogos perfeitos")
    print(f"   • Frequência recente: {melhor['Freq_50']} em 50 ({(melhor['Freq_50']/50)*100:.1f}%)")
    print(f"   • Média resultante: {melhor['Media_18']:.2f} de 15 nos últimos 50")
    
    pool_18_final = [n for n in pool_19 if n != melhor['Numero']]
    print(f"\n📦 POOL FINAL DE 18 NÚMEROS (removendo {melhor['Numero']}):")
    print(f"   {pool_18_final}")
    
    # Salvar relatório
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'impacto_remocao_numeros.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("ANÁLISE DE IMPACTO: REMOVER 1 NÚMERO DO POOL DE 19\n")
        f.write("=" * 120 + "\n\n")
        f.write(f"Pool atual: {pool_19}\n\n")
        
        f.write("RANKING (do menor ao maior impacto):\n\n")
        for rank, r in enumerate(resultados_sorted, 1):
            f.write(f"{rank:2d}. Número {r['Numero']:2d}: ")
            f.write(f"Perda={r['Perda_Acertos']:.2f}, ")
            f.write(f"Perf.Perdidos={r['Perf_Perdidos']}, ")
            f.write(f"Freq50={r['Freq_50']}, ")
            f.write(f"Média18={r['Media_18']:.2f}\n")
        
        f.write(f"\n\nRECOMENDAÇÃO: Remover número {melhor['Numero']}\n")
        f.write(f"Pool final de 18: {pool_18_final}\n")
    
    print(f"\n✓ Relatório salvo em: {report_path}")
    
    # Salvar pool de 18 otimizado
    pool_path = output_dir / 'pool_18_otimizado.txt'
    with open(pool_path, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, pool_18_final)))
    
    print(f"✓ Pool de 18 otimizado salvo em: {pool_path}")
    
    print("\n" + "=" * 120)
    
    return {
        'melhor_remover': melhor['Numero'],
        'pool_18_final': pool_18_final,
        'resultados': resultados_sorted
    }

if __name__ == "__main__":
    resultado = analyze_impact_of_removing_each()
    
    print(f"\n✅ Análise concluída!")
    print(f"✅ Melhor número para remover: {resultado['melhor_remover']}")
    print(f"✅ Pool final de 18: {resultado['pool_18_final']}")

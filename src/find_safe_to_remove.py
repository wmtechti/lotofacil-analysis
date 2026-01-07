import pandas as pd
from pathlib import Path

def find_safe_number_to_remove():
    # Pool atual de 19 números
    pool_19 = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    
    # Os 6 jogos perfeitos identificados anteriormente
    jogos_perfeitos = [
        [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 20, 22, 23, 25],      # Concurso 623
        [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 15, 18, 19, 20, 22],      # Concurso 1114
        [1, 2, 3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 23, 25],       # Concurso 2028
        [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 16, 18, 19, 20, 23],      # Concurso 2602
        [1, 2, 3, 4, 5, 8, 9, 11, 12, 15, 16, 19, 20, 23, 25],      # Concurso 2960
        [2, 3, 6, 8, 9, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]     # Concurso 3495
    ]
    
    print("=" * 120)
    print("ANÁLISE: NÚMEROS SEGUROS PARA REMOVER (QUE NÃO APARECEM NOS JOGOS PERFEITOS)")
    print("=" * 120)
    
    # Identificar quais números aparecem nos jogos perfeitos
    numeros_em_perfeitos = set()
    contagem_perfeitos = {}
    
    for numero in pool_19:
        contagem = sum(1 for jogo in jogos_perfeitos if numero in jogo)
        contagem_perfeitos[numero] = contagem
        if contagem > 0:
            numeros_em_perfeitos.add(numero)
    
    print(f"\nNúmeros do pool que aparecem em jogos perfeitos:")
    for num in sorted(pool_19):
        count = contagem_perfeitos[num]
        if count > 0:
            print(f"   {num:2d}: aparece em {count} de 6 jogos perfeitos")
    
    # Números que NÃO aparecem em jogos perfeitos
    numeros_seguros = [n for n in pool_19 if n not in numeros_em_perfeitos]
    
    print(f"\n🎯 Números SEGUROS para remover (não aparecem em jogos perfeitos):")
    if numeros_seguros:
        print(f"   {numeros_seguros}")
    else:
        print(f"   ❌ NENHUM! Todos os números aparecem em pelo menos 1 jogo perfeito")
        print(f"\n   Vamos analisar números que aparecem em MENOS jogos perfeitos...")
    
    # Carregar dados
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    ultimos_50 = df.tail(50)
    
    # Analisar impacto de cada número, focando nos que aparecem menos vezes nos perfeitos
    print("\n" + "=" * 120)
    print("RANKING: MENOR IMPACTO (priorizando números com menos aparições nos perfeitos)")
    print("-" * 120)
    print(f"{'Nº':>4} | {'Aparece':>8} | {'15→14':>8} | {'14→13':>8} | {'13→12':>8} | {'Perda':>8} | {'Freq50':>8} | {'HistPct':>9}")
    print(f"{'':>4} | {'Perf.':>8} | {'Perdidos':>8} | {'Perdidos':>8} | {'Perdidos':>8} | {'Média':>8} | {'(de 50)':>8} | {'':>9}")
    print("-" * 120)
    
    resultados = []
    
    for numero_remover in pool_19:
        pool_18_teste = [n for n in pool_19 if n != numero_remover]
        
        # Contar impacto por nível de acerto
        perda_15_para_14 = 0  # Jogos perfeitos perdidos
        perda_14_para_13 = 0  # Jogos de 14 que viram 13
        perda_13_para_12 = 0  # Jogos de 13 que viram 12
        
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            acertos_com_19 = len([n for n in numeros_sorteados if n in pool_19])
            acertos_com_18 = len([n for n in numeros_sorteados if n in pool_18_teste])
            
            if acertos_com_19 == 15 and acertos_com_18 == 14:
                perda_15_para_14 += 1
            elif acertos_com_19 == 14 and acertos_com_18 == 13:
                perda_14_para_13 += 1
            elif acertos_com_19 == 13 and acertos_com_18 == 12:
                perda_13_para_12 += 1
        
        # Performance nos últimos 50
        total_acertos_19 = 0
        total_acertos_18 = 0
        
        for idx, row in ultimos_50.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            total_acertos_19 += len([n for n in numeros_sorteados if n in pool_19])
            total_acertos_18 += len([n for n in numeros_sorteados if n in pool_18_teste])
        
        perda_acertos = (total_acertos_19 - total_acertos_18) / 50
        
        # Frequência
        freq_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                     if numero_remover in [row[f'Bola{i}'] for i in range(1, 16)])
        
        freq_hist = sum(1 for idx, row in df.iterrows() 
                       if numero_remover in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_hist_pct = (freq_hist / len(df)) * 100
        
        resultados.append({
            'Numero': numero_remover,
            'Aparece_Perf': contagem_perfeitos[numero_remover],
            'Perda_15_14': perda_15_para_14,
            'Perda_14_13': perda_14_para_13,
            'Perda_13_12': perda_13_para_12,
            'Perda_Media': perda_acertos,
            'Freq_50': freq_50,
            'Freq_Hist_Pct': freq_hist_pct
        })
    
    # Ordenar por: 1) menos aparições nos perfeitos, 2) não perde 15→14, 3) menor perda média
    resultados_sorted = sorted(resultados, 
                              key=lambda x: (x['Aparece_Perf'], 
                                           x['Perda_15_14'],
                                           x['Perda_14_13'],
                                           x['Perda_Media']))
    
    for r in resultados_sorted:
        # Destacar os melhores
        destaque = "👉 " if r['Aparece_Perf'] <= min(contagem_perfeitos.values()) and r['Perda_15_14'] == 0 else "   "
        
        print(f"{destaque}{r['Numero']:2d} | {r['Aparece_Perf']:8d} | {r['Perda_15_14']:8d} | {r['Perda_14_13']:8d} | {r['Perda_13_12']:8d} | {r['Perda_Media']:7.2f} | {r['Freq_50']:8d} | {r['Freq_Hist_Pct']:8.2f}%")
    
    # Recomendações
    print("\n" + "=" * 120)
    print("🎯 ANÁLISE DETALHADA DOS MELHORES CANDIDATOS")
    print("=" * 120)
    
    # Filtrar apenas os que não perdem jogos perfeitos
    sem_perder_perfeitos = [r for r in resultados_sorted if r['Perda_15_14'] == 0]
    
    if sem_perder_perfeitos:
        print(f"\n✅ Números que NÃO PERDEM JOGOS PERFEITOS (15→14 = 0):\n")
        
        for i, r in enumerate(sem_perder_perfeitos[:5], 1):
            print(f"{i}º) Número {r['Numero']:2d}:")
            print(f"      Aparece em {r['Aparece_Perf']} de 6 jogos perfeitos")
            print(f"      ✅ Jogos perfeitos perdidos: 0")
            print(f"      ⚠️  Jogos 14→13 perdidos: {r['Perda_14_13']}")
            print(f"      ⚠️  Jogos 13→12 perdidos: {r['Perda_13_12']}")
            print(f"      Perda média: {r['Perda_Media']:.2f} acertos/sorteio")
            print(f"      Frequência últimos 50: {r['Freq_50']}/50 ({(r['Freq_50']/50)*100:.1f}%)")
            print(f"      Frequência histórica: {r['Freq_Hist_Pct']:.2f}%")
            print()
    else:
        print(f"\n❌ Todos os números causam perda de jogos perfeitos!")
        print(f"\nNúmeros que perdem APENAS 1 jogo perfeito:\n")
        
        um_perfeito = [r for r in resultados_sorted if r['Perda_15_14'] == 1]
        for i, r in enumerate(um_perfeito[:3], 1):
            print(f"{i}º) Número {r['Numero']:2d}: perda de {r['Perda_15_14']} jogo perfeito, {r['Perda_14_13']} de 14→13")
    
    # Recomendação final
    melhor = sem_perder_perfeitos[0] if sem_perder_perfeitos else resultados_sorted[0]
    
    print("\n" + "=" * 120)
    print("🎯 RECOMENDAÇÃO FINAL")
    print("=" * 120)
    
    if melhor['Perda_15_14'] == 0:
        print(f"\n✅ REMOVER: Número {melhor['Numero']}")
        print(f"\n   Motivos:")
        print(f"   • ✅ NÃO perde NENHUM jogo perfeito (15 acertos)")
        print(f"   • Aparece em apenas {melhor['Aparece_Perf']} de 6 jogos perfeitos")
        print(f"   • Perda de {melhor['Perda_14_13']} jogos de 14→13 acertos")
        print(f"   • Perda de {melhor['Perda_13_12']} jogos de 13→12 acertos")
        print(f"   • Perda média: {melhor['Perda_Media']:.2f} acertos/sorteio")
        print(f"   • Frequência recente: {melhor['Freq_50']}/50 ({(melhor['Freq_50']/50)*100:.1f}%)")
    else:
        print(f"\n⚠️ ATENÇÃO: Número {melhor['Numero']} perde {melhor['Perda_15_14']} jogo(s) perfeito(s)")
        print(f"   Mas é o que tem MENOR IMPACTO TOTAL")
    
    pool_18_final = [n for n in pool_19 if n != melhor['Numero']]
    print(f"\n📦 POOL FINAL DE 18 NÚMEROS (removendo {melhor['Numero']}):")
    print(f"   {pool_18_final}")
    
    # Salvar relatório
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'remocao_segura_analise.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("ANÁLISE: NÚMEROS SEGUROS PARA REMOVER\n")
        f.write("=" * 120 + "\n\n")
        
        f.write("Critério: Não perder jogos perfeitos (15 acertos)\n\n")
        
        if sem_perder_perfeitos:
            f.write("NÚMEROS QUE NÃO PERDEM JOGOS PERFEITOS:\n\n")
            for r in sem_perder_perfeitos:
                f.write(f"Número {r['Numero']:2d}: ")
                f.write(f"Aparece em {r['Aparece_Perf']}/6 perfeitos, ")
                f.write(f"Perde {r['Perda_14_13']} de 14→13, ")
                f.write(f"Perde {r['Perda_13_12']} de 13→12, ")
                f.write(f"Perda média: {r['Perda_Media']:.2f}\n")
        else:
            f.write("NENHUM número pode ser removido sem perder jogos perfeitos!\n")
        
        f.write(f"\n\nRECOMENDAÇÃO: Remover número {melhor['Numero']}\n")
        f.write(f"Pool final de 18: {pool_18_final}\n")
    
    print(f"\n✓ Relatório salvo em: {report_path}")
    
    # Salvar pool otimizado
    pool_path = output_dir / 'pool_18_sem_perder_perfeitos.txt'
    with open(pool_path, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, pool_18_final)))
    
    print(f"✓ Pool de 18 salvo em: {pool_path}")
    
    print("\n" + "=" * 120)
    
    return melhor

if __name__ == "__main__":
    resultado = find_safe_number_to_remove()
    
    print(f"\n✅ Número recomendado para remoção: {resultado['Numero']}")
    print(f"✅ Jogos perfeitos preservados: {6 - resultado['Perda_15_14']} de 6")

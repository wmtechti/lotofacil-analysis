import pandas as pd
from pathlib import Path

def select_next_4_numbers():
    # Pool atual de 15 números
    pool_atual_15 = [1, 2, 3, 4, 5, 8, 9, 10, 12, 15, 16, 18, 19, 20, 22]
    
    # Números exclusivamente frios ainda não usados
    frios_restantes = [6, 7, 17, 21, 23]  # Já usei 8 e 16
    
    # Números exclusivamente quentes ainda não usados
    quentes_restantes = [11, 13, 14, 24, 25]  # Já usei 10 e 20
    
    # Carregar dados históricos
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    total_sorteios = len(df)
    ultimos_50 = df.tail(50)
    
    print("=" * 100)
    print("SELEÇÃO DOS PRÓXIMOS 4 NÚMEROS (2 FRIOS + 2 QUENTES) PARA COMPLETAR 18")
    print("=" * 100)
    
    print(f"\n📦 Pool atual (15 números): {pool_atual_15}")
    
    # Analisar frios restantes
    print("\n" + "=" * 100)
    print("ANÁLISE DOS 5 NÚMEROS FRIOS RESTANTES")
    print("-" * 100)
    
    freq_frios = {}
    freq_frios_50 = {}
    
    for numero in frios_restantes:
        # Histórico completo
        count = sum(1 for idx, row in df.iterrows() 
                   if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_frios[numero] = count
        
        # Últimos 50
        count_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                      if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_frios_50[numero] = count_50
    
    print(f"\n{'Número':>8} | {'Histórico':>11} | {'Freq %':>9} | {'Últ. 50':>9} | {'Freq %':>9} | {'Status'}")
    print("-" * 80)
    
    for numero in sorted(frios_restantes, key=lambda x: freq_frios[x]):
        hist = freq_frios[numero]
        hist_pct = (hist / total_sorteios) * 100
        ult50 = freq_frios_50[numero]
        ult50_pct = (ult50 / 50) * 100
        
        # Determinar status baseado em últimos 50
        if ult50_pct >= 65:
            status = "🔥 Esquentou"
        elif ult50_pct >= 55:
            status = "😐 Normal"
        else:
            status = "❄️ Ainda frio"
        
        print(f"{numero:8d} | {hist:11d} | {hist_pct:8.2f}% | {ult50:9d} | {ult50_pct:8.1f}% | {status}")
    
    # Selecionar os 2 próximos mais frios
    proximos_2_frios = sorted(frios_restantes, key=lambda x: freq_frios[x])[:2]
    
    print(f"\n✅ PRÓXIMOS 2 FRIOS selecionados: {proximos_2_frios}")
    for num in proximos_2_frios:
        print(f"   • Número {num}: {freq_frios[num]} aparições ({(freq_frios[num]/total_sorteios)*100:.2f}%) - Últimos 50: {freq_frios_50[num]} ({(freq_frios_50[num]/50)*100:.1f}%)")
    
    # Analisar quentes restantes
    print("\n" + "=" * 100)
    print("ANÁLISE DOS 5 NÚMEROS QUENTES RESTANTES")
    print("-" * 100)
    
    freq_quentes = {}
    freq_quentes_50 = {}
    
    for numero in quentes_restantes:
        # Histórico completo
        count = sum(1 for idx, row in df.iterrows() 
                   if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_quentes[numero] = count
        
        # Últimos 50
        count_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                      if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_quentes_50[numero] = count_50
    
    print(f"\n{'Número':>8} | {'Histórico':>11} | {'Freq %':>9} | {'Últ. 50':>9} | {'Freq %':>9} | {'Status'}")
    print("-" * 80)
    
    for numero in sorted(quentes_restantes, key=lambda x: freq_quentes[x], reverse=True):
        hist = freq_quentes[numero]
        hist_pct = (hist / total_sorteios) * 100
        ult50 = freq_quentes_50[numero]
        ult50_pct = (ult50 / 50) * 100
        
        # Determinar status baseado em últimos 50
        if ult50_pct >= 65:
            status = "🔥🔥 Muito quente"
        elif ult50_pct >= 55:
            status = "🔥 Quente"
        else:
            status = "😐 Esfriando"
        
        print(f"{numero:8d} | {hist:11d} | {hist_pct:8.2f}% | {ult50:9d} | {ult50_pct:8.1f}% | {status}")
    
    # Selecionar os 2 próximos mais quentes
    proximos_2_quentes = sorted(quentes_restantes, key=lambda x: freq_quentes[x], reverse=True)[:2]
    
    print(f"\n✅ PRÓXIMOS 2 QUENTES selecionados: {proximos_2_quentes}")
    for num in proximos_2_quentes:
        print(f"   • Número {num}: {freq_quentes[num]} aparições ({(freq_quentes[num]/total_sorteios)*100:.2f}%) - Últimos 50: {freq_quentes_50[num]} ({(freq_quentes_50[num]/50)*100:.1f}%)")
    
    # Pool final de 18 números
    pool_final_18 = sorted(pool_atual_15 + proximos_2_frios + proximos_2_quentes)
    
    print("\n" + "=" * 100)
    print("POOL FINAL DE 18 NÚMEROS PARA ESTRATÉGIA COMPLETA")
    print("=" * 100)
    
    print(f"\n🎯 BASE (11 números): [1, 2, 3, 4, 5, 9, 12, 15, 18, 19, 22]")
    print(f"❄️  4 FRIOS: [16, 8] + {proximos_2_frios}")
    print(f"🔥 4 QUENTES: [20, 10] + {proximos_2_quentes}")
    
    print(f"\n📦 POOL COMPLETO (18 números):")
    print(f"   {pool_final_18}")
    
    # Análise de paridade do pool final
    pares_final = [n for n in pool_final_18 if n % 2 == 0]
    impares_final = [n for n in pool_final_18 if n % 2 != 0]
    
    print(f"\n📊 Características do Pool Final:")
    print(f"   Total: {len(pool_final_18)} números")
    print(f"   Pares: {len(pares_final)} → {pares_final}")
    print(f"   Ímpares: {len(impares_final)} → {impares_final}")
    
    # Distribuição por dezena
    dezenas_final = {
        '01-05': [n for n in pool_final_18 if 1 <= n <= 5],
        '06-10': [n for n in pool_final_18 if 6 <= n <= 10],
        '11-15': [n for n in pool_final_18 if 11 <= n <= 15],
        '16-20': [n for n in pool_final_18 if 16 <= n <= 20],
        '21-25': [n for n in pool_final_18 if 21 <= n <= 25]
    }
    
    print(f"\n   Distribuição por Dezena:")
    for dezena, nums in dezenas_final.items():
        print(f"     {dezena}: {len(nums)} números → {nums}")
    
    # Performance nos últimos 50
    print("\n" + "=" * 100)
    print("PERFORMANCE DO POOL FINAL (18 NÚMEROS) NOS ÚLTIMOS 50 SORTEIOS")
    print("-" * 100)
    
    acertos_por_sorteio = []
    
    for idx, row in ultimos_50.iterrows():
        concurso = row['Concurso']
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in pool_final_18])
        acertos_por_sorteio.append(acertos)
    
    print(f"\nAcertos por sorteio:")
    print(f"  Mínimo: {min(acertos_por_sorteio)} de 15")
    print(f"  Máximo: {max(acertos_por_sorteio)} de 15")
    print(f"  Média: {sum(acertos_por_sorteio)/len(acertos_por_sorteio):.2f} de 15")
    print(f"  Taxa de cobertura: {(sum(acertos_por_sorteio)/len(acertos_por_sorteio)/15)*100:.1f}%")
    
    # Contar sorteios com alto número de acertos
    sorteios_15 = sum(1 for a in acertos_por_sorteio if a == 15)
    sorteios_14 = sum(1 for a in acertos_por_sorteio if a == 14)
    sorteios_13 = sum(1 for a in acertos_por_sorteio if a == 13)
    sorteios_12_ou_mais = sum(1 for a in acertos_por_sorteio if a >= 12)
    
    print(f"\n  Sorteios com 15 acertos (100%): {sorteios_15} ({(sorteios_15/50)*100:.1f}%)")
    print(f"  Sorteios com 14 acertos: {sorteios_14} ({(sorteios_14/50)*100:.1f}%)")
    print(f"  Sorteios com 13 acertos: {sorteios_13} ({(sorteios_13/50)*100:.1f}%)")
    print(f"  Sorteios com 12+ acertos: {sorteios_12_ou_mais} ({(sorteios_12_ou_mais/50)*100:.1f}%)")
    
    # Comparação com pool de 15
    print("\n" + "=" * 100)
    print("COMPARAÇÃO: POOL 15 vs POOL 18")
    print("-" * 100)
    
    # Recalcular para pool de 15
    acertos_15 = []
    for idx, row in ultimos_50.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in pool_atual_15])
        acertos_15.append(acertos)
    
    media_15 = sum(acertos_15) / len(acertos_15)
    media_18 = sum(acertos_por_sorteio) / len(acertos_por_sorteio)
    
    print(f"\nPool de 15 números:")
    print(f"  Média de acertos: {media_15:.2f} de 15 ({(media_15/15)*100:.1f}%)")
    
    print(f"\nPool de 18 números:")
    print(f"  Média de acertos: {media_18:.2f} de 15 ({(media_18/15)*100:.1f}%)")
    
    print(f"\nGanho com 3 números adicionais:")
    print(f"  +{media_18 - media_15:.2f} acertos por sorteio")
    print(f"  +{((media_18 - media_15)/15)*100:.1f} pontos percentuais")
    
    # Salvar resultado
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'pool_final_18_numeros.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("POOL FINAL DE 18 NÚMEROS - ESTRATÉGIA BALANCEADA COMPLETA\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"BASE (11 números): [1, 2, 3, 4, 5, 9, 12, 15, 18, 19, 22]\n")
        f.write(f"4 FRIOS: [16, 8, {proximos_2_frios[0]}, {proximos_2_frios[1]}]\n")
        f.write(f"4 QUENTES: [20, 10, {proximos_2_quentes[0]}, {proximos_2_quentes[1]}]\n\n")
        f.write(f"POOL COMPLETO: {pool_final_18}\n\n")
        f.write("=" * 100 + "\n\n")
        f.write("CARACTERÍSTICAS:\n\n")
        f.write(f"Total: {len(pool_final_18)} números\n")
        f.write(f"Pares: {len(pares_final)} → {pares_final}\n")
        f.write(f"Ímpares: {len(impares_final)} → {impares_final}\n\n")
        f.write("Distribuição por Dezena:\n")
        for dezena, nums in dezenas_final.items():
            f.write(f"  {dezena}: {len(nums)} números → {nums}\n")
        f.write("\n" + "=" * 100 + "\n\n")
        f.write("PERFORMANCE ÚLTIMOS 50 SORTEIOS:\n\n")
        f.write(f"Média de acertos: {media_18:.2f} de 15 ({(media_18/15)*100:.1f}%)\n")
        f.write(f"Mínimo: {min(acertos_por_sorteio)} / Máximo: {max(acertos_por_sorteio)}\n")
        f.write(f"Sorteios com 15 acertos: {sorteios_15}\n")
        f.write(f"Sorteios com 14 acertos: {sorteios_14}\n")
        f.write(f"Sorteios com 13 acertos: {sorteios_13}\n")
        f.write(f"Sorteios com 12+ acertos: {sorteios_12_ou_mais}\n\n")
        f.write(f"Ganho vs pool de 15: +{media_18 - media_15:.2f} acertos\n")
    
    print(f"\n✓ Relatório salvo em: {report_path}")
    
    # Salvar pool em formato simples
    pool_path = output_dir / 'pool_18_numeros.txt'
    with open(pool_path, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, pool_final_18)))
    
    print(f"✓ Pool salvo em: {pool_path}")
    
    print("\n" + "=" * 100)
    print("RESUMO FINAL")
    print("=" * 100)
    print(f"\n✅ Pool de 18 números: {pool_final_18}")
    print(f"✅ Cobertura média últimos 50: {(media_18/15)*100:.1f}%")
    print(f"✅ Paridade: {len(pares_final)} pares / {len(impares_final)} ímpares")
    print(f"✅ Ganho vs pool de 15: +{media_18 - media_15:.2f} acertos/sorteio")
    print(f"✅ Pronto para gerar C(18,15) = 816 combinações")
    print("=" * 100)
    
    return {
        'pool_final': pool_final_18,
        'frios': [16, 8] + proximos_2_frios,
        'quentes': [20, 10] + proximos_2_quentes,
        'media_cobertura': media_18
    }

if __name__ == "__main__":
    resultado = select_next_4_numbers()

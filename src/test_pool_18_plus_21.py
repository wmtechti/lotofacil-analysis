import pandas as pd
from pathlib import Path

def test_pool_18_plus_21():
    # Pool ótimo de 18 números
    pool_18_otimo = [1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20, 22, 24, 25]
    
    # Pool de 19 números (18 + 21)
    pool_19_com_21 = pool_18_otimo + [21]
    pool_19_com_21.sort()
    
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    print("=" * 140)
    print("TESTE: ADICIONAR NÚMERO 21 AO POOL ÓTIMO DE 18")
    print("=" * 140)
    
    print(f"\n📦 POOL ÓTIMO DE 18 NÚMEROS:")
    print(f"   {pool_18_otimo}")
    
    print(f"\n➕ ADICIONANDO: 21")
    
    print(f"\n📦 POOL NOVO DE 19 NÚMEROS (18 + 21):")
    print(f"   {pool_19_com_21}")
    
    # Analisar jogos perfeitos com pool de 18
    jogos_perfeitos_18 = []
    
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in pool_18_otimo])
        
        if acertos == 15:
            jogos_perfeitos_18.append({
                'Concurso': row['Concurso'],
                'Data': row['Data Sorteio'],
                'Numeros': numeros_sorteados
            })
    
    # Analisar jogos perfeitos com pool de 19 (com 21)
    jogos_perfeitos_19 = []
    
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in pool_19_com_21])
        
        if acertos == 15:
            jogos_perfeitos_19.append({
                'Concurso': row['Concurso'],
                'Data': row['Data Sorteio'],
                'Numeros': numeros_sorteados
            })
    
    # Distribuição completa
    dist_18 = {i: 0 for i in range(16)}
    dist_19 = {i: 0 for i in range(16)}
    
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        
        acertos_18 = len([n for n in numeros_sorteados if n in pool_18_otimo])
        dist_18[acertos_18] += 1
        
        acertos_19 = len([n for n in numeros_sorteados if n in pool_19_com_21])
        dist_19[acertos_19] += 1
    
    # Resultados
    print("\n" + "=" * 140)
    print("📊 COMPARAÇÃO DE RESULTADOS")
    print("=" * 140)
    
    print(f"\n{'Métrica':<40} | {'Pool 18 (sem 21)':>20} | {'Pool 19 (com 21)':>20} | {'Diferença':>15}")
    print("-" * 140)
    print(f"{'Jogos perfeitos (15 acertos)':<40} | {len(jogos_perfeitos_18):>20} | {len(jogos_perfeitos_19):>20} | {len(jogos_perfeitos_19) - len(jogos_perfeitos_18):>+15}")
    print(f"{'Jogos com 14 acertos':<40} | {dist_18[14]:>20} | {dist_19[14]:>20} | {dist_19[14] - dist_18[14]:>+15}")
    print(f"{'Jogos com 13 acertos':<40} | {dist_18[13]:>20} | {dist_19[13]:>20} | {dist_19[13] - dist_18[13]:>+15}")
    
    total_13_plus_18 = dist_18[13] + dist_18[14] + dist_18[15]
    total_13_plus_19 = dist_19[13] + dist_19[14] + dist_19[15]
    
    print(f"{'TOTAL 13+ acertos':<40} | {total_13_plus_18:>20} | {total_13_plus_19:>20} | {total_13_plus_19 - total_13_plus_18:>+15}")
    
    pct_13_plus_18 = (total_13_plus_18 / len(df)) * 100
    pct_13_plus_19 = (total_13_plus_19 / len(df)) * 100
    
    print(f"{'% de jogos com 13+ acertos':<40} | {pct_13_plus_18:>19.2f}% | {pct_13_plus_19:>19.2f}% | {pct_13_plus_19 - pct_13_plus_18:>+14.2f}%")
    
    # Detalhes dos jogos perfeitos com pool de 19
    print("\n" + "=" * 140)
    print(f"🎯 JOGOS PERFEITOS COM POOL DE 19 (18 + 21): {len(jogos_perfeitos_19)}")
    print("=" * 140)
    
    if jogos_perfeitos_19:
        for i, jogo in enumerate(jogos_perfeitos_19, 1):
            numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
            print(f"\n{i:2d}. Concurso {jogo['Concurso']} - {jogo['Data']}")
            print(f"    {numeros_str}")
            
            # Verificar se tem o 21
            if 21 in jogo['Numeros']:
                print(f"    ✅ Contém o número 21")
    else:
        print("\n❌ NENHUM jogo perfeito encontrado!")
    
    # Jogos perfeitos GANHOS ao adicionar 21
    concursos_18 = {j['Concurso'] for j in jogos_perfeitos_18}
    concursos_19 = {j['Concurso'] for j in jogos_perfeitos_19}
    
    perdidos = concursos_18 - concursos_19
    ganhos = concursos_19 - concursos_18
    
    print("\n" + "=" * 140)
    print(f"📈 JOGOS PERFEITOS GANHOS ao adicionar 21: {len(ganhos)}")
    print("=" * 140)
    
    if ganhos:
        for jogo in jogos_perfeitos_19:
            if jogo['Concurso'] in ganhos:
                numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
                print(f"\n✅ Concurso {jogo['Concurso']} - {jogo['Data']}")
                print(f"   {numeros_str}")
                print(f"   Número 21 estava presente neste jogo!")
    else:
        print("\n❌ Nenhum jogo perfeito novo adicionado")
    
    if perdidos:
        print("\n" + "=" * 140)
        print(f"📉 JOGOS PERFEITOS PERDIDOS: {len(perdidos)}")
        print("=" * 140)
        
        for jogo in jogos_perfeitos_18:
            if jogo['Concurso'] in perdidos:
                numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
                print(f"\n❌ Concurso {jogo['Concurso']} - {jogo['Data']}")
                print(f"   {numeros_str}")
    
    # Distribuição completa
    print("\n" + "=" * 140)
    print("📊 DISTRIBUIÇÃO COMPLETA DE ACERTOS")
    print("=" * 140)
    
    print(f"\n{'Acertos':>10} | {'Pool 18':>15} | {'% Pool 18':>12} | {'Pool 19':>15} | {'% Pool 19':>12} | {'Diferença':>15}")
    print("-" * 100)
    
    for acertos in range(15, 8, -1):
        pct_18 = (dist_18[acertos] / len(df)) * 100
        pct_19 = (dist_19[acertos] / len(df)) * 100
        diff = dist_19[acertos] - dist_18[acertos]
        
        print(f"{acertos:>10} | {dist_18[acertos]:>15} | {pct_18:>11.2f}% | {dist_19[acertos]:>15} | {pct_19:>11.2f}% | {diff:>+15}")
    
    # Análise nos últimos 50
    ultimos_50 = df.tail(50)
    
    total_acertos_18 = 0
    total_acertos_19 = 0
    
    for idx, row in ultimos_50.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        total_acertos_18 += len([n for n in numeros_sorteados if n in pool_18_otimo])
        total_acertos_19 += len([n for n in numeros_sorteados if n in pool_19_com_21])
    
    media_18 = total_acertos_18 / 50
    media_19 = total_acertos_19 / 50
    
    print("\n" + "=" * 140)
    print("📈 DESEMPENHO NOS ÚLTIMOS 50 SORTEIOS")
    print("=" * 140)
    
    print(f"\nPool 18 (sem 21): {media_18:.2f} acertos por sorteio")
    print(f"Pool 19 (com 21): {media_19:.2f} acertos por sorteio")
    print(f"Diferença:        {media_19 - media_18:+.2f} acertos por sorteio")
    
    # Frequência do 21 nos últimos 50
    freq_21_ultimos_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                              if 21 in [row[f'Bola{i}'] for i in range(1, 16)])
    
    print(f"\nNúmero 21 nos últimos 50: {freq_21_ultimos_50} aparições ({(freq_21_ultimos_50/50)*100:.1f}%)")
    
    # Recomendação final
    print("\n" + "=" * 140)
    print("🎯 RECOMENDAÇÃO FINAL")
    print("=" * 140)
    
    if len(jogos_perfeitos_19) > len(jogos_perfeitos_18):
        print(f"\n✅ ADICIONAR 21 É VANTAJOSO!")
        print(f"   • Ganha {len(jogos_perfeitos_19) - len(jogos_perfeitos_18)} jogos perfeitos")
        print(f"   • Total de jogos perfeitos: {len(jogos_perfeitos_19)} (vs {len(jogos_perfeitos_18)} sem o 21)")
    elif len(jogos_perfeitos_19) < len(jogos_perfeitos_18):
        print(f"\n❌ ADICIONAR 21 É DESVANTAJOSO!")
        print(f"   • Perde {len(jogos_perfeitos_18) - len(jogos_perfeitos_19)} jogos perfeitos")
        print(f"   • Total de jogos perfeitos: {len(jogos_perfeitos_19)} (vs {len(jogos_perfeitos_18)} sem o 21)")
    else:
        print(f"\n⚖️  ADICIONAR 21 É NEUTRO para jogos perfeitos")
        print(f"   • Mantém os mesmos {len(jogos_perfeitos_19)} jogos perfeitos")
    
    if total_13_plus_19 > total_13_plus_18:
        print(f"   • Ganha {total_13_plus_19 - total_13_plus_18} jogos com 13+ acertos")
    elif total_13_plus_19 < total_13_plus_18:
        print(f"   • Perde {total_13_plus_18 - total_13_plus_19} jogos com 13+ acertos")
    
    if media_19 > media_18:
        print(f"   • Melhora {media_19 - media_18:+.2f} acertos/sorteio nos últimos 50")
    else:
        print(f"   • Piora {media_19 - media_18:.2f} acertos/sorteio nos últimos 50")
    
    # Comparar com outros pools
    pool_original = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    pool_13_21 = [1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 15, 16, 18, 19, 20, 21, 23, 25]
    
    perfeitos_original = sum(1 for idx, row in df.iterrows() 
                            if len([n for n in [row[f'Bola{i}'] for i in range(1, 16)] 
                                   if n in pool_original]) == 15)
    
    perfeitos_13_21 = sum(1 for idx, row in df.iterrows() 
                         if len([n for n in [row[f'Bola{i}'] for i in range(1, 16)] 
                                if n in pool_13_21]) == 15)
    
    print("\n" + "=" * 140)
    print("📊 COMPARAÇÃO COM OUTROS POOLS")
    print("=" * 140)
    
    print(f"\n{'Pool':<50} | {'Números':>10} | {'Perfeitos':>12}")
    print("-" * 80)
    print(f"{'Pool Ótimo 18 (sem 21)':<50} | {len(pool_18_otimo):>10} | {len(jogos_perfeitos_18):>12}")
    print(f"{'Pool Ótimo 19 (18 + 21) ← TESTANDO':<50} | {len(pool_19_com_21):>10} | {len(jogos_perfeitos_19):>12}")
    print(f"{'Pool Original (10, 22)':<50} | {len(pool_original):>10} | {perfeitos_original:>12}")
    print(f"{'Pool com 13, 21':<50} | {len(pool_13_21):>10} | {perfeitos_13_21:>12}")
    
    # Salvar relatório
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if len(jogos_perfeitos_19) >= len(jogos_perfeitos_18):
        # Salvar pool de 19 com 21
        pool_path = output_dir / 'pool_19_otimo_com_21.txt'
        with open(pool_path, 'w', encoding='utf-8') as f:
            f.write(','.join(map(str, pool_19_com_21)))
        
        print(f"\n✓ Pool de 19 (com 21) salvo em: {pool_path}")
        
        # Salvar jogos perfeitos
        perfeitos_path = output_dir / 'jogos_perfeitos_pool_19_com_21.txt'
        with open(perfeitos_path, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write(f"JOGOS PERFEITOS COM POOL DE 19 (18 + 21): {len(jogos_perfeitos_19)}\n")
            f.write(f"Pool: {pool_19_com_21}\n")
            f.write("=" * 100 + "\n\n")
            
            for i, jogo in enumerate(jogos_perfeitos_19, 1):
                numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
                tem_21 = "✅ TEM 21" if 21 in jogo['Numeros'] else ""
                f.write(f"{i:2d}. Concurso {jogo['Concurso']} - {jogo['Data']} {tem_21}\n")
                f.write(f"    {numeros_str}\n\n")
        
        print(f"✓ Jogos perfeitos salvos em: {perfeitos_path}")
    
    print("\n" + "=" * 140)
    
    return {
        'pool_19': pool_19_com_21,
        'perfeitos_18': len(jogos_perfeitos_18),
        'perfeitos_19': len(jogos_perfeitos_19),
        'ganho': len(jogos_perfeitos_19) - len(jogos_perfeitos_18)
    }

if __name__ == "__main__":
    resultado = test_pool_18_plus_21()
    
    print(f"\n✅ Análise concluída!")
    print(f"✅ Pool 18 tinha {resultado['perfeitos_18']} jogos perfeitos")
    print(f"✅ Pool 19 (com 21) tem {resultado['perfeitos_19']} jogos perfeitos")
    print(f"✅ Ganho/Perda: {resultado['ganho']:+d} jogos perfeitos")

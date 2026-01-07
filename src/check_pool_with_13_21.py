import pandas as pd
from pathlib import Path

def check_new_pool_with_13_and_21():
    # Pool ORIGINAL de 19 números
    pool_original = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    
    # Pool NOVO (trocando 10→13 e 22→21)
    pool_novo = [1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 15, 16, 18, 19, 20, 21, 23, 25]
    
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    print("=" * 140)
    print("ANÁLISE: NOVO POOL COM TROCAS 10→13 e 22→21")
    print("=" * 140)
    
    print(f"\n📦 POOL ORIGINAL (19 números):")
    print(f"   {pool_original}")
    
    print(f"\n🔄 TROCAS REALIZADAS:")
    print(f"   ❌ SAIU: 10, 22")
    print(f"   ✅ ENTROU: 13, 21")
    
    print(f"\n📦 POOL NOVO (19 números):")
    print(f"   {pool_novo}")
    
    # Analisar jogos perfeitos do pool original
    jogos_perfeitos_original = []
    
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in pool_original])
        
        if acertos == 15:
            jogos_perfeitos_original.append({
                'Concurso': row['Concurso'],
                'Data': row['Data Sorteio'],
                'Numeros': numeros_sorteados
            })
    
    # Analisar jogos perfeitos do pool novo
    jogos_perfeitos_novo = []
    
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in pool_novo])
        
        if acertos == 15:
            jogos_perfeitos_novo.append({
                'Concurso': row['Concurso'],
                'Data': row['Data Sorteio'],
                'Numeros': numeros_sorteados
            })
    
    # Distribuição completa para ambos os pools
    dist_original = {i: 0 for i in range(16)}
    dist_novo = {i: 0 for i in range(16)}
    
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        
        acertos_original = len([n for n in numeros_sorteados if n in pool_original])
        dist_original[acertos_original] += 1
        
        acertos_novo = len([n for n in numeros_sorteados if n in pool_novo])
        dist_novo[acertos_novo] += 1
    
    # Exibir resultados
    print("\n" + "=" * 140)
    print("📊 COMPARAÇÃO DE RESULTADOS")
    print("=" * 140)
    
    print(f"\n{'Métrica':<40} | {'Pool Original':>20} | {'Pool Novo (13,21)':>20} | {'Diferença':>15}")
    print("-" * 140)
    print(f"{'Jogos perfeitos (15 acertos)':<40} | {len(jogos_perfeitos_original):>20} | {len(jogos_perfeitos_novo):>20} | {len(jogos_perfeitos_novo) - len(jogos_perfeitos_original):>+15}")
    print(f"{'Jogos com 14 acertos':<40} | {dist_original[14]:>20} | {dist_novo[14]:>20} | {dist_novo[14] - dist_original[14]:>+15}")
    print(f"{'Jogos com 13 acertos':<40} | {dist_original[13]:>20} | {dist_novo[13]:>20} | {dist_novo[13] - dist_original[13]:>+15}")
    
    total_13_plus_original = dist_original[13] + dist_original[14] + dist_original[15]
    total_13_plus_novo = dist_novo[13] + dist_novo[14] + dist_novo[15]
    
    print(f"{'TOTAL 13+ acertos':<40} | {total_13_plus_original:>20} | {total_13_plus_novo:>20} | {total_13_plus_novo - total_13_plus_original:>+15}")
    
    pct_13_plus_original = (total_13_plus_original / len(df)) * 100
    pct_13_plus_novo = (total_13_plus_novo / len(df)) * 100
    
    print(f"{'% de jogos com 13+ acertos':<40} | {pct_13_plus_original:>19.2f}% | {pct_13_plus_novo:>19.2f}% | {pct_13_plus_novo - pct_13_plus_original:>+14.2f}%")
    
    # Detalhes dos jogos perfeitos do NOVO pool
    print("\n" + "=" * 140)
    print(f"🎯 JOGOS PERFEITOS COM O NOVO POOL (15 ACERTOS): {len(jogos_perfeitos_novo)}")
    print("=" * 140)
    
    if jogos_perfeitos_novo:
        for i, jogo in enumerate(jogos_perfeitos_novo, 1):
            numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
            print(f"\n{i}. Concurso {jogo['Concurso']} - {jogo['Data']}")
            print(f"   Números: {numeros_str}")
            
            # Verificar se 13 ou 21 apareceram
            tem_13 = 13 in jogo['Numeros']
            tem_21 = 21 in jogo['Numeros']
            
            if tem_13 and tem_21:
                print(f"   ✅ Contém ambos: 13 E 21")
            elif tem_13:
                print(f"   ✅ Contém: 13")
            elif tem_21:
                print(f"   ✅ Contém: 21")
    else:
        print("\n❌ NENHUM jogo perfeito encontrado com este pool!")
    
    # Jogos perfeitos PERDIDOS (estavam no original mas não estão no novo)
    concursos_original = {j['Concurso'] for j in jogos_perfeitos_original}
    concursos_novo = {j['Concurso'] for j in jogos_perfeitos_novo}
    
    perdidos = concursos_original - concursos_novo
    ganhos = concursos_novo - concursos_original
    
    print("\n" + "=" * 140)
    print(f"📉 JOGOS PERFEITOS PERDIDOS (estavam no pool original): {len(perdidos)}")
    print("=" * 140)
    
    if perdidos:
        for jogo in jogos_perfeitos_original:
            if jogo['Concurso'] in perdidos:
                numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
                print(f"\n❌ Concurso {jogo['Concurso']} - {jogo['Data']}")
                print(f"   Números: {numeros_str}")
                
                # Mostrar qual número falta
                tem_10 = 10 in jogo['Numeros']
                tem_22 = 22 in jogo['Numeros']
                
                if tem_10 and tem_22:
                    print(f"   Motivo: tinha 10 E 22 (ambos removidos)")
                elif tem_10:
                    print(f"   Motivo: tinha 10 (removido)")
                elif tem_22:
                    print(f"   Motivo: tinha 22 (removido)")
    
    print("\n" + "=" * 140)
    print(f"📈 JOGOS PERFEITOS GANHOS (novos com 13 e/ou 21): {len(ganhos)}")
    print("=" * 140)
    
    if ganhos:
        for jogo in jogos_perfeitos_novo:
            if jogo['Concurso'] in ganhos:
                numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
                print(f"\n✅ Concurso {jogo['Concurso']} - {jogo['Data']}")
                print(f"   Números: {numeros_str}")
                
                tem_13 = 13 in jogo['Numeros']
                tem_21 = 21 in jogo['Numeros']
                
                if tem_13 and tem_21:
                    print(f"   Motivo: tem 13 E 21")
                elif tem_13:
                    print(f"   Motivo: tem 13")
                elif tem_21:
                    print(f"   Motivo: tem 21")
    else:
        print("\n❌ Nenhum jogo perfeito novo adicionado")
    
    # Distribuição completa
    print("\n" + "=" * 140)
    print("📊 DISTRIBUIÇÃO COMPLETA DE ACERTOS")
    print("=" * 140)
    
    print(f"\n{'Acertos':>10} | {'Pool Original':>20} | {'% Original':>15} | {'Pool Novo':>20} | {'% Novo':>15} | {'Diferença':>15}")
    print("-" * 140)
    
    for acertos in range(15, 8, -1):
        pct_orig = (dist_original[acertos] / len(df)) * 100
        pct_novo = (dist_novo[acertos] / len(df)) * 100
        diff = dist_novo[acertos] - dist_original[acertos]
        
        print(f"{acertos:>10} | {dist_original[acertos]:>20} | {pct_orig:>14.2f}% | {dist_novo[acertos]:>20} | {pct_novo:>14.2f}% | {diff:>+15}")
    
    # Análise nos últimos 50
    ultimos_50 = df.tail(50)
    
    total_acertos_original = 0
    total_acertos_novo = 0
    
    for idx, row in ultimos_50.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        total_acertos_original += len([n for n in numeros_sorteados if n in pool_original])
        total_acertos_novo += len([n for n in numeros_sorteados if n in pool_novo])
    
    media_original = total_acertos_original / 50
    media_novo = total_acertos_novo / 50
    
    print("\n" + "=" * 140)
    print("📈 DESEMPENHO NOS ÚLTIMOS 50 SORTEIOS")
    print("=" * 140)
    
    print(f"\nPool Original: {media_original:.2f} acertos por sorteio")
    print(f"Pool Novo:     {media_novo:.2f} acertos por sorteio")
    print(f"Diferença:     {media_novo - media_original:+.2f} acertos por sorteio")
    
    # Recomendação final
    print("\n" + "=" * 140)
    print("🎯 RECOMENDAÇÃO FINAL")
    print("=" * 140)
    
    if len(jogos_perfeitos_novo) > len(jogos_perfeitos_original):
        print(f"\n✅ TROCA VANTAJOSA!")
        print(f"   • Ganha {len(jogos_perfeitos_novo) - len(jogos_perfeitos_original)} jogos perfeitos")
        print(f"   • Total de jogos perfeitos: {len(jogos_perfeitos_novo)} (vs {len(jogos_perfeitos_original)} original)")
    elif len(jogos_perfeitos_novo) < len(jogos_perfeitos_original):
        print(f"\n❌ TROCA DESVANTAJOSA!")
        print(f"   • Perde {len(jogos_perfeitos_original) - len(jogos_perfeitos_novo)} jogos perfeitos")
        print(f"   • Total de jogos perfeitos: {len(jogos_perfeitos_novo)} (vs {len(jogos_perfeitos_original)} original)")
    else:
        print(f"\n⚖️  TROCA NEUTRA")
        print(f"   • Mantém os mesmos {len(jogos_perfeitos_novo)} jogos perfeitos")
    
    if total_13_plus_novo > total_13_plus_original:
        print(f"   • Ganha {total_13_plus_novo - total_13_plus_original} jogos com 13+ acertos")
    elif total_13_plus_novo < total_13_plus_original:
        print(f"   • Perde {total_13_plus_original - total_13_plus_novo} jogos com 13+ acertos")
    
    if media_novo > media_original:
        print(f"   • Melhora {media_novo - media_original:+.2f} acertos/sorteio nos últimos 50")
    else:
        print(f"   • Piora {media_novo - media_original:.2f} acertos/sorteio nos últimos 50")
    
    # Salvar relatórios
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvar novo pool
    pool_path = output_dir / 'pool_19_com_13_e_21.txt'
    with open(pool_path, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, pool_novo)))
    
    print(f"\n✓ Novo pool salvo em: {pool_path}")
    
    # Salvar jogos perfeitos
    if jogos_perfeitos_novo:
        perfeitos_path = output_dir / 'jogos_perfeitos_pool_13_21.txt'
        with open(perfeitos_path, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write(f"JOGOS PERFEITOS COM POOL [13, 21]: {len(jogos_perfeitos_novo)}\n")
            f.write("=" * 100 + "\n\n")
            
            for i, jogo in enumerate(jogos_perfeitos_novo, 1):
                numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
                f.write(f"{i}. Concurso {jogo['Concurso']} - {jogo['Data']}\n")
                f.write(f"   {numeros_str}\n\n")
        
        print(f"✓ Jogos perfeitos salvos em: {perfeitos_path}")
    
    # Relatório comparativo
    report_path = output_dir / 'comparacao_pool_13_21.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("COMPARAÇÃO: POOL ORIGINAL vs POOL COM 13 E 21\n")
        f.write("=" * 100 + "\n\n")
        
        f.write(f"Pool Original: {pool_original}\n")
        f.write(f"Pool Novo:     {pool_novo}\n\n")
        
        f.write(f"Jogos perfeitos (15): {len(jogos_perfeitos_original)} → {len(jogos_perfeitos_novo)} ({len(jogos_perfeitos_novo) - len(jogos_perfeitos_original):+d})\n")
        f.write(f"Jogos 14 acertos: {dist_original[14]} → {dist_novo[14]} ({dist_novo[14] - dist_original[14]:+d})\n")
        f.write(f"Jogos 13 acertos: {dist_original[13]} → {dist_novo[13]} ({dist_novo[13] - dist_original[13]:+d})\n")
        f.write(f"Total 13+: {total_13_plus_original} → {total_13_plus_novo} ({total_13_plus_novo - total_13_plus_original:+d})\n")
        f.write(f"Média últimos 50: {media_original:.2f} → {media_novo:.2f} ({media_novo - media_original:+.2f})\n")
    
    print(f"✓ Relatório comparativo salvo em: {report_path}")
    
    print("\n" + "=" * 140)
    
    return {
        'pool_novo': pool_novo,
        'jogos_perfeitos': len(jogos_perfeitos_novo),
        'total_13_plus': total_13_plus_novo,
        'media_50': media_novo
    }

if __name__ == "__main__":
    resultado = check_new_pool_with_13_and_21()
    
    print(f"\n✅ Análise concluída!")
    print(f"✅ Pool novo tem {resultado['jogos_perfeitos']} jogos perfeitos")
    print(f"✅ Total de 13+ acertos: {resultado['total_13_plus']}")
    print(f"✅ Média últimos 50: {resultado['media_50']:.2f}")

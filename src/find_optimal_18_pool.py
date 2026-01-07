import pandas as pd
import numpy as np
from pathlib import Path
from itertools import combinations

def find_optimal_18_pool():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    print("=" * 140)
    print("BUSCA PELO POOL ÓTIMO DE 18 NÚMEROS (MÁXIMO DE JOGOS PERFEITOS)")
    print("=" * 140)
    print(f"\nTotal de sorteios históricos: {len(df)}")
    
    # ETAPA 1: Encontrar TODOS os jogos perfeitos possíveis (testando pools)
    # Como temos 25 números, vamos analisar a frequência de cada número nos sorteios históricos
    
    print("\n" + "=" * 140)
    print("ETAPA 1: ANALISANDO FREQUÊNCIA DE CADA NÚMERO EM JOGOS PERFEITOS POTENCIAIS")
    print("=" * 140)
    
    # Para cada sorteio, os 15 números que saíram são um "jogo perfeito" potencial
    # Vamos contar quantas vezes cada número apareceu em sorteios
    
    freq_em_sorteios = {}
    
    for numero in range(1, 26):
        count = 0
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                count += 1
        
        freq_em_sorteios[numero] = count
    
    # Ordenar números por frequência
    numeros_ordenados = sorted(freq_em_sorteios.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nFREQUÊNCIA DE CADA NÚMERO NOS {len(df)} SORTEIOS:")
    print(f"\n{'Rank':>5} | {'Número':>8} | {'Aparições':>12} | {'Frequência':>12}")
    print("-" * 50)
    
    for rank, (numero, count) in enumerate(numeros_ordenados, 1):
        freq_pct = (count / len(df)) * 100
        destaque = "👉" if rank <= 18 else "  "
        print(f"{destaque}{rank:4d} | {numero:8d} | {count:12d} | {freq_pct:11.2f}%")
    
    # ETAPA 2: Selecionar top 18 números
    print("\n" + "=" * 140)
    print("ETAPA 2: SELECIONANDO TOP 18 NÚMEROS MAIS FREQUENTES")
    print("=" * 140)
    
    top_18_numeros = [num for num, _ in numeros_ordenados[:18]]
    top_18_numeros.sort()
    
    print(f"\n📦 POOL DE 18 NÚMEROS (mais frequentes):")
    print(f"   {top_18_numeros}")
    
    # ETAPA 3: Validar quantos jogos perfeitos este pool geraria
    print("\n" + "=" * 140)
    print("ETAPA 3: VALIDANDO JOGOS PERFEITOS COM ESTE POOL")
    print("=" * 140)
    
    jogos_perfeitos = []
    
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in top_18_numeros])
        
        if acertos == 15:
            jogos_perfeitos.append({
                'Concurso': row['Concurso'],
                'Data': row['Data Sorteio'],
                'Numeros': numeros_sorteados
            })
    
    print(f"\n🎯 JOGOS PERFEITOS ENCONTRADOS: {len(jogos_perfeitos)}")
    
    if jogos_perfeitos:
        print(f"\nDETALHES DOS JOGOS PERFEITOS:\n")
        for i, jogo in enumerate(jogos_perfeitos, 1):
            numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
            print(f"{i:2d}. Concurso {jogo['Concurso']} - {jogo['Data']}")
            print(f"    {numeros_str}")
    
    # ETAPA 4: Distribuição de acertos
    print("\n" + "=" * 140)
    print("ETAPA 4: DISTRIBUIÇÃO DE ACERTOS COM ESTE POOL")
    print("=" * 140)
    
    distribuicao = {i: 0 for i in range(16)}
    
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in top_18_numeros])
        distribuicao[acertos] += 1
    
    print(f"\n{'Acertos':>10} | {'Quantidade':>15} | {'Percentual':>15}")
    print("-" * 45)
    
    for acertos in range(15, 8, -1):
        pct = (distribuicao[acertos] / len(df)) * 100
        print(f"{acertos:>10} | {distribuicao[acertos]:>15} | {pct:>14.2f}%")
    
    total_13_plus = distribuicao[13] + distribuicao[14] + distribuicao[15]
    pct_13_plus = (total_13_plus / len(df)) * 100
    
    print("-" * 45)
    print(f"{'13+ total':>10} | {total_13_plus:>15} | {pct_13_plus:>14.2f}%")
    
    # ETAPA 5: Testar variações (remover 1 dos 18 e adicionar outro dos 7 restantes)
    print("\n" + "=" * 140)
    print("ETAPA 5: TESTANDO VARIAÇÕES (TROCAR 1 NÚMERO DOS 18)")
    print("=" * 140)
    
    numeros_fora = [num for num, _ in numeros_ordenados[18:]]
    
    print(f"\nNúmeros FORA do top 18: {numeros_fora}")
    print(f"\nTestando se alguma troca melhora o resultado...\n")
    
    melhor_pool = top_18_numeros.copy()
    melhor_perfeitos = len(jogos_perfeitos)
    
    melhores_alternativas = []
    
    for num_remover in top_18_numeros:
        for num_adicionar in numeros_fora:
            pool_teste = [n for n in top_18_numeros if n != num_remover]
            pool_teste.append(num_adicionar)
            pool_teste.sort()
            
            # Contar perfeitos
            count_perfeitos = 0
            for idx, row in df.iterrows():
                numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
                acertos = len([n for n in numeros_sorteados if n in pool_teste])
                if acertos == 15:
                    count_perfeitos += 1
            
            if count_perfeitos > melhor_perfeitos:
                melhor_perfeitos = count_perfeitos
                melhor_pool = pool_teste.copy()
                melhores_alternativas.append({
                    'pool': pool_teste.copy(),
                    'perfeitos': count_perfeitos,
                    'troca': f"Remover {num_remover}, Adicionar {num_adicionar}"
                })
                print(f"✅ MELHORIA ENCONTRADA: {count_perfeitos} perfeitos")
                print(f"   Troca: Remover {num_remover}, Adicionar {num_adicionar}")
                print(f"   Novo pool: {pool_teste}\n")
    
    if not melhores_alternativas:
        print("✅ Nenhuma troca simples melhora o resultado!")
        print("   O pool top 18 por frequência já é ótimo.\n")
    
    # ETAPA 6: Análise nos últimos 50 sorteios
    print("\n" + "=" * 140)
    print("ETAPA 6: DESEMPENHO NOS ÚLTIMOS 50 SORTEIOS")
    print("=" * 140)
    
    ultimos_50 = df.tail(50)
    
    total_acertos = 0
    for idx, row in ultimos_50.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        total_acertos += len([n for n in numeros_sorteados if n in melhor_pool])
    
    media_50 = total_acertos / 50
    
    print(f"\nMédia de acertos nos últimos 50: {media_50:.2f} de 15")
    print(f"Percentual de cobertura: {(media_50/15)*100:.1f}%")
    
    # Comparar com nossos pools anteriores
    pool_original = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    pool_13_21 = [1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 15, 16, 18, 19, 20, 21, 23, 25]
    
    # Contar perfeitos dos pools anteriores
    perfeitos_original = 0
    perfeitos_13_21 = 0
    
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        
        if len([n for n in numeros_sorteados if n in pool_original]) == 15:
            perfeitos_original += 1
        
        if len([n for n in numeros_sorteados if n in pool_13_21]) == 15:
            perfeitos_13_21 += 1
    
    print("\n" + "=" * 140)
    print("📊 COMPARAÇÃO COM POOLS ANTERIORES")
    print("=" * 140)
    
    print(f"\n{'Pool':<40} | {'Números':>10} | {'Perfeitos':>12} | {'% Melhor':>12}")
    print("-" * 80)
    print(f"{'Pool ÓTIMO (mais frequentes)':<40} | {len(melhor_pool):>10} | {melhor_perfeitos:>12} | {'-':>12}")
    print(f"{'Pool Original (10, 22)':<40} | {len(pool_original):>10} | {perfeitos_original:>12} | {((perfeitos_original/melhor_perfeitos)*100 - 100):>+11.1f}%")
    print(f"{'Pool com 13, 21':<40} | {len(pool_13_21):>10} | {perfeitos_13_21:>12} | {((perfeitos_13_21/melhor_perfeitos)*100 - 100):>+11.1f}%")
    
    # RECOMENDAÇÃO FINAL
    print("\n" + "=" * 140)
    print("🎯 POOL ÓTIMO FINAL - MÁXIMO DE JOGOS PERFEITOS")
    print("=" * 140)
    
    print(f"\n📦 POOL RECOMENDADO ({len(melhor_pool)} números):")
    print(f"   {melhor_pool}")
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Jogos perfeitos (15 acertos): {melhor_perfeitos}")
    print(f"   • Jogos com 14+ acertos: {distribuicao[14] + distribuicao[15]}")
    print(f"   • Jogos com 13+ acertos: {total_13_plus} ({pct_13_plus:.2f}%)")
    print(f"   • Média últimos 50 sorteios: {media_50:.2f} de 15")
    
    # Identificar os 7 números que ficaram de fora
    numeros_fora_final = [n for n in range(1, 26) if n not in melhor_pool]
    
    print(f"\n❌ Números EXCLUÍDOS (7):")
    print(f"   {numeros_fora_final}")
    
    for num in numeros_fora_final:
        freq = freq_em_sorteios[num]
        freq_pct = (freq / len(df)) * 100
        print(f"   • {num:2d}: {freq:4d} aparições ({freq_pct:.2f}%)")
    
    # Salvar resultados
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvar pool ótimo
    pool_path = output_dir / 'pool_otimo_18_numeros.txt'
    with open(pool_path, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, melhor_pool)))
    
    print(f"\n✓ Pool ótimo salvo em: {pool_path}")
    
    # Salvar jogos perfeitos
    if jogos_perfeitos:
        perfeitos_path = output_dir / 'jogos_perfeitos_pool_otimo.txt'
        with open(perfeitos_path, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write(f"JOGOS PERFEITOS COM POOL ÓTIMO: {len(jogos_perfeitos)}\n")
            f.write(f"Pool: {melhor_pool}\n")
            f.write("=" * 100 + "\n\n")
            
            for i, jogo in enumerate(jogos_perfeitos, 1):
                numeros_str = ','.join([f"{n:02d}" for n in jogo['Numeros']])
                f.write(f"{i:2d}. Concurso {jogo['Concurso']} - {jogo['Data']}\n")
                f.write(f"    {numeros_str}\n\n")
        
        print(f"✓ Jogos perfeitos salvos em: {perfeitos_path}")
    
    # Relatório completo
    report_path = output_dir / 'analise_pool_otimo.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("POOL ÓTIMO DE 18 NÚMEROS - MÁXIMO DE JOGOS PERFEITOS\n")
        f.write("=" * 100 + "\n\n")
        
        f.write(f"Pool: {melhor_pool}\n\n")
        
        f.write(f"Jogos perfeitos (15): {melhor_perfeitos}\n")
        f.write(f"Jogos 14 acertos: {distribuicao[14]}\n")
        f.write(f"Jogos 13 acertos: {distribuicao[13]}\n")
        f.write(f"Total 13+: {total_13_plus} ({pct_13_plus:.2f}%)\n")
        f.write(f"Média últimos 50: {media_50:.2f}\n\n")
        
        f.write(f"Números excluídos: {numeros_fora_final}\n\n")
        
        f.write("COMPARAÇÃO:\n")
        f.write(f"Pool ótimo:        {melhor_perfeitos} perfeitos\n")
        f.write(f"Pool original:     {perfeitos_original} perfeitos\n")
        f.write(f"Pool com 13, 21:   {perfeitos_13_21} perfeitos\n")
    
    print(f"✓ Relatório completo salvo em: {report_path}")
    
    print("\n" + "=" * 140)
    
    return {
        'pool': melhor_pool,
        'perfeitos': melhor_perfeitos,
        'total_13_plus': total_13_plus,
        'media_50': media_50
    }

if __name__ == "__main__":
    resultado = find_optimal_18_pool()
    
    print(f"\n✅ Análise concluída!")
    print(f"✅ Pool ótimo tem {resultado['perfeitos']} jogos perfeitos")
    print(f"✅ Total de 13+ acertos: {resultado['total_13_plus']}")
    print(f"✅ Média últimos 50: {resultado['media_50']:.2f}")

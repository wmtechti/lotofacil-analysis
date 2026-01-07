import pandas as pd
from pathlib import Path

def select_4_complementary_numbers():
    # Base de 11 números
    numeros_base = [1, 2, 3, 4, 5, 9, 12, 15, 18, 19, 22]
    
    # 7 números exclusivamente frios (não estão nos quentes)
    frios_exclusivos = [6, 7, 8, 16, 17, 21, 23]
    
    # 7 números exclusivamente quentes (não estão nos frios)
    quentes_exclusivos = [10, 11, 13, 14, 20, 24, 25]
    
    # Carregar dados históricos
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    total_sorteios = len(df)
    ultimos_50 = df.tail(50)
    
    print("=" * 100)
    print("SELEÇÃO DOS 4 NÚMEROS COMPLEMENTARES (2 FRIOS + 2 QUENTES)")
    print("=" * 100)
    
    # Analisar frequência dos 7 frios exclusivos
    print("\n" + "=" * 100)
    print("ANÁLISE DOS 7 NÚMEROS EXCLUSIVAMENTE FRIOS")
    print("-" * 100)
    
    freq_frios = {}
    freq_frios_50 = {}
    
    for numero in frios_exclusivos:
        # Histórico completo
        count = sum(1 for idx, row in df.iterrows() 
                   if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_frios[numero] = count
        
        # Últimos 50
        count_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                      if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_frios_50[numero] = count_50
    
    print(f"\n{'Número':>8} | {'Histórico':>11} | {'Freq %':>9} | {'Últ. 50':>9} | {'Freq %':>9}")
    print("-" * 65)
    
    for numero in sorted(frios_exclusivos, key=lambda x: freq_frios[x]):
        hist = freq_frios[numero]
        hist_pct = (hist / total_sorteios) * 100
        ult50 = freq_frios_50[numero]
        ult50_pct = (ult50 / 50) * 100
        print(f"{numero:8d} | {hist:11d} | {hist_pct:8.2f}% | {ult50:9d} | {ult50_pct:8.1f}%")
    
    # Selecionar os 2 mais frios
    dois_mais_frios = sorted(frios_exclusivos, key=lambda x: freq_frios[x])[:2]
    
    print(f"\n✅ 2 MAIS FRIOS selecionados: {dois_mais_frios}")
    
    # Analisar frequência dos 7 quentes exclusivos
    print("\n" + "=" * 100)
    print("ANÁLISE DOS 7 NÚMEROS EXCLUSIVAMENTE QUENTES")
    print("-" * 100)
    
    freq_quentes = {}
    freq_quentes_50 = {}
    
    for numero in quentes_exclusivos:
        # Histórico completo
        count = sum(1 for idx, row in df.iterrows() 
                   if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_quentes[numero] = count
        
        # Últimos 50
        count_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                      if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_quentes_50[numero] = count_50
    
    print(f"\n{'Número':>8} | {'Histórico':>11} | {'Freq %':>9} | {'Últ. 50':>9} | {'Freq %':>9}")
    print("-" * 65)
    
    for numero in sorted(quentes_exclusivos, key=lambda x: freq_quentes[x], reverse=True):
        hist = freq_quentes[numero]
        hist_pct = (hist / total_sorteios) * 100
        ult50 = freq_quentes_50[numero]
        ult50_pct = (ult50 / 50) * 100
        print(f"{numero:8d} | {hist:11d} | {hist_pct:8.2f}% | {ult50:9d} | {ult50_pct:8.1f}%")
    
    # Selecionar os 2 mais quentes
    dois_mais_quentes = sorted(quentes_exclusivos, key=lambda x: freq_quentes[x], reverse=True)[:2]
    
    print(f"\n✅ 2 MAIS QUENTES selecionados: {dois_mais_quentes}")
    
    # Pool final de 15 números
    pool_final_15 = sorted(numeros_base + dois_mais_frios + dois_mais_quentes)
    
    print("\n" + "=" * 100)
    print("POOL FINAL DE 15 NÚMEROS PARA ESTRATÉGIA")
    print("=" * 100)
    
    print(f"\n🎯 BASE (11 números): {numeros_base}")
    print(f"❄️  2 FRIOS: {dois_mais_frios}")
    print(f"🔥 2 QUENTES: {dois_mais_quentes}")
    
    print(f"\n📦 POOL COMPLETO (15 números):")
    print(f"   {pool_final_15}")
    
    # Análise de paridade do pool final
    pares_final = [n for n in pool_final_15 if n % 2 == 0]
    impares_final = [n for n in pool_final_15 if n % 2 != 0]
    
    print(f"\n📊 Características do Pool Final:")
    print(f"   Pares: {len(pares_final)} → {pares_final}")
    print(f"   Ímpares: {len(impares_final)} → {impares_final}")
    
    # Distribuição por dezena
    dezenas_final = {
        '01-05': [n for n in pool_final_15 if 1 <= n <= 5],
        '06-10': [n for n in pool_final_15 if 6 <= n <= 10],
        '11-15': [n for n in pool_final_15 if 11 <= n <= 15],
        '16-20': [n for n in pool_final_15 if 16 <= n <= 20],
        '21-25': [n for n in pool_final_15 if 21 <= n <= 25]
    }
    
    print(f"\n   Distribuição por Dezena:")
    for dezena, nums in dezenas_final.items():
        print(f"     {dezena}: {len(nums)} números → {nums if nums else 'nenhum'}")
    
    # Performance nos últimos 50
    print("\n" + "=" * 100)
    print("PERFORMANCE DO POOL FINAL NOS ÚLTIMOS 50 SORTEIOS")
    print("-" * 100)
    
    acertos_por_sorteio = []
    
    for idx, row in ultimos_50.iterrows():
        concurso = row['Concurso']
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in pool_final_15])
        acertos_por_sorteio.append(acertos)
    
    print(f"\nAcertos por sorteio:")
    print(f"  Mínimo: {min(acertos_por_sorteio)} de 15")
    print(f"  Máximo: {max(acertos_por_sorteio)} de 15")
    print(f"  Média: {sum(acertos_por_sorteio)/len(acertos_por_sorteio):.2f} de 15")
    print(f"  Taxa de cobertura: {(sum(acertos_por_sorteio)/len(acertos_por_sorteio)/15)*100:.1f}%")
    
    # Contar sorteios com 15 acertos (jogo perfeito)
    sorteios_15 = sum(1 for a in acertos_por_sorteio if a == 15)
    sorteios_14 = sum(1 for a in acertos_por_sorteio if a == 14)
    sorteios_13 = sum(1 for a in acertos_por_sorteio if a == 13)
    
    print(f"\n  Sorteios com 15 acertos: {sorteios_15} ({(sorteios_15/50)*100:.1f}%)")
    print(f"  Sorteios com 14 acertos: {sorteios_14} ({(sorteios_14/50)*100:.1f}%)")
    print(f"  Sorteios com 13 acertos: {sorteios_13} ({(sorteios_13/50)*100:.1f}%)")
    
    # Salvar resultado
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'pool_final_15_numeros.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("POOL FINAL DE 15 NÚMEROS - ESTRATÉGIA BALANCEADA\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"BASE (11 números): {numeros_base}\n")
        f.write(f"2 MAIS FRIOS: {dois_mais_frios}\n")
        f.write(f"2 MAIS QUENTES: {dois_mais_quentes}\n\n")
        f.write(f"POOL COMPLETO: {pool_final_15}\n\n")
        f.write("=" * 100 + "\n\n")
        f.write("CARACTERÍSTICAS:\n\n")
        f.write(f"Pares: {len(pares_final)} → {pares_final}\n")
        f.write(f"Ímpares: {len(impares_final)} → {impares_final}\n\n")
        f.write("Distribuição por Dezena:\n")
        for dezena, nums in dezenas_final.items():
            f.write(f"  {dezena}: {len(nums)} números → {nums if nums else 'nenhum'}\n")
        f.write("\n" + "=" * 100 + "\n\n")
        f.write("PERFORMANCE ÚLTIMOS 50 SORTEIOS:\n\n")
        f.write(f"Média de acertos: {sum(acertos_por_sorteio)/len(acertos_por_sorteio):.2f} de 15\n")
        f.write(f"Taxa de cobertura: {(sum(acertos_por_sorteio)/len(acertos_por_sorteio)/15)*100:.1f}%\n")
        f.write(f"Sorteios com 15 acertos: {sorteios_15}\n")
        f.write(f"Sorteios com 14 acertos: {sorteios_14}\n")
        f.write(f"Sorteios com 13 acertos: {sorteios_13}\n")
    
    print(f"\n✓ Relatório salvo em: {report_path}")
    
    # Salvar pool em formato simples
    pool_path = output_dir / 'pool_15_numeros.txt'
    with open(pool_path, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, pool_final_15)))
    
    print(f"✓ Pool salvo em: {pool_path}")
    
    print("\n" + "=" * 100)
    print("RESUMO FINAL")
    print("=" * 100)
    print(f"\n✅ Pool de 15 números pronto para gerar jogos: {pool_final_15}")
    print(f"✅ Cobertura média nos últimos 50: {(sum(acertos_por_sorteio)/len(acertos_por_sorteio)/15)*100:.1f}%")
    print(f"✅ Paridade: {len(pares_final)} pares / {len(impares_final)} ímpares")
    print("=" * 100)
    
    return {
        'pool_final': pool_final_15,
        'base': numeros_base,
        'frios': dois_mais_frios,
        'quentes': dois_mais_quentes
    }

if __name__ == "__main__":
    resultado = select_4_complementary_numbers()

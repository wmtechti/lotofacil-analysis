import pandas as pd
from pathlib import Path

def analyze_specific_numbers():
    # Números para análise
    numeros_analise = [10, 13, 21]
    
    # Pools definidos
    numeros_base = [1, 2, 3, 4, 5, 9, 12, 15, 18, 19, 22]
    frios_exclusivos = [6, 7, 8, 16, 17, 21, 23]
    quentes_exclusivos = [10, 11, 13, 14, 20, 24, 25]
    pool_18_atual = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    
    # Carregar dados
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    total_sorteios = len(df)
    ultimos_50 = df.tail(50)
    ultimos_100 = df.tail(100)
    
    print("=" * 100)
    print("ANÁLISE DETALHADA DOS NÚMEROS: 10, 13 e 21")
    print("=" * 100)
    
    # Para cada número
    for numero in numeros_analise:
        print("\n" + "=" * 100)
        print(f"NÚMERO {numero}")
        print("=" * 100)
        
        # Classificação
        if numero in numeros_base:
            classificacao = "🎯 BASE (aparece em frios E quentes)"
        elif numero in frios_exclusivos:
            classificacao = "❄️ EXCLUSIVAMENTE FRIO"
        elif numero in quentes_exclusivos:
            classificacao = "🔥 EXCLUSIVAMENTE QUENTE"
        else:
            classificacao = "❓ Não classificado"
        
        print(f"\nClassificação: {classificacao}")
        
        if numero in pool_18_atual:
            print(f"✅ INCLUÍDO no pool de 18 números")
        else:
            print(f"❌ NÃO INCLUÍDO no pool de 18 números")
        
        # Frequência histórica
        aparicoes_hist = sum(1 for idx, row in df.iterrows() 
                            if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_hist_pct = (aparicoes_hist / total_sorteios) * 100
        
        # Frequência últimos 100
        aparicoes_100 = sum(1 for idx, row in ultimos_100.iterrows() 
                           if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_100_pct = (aparicoes_100 / 100) * 100
        
        # Frequência últimos 50
        aparicoes_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                          if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_50_pct = (aparicoes_50 / 50) * 100
        
        print(f"\n📊 FREQUÊNCIA:")
        print(f"   Histórico completo ({total_sorteios} sorteios): {aparicoes_hist} aparições ({freq_hist_pct:.2f}%)")
        print(f"   Últimos 100 sorteios: {aparicoes_100} aparições ({freq_100_pct:.1f}%)")
        print(f"   Últimos 50 sorteios: {aparicoes_50} aparições ({freq_50_pct:.1f}%)")
        
        # Desvio
        esperado = total_sorteios * 0.6  # 60% é o esperado
        desvio = ((aparicoes_hist - esperado) / esperado) * 100
        
        if desvio > 0:
            status_temp = f"🔥 Acima da média (+{desvio:.2f}%)"
        else:
            status_temp = f"❄️ Abaixo da média ({desvio:.2f}%)"
        
        print(f"   Desvio histórico: {status_temp}")
        
        # Tendência recente
        tendencia_100_vs_hist = freq_100_pct - freq_hist_pct
        tendencia_50_vs_100 = freq_50_pct - freq_100_pct
        
        print(f"\n📈 TENDÊNCIA:")
        if tendencia_50_vs_100 > 5:
            print(f"   Últimos 50 vs 100: 🔥🔥 ESQUENTANDO (+{tendencia_50_vs_100:.1f} pp)")
        elif tendencia_50_vs_100 > 2:
            print(f"   Últimos 50 vs 100: 🔥 Aquecendo (+{tendencia_50_vs_100:.1f} pp)")
        elif tendencia_50_vs_100 < -5:
            print(f"   Últimos 50 vs 100: ❄️❄️ ESFRIANDO ({tendencia_50_vs_100:.1f} pp)")
        elif tendencia_50_vs_100 < -2:
            print(f"   Últimos 50 vs 100: ❄️ Resfriando ({tendencia_50_vs_100:.1f} pp)")
        else:
            print(f"   Últimos 50 vs 100: 😐 Estável ({tendencia_50_vs_100:+.1f} pp)")
        
        # Análise de gaps (últimos 50)
        gaps = []
        ultimo_aparecimento = -1
        
        for i, (idx, row) in enumerate(ultimos_50.iterrows()):
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                if ultimo_aparecimento >= 0:
                    gap = i - ultimo_aparecimento
                    gaps.append(gap)
                ultimo_aparecimento = i
        
        if gaps:
            gap_medio = sum(gaps) / len(gaps)
            gap_minimo = min(gaps)
            gap_maximo = max(gaps)
            
            print(f"\n⏱️ CICLOS (últimos 50 sorteios):")
            print(f"   Gap médio entre aparições: {gap_medio:.2f} sorteios")
            print(f"   Gap mínimo: {gap_minimo} sorteios")
            print(f"   Gap máximo: {gap_maximo} sorteios")
            
            # Último gap
            sorteios_desde_ultima = 49 - ultimo_aparecimento if ultimo_aparecimento >= 0 else 50
            print(f"   Sorteios desde última aparição: {sorteios_desde_ultima}")
            
            if sorteios_desde_ultima > gap_medio * 1.5:
                print(f"   ⚠️ ALERTA: Está {sorteios_desde_ultima - gap_medio:.1f} sorteios acima do gap médio!")
            elif sorteios_desde_ultima <= gap_medio * 0.5:
                print(f"   ✅ Apareceu recentemente (abaixo do gap médio)")
        
        # Últimas 10 aparições
        ultimas_aparicoes = []
        for i, (idx, row) in enumerate(ultimos_50.iterrows()):
            concurso = row['Concurso']
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                ultimas_aparicoes.append(concurso)
        
        print(f"\n🎯 ÚLTIMAS APARIÇÕES (últimos 50 sorteios):")
        if ultimas_aparicoes:
            print(f"   Total: {len(ultimas_aparicoes)} vezes")
            print(f"   Concursos: {ultimas_aparicoes[:10] if len(ultimas_aparicoes) >= 10 else ultimas_aparicoes}")
        else:
            print(f"   ⚠️ NÃO APARECEU nos últimos 50 sorteios!")
        
        # Paridade
        paridade = "PAR" if numero % 2 == 0 else "ÍMPAR"
        print(f"\n🔢 CARACTERÍSTICAS:")
        print(f"   Paridade: {paridade}")
        print(f"   Dezena: {((numero-1)//5)*5 + 1}-{((numero-1)//5 + 1)*5}")
    
    # Comparação entre os 3
    print("\n" + "=" * 100)
    print("COMPARAÇÃO ENTRE OS 3 NÚMEROS")
    print("=" * 100)
    
    print(f"\n{'Número':>8} | {'Classificação':>25} | {'No Pool 18':>12} | {'Hist %':>9} | {'Últ.50':>9} | {'Tendência':>15}")
    print("-" * 100)
    
    for numero in numeros_analise:
        if numero in numeros_base:
            classif = "BASE"
        elif numero in frios_exclusivos:
            classif = "FRIO EXCLUSIVO"
        elif numero in quentes_exclusivos:
            classif = "QUENTE EXCLUSIVO"
        else:
            classif = "Outro"
        
        no_pool = "✅ SIM" if numero in pool_18_atual else "❌ NÃO"
        
        aparicoes_hist = sum(1 for idx, row in df.iterrows() 
                            if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_hist_pct = (aparicoes_hist / total_sorteios) * 100
        
        aparicoes_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                          if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        
        aparicoes_100 = sum(1 for idx, row in ultimos_100.iterrows() 
                           if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_100_pct = (aparicoes_100 / 100) * 100
        freq_50_pct = (aparicoes_50 / 50) * 100
        
        tendencia = freq_50_pct - freq_100_pct
        if tendencia > 5:
            tend_str = "🔥🔥 Esquentando"
        elif tendencia > 0:
            tend_str = "🔥 Aquecendo"
        elif tendencia < -5:
            tend_str = "❄️❄️ Esfriando"
        elif tendencia < 0:
            tend_str = "❄️ Resfriando"
        else:
            tend_str = "😐 Estável"
        
        print(f"{numero:8d} | {classif:>25} | {no_pool:>12} | {freq_hist_pct:8.2f}% | {aparicoes_50:9d} | {tend_str:>15}")
    
    # Recomendação
    print("\n" + "=" * 100)
    print("RECOMENDAÇÕES")
    print("=" * 100)
    
    print("\n🔟 NÚMERO 10:")
    aparicoes_10 = sum(1 for idx, row in ultimos_50.iterrows() 
                      if 10 in [row[f'Bola{i}'] for i in range(1, 16)])
    if 10 in pool_18_atual:
        print(f"   ✅ JÁ INCLUÍDO no pool de 18")
        print(f"   • Classificação: 🔥 Quente exclusivo")
        print(f"   • Performance recente: {aparicoes_10} aparições em 50 sorteios ({(aparicoes_10/50)*100:.1f}%)")
        print(f"   • Recomendação: MANTER no pool")
    
    print("\n1️⃣3️⃣ NÚMERO 13:")
    aparicoes_13 = sum(1 for idx, row in ultimos_50.iterrows() 
                      if 13 in [row[f'Bola{i}'] for i in range(1, 16)])
    if 13 not in pool_18_atual:
        print(f"   ❌ NÃO INCLUÍDO no pool de 18")
        print(f"   • Classificação: 🔥 Quente exclusivo")
        print(f"   • Performance recente: {aparicoes_13} aparições em 50 sorteios ({(aparicoes_13/50)*100:.1f}%)")
        print(f"   • Está na lista de quentes restantes (posição 3 de 5)")
        if aparicoes_13 >= 30:
            print(f"   • Recomendação: ⚠️ CONSIDERAR INCLUIR (performance alta)")
        else:
            print(f"   • Recomendação: OK manter fora (performance moderada)")
    
    print("\n2️⃣1️⃣ NÚMERO 21:")
    aparicoes_21 = sum(1 for idx, row in ultimos_50.iterrows() 
                      if 21 in [row[f'Bola{i}'] for i in range(1, 16)])
    if 21 not in pool_18_atual:
        print(f"   ❌ NÃO INCLUÍDO no pool de 18")
        print(f"   • Classificação: ❄️ Frio exclusivo")
        print(f"   • Performance recente: {aparicoes_21} aparições em 50 sorteios ({(aparicoes_21/50)*100:.1f}%)")
        print(f"   • Frequência histórica: 59,36% (5º mais frio)")
        if aparicoes_21 <= 20:
            print(f"   • Recomendação: OK manter fora (performance baixa)")
        else:
            print(f"   • Recomendação: CONSIDERAR se quiser mais equilíbrio")
    
    # Salvar relatório
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'analise_numeros_10_13_21.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("ANÁLISE DETALHADA DOS NÚMEROS: 10, 13 e 21\n")
        f.write("=" * 100 + "\n\n")
        
        for numero in numeros_analise:
            aparicoes_hist = sum(1 for idx, row in df.iterrows() 
                                if numero in [row[f'Bola{i}'] for i in range(1, 16)])
            freq_hist_pct = (aparicoes_hist / total_sorteios) * 100
            
            aparicoes_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                              if numero in [row[f'Bola{i}'] for i in range(1, 16)])
            freq_50_pct = (aparicoes_50 / 50) * 100
            
            f.write(f"\nNÚMERO {numero}:\n")
            f.write(f"  Histórico: {aparicoes_hist} aparições ({freq_hist_pct:.2f}%)\n")
            f.write(f"  Últimos 50: {aparicoes_50} aparições ({freq_50_pct:.1f}%)\n")
            
            if numero in pool_18_atual:
                f.write(f"  Status: INCLUÍDO no pool de 18\n")
            else:
                f.write(f"  Status: NÃO INCLUÍDO no pool de 18\n")
            
            f.write("\n")
    
    print(f"\n✓ Relatório salvo em: {report_path}")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    analyze_specific_numbers()

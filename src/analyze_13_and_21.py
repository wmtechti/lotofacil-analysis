import pandas as pd
import numpy as np
from pathlib import Path

def analyze_numbers_13_and_21():
    # Números para análise (não estão no pool de 19)
    numeros_analise = [13, 21]
    
    # Pool atual de 19 para comparação
    pool_19 = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    ultimos_50 = df.tail(50)
    
    ultimo_concurso = df.iloc[-1]['Concurso']
    
    print("=" * 140)
    print("ANÁLISE DETALHADA: NÚMEROS 13 e 21 (NÃO INCLUÍDOS NO POOL)")
    print("=" * 140)
    print(f"\nÚltimo concurso: {ultimo_concurso}")
    print(f"Pool atual de 19 números: {pool_19}")
    print(f"Números a analisar: {numeros_analise} (FORA do pool)\n")
    
    resultados = []
    
    for numero in numeros_analise:
        print("=" * 140)
        print(f"🔢 NÚMERO {numero}")
        print("=" * 140)
        
        # Encontrar todas as aparições
        aparicoes = []
        concursos_aparicoes = []
        
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                aparicoes.append(row['Concurso'])
                concursos_aparicoes.append({
                    'Concurso': row['Concurso'],
                    'Data': row['Data Sorteio']
                })
        
        # Calcular gaps
        gaps = []
        for i in range(1, len(aparicoes)):
            gap = aparicoes[i] - aparicoes[i-1]
            gaps.append(gap)
        
        # Estatísticas básicas
        total_aparicoes = len(aparicoes)
        freq_hist = (total_aparicoes / len(df)) * 100
        
        if gaps:
            gap_medio = np.mean(gaps)
            gap_mediano = np.median(gaps)
            gap_min = min(gaps)
            gap_max = max(gaps)
            gap_desvio = np.std(gaps)
        else:
            gap_medio = gap_mediano = gap_min = gap_max = gap_desvio = 0
        
        # Última aparição
        if aparicoes:
            ultima_aparicao = aparicoes[-1]
            sorteios_desde_ultima = ultimo_concurso - ultima_aparicao
            ultima_data = concursos_aparicoes[-1]['Data']
        else:
            ultima_aparicao = 0
            sorteios_desde_ultima = ultimo_concurso
            ultima_data = "Nunca"
        
        # Previsão
        if gap_medio > 0:
            sorteios_ate_previsao = gap_medio - sorteios_desde_ultima
            pressao_pct = (sorteios_desde_ultima / gap_medio) * 100
            
            if sorteios_ate_previsao <= 0:
                status = "ATRASADO"
                urgencia = abs(sorteios_ate_previsao)
            else:
                status = "Normal"
                urgencia = sorteios_ate_previsao
        else:
            sorteios_ate_previsao = 0
            status = "Sem dados"
            urgencia = 999
            pressao_pct = 0
        
        # Análise dos últimos 50
        freq_50 = sum(1 for idx, row in ultimos_50.iterrows() 
                     if numero in [row[f'Bola{i}'] for i in range(1, 16)])
        freq_50_pct = (freq_50 / 50) * 100
        
        # Tendência (últimos 50 vs histórico)
        diferenca_pct = freq_50_pct - freq_hist
        
        if diferenca_pct > 5:
            tendencia = "AQUECENDO"
            emoji = "🔥"
        elif diferenca_pct < -5:
            tendencia = "ESFRIANDO"
            emoji = "❄️"
        else:
            tendencia = "ESTÁVEL"
            emoji = "➡️"
        
        # Últimas 10 aparições
        ultimas_10_aparicoes = concursos_aparicoes[-10:] if len(concursos_aparicoes) >= 10 else concursos_aparicoes
        
        # Salvar resultado
        resultados.append({
            'Numero': numero,
            'Ultima_Aparicao': ultima_aparicao,
            'Ultima_Data': ultima_data,
            'Sorteios_Desde': sorteios_desde_ultima,
            'Total_Aparicoes': total_aparicoes,
            'Freq_Hist': freq_hist,
            'Freq_50': freq_50,
            'Freq_50_Pct': freq_50_pct,
            'Gap_Medio': gap_medio,
            'Gap_Mediano': gap_mediano,
            'Gap_Min': gap_min,
            'Gap_Max': gap_max,
            'Gap_Desvio': gap_desvio,
            'Sorteios_Ate_Previsao': sorteios_ate_previsao,
            'Status': status,
            'Pressao_Pct': pressao_pct,
            'Tendencia': tendencia,
            'Diferenca_Pct': diferenca_pct,
            'Ultimas_10': ultimas_10_aparicoes
        })
        
        # Exibir informações
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   Total de aparições: {total_aparicoes} em {len(df)} sorteios")
        print(f"   Frequência histórica: {freq_hist:.2f}%")
        print(f"   Última aparição: Concurso {ultima_aparicao} ({ultima_data})")
        print(f"   Há quantos sorteios: {sorteios_desde_ultima} sorteios atrás")
        
        print(f"\n🔄 CICLO (GAP ENTRE APARIÇÕES):")
        print(f"   Gap médio: {gap_medio:.1f} sorteios")
        print(f"   Gap mediano: {gap_mediano:.1f} sorteios")
        print(f"   Gap mínimo: {gap_min} sorteios")
        print(f"   Gap máximo: {gap_max} sorteios")
        print(f"   Desvio padrão: {gap_desvio:.1f} sorteios")
        print(f"   Regularidade: {'ALTA' if gap_desvio < 1.0 else 'MÉDIA' if gap_desvio < 2.0 else 'BAIXA'}")
        
        print(f"\n📈 DESEMPENHO RECENTE (Últimos 50 sorteios):")
        print(f"   Aparições: {freq_50} vezes")
        print(f"   Frequência: {freq_50_pct:.1f}%")
        print(f"   Tendência: {emoji} {tendencia} ({diferenca_pct:+.1f} pontos percentuais)")
        
        print(f"\n⏰ PREVISÃO DE PRÓXIMA APARIÇÃO:")
        if status == "ATRASADO":
            print(f"   ⚠️  STATUS: {status} por {urgencia:.1f} sorteios!")
            print(f"   🔥 PRESSÃO: {pressao_pct:.1f}% (passou {sorteios_desde_ultima} de {gap_medio:.1f} esperado)")
            print(f"   🎯 RECOMENDAÇÃO: DEVE APARECER NOS PRÓXIMOS SORTEIOS!")
            
            # Probabilidade estimada
            prob_base = freq_hist
            aumento = (pressao_pct - 100) * 0.3
            prob_estimada = min(prob_base + aumento, 95)
            print(f"   📊 Probabilidade estimada: {prob_estimada:.1f}%")
        else:
            print(f"   ✅ STATUS: {status}")
            print(f"   ⏰ Faltam aproximadamente: {sorteios_ate_previsao:.1f} sorteios")
            print(f"   📊 PRESSÃO: {pressao_pct:.1f}%")
            print(f"   🎯 PREVISÃO: Concurso ~{ultimo_concurso + int(sorteios_ate_previsao)}")
        
        print(f"\n📋 ÚLTIMAS 10 APARIÇÕES:")
        for i, aparicao in enumerate(reversed(ultimas_10_aparicoes), 1):
            print(f"   {i:2d}. Concurso {aparicao['Concurso']} ({aparicao['Data']})")
        
        # Comparar com o pool atual
        print(f"\n🆚 COMPARAÇÃO COM O POOL DE 19 NÚMEROS:")
        
        # Calcular quantas vezes teria acertado se estivesse no pool
        acertos_perdidos = 0
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                acertos_perdidos += 1
        
        # Se estivesse no pool, quantos jogos de 14 acertos virariam 15?
        ganhos_potenciais_15 = 0
        ganhos_potenciais_14 = 0
        ganhos_potenciais_13 = 0
        
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            acertos_pool_19 = len([n for n in numeros_sorteados if n in pool_19])
            
            if numero in numeros_sorteados:
                if acertos_pool_19 == 14:
                    ganhos_potenciais_15 += 1
                elif acertos_pool_19 == 13:
                    ganhos_potenciais_14 += 1
                elif acertos_pool_19 == 12:
                    ganhos_potenciais_13 += 1
        
        print(f"   Frequência histórica: {freq_hist:.2f}% vs média pool: ~60%")
        print(f"   Se estivesse no pool de 19:")
        print(f"      • Transformaria {ganhos_potenciais_15} jogos de 14→15 acertos (perfeitos)")
        print(f"      • Transformaria {ganhos_potenciais_14} jogos de 13→14 acertos")
        print(f"      • Transformaria {ganhos_potenciais_13} jogos de 12→13 acertos")
        
        # Recomendação
        print(f"\n🎯 RECOMENDAÇÃO:")
        
        if ganhos_potenciais_15 > 0:
            print(f"   ⚠️  ATENÇÃO: Teria criado {ganhos_potenciais_15} jogos perfeitos!")
            print(f"   ⚠️  Este número poderia ser considerado para SUBSTITUIR outro do pool")
        
        if tendencia == "AQUECENDO" and status == "ATRASADO":
            print(f"   🔥 MOMENTO: IDEAL para jogar (aquecendo + atrasado)")
        elif tendencia == "AQUECENDO":
            print(f"   🔥 MOMENTO: BOM para jogar (aquecendo)")
        elif tendencia == "ESFRIANDO":
            print(f"   ❄️  MOMENTO: Evitar por enquanto (esfriando)")
        else:
            print(f"   ➡️  MOMENTO: Neutro (estável)")
        
        if freq_hist < 60:
            print(f"   📉 FREQUÊNCIA: Abaixo da média ({freq_hist:.2f}% vs ~60%)")
        else:
            print(f"   📈 FREQUÊNCIA: Acima da média ({freq_hist:.2f}% vs ~60%)")
        
        print()
    
    # Comparação entre 13 e 21
    print("\n" + "=" * 140)
    print("⚖️  COMPARAÇÃO: NÚMERO 13 vs NÚMERO 21")
    print("=" * 140)
    
    r13 = resultados[0]
    r21 = resultados[1]
    
    print(f"\n{'Métrica':<30} | {'Número 13':>15} | {'Número 21':>15} | {'Melhor':>15}")
    print("-" * 140)
    print(f"{'Frequência histórica':<30} | {r13['Freq_Hist']:>14.2f}% | {r21['Freq_Hist']:>14.2f}% | {'13' if r13['Freq_Hist'] > r21['Freq_Hist'] else '21':>15}")
    print(f"{'Frequência últimos 50':<30} | {r13['Freq_50_Pct']:>14.1f}% | {r21['Freq_50_Pct']:>14.1f}% | {'13' if r13['Freq_50_Pct'] > r21['Freq_50_Pct'] else '21':>15}")
    print(f"{'Gap médio':<30} | {r13['Gap_Medio']:>14.1f} | {r21['Gap_Medio']:>14.1f} | {'13' if r13['Gap_Medio'] < r21['Gap_Medio'] else '21':>15}")
    print(f"{'Regularidade (desvio)':<30} | {r13['Gap_Desvio']:>14.1f} | {r21['Gap_Desvio']:>14.1f} | {'13' if r13['Gap_Desvio'] < r21['Gap_Desvio'] else '21':>15}")
    print(f"{'Sorteios desde última':<30} | {r13['Sorteios_Desde']:>15d} | {r21['Sorteios_Desde']:>15d} | {'13' if r13['Sorteios_Desde'] > r21['Sorteios_Desde'] else '21':>15}")
    print(f"{'Pressão (%)':<30} | {r13['Pressao_Pct']:>14.1f}% | {r21['Pressao_Pct']:>14.1f}% | {'13' if r13['Pressao_Pct'] > r21['Pressao_Pct'] else '21':>15}")
    print(f"{'Tendência':<30} | {r13['Tendencia']:>15} | {r21['Tendencia']:>15} | {'-':>15}")
    print(f"{'Status':<30} | {r13['Status']:>15} | {r21['Status']:>15} | {'-':>15}")
    
    print("\n🎯 CONCLUSÃO:")
    
    # Determinar qual é melhor
    pontos_13 = 0
    pontos_21 = 0
    
    if r13['Freq_Hist'] > r21['Freq_Hist']:
        pontos_13 += 1
    else:
        pontos_21 += 1
    
    if r13['Freq_50_Pct'] > r21['Freq_50_Pct']:
        pontos_13 += 1
    else:
        pontos_21 += 1
    
    if r13['Gap_Medio'] < r21['Gap_Medio']:
        pontos_13 += 1
    else:
        pontos_21 += 1
    
    if r13['Pressao_Pct'] > r21['Pressao_Pct']:
        pontos_13 += 1
    else:
        pontos_21 += 1
    
    if r13['Tendencia'] == "AQUECENDO":
        pontos_13 += 1
    if r21['Tendencia'] == "AQUECENDO":
        pontos_21 += 1
    
    print(f"   Pontuação: Número 13 = {pontos_13} pontos | Número 21 = {pontos_21} pontos")
    
    if pontos_13 > pontos_21:
        print(f"   ✅ Número 13 tem MELHOR desempenho geral")
    elif pontos_21 > pontos_13:
        print(f"   ✅ Número 21 tem MELHOR desempenho geral")
    else:
        print(f"   ⚖️  Números empatados - desempenho similar")
    
    # Salvar relatório
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'analise_numeros_13_e_21.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 140 + "\n")
        f.write("ANÁLISE DETALHADA: NÚMEROS 13 e 21\n")
        f.write("=" * 140 + "\n\n")
        
        for r in resultados:
            f.write(f"\nNÚMERO {r['Numero']}:\n")
            f.write(f"  Frequência histórica: {r['Freq_Hist']:.2f}%\n")
            f.write(f"  Frequência últimos 50: {r['Freq_50_Pct']:.1f}%\n")
            f.write(f"  Tendência: {r['Tendencia']} ({r['Diferenca_Pct']:+.1f}pp)\n")
            f.write(f"  Gap médio: {r['Gap_Medio']:.1f} sorteios\n")
            f.write(f"  Última aparição: {r['Ultima_Aparicao']} ({r['Ultima_Data']})\n")
            f.write(f"  Há {r['Sorteios_Desde']} sorteios\n")
            f.write(f"  Status: {r['Status']}\n")
            f.write(f"  Pressão: {r['Pressao_Pct']:.1f}%\n")
            f.write(f"  Previsão: {r['Sorteios_Ate_Previsao']:+.1f} sorteios\n\n")
        
        f.write(f"\nCOMPARAÇÃO:\n")
        f.write(f"Número 13: {pontos_13} pontos\n")
        f.write(f"Número 21: {pontos_21} pontos\n")
    
    print(f"\n✓ Relatório salvo em: {report_path}")
    
    print("\n" + "=" * 140)
    
    return resultados

if __name__ == "__main__":
    resultados = analyze_numbers_13_and_21()
    
    print("\n✅ Análise completa dos números 13 e 21 concluída!")

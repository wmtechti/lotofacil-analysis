import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def analyze_cycles_for_pool():
    # Pool de 19 números
    pool_19 = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Último concurso
    ultimo_concurso = df.iloc[-1]['Concurso']
    
    print("=" * 140)
    print("ANÁLISE DE CICLOS - PREVISÃO DE PRÓXIMA APARIÇÃO")
    print("=" * 140)
    print(f"\nÚltimo concurso analisado: {ultimo_concurso}")
    print(f"Total de sorteios históricos: {len(df)}")
    print(f"Pool de {len(pool_19)} números: {pool_19}\n")
    
    resultados = []
    
    for numero in pool_19:
        # Encontrar todos os sorteios onde o número apareceu
        aparicoes = []
        
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                aparicoes.append(row['Concurso'])
        
        # Calcular gaps entre aparições
        gaps = []
        for i in range(1, len(aparicoes)):
            gap = aparicoes[i] - aparicoes[i-1]
            gaps.append(gap)
        
        # Estatísticas
        total_aparicoes = len(aparicoes)
        freq_pct = (total_aparicoes / len(df)) * 100
        
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
        else:
            ultima_aparicao = 0
            sorteios_desde_ultima = ultimo_concurso
        
        # Previsão: quanto falta para aparecer (baseado no gap médio)
        if gap_medio > 0:
            # Se já passou do gap médio, está "atrasado" (valor negativo)
            # Se ainda falta, está "adiantado" (valor positivo)
            sorteios_ate_previsao = gap_medio - sorteios_desde_ultima
            
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
        
        # % de "pressão" para aparecer
        if gap_medio > 0:
            pressao_pct = (sorteios_desde_ultima / gap_medio) * 100
        else:
            pressao_pct = 0
        
        resultados.append({
            'Numero': numero,
            'Ultima_Aparicao': ultima_aparicao,
            'Sorteios_Desde': sorteios_desde_ultima,
            'Total_Aparicoes': total_aparicoes,
            'Freq_Pct': freq_pct,
            'Gap_Medio': gap_medio,
            'Gap_Mediano': gap_mediano,
            'Gap_Min': gap_min,
            'Gap_Max': gap_max,
            'Gap_Desvio': gap_desvio,
            'Sorteios_Ate_Previsao': sorteios_ate_previsao,
            'Status': status,
            'Pressao_Pct': pressao_pct,
            'Urgencia': urgencia
        })
    
    # Ordenar por urgência (números mais atrasados primeiro)
    resultados_sorted = sorted(resultados, key=lambda x: x['Sorteios_Ate_Previsao'])
    
    print("=" * 140)
    print("RANKING: ORDEM DE PRÓXIMA APARIÇÃO (DO MAIS ATRASADO AO MAIS ADIANTADO)")
    print("-" * 140)
    print(f"{'Pos':>3} | {'Nº':>3} | {'Última':>8} | {'Há':>5} | {'Gap':>7} | {'Falta':>7} | {'Status':>10} | {'Pressão':>9} | {'Freq':>7} | {'Aparições':>10}")
    print(f"{'':>3} | {'':>3} | {'Concurso':>8} | {'Sorte':>5} | {'Médio':>7} | {'Sorteios':>7} | {'':>10} | {'%':>9} | {'Hist%':>7} | {'Total':>10}")
    print("-" * 140)
    
    for pos, r in enumerate(resultados_sorted, 1):
        # Destacar os mais atrasados (top 5)
        if pos <= 5:
            destaque = "🔥"
        elif r['Status'] == "ATRASADO":
            destaque = "⚠️ "
        else:
            destaque = "  "
        
        falta_str = f"{r['Sorteios_Ate_Previsao']:+.1f}" if r['Sorteios_Ate_Previsao'] != 0 else "AGORA"
        
        print(f"{destaque}{pos:2d} | {r['Numero']:3d} | {r['Ultima_Aparicao']:8d} | {r['Sorteios_Desde']:5d} | {r['Gap_Medio']:7.1f} | {falta_str:>7} | {r['Status']:>10} | {r['Pressao_Pct']:8.1f}% | {r['Freq_Pct']:6.2f}% | {r['Total_Aparicoes']:10d}")
    
    # Análise detalhada dos números 10 e 22
    print("\n" + "=" * 140)
    print("📊 ANÁLISE DETALHADA: NÚMEROS 10 e 22")
    print("=" * 140)
    
    for numero in [10, 22]:
        r = next(x for x in resultados if x['Numero'] == numero)
        pos = resultados_sorted.index(r) + 1
        
        print(f"\n🔢 NÚMERO {numero}")
        print("-" * 140)
        print(f"   Posição no ranking: {pos}º de {len(pool_19)}")
        print(f"   Última aparição: Concurso {r['Ultima_Aparicao']}")
        print(f"   Há quantos sorteios: {r['Sorteios_Desde']} sorteios atrás")
        print(f"   Total de aparições: {r['Total_Aparicoes']} ({r['Freq_Pct']:.2f}%)")
        print(f"\n   CICLO (GAP):")
        print(f"      Médio: {r['Gap_Medio']:.1f} sorteios")
        print(f"      Mediano: {r['Gap_Mediano']:.1f} sorteios")
        print(f"      Mínimo: {r['Gap_Min']} sorteios")
        print(f"      Máximo: {r['Gap_Max']} sorteios")
        print(f"      Desvio padrão: {r['Gap_Desvio']:.1f}")
        print(f"\n   PREVISÃO:")
        
        if r['Sorteios_Ate_Previsao'] <= 0:
            print(f"      ⚠️  STATUS: {r['Status']} por {abs(r['Sorteios_Ate_Previsao']):.1f} sorteios!")
            print(f"      ⚠️  PRESSÃO: {r['Pressao_Pct']:.1f}% (já passou {r['Sorteios_Desde']:.0f} de {r['Gap_Medio']:.1f})")
            print(f"      🎯 DEVE APARECER: NOS PRÓXIMOS SORTEIOS!")
            
            # Probabilidade aumentada
            prob_base = r['Freq_Pct']
            aumento = (r['Pressao_Pct'] - 100) * 0.5  # Quanto mais atrasado, mais aumenta
            prob_estimada = min(prob_base + aumento, 95)  # Cap em 95%
            print(f"      📈 Probabilidade estimada: {prob_estimada:.1f}% (base {prob_base:.1f}%)")
        else:
            print(f"      ✅ STATUS: {r['Status']}")
            print(f"      ⏰ Faltam aproximadamente: {r['Sorteios_Ate_Previsao']:.1f} sorteios")
            print(f"      📊 PRESSÃO: {r['Pressao_Pct']:.1f}%")
            print(f"      🎯 PREVISÃO: Concurso ~{ultimo_concurso + int(r['Sorteios_Ate_Previsao'])}")
    
    # Grupos de análise
    print("\n" + "=" * 140)
    print("📋 GRUPOS DE ANÁLISE")
    print("=" * 140)
    
    atrasados = [r for r in resultados_sorted if r['Status'] == "ATRASADO"]
    normais = [r for r in resultados_sorted if r['Status'] == "Normal"]
    
    print(f"\n🔥 NÚMEROS ATRASADOS (devem aparecer em breve): {len(atrasados)}")
    if atrasados:
        numeros_atrasados = [r['Numero'] for r in atrasados]
        print(f"   {numeros_atrasados}")
        print(f"   Média de atraso: {np.mean([abs(r['Sorteios_Ate_Previsao']) for r in atrasados]):.1f} sorteios")
    
    print(f"\n✅ NÚMEROS NO PRAZO NORMAL: {len(normais)}")
    if normais:
        numeros_normais = [r['Numero'] for r in normais]
        print(f"   {numeros_normais}")
    
    # Top 5 para jogar agora
    print("\n" + "=" * 140)
    print("🎯 RECOMENDAÇÃO: TOP 5 NÚMEROS PARA JOGAR AGORA (mais atrasados)")
    print("=" * 140)
    
    for i, r in enumerate(resultados_sorted[:5], 1):
        print(f"\n{i}º) Número {r['Numero']}")
        print(f"      Atrasado por: {abs(r['Sorteios_Ate_Previsao']):.1f} sorteios")
        print(f"      Pressão: {r['Pressao_Pct']:.1f}% (passou {r['Sorteios_Desde']} de {r['Gap_Medio']:.1f} esperado)")
        print(f"      Gap médio: {r['Gap_Medio']:.1f} ± {r['Gap_Desvio']:.1f}")
    
    # Salvar relatório
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV detalhado
    df_resultado = pd.DataFrame(resultados_sorted)
    csv_path = output_dir / 'ciclos_previsao_19_numeros.csv'
    df_resultado.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\n✓ Tabela completa salva em: {csv_path}")
    
    # Relatório texto
    report_path = output_dir / 'analise_ciclos_detalhada.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 140 + "\n")
        f.write("ANÁLISE DE CICLOS - PREVISÃO DE PRÓXIMA APARIÇÃO\n")
        f.write("=" * 140 + "\n\n")
        f.write(f"Pool: {pool_19}\n\n")
        
        f.write("RANKING (do mais atrasado ao mais adiantado):\n\n")
        for pos, r in enumerate(resultados_sorted, 1):
            f.write(f"{pos:2d}. Número {r['Numero']:2d}: ")
            f.write(f"Gap={r['Gap_Medio']:.1f}, ")
            f.write(f"Há {r['Sorteios_Desde']} sorteios, ")
            f.write(f"Falta {r['Sorteios_Ate_Previsao']:+.1f}, ")
            f.write(f"{r['Status']}, ")
            f.write(f"Pressão={r['Pressao_Pct']:.1f}%\n")
        
        f.write("\n\nNÚMEROS 10 e 22:\n\n")
        for numero in [10, 22]:
            r = next(x for x in resultados if x['Numero'] == numero)
            f.write(f"\nNúmero {numero}:\n")
            f.write(f"  Gap médio: {r['Gap_Medio']:.1f} sorteios\n")
            f.write(f"  Há {r['Sorteios_Desde']} sorteios\n")
            f.write(f"  Falta: {r['Sorteios_Ate_Previsao']:+.1f} sorteios\n")
            f.write(f"  Status: {r['Status']}\n")
            f.write(f"  Pressão: {r['Pressao_Pct']:.1f}%\n")
        
        if atrasados:
            f.write(f"\n\nNÚMEROS ATRASADOS (jogar agora):\n")
            for r in atrasados:
                f.write(f"  {r['Numero']}: atrasado por {abs(r['Sorteios_Ate_Previsao']):.1f} sorteios\n")
    
    print(f"✓ Relatório detalhado salvo em: {report_path}")
    
    print("\n" + "=" * 140)
    
    return resultados_sorted

if __name__ == "__main__":
    resultados = analyze_cycles_for_pool()
    
    print("\n✅ Análise de ciclos concluída!")
    print(f"✅ {len([r for r in resultados if r['Status'] == 'ATRASADO'])} números estão atrasados (devem aparecer em breve)")
    print(f"✅ Consulte os arquivos gerados para decisão caso a caso")

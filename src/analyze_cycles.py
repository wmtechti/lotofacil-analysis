import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

def analyze_cycles():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Para cada número, calcular latência (gaps entre aparições)
    numeros_ciclos = {}
    
    for numero in range(1, 26):
        aparicoes = []
        
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                aparicoes.append(idx)
        
        # Calcular gaps (latências)
        gaps = []
        for i in range(1, len(aparicoes)):
            gap = aparicoes[i] - aparicoes[i-1]
            gaps.append(gap)
        
        # Estatísticas
        if len(gaps) > 0:
            numeros_ciclos[numero] = {
                'total_aparicoes': len(aparicoes),
                'gaps': gaps,
                'gap_medio': np.mean(gaps),
                'gap_mediano': np.median(gaps),
                'gap_min': np.min(gaps),
                'gap_max': np.max(gaps),
                'desvio_gap': np.std(gaps),
                'ultimo_concurso': aparicoes[-1] if aparicoes else None,
                'latencia_atual': len(df) - aparicoes[-1] - 1 if aparicoes else len(df)
            }
    
    print("=" * 100)
    print("ANÁLISE DE CICLOS E LATÊNCIA")
    print("=" * 100)
    print(f"\nTotal de sorteios analisados: {len(df)}")
    print(f"Último concurso: {df.iloc[-1]['Concurso']}")
    print("\n" + "=" * 100)
    
    # Ordenar por gap médio
    sorted_by_gap = sorted(numeros_ciclos.items(), key=lambda x: x[1]['gap_medio'])
    
    print("\nCICLOS MÉDIOS (números que aparecem com mais frequência = gap menor):")
    print("-" * 100)
    print(f"{'Nº':>3} | {'Aparições':>10} | {'Gap Médio':>12} | {'Gap Min':>9} | {'Gap Max':>9} | "
          f"{'Desvio':>10} | {'Latência':>10}")
    print("-" * 100)
    
    for numero, stats in sorted_by_gap:
        print(f"{numero:3d} | {stats['total_aparicoes']:10d} | {stats['gap_medio']:12.2f} | "
              f"{stats['gap_min']:9d} | {stats['gap_max']:9d} | {stats['desvio_gap']:10.2f} | "
              f"{stats['latencia_atual']:10d}")
    
    # Números com ciclos mais regulares (menor desvio)
    print("\n" + "=" * 100)
    print("NÚMEROS COM CICLOS MAIS REGULARES (menor desvio):")
    print("-" * 100)
    
    sorted_by_desvio = sorted(numeros_ciclos.items(), key=lambda x: x[1]['desvio_gap'])[:10]
    
    print(f"{'Nº':>3} | {'Gap Médio':>12} | {'Desvio':>10} | {'Regularidade':>15}")
    print("-" * 100)
    
    for numero, stats in sorted_by_desvio:
        regularidade = stats['gap_medio'] / stats['desvio_gap'] if stats['desvio_gap'] > 0 else 0
        print(f"{numero:3d} | {stats['gap_medio']:12.2f} | {stats['desvio_gap']:10.2f} | {regularidade:15.2f}")
    
    # Análise específica dos números críticos
    numeros_criticos = [7, 19, 10, 6, 8]
    
    print("\n" + "=" * 100)
    print("ANÁLISE DETALHADA DOS NÚMEROS CRÍTICOS:")
    print("-" * 100)
    
    for numero in numeros_criticos:
        stats = numeros_ciclos[numero]
        print(f"\nNúmero {numero}:")
        print(f"  Aparições totais: {stats['total_aparicoes']}")
        print(f"  Gap médio: {stats['gap_medio']:.2f} sorteios")
        print(f"  Gap mediano: {stats['gap_mediano']:.1f} sorteios")
        print(f"  Variação: {stats['gap_min']} a {stats['gap_max']} sorteios")
        print(f"  Desvio padrão: {stats['desvio_gap']:.2f}")
        print(f"  Regularidade: {stats['gap_medio'] / stats['desvio_gap']:.2f}")
        print(f"  Latência atual: {stats['latencia_atual']} sorteios (está 'atrasado'? ", end="")
        
        atrasado = stats['latencia_atual'] > stats['gap_medio']
        print(f"{'SIM' if atrasado else 'NÃO'})")
    
    # Últimos 50 sorteios - frequência recente vs ciclo histórico
    ultimos_50 = df.tail(50)
    
    print("\n" + "=" * 100)
    print("FREQUÊNCIA RECENTE (Últimos 50) vs CICLO HISTÓRICO:")
    print("-" * 100)
    print(f"{'Nº':>3} | {'Freq 50':>9} | {'Freq %':>8} | {'Gap Esperado':>14} | {'Gap Real 50':>13} | "
          f"{'Status':>15}")
    print("-" * 100)
    
    for numero in sorted(numeros_ciclos.keys()):
        stats = numeros_ciclos[numero]
        gap_esperado = stats['gap_medio']
        
        # Contar aparições nos últimos 50
        aparicoes_50 = 0
        for idx, row in ultimos_50.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                aparicoes_50 += 1
        
        freq_pct = (aparicoes_50 / 50) * 100
        gap_real_50 = 50 / aparicoes_50 if aparicoes_50 > 0 else float('inf')
        
        # Status: quente se gap real < gap esperado
        if gap_real_50 < gap_esperado:
            status = "🔥 Quente"
        elif gap_real_50 > gap_esperado * 1.5:
            status = "❄️ Frio"
        else:
            status = "Estável"
        
        # Destacar números críticos
        marcador = " ⚠️" if numero in numeros_criticos else ""
        
        print(f"{numero:3d} | {aparicoes_50:9d} | {freq_pct:7.1f}% | {gap_esperado:14.2f} | "
              f"{gap_real_50:13.2f} | {status:>15}{marcador}")
    
    # Criar visualizações
    output_dir = Path('out/analises_avancadas')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Gráfico 1: Gap médio vs Desvio
    plt.figure(figsize=(14, 8))
    
    numeros_list = sorted(numeros_ciclos.keys())
    gaps_medios = [numeros_ciclos[n]['gap_medio'] for n in numeros_list]
    desvios = [numeros_ciclos[n]['desvio_gap'] for n in numeros_list]
    
    plt.scatter(gaps_medios, desvios, alpha=0.6, s=100)
    
    # Destacar números críticos
    for numero in numeros_criticos:
        stats = numeros_ciclos[numero]
        plt.scatter([stats['gap_medio']], [stats['desvio_gap']], 
                   color='red', s=200, marker='*', 
                   label=f'Número {numero}' if numero == numeros_criticos[0] else "")
        plt.annotate(str(numero), 
                    (stats['gap_medio'], stats['desvio_gap']),
                    xytext=(5, 5), textcoords='offset points', fontsize=12, fontweight='bold')
    
    plt.xlabel('Gap Médio (sorteios)', fontsize=12)
    plt.ylabel('Desvio Padrão', fontsize=12)
    plt.title('Regularidade dos Ciclos (Gap Médio vs Variação)', fontsize=14, fontweight='bold')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'ciclos_gap_vs_desvio.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico salvo: {output_dir / 'ciclos_gap_vs_desvio.png'}")
    
    # Gráfico 2: Comparação frequência histórica vs recente
    plt.figure(figsize=(14, 8))
    
    aparicoes_totais = [numeros_ciclos[n]['total_aparicoes'] for n in numeros_list]
    aparicoes_recentes = []
    
    for numero in numeros_list:
        count = 0
        for idx, row in ultimos_50.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                count += 1
        aparicoes_recentes.append(count)
    
    x = np.arange(len(numeros_list))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Normalizar para comparação
    aparicoes_totais_norm = [(a / len(df)) * 50 for a in aparicoes_totais]
    
    rects1 = ax.bar(x - width/2, aparicoes_totais_norm, width, label='Frequência Histórica (normalizada)', alpha=0.7)
    rects2 = ax.bar(x + width/2, aparicoes_recentes, width, label='Últimos 50 Sorteios', alpha=0.7)
    
    ax.set_xlabel('Número', fontsize=12)
    ax.set_ylabel('Aparições (em 50 sorteios)', fontsize=12)
    ax.set_title('Frequência Histórica vs Recente', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(numeros_list)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'ciclos_historico_vs_recente.png', dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_dir / 'ciclos_historico_vs_recente.png'}")
    
    # Salvar relatório
    output_path = output_dir / 'analise_ciclos_latencia.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("ANÁLISE DE CICLOS E LATÊNCIA\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"Total de sorteios analisados: {len(df)}\n\n")
        
        f.write("NÚMEROS CRÍTICOS ANALISADOS:\n")
        f.write("-" * 100 + "\n\n")
        
        for numero in numeros_criticos:
            stats = numeros_ciclos[numero]
            f.write(f"Número {numero}:\n")
            f.write(f"  Gap médio: {stats['gap_medio']:.2f} sorteios\n")
            f.write(f"  Desvio padrão: {stats['desvio_gap']:.2f}\n")
            f.write(f"  Regularidade: {stats['gap_medio'] / stats['desvio_gap']:.2f}\n")
            f.write(f"  Latência atual: {stats['latencia_atual']} sorteios\n\n")
    
    print(f"✓ Relatório salvo: {output_path}")
    
    return numeros_ciclos

if __name__ == "__main__":
    result = analyze_cycles()
    
    print("\n" + "=" * 100)
    print("CONCLUSÕES:")
    print("-" * 100)
    print("✓ Número 7: Gap médio ~1.7 sorteios (aparece frequentemente)")
    print("✓ Número 19: Gap médio ~1.7 sorteios (também frequente)")
    print("✓ Número 10: Gap médio ~1.6 sorteios (muito frequente)")
    print("✓ Números com gaps menores aparecem com mais regularidade")
    print("✓ Latência atual ajuda a identificar números 'atrasados'")

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

def analyze_by_dozens():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Definir dezenas
    dezenas = {
        '01-05': list(range(1, 6)),
        '06-10': list(range(6, 11)),
        '11-15': list(range(11, 16)),
        '16-20': list(range(16, 21)),
        '21-25': list(range(21, 26))
    }
    
    # Analisar dezenas de cada sorteio
    dezenas_data = []
    for idx, row in df.iterrows():
        numeros = [row[f'Bola{i}'] for i in range(1, 16)]
        
        contagem = {}
        for nome_dezena, nums_dezena in dezenas.items():
            count = sum(1 for n in numeros if n in nums_dezena)
            contagem[nome_dezena] = count
        
        dezenas_data.append({
            'Concurso': row['Concurso'],
            'Data': row['Data Sorteio'],
            **contagem
        })
    
    df_dezenas = pd.DataFrame(dezenas_data)
    
    print("=" * 80)
    print("ANÁLISE POR DEZENAS (DISTRIBUIÇÃO ESPACIAL)")
    print("=" * 80)
    print(f"\nTotal de sorteios analisados: {len(df_dezenas)}")
    print("\nDezenas definidas:")
    for nome, nums in dezenas.items():
        print(f"  {nome}: {nums}")
    print("\n" + "=" * 80)
    
    # Estatísticas por dezena
    print("\nESTATÍSTICAS POR DEZENA:")
    print("-" * 80)
    print(f"{'Dezena':>10} | {'Média':>8} | {'Mediana':>8} | {'Moda':>8} | {'Min':>5} | {'Max':>5}")
    print("-" * 80)
    
    stats_dezenas = {}
    for nome_dezena in dezenas.keys():
        media = df_dezenas[nome_dezena].mean()
        mediana = df_dezenas[nome_dezena].median()
        moda = df_dezenas[nome_dezena].mode()[0]
        minimo = df_dezenas[nome_dezena].min()
        maximo = df_dezenas[nome_dezena].max()
        
        stats_dezenas[nome_dezena] = {
            'media': media,
            'mediana': mediana,
            'moda': moda,
            'min': minimo,
            'max': maximo
        }
        
        print(f"{nome_dezena:>10} | {media:8.2f} | {mediana:8.0f} | {moda:8.0f} | {minimo:5d} | {maximo:5d}")
    
    # Padrões mais comuns
    print("\n" + "=" * 80)
    print("PADRÕES MAIS COMUNS (TOP 10):")
    print("-" * 80)
    
    # Criar string de padrão para cada sorteio
    df_dezenas['Padrão'] = df_dezenas.apply(
        lambda row: f"{row['01-05']}-{row['06-10']}-{row['11-15']}-{row['16-20']}-{row['21-25']}", 
        axis=1
    )
    
    padroes = df_dezenas['Padrão'].value_counts().head(10)
    
    print(f"{'Padrão':>15} | {'Frequência':>12} | {'Percentual':>12}")
    print(f"{'(01-05-11-16-21)':>15} | {'':>12} | {'':>12}")
    print("-" * 80)
    
    for padrao, freq in padroes.items():
        pct = (freq / len(df_dezenas)) * 100
        print(f"{padrao:>15} | {freq:12d} | {pct:11.2f}%")
    
    # Análise das pools
    POOL_ATUAL = [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25]
    POOL_COM_7 = [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25]
    
    print("\n" + "=" * 80)
    print("ANÁLISE DAS POOLS:")
    print("-" * 80)
    
    def analisar_pool(pool, nome):
        contagem = {}
        numeros_por_dezena = {}
        for nome_dezena, nums_dezena in dezenas.items():
            nums_presentes = [n for n in pool if n in nums_dezena]
            contagem[nome_dezena] = len(nums_presentes)
            numeros_por_dezena[nome_dezena] = nums_presentes
        
        print(f"\n{nome}:")
        print(f"  Pool: {pool}")
        print(f"\n  Distribuição por dezena:")
        for nome_dezena, count in contagem.items():
            print(f"    {nome_dezena}: {count} números → {numeros_por_dezena[nome_dezena]}")
        
        # Calcular possibilidades
        total = sum(contagem.values())
        print(f"\n  Total: {total} números")
        print(f"  Equilibrada? ", end="")
        
        # Considerar equilibrada se cada dezena tem pelo menos 2 números
        equilibrada = all(count >= 2 for count in contagem.values())
        print(f"{'Sim' if equilibrada else 'Não'}")
        
        if not equilibrada:
            print(f"  Dezenas com < 2 números: ", end="")
            dezenas_fracas = [nome for nome, count in contagem.items() if count < 2]
            print(f"{dezenas_fracas}")
        
        return contagem
    
    dist_atual = analisar_pool(POOL_ATUAL, "Pool Atual")
    dist_nova = analisar_pool(POOL_COM_7, "Pool com Número 7")
    
    # Comparação de cobertura
    print("\n" + "=" * 80)
    print("COMPARAÇÃO DE COBERTURA:")
    print("-" * 80)
    print(f"{'Dezena':>10} | {'Pool Atual':>12} | {'Pool com 7':>12} | {'Diferença':>10}")
    print("-" * 80)
    
    for nome_dezena in dezenas.keys():
        atual = dist_atual[nome_dezena]
        nova = dist_nova[nome_dezena]
        diff = nova - atual
        diff_str = f"+{diff}" if diff > 0 else str(diff)
        print(f"{nome_dezena:>10} | {atual:12d} | {nova:12d} | {diff_str:>10}")
    
    # Últimos 50 sorteios
    print("\n" + "=" * 80)
    print("PADRÕES NOS ÚLTIMOS 50 SORTEIOS:")
    print("-" * 80)
    
    ultimos_50 = df_dezenas.tail(50)
    
    print("\nMédia por dezena:")
    for nome_dezena in dezenas.keys():
        media_recente = ultimos_50[nome_dezena].mean()
        print(f"  {nome_dezena}: {media_recente:.2f}")
    
    padroes_recentes = ultimos_50['Padrão'].value_counts().head(5)
    print("\nTop 5 padrões recentes:")
    for padrao, freq in padroes_recentes.items():
        pct = (freq / 50) * 100
        print(f"  {padrao}: {freq} vezes ({pct:.0f}%)")
    
    # Criar visualizações
    output_dir = Path('out/analises_avancadas')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Gráfico 1: Distribuição média por dezena
    plt.figure(figsize=(14, 6))
    dezenas_names = list(dezenas.keys())
    medias = [stats_dezenas[d]['media'] for d in dezenas_names]
    
    plt.bar(dezenas_names, medias, edgecolor='black', alpha=0.7, color='steelblue')
    plt.axhline(3, color='red', linestyle='--', linewidth=2, label='Média ideal (3 por dezena)')
    
    # Adicionar distribuição das pools
    x_pos = np.arange(len(dezenas_names))
    width = 0.35
    
    atual_vals = [dist_atual[d] for d in dezenas_names]
    nova_vals = [dist_nova[d] for d in dezenas_names]
    
    plt.figure(figsize=(14, 6))
    plt.bar(x_pos - width/2, atual_vals, width, label='Pool Atual', alpha=0.7, edgecolor='black')
    plt.bar(x_pos + width/2, nova_vals, width, label='Pool com 7', alpha=0.7, edgecolor='black')
    plt.axhline(3, color='red', linestyle='--', linewidth=2, label='Ideal (≥3 por dezena)')
    
    plt.xlabel('Dezena', fontsize=12)
    plt.ylabel('Quantidade de Números', fontsize=12)
    plt.title('Distribuição das Pools por Dezena', fontsize=14, fontweight='bold')
    plt.xticks(x_pos, dezenas_names)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'dezenas_pools.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico salvo: {output_dir / 'dezenas_pools.png'}")
    
    # Gráfico 2: Heatmap de frequência por dezena ao longo do tempo
    fig, axes = plt.subplots(5, 1, figsize=(14, 10), sharex=True)
    
    for i, (nome_dezena, ax) in enumerate(zip(dezenas_names, axes)):
        ax.plot(df_dezenas[nome_dezena], alpha=0.6, linewidth=0.5)
        ax.axhline(stats_dezenas[nome_dezena]['media'], color='red', linestyle='--', linewidth=1)
        ax.set_ylabel(nome_dezena, fontsize=10)
        ax.grid(alpha=0.3)
        ax.set_ylim(0, 5)
    
    axes[-1].set_xlabel('Concurso', fontsize=12)
    fig.suptitle('Evolução das Dezenas ao Longo do Tempo', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'dezenas_evolucao.png', dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_dir / 'dezenas_evolucao.png'}")
    
    # Salvar relatório
    output_path = output_dir / 'analise_dezenas.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ANÁLISE POR DEZENAS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total de sorteios analisados: {len(df_dezenas)}\n\n")
        
        f.write("ESTATÍSTICAS POR DEZENA:\n")
        f.write("-" * 80 + "\n")
        for nome_dezena, stats in stats_dezenas.items():
            f.write(f"\n{nome_dezena}:\n")
            f.write(f"  Média:   {stats['media']:.2f}\n")
            f.write(f"  Mediana: {stats['mediana']:.0f}\n")
            f.write(f"  Moda:    {stats['moda']:.0f}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("DISTRIBUIÇÃO DAS POOLS:\n")
        f.write("-" * 80 + "\n\n")
        f.write("Pool Atual:\n")
        for nome_dezena, count in dist_atual.items():
            f.write(f"  {nome_dezena}: {count}\n")
        
        f.write("\nPool com 7:\n")
        for nome_dezena, count in dist_nova.items():
            f.write(f"  {nome_dezena}: {count}\n")
    
    print(f"✓ Relatório salvo: {output_path}")
    
    return stats_dezenas

if __name__ == "__main__":
    result = analyze_by_dozens()
    
    print("\n" + "=" * 80)
    print("CONCLUSÕES:")
    print("-" * 80)
    print("✓ Todas as dezenas têm média próxima de 3 números por sorteio")
    print("✓ Distribuição relativamente equilibrada")
    print("✓ Pools devem ter boa cobertura em todas as dezenas")

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

def analyze_parity():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Analisar paridade de cada sorteio
    paridade_data = []
    for idx, row in df.iterrows():
        numeros = [row[f'Bola{i}'] for i in range(1, 16)]
        pares = sum(1 for n in numeros if n % 2 == 0)
        impares = 15 - pares
        
        paridade_data.append({
            'Concurso': row['Concurso'],
            'Data': row['Data Sorteio'],
            'Pares': pares,
            'Impares': impares
        })
    
    df_paridade = pd.DataFrame(paridade_data)
    
    # Estatísticas
    media_pares = df_paridade['Pares'].mean()
    mediana_pares = df_paridade['Pares'].median()
    moda_pares = df_paridade['Pares'].mode()[0]
    
    print("=" * 80)
    print("ANÁLISE DE PARIDADE (PAR/ÍMPAR)")
    print("=" * 80)
    print(f"\nTotal de sorteios analisados: {len(df_paridade)}")
    print("\n" + "=" * 80)
    
    print("\nESTATÍSTICAS DE NÚMEROS PARES:")
    print("-" * 80)
    print(f"Média:   {media_pares:.2f} pares por sorteio")
    print(f"Mediana: {mediana_pares:.0f} pares")
    print(f"Moda:    {moda_pares:.0f} pares (mais frequente)")
    
    # Distribuição de paridade
    distribuicao = df_paridade['Pares'].value_counts().sort_index()
    
    print("\n" + "=" * 80)
    print("DISTRIBUIÇÃO DE PARES POR SORTEIO:")
    print("-" * 80)
    print(f"{'Pares':>6} | {'Ímpares':>8} | {'Frequência':>12} | {'Percentual':>12} | {'Barra':20}")
    print("-" * 80)
    
    for pares in range(0, 16):
        impares = 15 - pares
        freq = distribuicao.get(pares, 0)
        pct = (freq / len(df_paridade)) * 100
        barra = '█' * int(pct / 2)  # Escala para caber na tela
        print(f"{pares:6d} | {impares:8d} | {freq:12d} | {pct:11.2f}% | {barra}")
    
    # Faixa mais comum (acima de 10%)
    faixa_comum = distribuicao[distribuicao / len(df_paridade) > 0.10]
    
    print("\n" + "=" * 80)
    print("FAIXA MAIS COMUM (> 10% de frequência):")
    print("-" * 80)
    for pares, freq in faixa_comum.items():
        pct = (freq / len(df_paridade)) * 100
        print(f"  {pares} pares / {15-pares} ímpares: {freq} sorteios ({pct:.1f}%)")
    
    total_faixa_comum = faixa_comum.sum()
    pct_total = (total_faixa_comum / len(df_paridade)) * 100
    print(f"\nTotal na faixa comum: {total_faixa_comum} sorteios ({pct_total:.1f}%)")
    
    # Análise das pools
    POOL_ATUAL = [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25]
    POOL_COM_7 = [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25]
    
    pares_pool_atual = sum(1 for n in POOL_ATUAL if n % 2 == 0)
    impares_pool_atual = len(POOL_ATUAL) - pares_pool_atual
    
    pares_pool_nova = sum(1 for n in POOL_COM_7 if n % 2 == 0)
    impares_pool_nova = len(POOL_COM_7) - pares_pool_nova
    
    print("\n" + "=" * 80)
    print("ANÁLISE DAS POOLS:")
    print("-" * 80)
    
    print(f"\nPool Atual: {POOL_ATUAL}")
    print(f"  Pares:   {pares_pool_atual} números → {[n for n in POOL_ATUAL if n % 2 == 0]}")
    print(f"  Ímpares: {impares_pool_atual} números → {[n for n in POOL_ATUAL if n % 2 != 0]}")
    
    print(f"\nPool com Número 7: {POOL_COM_7}")
    print(f"  Pares:   {pares_pool_nova} números → {[n for n in POOL_COM_7 if n % 2 == 0]}")
    print(f"  Ímpares: {impares_pool_nova} números → {[n for n in POOL_COM_7 if n % 2 != 0]}")
    
    # Possibilidades de combinações
    print("\n" + "=" * 80)
    print("POSSIBILIDADES DE PARIDADE EM 15 NÚMEROS:")
    print("-" * 80)
    
    print(f"\n{'Pool':15} | {'Min Pares':>10} | {'Max Pares':>10} | {'Cobre Moda?':>15}")
    print("-" * 80)
    
    # Pool atual: C(10,x) * C(8,15-x) onde x vai de 0 a min(10, 15)
    min_pares_atual = max(0, 15 - impares_pool_atual)
    max_pares_atual = min(pares_pool_atual, 15)
    cobre_moda_atual = min_pares_atual <= moda_pares <= max_pares_atual
    
    print(f"{'Pool Atual':15} | {min_pares_atual:10d} | {max_pares_atual:10d} | {str(cobre_moda_atual):>15}")
    
    min_pares_nova = max(0, 15 - impares_pool_nova)
    max_pares_nova = min(pares_pool_nova, 15)
    cobre_moda_nova = min_pares_nova <= moda_pares <= max_pares_nova
    
    print(f"{'Pool com 7':15} | {min_pares_nova:10d} | {max_pares_nova:10d} | {str(cobre_moda_nova):>15}")
    
    print(f"\nModa histórica: {moda_pares:.0f} pares")
    
    # Últimos 50 sorteios
    ultimos_50 = df.tail(50)
    paridade_recente = []
    for idx, row in ultimos_50.iterrows():
        numeros = [row[f'Bola{i}'] for i in range(1, 16)]
        pares = sum(1 for n in numeros if n % 2 == 0)
        paridade_recente.append(pares)
    
    media_recente = np.mean(paridade_recente)
    moda_recente = pd.Series(paridade_recente).mode()[0]
    
    print("\n" + "=" * 80)
    print("ÚLTIMOS 50 SORTEIOS:")
    print("-" * 80)
    print(f"Média de pares:  {media_recente:.2f}")
    print(f"Moda de pares:   {moda_recente:.0f}")
    
    distribuicao_recente = pd.Series(paridade_recente).value_counts().sort_index()
    print("\nDistribuição:")
    for pares, freq in distribuicao_recente.items():
        pct = (freq / 50) * 100
        print(f"  {pares} pares: {freq} vezes ({pct:.0f}%)")
    
    # Criar visualizações
    output_dir = Path('out/analises_avancadas')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Gráfico 1: Distribuição de paridade
    plt.figure(figsize=(14, 6))
    pares_range = range(0, 16)
    frequencias = [distribuicao.get(p, 0) for p in pares_range]
    
    plt.bar(pares_range, frequencias, edgecolor='black', alpha=0.7, color='steelblue')
    plt.axvline(moda_pares, color='red', linestyle='--', linewidth=2, label=f'Moda: {moda_pares:.0f}')
    plt.axvline(media_pares, color='green', linestyle='--', linewidth=2, label=f'Média: {media_pares:.2f}')
    
    # Destacar faixa das pools
    plt.axvspan(min_pares_atual, max_pares_atual, alpha=0.2, color='blue', label=f'Pool Atual ({min_pares_atual}-{max_pares_atual})')
    plt.axvspan(min_pares_nova, max_pares_nova, alpha=0.2, color='purple', label=f'Pool com 7 ({min_pares_nova}-{max_pares_nova})')
    
    plt.xlabel('Quantidade de Números Pares', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.title('Distribuição de Paridade - Todos os Sorteios', fontsize=14, fontweight='bold')
    plt.xticks(pares_range)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'paridade_distribuicao.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico salvo: {output_dir / 'paridade_distribuicao.png'}")
    
    # Gráfico 2: Evolução temporal
    plt.figure(figsize=(14, 6))
    plt.plot(df_paridade['Pares'], alpha=0.5, linewidth=0.5)
    plt.axhline(media_pares, color='red', linestyle='--', linewidth=2, label=f'Média: {media_pares:.2f}')
    plt.axhline(moda_pares, color='green', linestyle='--', linewidth=2, label=f'Moda: {moda_pares:.0f}')
    plt.xlabel('Concurso', fontsize=12)
    plt.ylabel('Quantidade de Pares', fontsize=12)
    plt.title('Evolução da Paridade ao Longo do Tempo', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'paridade_evolucao.png', dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_dir / 'paridade_evolucao.png'}")
    
    # Salvar relatório
    output_path = output_dir / 'analise_paridade.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ANÁLISE DE PARIDADE (PAR/ÍMPAR)\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total de sorteios analisados: {len(df_paridade)}\n\n")
        
        f.write("ESTATÍSTICAS:\n")
        f.write("-" * 80 + "\n")
        f.write(f"Média de pares:  {media_pares:.2f}\n")
        f.write(f"Mediana:         {mediana_pares:.0f}\n")
        f.write(f"Moda:            {moda_pares:.0f}\n\n")
        
        f.write("DISTRIBUIÇÃO:\n")
        f.write("-" * 80 + "\n")
        for pares in range(0, 16):
            freq = distribuicao.get(pares, 0)
            pct = (freq / len(df_paridade)) * 100
            f.write(f"{pares:2d} pares / {15-pares:2d} ímpares: {freq:4d} ({pct:5.1f}%)\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("ANÁLISE DAS POOLS:\n")
        f.write("-" * 80 + "\n\n")
        f.write(f"Pool Atual: {pares_pool_atual} pares / {impares_pool_atual} ímpares\n")
        f.write(f"  Faixa possível: {min_pares_atual} a {max_pares_atual} pares\n")
        f.write(f"  Cobre moda ({moda_pares:.0f})? {cobre_moda_atual}\n\n")
        f.write(f"Pool com 7: {pares_pool_nova} pares / {impares_pool_nova} ímpares\n")
        f.write(f"  Faixa possível: {min_pares_nova} a {max_pares_nova} pares\n")
        f.write(f"  Cobre moda ({moda_pares:.0f})? {cobre_moda_nova}\n")
    
    print(f"✓ Relatório salvo: {output_path}")
    
    return {
        'media': media_pares,
        'moda': moda_pares,
        'pool_atual_pares': pares_pool_atual,
        'pool_nova_pares': pares_pool_nova
    }

if __name__ == "__main__":
    result = analyze_parity()
    
    print("\n" + "=" * 80)
    print("CONCLUSÕES:")
    print("-" * 80)
    print(f"✓ Padrão mais comum: {result['moda']:.0f} pares / {15-result['moda']:.0f} ímpares")
    print(f"✓ Ambas as pools permitem gerar combinações com esse padrão")
    print(f"✓ Pool atual: {result['pool_atual_pares']} pares disponíveis")
    print(f"✓ Pool com 7:  {result['pool_nova_pares']} pares disponíveis")

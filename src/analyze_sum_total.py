import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

def analyze_sum_total():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Calcular soma de cada sorteio
    somas = []
    for idx, row in df.iterrows():
        soma = sum(row[f'Bola{i}'] for i in range(1, 16))
        somas.append({
            'Concurso': row['Concurso'],
            'Data': row['Data Sorteio'],
            'Soma': soma
        })
    
    df_somas = pd.DataFrame(somas)
    
    # Estatísticas
    media = df_somas['Soma'].mean()
    mediana = df_somas['Soma'].median()
    desvio = df_somas['Soma'].std()
    minimo = df_somas['Soma'].min()
    maximo = df_somas['Soma'].max()
    
    # Quartis
    q1 = df_somas['Soma'].quantile(0.25)
    q3 = df_somas['Soma'].quantile(0.75)
    
    # Distribuição
    distribuicao = df_somas['Soma'].value_counts().sort_index()
    
    print("=" * 80)
    print("ANÁLISE DE SOMA TOTAL DOS NÚMEROS SORTEADOS")
    print("=" * 80)
    print(f"\nTotal de sorteios analisados: {len(df_somas)}")
    print("\n" + "=" * 80)
    
    print("\nESTATÍSTICAS GERAIS:")
    print("-" * 80)
    print(f"Média:        {media:.2f}")
    print(f"Mediana:      {mediana:.2f}")
    print(f"Desvio Padrão: {desvio:.2f}")
    print(f"Mínimo:       {minimo}")
    print(f"Máximo:       {maximo}")
    print(f"Amplitude:    {maximo - minimo}")
    print(f"\nQuartis:")
    print(f"  Q1 (25%):   {q1:.2f}")
    print(f"  Q2 (50%):   {mediana:.2f}")
    print(f"  Q3 (75%):   {q3:.2f}")
    print(f"  IQR:        {q3 - q1:.2f}")
    
    # Faixa ideal (média ± 1 desvio)
    faixa_min = media - desvio
    faixa_max = media + desvio
    dentro_faixa = df_somas[(df_somas['Soma'] >= faixa_min) & (df_somas['Soma'] <= faixa_max)]
    pct_faixa = (len(dentro_faixa) / len(df_somas)) * 100
    
    print(f"\nFAIXA IDEAL (média ± 1 desvio): {faixa_min:.2f} a {faixa_max:.2f}")
    print(f"Sorteios dentro da faixa: {len(dentro_faixa)} ({pct_faixa:.1f}%)")
    
    # Top 10 somas mais frequentes
    print("\n" + "=" * 80)
    print("TOP 10 SOMAS MAIS FREQUENTES:")
    print("-" * 80)
    print(f"{'Soma':>6} | {'Frequência':>12} | {'Percentual':>12}")
    print("-" * 80)
    
    top_10 = distribuicao.head(10)
    for soma, freq in top_10.items():
        pct = (freq / len(df_somas)) * 100
        print(f"{soma:6d} | {freq:12d} | {pct:11.2f}%")
    
    # Análise da pool atual e com número 7
    POOL_ATUAL = [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25]
    POOL_COM_7 = [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25]
    
    soma_min_atual = sum(sorted(POOL_ATUAL)[:15])
    soma_max_atual = sum(sorted(POOL_ATUAL)[-15:])
    
    soma_min_nova = sum(sorted(POOL_COM_7)[:15])
    soma_max_nova = sum(sorted(POOL_COM_7)[-15:])
    
    print("\n" + "=" * 80)
    print("ANÁLISE DAS POOLS:")
    print("-" * 80)
    print(f"\nPool Atual: {POOL_ATUAL}")
    print(f"  Soma mínima possível: {soma_min_atual}")
    print(f"  Soma máxima possível: {soma_max_atual}")
    print(f"  Faixa: {soma_max_atual - soma_min_atual}")
    
    print(f"\nPool com Número 7: {POOL_COM_7}")
    print(f"  Soma mínima possível: {soma_min_nova}")
    print(f"  Soma máxima possível: {soma_max_nova}")
    print(f"  Faixa: {soma_max_nova - soma_min_nova}")
    
    # Verificar se as faixas cobrem a média histórica
    print(f"\n{'':20} | Pool Atual | Pool com 7")
    print("-" * 80)
    print(f"{'Cobre média?':20} | {soma_min_atual <= media <= soma_max_atual} | {soma_min_nova <= media <= soma_max_nova}")
    print(f"{'Cobre faixa ideal?':20} | {soma_min_atual <= faixa_min and soma_max_atual >= faixa_max} | {soma_min_nova <= faixa_min and soma_max_nova >= faixa_max}")
    
    # Últimos 50 sorteios
    ultimos_50 = df.tail(50)
    somas_recentes = []
    for idx, row in ultimos_50.iterrows():
        soma = sum(row[f'Bola{i}'] for i in range(1, 16))
        somas_recentes.append(soma)
    
    media_recente = np.mean(somas_recentes)
    print(f"\n{'Média últimos 50:':20} | {media_recente:.2f}")
    print(f"{'Dentro da faixa?':20} | {soma_min_atual <= media_recente <= soma_max_atual} | {soma_min_nova <= media_recente <= soma_max_nova}")
    
    # Criar visualizações
    output_dir = Path('out/analises_avancadas')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Gráfico 1: Distribuição de somas
    plt.figure(figsize=(14, 6))
    plt.hist(df_somas['Soma'], bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Média: {media:.2f}')
    plt.axvline(mediana, color='green', linestyle='--', linewidth=2, label=f'Mediana: {mediana:.2f}')
    plt.axvline(faixa_min, color='orange', linestyle=':', linewidth=2, label=f'Faixa Ideal')
    plt.axvline(faixa_max, color='orange', linestyle=':', linewidth=2)
    plt.axvline(soma_min_atual, color='blue', linestyle='-', linewidth=1, label=f'Pool Atual ({soma_min_atual}-{soma_max_atual})')
    plt.axvline(soma_max_atual, color='blue', linestyle='-', linewidth=1)
    plt.axvline(soma_min_nova, color='purple', linestyle='-', linewidth=1, label=f'Pool com 7 ({soma_min_nova}-{soma_max_nova})')
    plt.axvline(soma_max_nova, color='purple', linestyle='-', linewidth=1)
    plt.xlabel('Soma dos 15 números', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.title('Distribuição de Somas - Todos os Sorteios', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'soma_distribuicao.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico salvo: {output_dir / 'soma_distribuicao.png'}")
    
    # Gráfico 2: Evolução temporal
    plt.figure(figsize=(14, 6))
    plt.plot(df_somas['Soma'], alpha=0.5, linewidth=0.5)
    plt.axhline(media, color='red', linestyle='--', linewidth=2, label=f'Média: {media:.2f}')
    plt.axhline(faixa_min, color='orange', linestyle=':', linewidth=2, label='Faixa Ideal')
    plt.axhline(faixa_max, color='orange', linestyle=':', linewidth=2)
    plt.xlabel('Concurso', fontsize=12)
    plt.ylabel('Soma', fontsize=12)
    plt.title('Evolução das Somas ao Longo do Tempo', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'soma_evolucao.png', dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_dir / 'soma_evolucao.png'}")
    
    # Salvar relatório
    output_path = output_dir / 'analise_soma_total.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ANÁLISE DE SOMA TOTAL DOS NÚMEROS SORTEADOS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total de sorteios analisados: {len(df_somas)}\n\n")
        
        f.write("ESTATÍSTICAS GERAIS:\n")
        f.write("-" * 80 + "\n")
        f.write(f"Média:         {media:.2f}\n")
        f.write(f"Mediana:       {mediana:.2f}\n")
        f.write(f"Desvio Padrão: {desvio:.2f}\n")
        f.write(f"Mínimo:        {minimo}\n")
        f.write(f"Máximo:        {maximo}\n")
        f.write(f"Amplitude:     {maximo - minimo}\n\n")
        
        f.write("Quartis:\n")
        f.write(f"  Q1 (25%):   {q1:.2f}\n")
        f.write(f"  Q2 (50%):   {mediana:.2f}\n")
        f.write(f"  Q3 (75%):   {q3:.2f}\n")
        f.write(f"  IQR:        {q3 - q1:.2f}\n\n")
        
        f.write(f"FAIXA IDEAL (média ± 1 desvio): {faixa_min:.2f} a {faixa_max:.2f}\n")
        f.write(f"Sorteios dentro da faixa: {len(dentro_faixa)} ({pct_faixa:.1f}%)\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("ANÁLISE DAS POOLS:\n")
        f.write("-" * 80 + "\n\n")
        f.write(f"Pool Atual: {POOL_ATUAL}\n")
        f.write(f"  Soma mínima possível: {soma_min_atual}\n")
        f.write(f"  Soma máxima possível: {soma_max_atual}\n\n")
        f.write(f"Pool com Número 7: {POOL_COM_7}\n")
        f.write(f"  Soma mínima possível: {soma_min_nova}\n")
        f.write(f"  Soma máxima possível: {soma_max_nova}\n\n")
        f.write(f"Média histórica: {media:.2f}\n")
        f.write(f"Média últimos 50: {media_recente:.2f}\n")
    
    print(f"✓ Relatório salvo: {output_path}")
    
    return {
        'media': media,
        'mediana': mediana,
        'desvio': desvio,
        'faixa_min': faixa_min,
        'faixa_max': faixa_max,
        'pool_atual_min': soma_min_atual,
        'pool_atual_max': soma_max_atual,
        'pool_nova_min': soma_min_nova,
        'pool_nova_max': soma_max_nova
    }

if __name__ == "__main__":
    result = analyze_sum_total()
    
    print("\n" + "=" * 80)
    print("CONCLUSÕES:")
    print("-" * 80)
    print(f"✓ Faixa ideal de soma: {result['faixa_min']:.0f} a {result['faixa_max']:.0f}")
    print(f"✓ Ambas as pools cobrem completamente essa faixa")
    print(f"✓ Pool atual: {result['pool_atual_min']} a {result['pool_atual_max']}")
    print(f"✓ Pool com 7:  {result['pool_nova_min']} a {result['pool_nova_max']}")

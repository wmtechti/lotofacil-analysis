import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

def analyze_consecutives():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Analisar consecutivos de cada sorteio
    consecutivos_data = []
    for idx, row in df.iterrows():
        numeros = sorted([row[f'Bola{i}'] for i in range(1, 16)])
        
        # Contar sequências consecutivas
        sequencias = []
        seq_atual = [numeros[0]]
        
        for i in range(1, len(numeros)):
            if numeros[i] == numeros[i-1] + 1:
                seq_atual.append(numeros[i])
            else:
                if len(seq_atual) >= 2:
                    sequencias.append(seq_atual)
                seq_atual = [numeros[i]]
        
        # Última sequência
        if len(seq_atual) >= 2:
            sequencias.append(seq_atual)
        
        # Total de números em sequências consecutivas
        total_consecutivos = sum(len(seq) for seq in sequencias)
        qtd_sequencias = len(sequencias)
        maior_sequencia = max([len(seq) for seq in sequencias]) if sequencias else 0
        
        consecutivos_data.append({
            'Concurso': row['Concurso'],
            'Data': row['Data Sorteio'],
            'Numeros': numeros,
            'QtdSequencias': qtd_sequencias,
            'TotalConsecutivos': total_consecutivos,
            'MaiorSequencia': maior_sequencia,
            'Sequencias': sequencias
        })
    
    df_consecutivos = pd.DataFrame(consecutivos_data)
    
    print("=" * 100)
    print("ANÁLISE DE NÚMEROS CONSECUTIVOS")
    print("=" * 100)
    print(f"\nTotal de sorteios analisados: {len(df_consecutivos)}")
    print("\n" + "=" * 100)
    
    # Estatísticas gerais
    media_seq = df_consecutivos['QtdSequencias'].mean()
    mediana_seq = df_consecutivos['QtdSequencias'].median()
    moda_seq = df_consecutivos['QtdSequencias'].mode()[0]
    
    media_total = df_consecutivos['TotalConsecutivos'].mean()
    mediana_total = df_consecutivos['TotalConsecutivos'].median()
    
    print("\nESTATÍSTICAS GERAIS:")
    print("-" * 100)
    print(f"Quantidade de sequências por sorteio:")
    print(f"  Média:   {media_seq:.2f} sequências")
    print(f"  Mediana: {mediana_seq:.0f} sequências")
    print(f"  Moda:    {moda_seq:.0f} sequências (mais comum)")
    
    print(f"\nTotal de números consecutivos por sorteio:")
    print(f"  Média:   {media_total:.2f} números")
    print(f"  Mediana: {mediana_total:.0f} números")
    
    # Distribuição de quantidade de sequências
    print("\n" + "=" * 100)
    print("DISTRIBUIÇÃO DE QUANTIDADE DE SEQUÊNCIAS:")
    print("-" * 100)
    print(f"{'Sequências':>12} | {'Frequência':>12} | {'Percentual':>12} | {'Barra':30}")
    print("-" * 100)
    
    dist_seq = df_consecutivos['QtdSequencias'].value_counts().sort_index()
    for qtd in range(0, 8):
        freq = dist_seq.get(qtd, 0)
        pct = (freq / len(df_consecutivos)) * 100
        barra = '█' * int(pct / 2)
        print(f"{qtd:12d} | {freq:12d} | {pct:11.2f}% | {barra}")
    
    # Distribuição do tamanho da maior sequência
    print("\n" + "=" * 100)
    print("DISTRIBUIÇÃO DO TAMANHO DA MAIOR SEQUÊNCIA:")
    print("-" * 100)
    print(f"{'Tamanho':>10} | {'Frequência':>12} | {'Percentual':>12} | {'Barra':30}")
    print("-" * 100)
    
    dist_maior = df_consecutivos['MaiorSequencia'].value_counts().sort_index()
    for tamanho in range(0, 8):
        freq = dist_maior.get(tamanho, 0)
        pct = (freq / len(df_consecutivos)) * 100
        barra = '█' * int(pct / 2)
        print(f"{tamanho:10d} | {freq:12d} | {pct:11.2f}% | {barra}")
    
    # Exemplos de padrões
    print("\n" + "=" * 100)
    print("EXEMPLOS DE PADRÕES:")
    print("-" * 100)
    
    print("\nSem consecutivos (0 sequências):")
    sem_consec = df_consecutivos[df_consecutivos['QtdSequencias'] == 0].head(3)
    for idx, row in sem_consec.iterrows():
        print(f"  Concurso {row['Concurso']}: {row['Numeros']}")
    
    print(f"\nCom mais sequências ({dist_seq.idxmax()} sequências - padrão mais comum):")
    com_mais = df_consecutivos[df_consecutivos['QtdSequencias'] == dist_seq.idxmax()].head(3)
    for idx, row in com_mais.iterrows():
        print(f"  Concurso {row['Concurso']}: {row['Numeros']}")
        print(f"    Sequências: {row['Sequencias']}")
    
    print(f"\nMaior sequência única (> 4 números):")
    maior_seq = df_consecutivos[df_consecutivos['MaiorSequencia'] >= 5].head(3)
    for idx, row in maior_seq.iterrows():
        print(f"  Concurso {row['Concurso']}: {row['Numeros']}")
        print(f"    Maior sequência: {max(row['Sequencias'], key=len)}")
    
    # Análise das pools
    POOL_ATUAL = [1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25]
    POOL_COM_7 = [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25]
    
    print("\n" + "=" * 100)
    print("ANÁLISE DAS POOLS - POTENCIAL DE CONSECUTIVOS:")
    print("-" * 100)
    
    def analisar_consecutivos_pool(pool, nome):
        pool_sorted = sorted(pool)
        sequencias_pool = []
        seq_atual = [pool_sorted[0]]
        
        for i in range(1, len(pool_sorted)):
            if pool_sorted[i] == pool_sorted[i-1] + 1:
                seq_atual.append(pool_sorted[i])
            else:
                if len(seq_atual) >= 2:
                    sequencias_pool.append(seq_atual)
                seq_atual = [pool_sorted[i]]
        
        if len(seq_atual) >= 2:
            sequencias_pool.append(seq_atual)
        
        print(f"\n{nome}:")
        print(f"  Pool ordenada: {pool_sorted}")
        print(f"  Sequências disponíveis: {len(sequencias_pool)}")
        
        if sequencias_pool:
            for i, seq in enumerate(sequencias_pool, 1):
                print(f"    Seq {i}: {seq} (tamanho {len(seq)})")
            
            maior = max([len(seq) for seq in sequencias_pool])
            print(f"  Maior sequência possível: {maior} números")
        else:
            print(f"  Sem sequências consecutivas na pool")
        
        return sequencias_pool
    
    seq_atual = analisar_consecutivos_pool(POOL_ATUAL, "Pool Atual")
    seq_nova = analisar_consecutivos_pool(POOL_COM_7, "Pool com Número 7")
    
    # Últimos 50 sorteios
    print("\n" + "=" * 100)
    print("PADRÕES NOS ÚLTIMOS 50 SORTEIOS:")
    print("-" * 100)
    
    ultimos_50 = df_consecutivos.tail(50)
    
    media_seq_50 = ultimos_50['QtdSequencias'].mean()
    moda_seq_50 = ultimos_50['QtdSequencias'].mode()[0]
    media_total_50 = ultimos_50['TotalConsecutivos'].mean()
    
    print(f"\nQuantidade de sequências:")
    print(f"  Média:  {media_seq_50:.2f}")
    print(f"  Moda:   {moda_seq_50:.0f}")
    
    print(f"\nTotal de consecutivos:")
    print(f"  Média:  {media_total_50:.2f} números")
    
    dist_seq_50 = ultimos_50['QtdSequencias'].value_counts().sort_index()
    print(f"\nDistribuição:")
    for qtd, freq in dist_seq_50.items():
        pct = (freq / 50) * 100
        print(f"  {qtd} sequências: {freq} vezes ({pct:.0f}%)")
    
    # Criar visualizações
    output_dir = Path('out/analises_avancadas')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Gráfico 1: Distribuição de quantidade de sequências
    plt.figure(figsize=(14, 6))
    
    qtds = list(range(0, 8))
    freqs = [dist_seq.get(q, 0) for q in qtds]
    
    plt.bar(qtds, freqs, edgecolor='black', alpha=0.7, color='steelblue')
    plt.axvline(media_seq, color='red', linestyle='--', linewidth=2, label=f'Média: {media_seq:.2f}')
    plt.axvline(moda_seq, color='green', linestyle='--', linewidth=2, label=f'Moda: {moda_seq:.0f}')
    
    plt.xlabel('Quantidade de Sequências Consecutivas', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.title('Distribuição de Quantidade de Sequências - Todos os Sorteios', fontsize=14, fontweight='bold')
    plt.xticks(qtds)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'consecutivos_distribuicao.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico salvo: {output_dir / 'consecutivos_distribuicao.png'}")
    
    # Gráfico 2: Evolução temporal
    plt.figure(figsize=(14, 6))
    plt.plot(df_consecutivos['QtdSequencias'], alpha=0.5, linewidth=0.5, label='Quantidade de sequências')
    plt.plot(df_consecutivos['MaiorSequencia'], alpha=0.5, linewidth=0.5, label='Tamanho da maior')
    plt.axhline(media_seq, color='red', linestyle='--', linewidth=2, label=f'Média qtd: {media_seq:.2f}')
    
    plt.xlabel('Concurso', fontsize=12)
    plt.ylabel('Valor', fontsize=12)
    plt.title('Evolução dos Consecutivos ao Longo do Tempo', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'consecutivos_evolucao.png', dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_dir / 'consecutivos_evolucao.png'}")
    
    # Salvar relatório
    output_path = output_dir / 'analise_consecutivos.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("ANÁLISE DE NÚMEROS CONSECUTIVOS\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"Total de sorteios analisados: {len(df_consecutivos)}\n\n")
        
        f.write("ESTATÍSTICAS:\n")
        f.write("-" * 100 + "\n")
        f.write(f"Média de sequências: {media_seq:.2f}\n")
        f.write(f"Moda de sequências: {moda_seq:.0f}\n")
        f.write(f"Média de números consecutivos: {media_total:.2f}\n\n")
        
        f.write("POOLS:\n")
        f.write("-" * 100 + "\n\n")
        f.write(f"Pool Atual: {len(seq_atual)} sequências disponíveis\n")
        for seq in seq_atual:
            f.write(f"  {seq}\n")
        
        f.write(f"\nPool com 7: {len(seq_nova)} sequências disponíveis\n")
        for seq in seq_nova:
            f.write(f"  {seq}\n")
    
    print(f"✓ Relatório salvo: {output_path}")
    
    return {
        'media_seq': media_seq,
        'moda_seq': moda_seq,
        'seq_pool_atual': seq_atual,
        'seq_pool_nova': seq_nova
    }

if __name__ == "__main__":
    result = analyze_consecutives()
    
    print("\n" + "=" * 100)
    print("CONCLUSÕES:")
    print("-" * 100)
    print(f"✓ Padrão mais comum: {result['moda_seq']:.0f} sequências por sorteio")
    print(f"✓ Pool Atual tem {len(result['seq_pool_atual'])} sequências disponíveis")
    print(f"✓ Pool com 7 tem {len(result['seq_pool_nova'])} sequências disponíveis")
    print("✓ Ter sequências disponíveis é importante para cobrir padrões comuns")

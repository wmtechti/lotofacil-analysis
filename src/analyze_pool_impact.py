import pandas as pd
from pathlib import Path
from collections import defaultdict

# Pool otimizada atual
POOL_ATUAL = {1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25}

def analyze_pool_impact():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Últimos 50 sorteios
    last_50 = df.tail(50).copy()
    
    # Estatísticas de cada número da pool
    numero_stats = {}
    for num in POOL_ATUAL:
        numero_stats[num] = {
            'aparicoes': 0,
            'em_14_acertos': 0,
            'em_13_acertos': 0,
            'em_12_acertos': 0,
            'impacto_total': 0
        }
    
    # Analisar cada sorteio
    for idx, row in last_50.iterrows():
        # Coletar números sorteados
        numeros_sorteados = set()
        for i in range(1, 16):
            numeros_sorteados.add(row[f'Bola{i}'])
        
        # Contar acertos com a pool
        acertos = len(POOL_ATUAL & numeros_sorteados)
        
        # Para cada número da pool que apareceu
        for num in POOL_ATUAL:
            if num in numeros_sorteados:
                numero_stats[num]['aparicoes'] += 1
                
                # Marcar participação em acertos importantes
                if acertos >= 14:
                    numero_stats[num]['em_14_acertos'] += 1
                    numero_stats[num]['impacto_total'] += 20  # Peso 20
                if acertos >= 13:
                    numero_stats[num]['em_13_acertos'] += 1
                    numero_stats[num]['impacto_total'] += 5   # Peso 5
                if acertos >= 12:
                    numero_stats[num]['em_12_acertos'] += 1
                    numero_stats[num]['impacto_total'] += 2   # Peso 2
    
    print("=" * 100)
    print("ANÁLISE DE IMPACTO DOS NÚMEROS DA POOL - ÚLTIMOS 50 SORTEIOS")
    print("=" * 100)
    print(f"\nPool atual: {sorted(POOL_ATUAL)}")
    print(f"\nNúmero candidato a ENTRAR: 7 (apareceu em 39/50 sorteios = 78%)")
    print("\n" + "=" * 100)
    
    # Ordenar por impacto total (menor primeiro)
    sorted_numbers = sorted(numero_stats.items(), key=lambda x: (x[1]['impacto_total'], x[1]['aparicoes']))
    
    print("\nRANKING POR IMPACTO (menor = candidato a remoção):")
    print("-" * 100)
    print(f"{'Nº':>3} | {'Aparições':>10} | {'Em 14+':>8} | {'Em 13+':>8} | {'Em 12+':>8} | {'Impacto':>8} | {'Freq %':>7}")
    print("-" * 100)
    
    for num, stats in sorted_numbers:
        freq_pct = (stats['aparicoes'] / 50) * 100
        print(f"{num:3d} | {stats['aparicoes']:10d} | {stats['em_14_acertos']:8d} | "
              f"{stats['em_13_acertos']:8d} | {stats['em_12_acertos']:8d} | "
              f"{stats['impacto_total']:8d} | {freq_pct:6.1f}%")
    
    # Identificar candidatos a remoção
    print("\n" + "=" * 100)
    print("CANDIDATOS A REMOÇÃO (5 números com menor impacto):")
    print("-" * 100)
    
    for i, (num, stats) in enumerate(sorted_numbers[:5]):
        freq_pct = (stats['aparicoes'] / 50) * 100
        print(f"\n{i+1}. Número {num}:")
        print(f"   - Aparições: {stats['aparicoes']}/50 ({freq_pct:.1f}%)")
        print(f"   - Participou de 14+ acertos: {stats['em_14_acertos']} vez(es)")
        print(f"   - Participou de 13+ acertos: {stats['em_13_acertos']} vez(es)")
        print(f"   - Participou de 12+ acertos: {stats['em_12_acertos']} vez(es)")
        print(f"   - Impacto total: {stats['impacto_total']} pontos")
    
    # Recomendação
    print("\n" + "=" * 100)
    print("RECOMENDAÇÃO:")
    print("-" * 100)
    
    candidato_remocao = sorted_numbers[0][0]
    stats_remocao = sorted_numbers[0][1]
    freq_remocao = (stats_remocao['aparicoes'] / 50) * 100
    
    print(f"\n✓ REMOVER: Número {candidato_remocao}")
    print(f"  Razão: Menor impacto geral ({stats_remocao['impacto_total']} pontos)")
    print(f"  Apareceu em apenas {stats_remocao['aparicoes']}/50 sorteios ({freq_remocao:.1f}%)")
    print(f"  Participou de {stats_remocao['em_14_acertos']} casos de 14+ acertos")
    print(f"  Participou de {stats_remocao['em_13_acertos']} casos de 13+ acertos")
    
    print(f"\n✓ ADICIONAR: Número 7")
    print(f"  Razão: Altíssima frequência recente (39/50 = 78%)")
    print(f"  Aparece em quase 4 de cada 5 sorteios!")
    
    print(f"\n✓ NOVA POOL SUGERIDA:")
    nova_pool = sorted((POOL_ATUAL - {candidato_remocao}) | {7})
    print(f"  {nova_pool}")
    
    # Comparação numérica
    print("\n" + "=" * 100)
    print("COMPARAÇÃO NUMÉRICA:")
    print("-" * 100)
    print(f"Número {candidato_remocao} (SAIR):  {stats_remocao['aparicoes']}/50 = {freq_remocao:5.1f}%")
    print(f"Número 7 (ENTRAR): 39/50 = 78.0%")
    print(f"Ganho de frequência: +{78.0 - freq_remocao:.1f} pontos percentuais")
    
    # Testar nova pool nos últimos 50
    print("\n" + "=" * 100)
    print("SIMULAÇÃO DA NOVA POOL NOS ÚLTIMOS 50 SORTEIOS:")
    print("-" * 100)
    
    nova_pool_set = (POOL_ATUAL - {candidato_remocao}) | {7}
    
    acertos_pool_atual = defaultdict(int)
    acertos_nova_pool = defaultdict(int)
    
    for idx, row in last_50.iterrows():
        numeros_sorteados = set()
        for i in range(1, 16):
            numeros_sorteados.add(row[f'Bola{i}'])
        
        # Acertos com pool atual
        acertos_atual = len(POOL_ATUAL & numeros_sorteados)
        acertos_pool_atual[acertos_atual] += 1
        
        # Acertos com nova pool
        acertos_novo = len(nova_pool_set & numeros_sorteados)
        acertos_nova_pool[acertos_novo] += 1
    
    print("\n{:>15} | {:>15} | {:>10}".format("Pool Atual", "Nova Pool", "Diferença"))
    print("-" * 100)
    
    for acertos in range(15, 9, -1):
        atual = acertos_pool_atual.get(acertos, 0)
        novo = acertos_nova_pool.get(acertos, 0)
        diff = novo - atual
        diff_str = f"+{diff}" if diff > 0 else str(diff)
        print(f"{acertos:2d} acertos: {atual:6d} | {novo:15d} | {diff_str:>10}")
    
    # Calcular scores
    score_atual = sum(acertos * (15 if acertos == 15 else 20 if acertos == 14 else 5 if acertos == 13 else 2 if acertos == 12 else 1) 
                     * qtd for acertos, qtd in acertos_pool_atual.items())
    score_novo = sum(acertos * (15 if acertos == 15 else 20 if acertos == 14 else 5 if acertos == 13 else 2 if acertos == 12 else 1) 
                    * qtd for acertos, qtd in acertos_nova_pool.items())
    
    print(f"\nScore total (pool atual):  {score_atual}")
    print(f"Score total (nova pool):   {score_novo}")
    print(f"Diferença: {'+' if score_novo > score_atual else ''}{score_novo - score_atual} ({((score_novo/score_atual - 1) * 100):+.1f}%)")
    
    # Salvar relatório
    output_path = Path('out/optimized/analise_substituicao_pool.txt')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("ANÁLISE DE IMPACTO DOS NÚMEROS DA POOL - ÚLTIMOS 50 SORTEIOS\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"Pool atual: {sorted(POOL_ATUAL)}\n")
        f.write(f"Número candidato a ENTRAR: 7 (apareceu em 39/50 sorteios = 78%)\n\n")
        f.write("=" * 100 + "\n\n")
        
        f.write("RANKING POR IMPACTO (menor = candidato a remoção):\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'Nº':>3} | {'Aparições':>10} | {'Em 14+':>8} | {'Em 13+':>8} | {'Em 12+':>8} | {'Impacto':>8} | {'Freq %':>7}\n")
        f.write("-" * 100 + "\n")
        
        for num, stats in sorted_numbers:
            freq_pct = (stats['aparicoes'] / 50) * 100
            f.write(f"{num:3d} | {stats['aparicoes']:10d} | {stats['em_14_acertos']:8d} | "
                   f"{stats['em_13_acertos']:8d} | {stats['em_12_acertos']:8d} | "
                   f"{stats['impacto_total']:8d} | {freq_pct:6.1f}%\n")
        
        f.write("\n" + "=" * 100 + "\n")
        f.write("RECOMENDAÇÃO:\n")
        f.write("-" * 100 + "\n\n")
        f.write(f"REMOVER: Número {candidato_remocao}\n")
        f.write(f"  Apareceu em apenas {stats_remocao['aparicoes']}/50 sorteios ({freq_remocao:.1f}%)\n")
        f.write(f"  Impacto total: {stats_remocao['impacto_total']} pontos\n\n")
        f.write(f"ADICIONAR: Número 7\n")
        f.write(f"  Frequência recente: 39/50 = 78%\n\n")
        f.write(f"NOVA POOL: {nova_pool}\n\n")
        f.write(f"Ganho de frequência: +{78.0 - freq_remocao:.1f} pontos percentuais\n")
        
        f.write("\n" + "=" * 100 + "\n")
        f.write("SIMULAÇÃO:\n")
        f.write(f"Score atual: {score_atual}\n")
        f.write(f"Score novo:  {score_novo}\n")
        f.write(f"Diferença:   {'+' if score_novo > score_atual else ''}{score_novo - score_atual} ({((score_novo/score_atual - 1) * 100):+.1f}%)\n")
    
    print(f"\n✓ Relatório salvo em: {output_path}")
    
    # Salvar nova pool
    nova_pool_path = Path('out/optimized/pool_com_numero_7.txt')
    with open(nova_pool_path, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, nova_pool)))
    
    print(f"✓ Nova pool salva em: {nova_pool_path}")

if __name__ == "__main__":
    analyze_pool_impact()

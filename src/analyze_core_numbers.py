import pandas as pd
from pathlib import Path

def analyze_core_numbers():
    # Pool de 18 números mais frios
    pool_frios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16, 17, 18, 19, 21, 22, 23]
    
    # Pool de 18 números mais quentes
    pool_quentes = [1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20, 22, 24, 25]
    
    # Interseção - números que aparecem em AMBAS as listas
    numeros_core = sorted(list(set(pool_frios) & set(pool_quentes)))
    
    # Números exclusivos
    frios_exclusivos = sorted([n for n in pool_frios if n not in pool_quentes])
    quentes_exclusivos = sorted([n for n in pool_quentes if n not in pool_frios])
    
    print("=" * 100)
    print("ANÁLISE DOS 11 NÚMEROS DA BASE (CORE)")
    print("=" * 100)
    
    print("\n🎯 OS 11 NÚMEROS QUE APARECEM EM AMBAS AS LISTAS (FRIOS E QUENTES):")
    print("-" * 100)
    print(f"\n{numeros_core}")
    print(f"\nTotal: {len(numeros_core)} números")
    
    # Análise de paridade
    pares_core = [n for n in numeros_core if n % 2 == 0]
    impares_core = [n for n in numeros_core if n % 2 != 0]
    
    print(f"\nParidade:")
    print(f"  Pares: {len(pares_core)} → {pares_core}")
    print(f"  Ímpares: {len(impares_core)} → {impares_core}")
    
    # Análise por dezena
    dezenas = {
        '01-05': [n for n in numeros_core if 1 <= n <= 5],
        '06-10': [n for n in numeros_core if 6 <= n <= 10],
        '11-15': [n for n in numeros_core if 11 <= n <= 15],
        '16-20': [n for n in numeros_core if 16 <= n <= 20],
        '21-25': [n for n in numeros_core if 21 <= n <= 25]
    }
    
    print(f"\nDistribuição por Dezena:")
    for dezena, nums in dezenas.items():
        print(f"  {dezena}: {len(nums)} números → {nums if nums else 'nenhum'}")
    
    print("\n" + "=" * 100)
    print("NÚMEROS EXCLUSIVOS DE CADA LISTA:")
    print("-" * 100)
    
    print(f"\n❄️ 7 Números EXCLUSIVAMENTE FRIOS:")
    print(f"   {frios_exclusivos}")
    
    print(f"\n🔥 7 Números EXCLUSIVAMENTE QUENTES:")
    print(f"   {quentes_exclusivos}")
    
    # Carregar dados históricos
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Contar frequência dos 11 números core
    print("\n" + "=" * 100)
    print("FREQUÊNCIA DOS 11 NÚMEROS CORE (HISTÓRICO COMPLETO)")
    print("-" * 100)
    
    total_sorteios = len(df)
    
    frequencias_core = {}
    for numero in numeros_core:
        count = 0
        for idx, row in df.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                count += 1
        frequencias_core[numero] = count
    
    print(f"\n{'Número':>8} | {'Aparições':>11} | {'Frequência':>12} | {'Status':>15}")
    print("-" * 60)
    
    for numero in sorted(numeros_core):
        freq = frequencias_core[numero]
        freq_pct = (freq / total_sorteios) * 100
        
        if freq_pct >= 60.5:
            status = "🔥 Acima média"
        elif freq_pct >= 59.5:
            status = "😐 Média"
        else:
            status = "❄️ Abaixo média"
        
        print(f"{numero:8d} | {freq:11d} | {freq_pct:11.2f}% | {status:>15}")
    
    # Últimos 50 sorteios
    ultimos_50 = df.tail(50)
    
    print("\n" + "=" * 100)
    print("FREQUÊNCIA DOS 11 NÚMEROS CORE (ÚLTIMOS 50 SORTEIOS)")
    print("-" * 100)
    
    frequencias_core_50 = {}
    for numero in numeros_core:
        count = 0
        for idx, row in ultimos_50.iterrows():
            numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
            if numero in numeros_sorteados:
                count += 1
        frequencias_core_50[numero] = count
    
    print(f"\n{'Número':>8} | {'Aparições':>11} | {'Frequência':>12} | {'Status':>20}")
    print("-" * 65)
    
    for numero in sorted(numeros_core):
        freq = frequencias_core_50[numero]
        freq_pct = (freq / 50) * 100
        
        if freq_pct >= 70:
            status = "🔥🔥 Muito Quente"
        elif freq_pct >= 60:
            status = "🔥 Quente"
        elif freq_pct >= 50:
            status = "😐 Normal"
        else:
            status = "❄️ Frio"
        
        print(f"{numero:8d} | {freq:11d} | {freq_pct:11.1f}% | {status:>20}")
    
    # Média de aparições dos 11 core nos últimos 50
    total_core_50 = sum(frequencias_core_50.values())
    media_core_50 = total_core_50 / 11
    
    print("\n" + "=" * 100)
    print("ANÁLISE DE COBERTURA COM OS 11 NÚMEROS CORE")
    print("-" * 100)
    
    # Calcular quantos dos 11 aparecem em cada sorteio
    cobertura_por_sorteio = []
    
    for idx, row in ultimos_50.iterrows():
        concurso = row['Concurso']
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        core_no_sorteio = [n for n in numeros_sorteados if n in numeros_core]
        qtd = len(core_no_sorteio)
        cobertura_por_sorteio.append(qtd)
    
    media_cobertura = sum(cobertura_por_sorteio) / len(cobertura_por_sorteio)
    
    print(f"\nNos últimos 50 sorteios:")
    print(f"  Mínimo de números core em 1 sorteio: {min(cobertura_por_sorteio)}")
    print(f"  Máximo de números core em 1 sorteio: {max(cobertura_por_sorteio)}")
    print(f"  Média de números core por sorteio: {media_cobertura:.2f} de 11")
    print(f"  Taxa de cobertura: {(media_cobertura/15)*100:.1f}% dos 15 números sorteados")
    
    # Salvar relatório
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'numeros_core_base.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("OS 11 NÚMEROS DA BASE (CORE)\n")
        f.write("=" * 100 + "\n\n")
        f.write("Números que aparecem em AMBAS as listas (Frios E Quentes):\n\n")
        f.write(f"{numeros_core}\n\n")
        f.write("=" * 100 + "\n\n")
        f.write("CARACTERÍSTICAS:\n\n")
        f.write(f"Total: {len(numeros_core)} números\n")
        f.write(f"Pares: {len(pares_core)} → {pares_core}\n")
        f.write(f"Ímpares: {len(impares_core)} → {impares_core}\n\n")
        f.write("Distribuição por Dezena:\n")
        for dezena, nums in dezenas.items():
            f.write(f"  {dezena}: {len(nums)} números → {nums if nums else 'nenhum'}\n")
        f.write("\n" + "=" * 100 + "\n\n")
        f.write("FREQUÊNCIA HISTÓRICA:\n\n")
        for numero in sorted(numeros_core):
            freq = frequencias_core[numero]
            freq_pct = (freq / total_sorteios) * 100
            f.write(f"Número {numero:2d}: {freq:4d} aparições ({freq_pct:.2f}%)\n")
        f.write("\n" + "=" * 100 + "\n\n")
        f.write("ÚLTIMOS 50 SORTEIOS:\n\n")
        for numero in sorted(numeros_core):
            freq = frequencias_core_50[numero]
            freq_pct = (freq / 50) * 100
            f.write(f"Número {numero:2d}: {freq:2d} aparições ({freq_pct:.1f}%)\n")
        f.write(f"\nMédia de cobertura: {media_cobertura:.2f} de 11 números por sorteio\n")
        f.write(f"Taxa de cobertura: {(media_cobertura/15)*100:.1f}% dos números sorteados\n")
    
    print(f"\n✓ Relatório salvo em: {report_path}")
    
    print("\n" + "=" * 100)
    print("RECOMENDAÇÃO:")
    print("-" * 100)
    print(f"\n✅ Use estes 11 números como BASE da sua estratégia:")
    print(f"   {numeros_core}")
    print(f"\n✅ Eles representam o 'núcleo estável' da Lotofácil")
    print(f"✅ Média de {media_cobertura:.2f} aparições por sorteio nos últimos 50")
    print(f"✅ Equivale a {(media_cobertura/15)*100:.1f}% dos números sorteados")
    print("=" * 100)
    
    return {
        'core': numeros_core,
        'frios_exclusivos': frios_exclusivos,
        'quentes_exclusivos': quentes_exclusivos,
        'media_cobertura': media_cobertura
    }

if __name__ == "__main__":
    resultado = analyze_core_numbers()

import pandas as pd
from pathlib import Path

# Pool otimizada
POOL_OTIMIZADA = {1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25}

def analyze_last_50():
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Últimos 50 sorteios
    last_50 = df.tail(50).copy()
    
    results = {
        15: [],
        14: [],
        13: [],
        12: [],
        11: [],
        10: []
    }
    
    print("=" * 80)
    print("ANÁLISE DOS ÚLTIMOS 50 SORTEIOS - POOL OTIMIZADA")
    print("=" * 80)
    print(f"\nPool: {sorted(POOL_OTIMIZADA)}")
    print(f"\nPeríodo: Concurso {last_50.iloc[0]['Concurso']} até {last_50.iloc[-1]['Concurso']}")
    print(f"Data: {last_50.iloc[0]['Data Sorteio']} até {last_50.iloc[-1]['Data Sorteio']}")
    print("\n" + "=" * 80)
    
    # Analisar cada sorteio
    for idx, row in last_50.iterrows():
        concurso = row['Concurso']
        data = row['Data Sorteio']
        
        # Coletar números sorteados
        numeros_sorteados = set()
        for i in range(1, 16):
            numeros_sorteados.add(row[f'Bola{i}'])
        
        # Contar acertos
        acertos = len(POOL_OTIMIZADA & numeros_sorteados)
        
        if acertos >= 10:
            results[acertos].append({
                'concurso': concurso,
                'data': data,
                'sorteados': sorted(numeros_sorteados),
                'acertos': acertos
            })
    
    # Relatório por categoria
    print("\nRESULTADOS POR CATEGORIA:")
    print("-" * 80)
    
    total_acertos = 0
    for acertos in [15, 14, 13, 12, 11, 10]:
        quantidade = len(results[acertos])
        total_acertos += quantidade
        print(f"\n{acertos} acertos: {quantidade} sorteios")
        
        if quantidade > 0:
            for r in results[acertos]:
                numeros_faltaram = sorted(POOL_OTIMIZADA - set(r['sorteados']))
                numeros_extras = sorted(set(r['sorteados']) - POOL_OTIMIZADA)
                
                print(f"  • Concurso {r['concurso']} ({r['data']})")
                print(f"    Sorteados: {r['sorteados']}")
                print(f"    Faltaram da pool: {numeros_faltaram}")
                print(f"    Extras (fora da pool): {numeros_extras}")
    
    # Estatísticas gerais
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS GERAIS:")
    print("-" * 80)
    print(f"Total de sorteios analisados: 50")
    print(f"Sorteios com 10+ acertos: {total_acertos} ({total_acertos/50*100:.1f}%)")
    print(f"\nDistribuição:")
    for acertos in [15, 14, 13, 12, 11, 10]:
        qtd = len(results[acertos])
        perc = qtd/50*100
        print(f"  {acertos} acertos: {qtd:2d} ({perc:5.1f}%)")
    
    # Média de acertos
    total_pontos = sum(acertos * len(results[acertos]) for acertos in results)
    media = total_pontos / 50
    print(f"\nMédia de acertos por sorteio: {media:.2f}")
    
    # Salvar relatório
    output_path = Path('out/optimized/analise_ultimos_50_sorteios.txt')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ANÁLISE DOS ÚLTIMOS 50 SORTEIOS - POOL OTIMIZADA\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Pool: {sorted(POOL_OTIMIZADA)}\n\n")
        f.write(f"Período: Concurso {last_50.iloc[0]['Concurso']} até {last_50.iloc[-1]['Concurso']}\n")
        f.write(f"Data: {last_50.iloc[0]['Data Sorteio']} até {last_50.iloc[-1]['Data Sorteio']}\n\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("RESULTADOS POR CATEGORIA:\n")
        f.write("-" * 80 + "\n")
        
        for acertos in [15, 14, 13, 12, 11, 10]:
            quantidade = len(results[acertos])
            f.write(f"\n{acertos} acertos: {quantidade} sorteios\n")
            
            if quantidade > 0:
                for r in results[acertos]:
                    numeros_faltaram = sorted(POOL_OTIMIZADA - set(r['sorteados']))
                    numeros_extras = sorted(set(r['sorteados']) - POOL_OTIMIZADA)
                    
                    f.write(f"  • Concurso {r['concurso']} ({r['data']})\n")
                    f.write(f"    Sorteados: {r['sorteados']}\n")
                    f.write(f"    Faltaram da pool: {numeros_faltaram}\n")
                    f.write(f"    Extras (fora da pool): {numeros_extras}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("ESTATÍSTICAS GERAIS:\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total de sorteios analisados: 50\n")
        f.write(f"Sorteios com 10+ acertos: {total_acertos} ({total_acertos/50*100:.1f}%)\n\n")
        f.write("Distribuição:\n")
        for acertos in [15, 14, 13, 12, 11, 10]:
            qtd = len(results[acertos])
            perc = qtd/50*100
            f.write(f"  {acertos} acertos: {qtd:2d} ({perc:5.1f}%)\n")
        
        f.write(f"\nMédia de acertos por sorteio: {media:.2f}\n")
    
    print(f"\n✓ Relatório salvo em: {output_path}")

if __name__ == "__main__":
    analyze_last_50()

import pandas as pd
from pathlib import Path

def generate_coldest_summary():
    # Pool de 18 números mais frios
    pool_frios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16, 17, 18, 19, 21, 22, 23]
    
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    # Pegar últimos 50 sorteios
    ultimos_50 = df.tail(50).copy()
    
    print("=" * 100)
    print("LISTA DOS ÚLTIMOS 50 SORTEIOS - NÚMEROS FRIOS")
    print("=" * 100)
    print(f"\nPool de 18 Números Frios: {pool_frios}")
    print("\n" + "=" * 100)
    
    resultados = []
    
    for idx, row in ultimos_50.iterrows():
        concurso = row['Concurso']
        numeros_sorteados = sorted([row[f'Bola{i}'] for i in range(1, 16)])
        
        # Identificar quais números frios saíram
        frios_sorteados = sorted([num for num in numeros_sorteados if num in pool_frios])
        qtd_frios = len(frios_sorteados)
        
        resultados.append({
            'Concurso': concurso,
            'Numeros_Sorteados': numeros_sorteados,
            'Qtd_Frios': qtd_frios,
            'Frios_Sorteados': frios_sorteados
        })
    
    # Tabela formatada
    print(f"{'#':>3} | {'Concurso':>8} | {'Total Frios':>12} | Números Frios que Saíram")
    print("-" * 100)
    
    for i, r in enumerate(resultados, 1):
        frios_str = ', '.join([f"{n:02d}" for n in r['Frios_Sorteados']])
        print(f"{i:3d} | {r['Concurso']:8d} | {r['Qtd_Frios']:12d} | {frios_str}")
    
    # Estatísticas
    qtds_frios = [r['Qtd_Frios'] for r in resultados]
    
    print("\n" + "=" * 100)
    print("RESUMO ESTATÍSTICO")
    print("=" * 100)
    print(f"Total de sorteios analisados: 50")
    print(f"Mínimo de frios por sorteio: {min(qtds_frios)}")
    print(f"Máximo de frios por sorteio: {max(qtds_frios)}")
    print(f"Média de frios por sorteio: {sum(qtds_frios)/len(qtds_frios):.2f}")
    print(f"Total de números frios sorteados: {sum(qtds_frios)}")
    
    # Salvar em arquivo TXT formatado
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'lista_50_sorteios_frios.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("LISTA DOS ÚLTIMOS 50 SORTEIOS - NÚMEROS FRIOS\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"Pool de 18 Números Frios: {pool_frios}\n\n")
        f.write("=" * 100 + "\n\n")
        
        f.write(f"{'#':>3} | {'Concurso':>8} | {'Total Frios':>12} | Números Frios que Saíram\n")
        f.write("-" * 100 + "\n")
        
        for i, r in enumerate(resultados, 1):
            frios_str = ', '.join([f"{n:02d}" for n in r['Frios_Sorteados']])
            f.write(f"{i:3d} | {r['Concurso']:8d} | {r['Qtd_Frios']:12d} | {frios_str}\n")
        
        f.write("\n" + "=" * 100 + "\n")
        f.write("RESUMO ESTATÍSTICO\n")
        f.write("=" * 100 + "\n")
        f.write(f"Total de sorteios analisados: 50\n")
        f.write(f"Mínimo de frios por sorteio: {min(qtds_frios)}\n")
        f.write(f"Máximo de frios por sorteio: {max(qtds_frios)}\n")
        f.write(f"Média de frios por sorteio: {sum(qtds_frios)/len(qtds_frios):.2f}\n")
        f.write(f"Total de números frios sorteados: {sum(qtds_frios)}\n")
    
    print(f"\n✓ Lista completa salva em: {report_path}")
    
    # Salvar em CSV
    csv_path = output_dir / 'lista_50_sorteios_frios.csv'
    df_resultado = pd.DataFrame([
        {
            'Posicao': i,
            'Concurso': r['Concurso'],
            'Total_Frios': r['Qtd_Frios'],
            'Numeros_Frios': ', '.join([f"{n:02d}" for n in r['Frios_Sorteados']])
        }
        for i, r in enumerate(resultados, 1)
    ])
    df_resultado.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"✓ CSV salvo em: {csv_path}")
    
    return resultados

if __name__ == "__main__":
    resultados = generate_coldest_summary()
    
    print("\n" + "=" * 100)
    print("✓ Análise concluída com sucesso!")
    print("=" * 100)

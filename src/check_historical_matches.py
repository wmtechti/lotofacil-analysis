import pandas as pd
from pathlib import Path

def check_perfect_matches():
    # Pool de 19 números
    pool_19 = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 25]
    
    # Carregar sorteios
    df = pd.read_csv('data/lotofacil_sorteios.csv')
    
    print("=" * 120)
    print("ANÁLISE DE ACERTOS HISTÓRICOS COM O POOL DE 19 NÚMEROS")
    print("=" * 120)
    print(f"\nPool analisado: {pool_19}")
    print(f"Total de números no pool: {len(pool_19)}")
    print(f"\nTotal de sorteios analisados: {len(df)}")
    
    # Buscar sorteios com 15, 14 e 13 acertos
    sorteios_15_acertos = []
    sorteios_14_acertos = []
    sorteios_13_acertos = []
    
    for idx, row in df.iterrows():
        concurso = row['Concurso']
        data = row['Data Sorteio']
        numeros_sorteados = sorted([row[f'Bola{i}'] for i in range(1, 16)])
        
        # Contar quantos números do sorteio estão no pool
        acertos = len([n for n in numeros_sorteados if n in pool_19])
        
        if acertos == 15:
            sorteios_15_acertos.append({
                'Concurso': concurso,
                'Data': data,
                'Numeros': numeros_sorteados,
                'Acertos': acertos
            })
        elif acertos == 14:
            numeros_no_pool = [n for n in numeros_sorteados if n in pool_19]
            numero_fora = [n for n in numeros_sorteados if n not in pool_19]
            sorteios_14_acertos.append({
                'Concurso': concurso,
                'Data': data,
                'Numeros': numeros_sorteados,
                'No_Pool': numeros_no_pool,
                'Fora_Pool': numero_fora,
                'Acertos': acertos
            })
        elif acertos == 13:
            numeros_no_pool = [n for n in numeros_sorteados if n in pool_19]
            numeros_fora = [n for n in numeros_sorteados if n not in pool_19]
            sorteios_13_acertos.append({
                'Concurso': concurso,
                'Data': data,
                'Numeros': numeros_sorteados,
                'No_Pool': numeros_no_pool,
                'Fora_Pool': numeros_fora,
                'Acertos': acertos
            })
    
    # Mostrar resultados
    print("\n" + "=" * 120)
    print("🎯 SORTEIOS COM 15 ACERTOS (100% - JOGO PERFEITO!)")
    print("=" * 120)
    
    if sorteios_15_acertos:
        print(f"\n✅ ENCONTRADOS {len(sorteios_15_acertos)} SORTEIOS COM 15 ACERTOS!\n")
        print(f"{'#':>4} | {'Concurso':>9} | {'Data':>12} | Números Sorteados")
        print("-" * 120)
        
        for i, s in enumerate(sorteios_15_acertos, 1):
            nums_str = ', '.join([f"{n:02d}" for n in s['Numeros']])
            print(f"{i:4d} | {s['Concurso']:9d} | {s['Data']:>12} | {nums_str}")
    else:
        print("\n❌ NENHUM sorteio histórico com 15 acertos (jogo perfeito).")
        print("   Isso significa que em TODOS os sorteios, pelo menos 1 número estava fora do pool.")
    
    print("\n" + "=" * 120)
    print("🎯 SORTEIOS COM 14 ACERTOS")
    print("=" * 120)
    
    if sorteios_14_acertos:
        print(f"\n✅ ENCONTRADOS {len(sorteios_14_acertos)} SORTEIOS COM 14 ACERTOS!\n")
        print(f"{'#':>4} | {'Concurso':>9} | {'Data':>12} | {'Fora':>5} | Números Sorteados")
        print("-" * 120)
        
        for i, s in enumerate(sorteios_14_acertos[:50], 1):  # Limitar a 50 primeiros
            nums_str = ', '.join([f"**{n:02d}**" if n not in pool_19 else f"{n:02d}" for n in s['Numeros']])
            fora_str = ', '.join([f"{n:02d}" for n in s['Fora_Pool']])
            print(f"{i:4d} | {s['Concurso']:9d} | {s['Data']:>12} | {fora_str:>5} | {nums_str}")
        
        if len(sorteios_14_acertos) > 50:
            print(f"\n... e mais {len(sorteios_14_acertos) - 50} sorteios (mostrando apenas os primeiros 50)")
    else:
        print("\n❌ NENHUM sorteio histórico com 14 acertos.")
    
    print("\n" + "=" * 120)
    print("🎯 SORTEIOS COM 13 ACERTOS")
    print("=" * 120)
    
    if sorteios_13_acertos:
        print(f"\n✅ ENCONTRADOS {len(sorteios_13_acertos)} SORTEIOS COM 13 ACERTOS!\n")
        print(f"{'#':>4} | {'Concurso':>9} | {'Data':>12} | {'Fora Pool':>15} | Números Sorteados")
        print("-" * 120)
        
        for i, s in enumerate(sorteios_13_acertos[:50], 1):  # Limitar a 50 primeiros
            fora_str = ', '.join([f"{n:02d}" for n in s['Fora_Pool']])
            nums_str = ', '.join([f"**{n:02d}**" if n not in pool_19 else f"{n:02d}" for n in s['Numeros']])
            print(f"{i:4d} | {s['Concurso']:9d} | {s['Data']:>12} | {fora_str:>15} | {nums_str}")
        
        if len(sorteios_13_acertos) > 50:
            print(f"\n... e mais {len(sorteios_13_acertos) - 50} sorteios (mostrando apenas os primeiros 50)")
    else:
        print("\n❌ NENHUM sorteio histórico com 13 acertos.")
    
    # Estatísticas gerais
    print("\n" + "=" * 120)
    print("📊 ESTATÍSTICAS GERAIS")
    print("=" * 120)
    
    total_sorteios = len(df)
    
    print(f"\nTotal de sorteios analisados: {total_sorteios}")
    print(f"\nSorteios com 15 acertos: {len(sorteios_15_acertos)} ({(len(sorteios_15_acertos)/total_sorteios)*100:.2f}%)")
    print(f"Sorteios com 14 acertos: {len(sorteios_14_acertos)} ({(len(sorteios_14_acertos)/total_sorteios)*100:.2f}%)")
    print(f"Sorteios com 13 acertos: {len(sorteios_13_acertos)} ({(len(sorteios_13_acertos)/total_sorteios)*100:.2f}%)")
    print(f"Sorteios com 13+ acertos: {len(sorteios_15_acertos) + len(sorteios_14_acertos) + len(sorteios_13_acertos)} ({((len(sorteios_15_acertos) + len(sorteios_14_acertos) + len(sorteios_13_acertos))/total_sorteios)*100:.2f}%)")
    
    # Distribuição completa
    distribuicao = {}
    for idx, row in df.iterrows():
        numeros_sorteados = [row[f'Bola{i}'] for i in range(1, 16)]
        acertos = len([n for n in numeros_sorteados if n in pool_19])
        distribuicao[acertos] = distribuicao.get(acertos, 0) + 1
    
    print("\n" + "=" * 120)
    print("DISTRIBUIÇÃO COMPLETA DE ACERTOS")
    print("-" * 120)
    print(f"{'Acertos':>10} | {'Sorteios':>10} | {'Percentual':>12} | Barra")
    print("-" * 120)
    
    for acertos in sorted(distribuicao.keys(), reverse=True):
        count = distribuicao[acertos]
        pct = (count / total_sorteios) * 100
        barra = "█" * int(pct / 2)
        print(f"{acertos:10d} | {count:10d} | {pct:11.2f}% | {barra}")
    
    # Salvar relatórios
    output_dir = Path('out/estrategia_frios')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Relatório de 15 acertos
    if sorteios_15_acertos:
        report_15_path = output_dir / 'sorteios_15_acertos.txt'
        with open(report_15_path, 'w', encoding='utf-8') as f:
            f.write("=" * 120 + "\n")
            f.write("SORTEIOS COM 15 ACERTOS (JOGO PERFEITO)\n")
            f.write("=" * 120 + "\n\n")
            for s in sorteios_15_acertos:
                nums_str = ', '.join([f"{n:02d}" for n in s['Numeros']])
                f.write(f"Concurso {s['Concurso']:5d} | Data: {s['Data']} | Números: {nums_str}\n")
        print(f"\n✓ Sorteios com 15 acertos salvos em: {report_15_path}")
    
    # Relatório de 14 acertos
    if sorteios_14_acertos:
        report_14_path = output_dir / 'sorteios_14_acertos.txt'
        with open(report_14_path, 'w', encoding='utf-8') as f:
            f.write("=" * 120 + "\n")
            f.write(f"SORTEIOS COM 14 ACERTOS (Total: {len(sorteios_14_acertos)})\n")
            f.write("=" * 120 + "\n\n")
            for s in sorteios_14_acertos:
                nums_str = ', '.join([f"{n:02d}" for n in s['Numeros']])
                fora_str = ', '.join([f"{n:02d}" for n in s['Fora_Pool']])
                f.write(f"Concurso {s['Concurso']:5d} | Data: {s['Data']} | Fora: {fora_str} | Números: {nums_str}\n")
        print(f"✓ Sorteios com 14 acertos salvos em: {report_14_path}")
    
    # Relatório de 13 acertos
    if sorteios_13_acertos:
        report_13_path = output_dir / 'sorteios_13_acertos.txt'
        with open(report_13_path, 'w', encoding='utf-8') as f:
            f.write("=" * 120 + "\n")
            f.write(f"SORTEIOS COM 13 ACERTOS (Total: {len(sorteios_13_acertos)})\n")
            f.write("=" * 120 + "\n\n")
            for s in sorteios_13_acertos:
                nums_str = ', '.join([f"{n:02d}" for n in s['Numeros']])
                fora_str = ', '.join([f"{n:02d}" for n in s['Fora_Pool']])
                f.write(f"Concurso {s['Concurso']:5d} | Data: {s['Data']} | Fora: {fora_str} | Números: {nums_str}\n")
        print(f"✓ Sorteios com 13 acertos salvos em: {report_13_path}")
    
    print("\n" + "=" * 120)
    
    return {
        '15_acertos': len(sorteios_15_acertos),
        '14_acertos': len(sorteios_14_acertos),
        '13_acertos': len(sorteios_13_acertos),
        'distribuicao': distribuicao
    }

if __name__ == "__main__":
    resultado = check_perfect_matches()
    
    print("\n✓ Análise concluída!")

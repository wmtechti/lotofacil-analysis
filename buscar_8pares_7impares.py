"""
Buscar combinações com 8 pares e 7 ímpares no arquivo
combinacoes_soma_195_composicao_4_2_3_2_4.csv
"""

import pandas as pd
from pathlib import Path

# Ler arquivo
arquivo = Path('data/combinacoes_soma_195_composicao_4_2_3_2_4.csv')
df = pd.read_csv(arquivo)

print("="*70)
print("BUSCANDO COMBINAÇÕES COM 8 PARES E 7 ÍMPARES")
print("="*70)

# Filtrar combinações
combinacoes_encontradas = []

for idx, row in df.iterrows():
    # Extrair números
    combo_str = row['Combinacao']
    numeros = [int(n) for n in combo_str.split('-')]
    
    # Contar pares e ímpares
    pares = sum(1 for n in numeros if n % 2 == 0)
    impares = 15 - pares
    
    # Verificar se corresponde ao critério
    if pares == 8 and impares == 7:
        nums_pares = [n for n in numeros if n % 2 == 0]
        nums_impares = [n for n in numeros if n % 2 != 0]
        
        combinacoes_encontradas.append({
            'ID': row['ID'],
            'Combinacao': combo_str,
            'Pares': pares,
            'Impares': impares,
            'Numeros_Pares': nums_pares,
            'Numeros_Impares': nums_impares,
            'c1': row['c1'],
            'c2': row['c2'],
            'c3': row['c3'],
            'c4': row['c4'],
            'c5': row['c5']
        })

print(f"\n✅ Total encontrado: {len(combinacoes_encontradas)} combinações\n")

if len(combinacoes_encontradas) > 0:
    # Mostrar a primeira combinação
    primeira = combinacoes_encontradas[0]
    
    print("="*70)
    print("COMBINAÇÃO ENCONTRADA:")
    print("="*70)
    print(f"\nID: {primeira['ID']}")
    print(f"Combinação: {primeira['Combinacao']}")
    print(f"\nParidade: {primeira['Pares']} pares / {primeira['Impares']} ímpares")
    print(f"\nNúmeros PARES ({len(primeira['Numeros_Pares'])}): {primeira['Numeros_Pares']}")
    print(f"Números ÍMPARES ({len(primeira['Numeros_Impares'])}): {primeira['Numeros_Impares']}")
    print(f"\nComposição por grupos:")
    print(f"  c1 (1-5):   {primeira['c1']}")
    print(f"  c2 (6-10):  {primeira['c2']}")
    print(f"  c3 (11-15): {primeira['c3']}")
    print(f"  c4 (16-20): {primeira['c4']}")
    print(f"  c5 (21-25): {primeira['c5']}")
    print("="*70)
    
    # Mostrar mais algumas se houver
    if len(combinacoes_encontradas) > 1:
        print(f"\n📋 Mais {min(9, len(combinacoes_encontradas)-1)} exemplos:")
        print("-"*70)
        for i, combo in enumerate(combinacoes_encontradas[1:10], 2):
            print(f"{i:2d}. {combo['Combinacao']} (ID: {combo['ID']})")
        
        if len(combinacoes_encontradas) > 10:
            print(f"\n... e mais {len(combinacoes_encontradas) - 10} combinações")
else:
    print("⚠️ Nenhuma combinação encontrada com 8 pares e 7 ímpares!")

print("\n" + "="*70)

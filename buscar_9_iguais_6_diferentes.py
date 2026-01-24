"""
Buscar combinações com 9 números iguais e 6 diferentes
em relação à combinação de referência
"""

import pandas as pd
from pathlib import Path

# Combinação de referência
combo_ref_str = "01-02-03-04-06-07-11-14-15-18-20-22-23-24-25"
combo_ref = set([int(n) for n in combo_ref_str.split('-')])

print("="*70)
print("BUSCANDO COMBINAÇÕES COM 9 NÚMEROS IGUAIS E 6 DIFERENTES")
print("="*70)
print(f"\nCombinação de referência:")
print(f"{combo_ref_str}")
print(f"Números: {sorted(combo_ref)}")

# Ler arquivo
arquivo = Path('data/combinacoes_soma_195_composicao_4_2_3_2_4.csv')
df = pd.read_csv(arquivo)

# Filtrar combinações
combinacoes_encontradas = []

for idx, row in df.iterrows():
    # Extrair números
    combo_str = row['Combinacao']
    numeros = set([int(n) for n in combo_str.split('-')])
    
    # Contar números em comum
    em_comum = combo_ref & numeros
    diferentes = combo_ref ^ numeros  # Diferença simétrica (números que não estão em ambos)
    
    # Números que estão apenas na referência
    so_na_ref = combo_ref - numeros
    # Números que estão apenas na combinação atual
    so_na_atual = numeros - combo_ref
    
    # Verificar se tem exatamente 9 em comum (6 diferentes)
    if len(em_comum) == 9:
        combinacoes_encontradas.append({
            'ID': row['ID'],
            'Combinacao': combo_str,
            'Em_Comum': sorted(em_comum),
            'Qtd_Comum': len(em_comum),
            'Saem': sorted(so_na_ref),
            'Entram': sorted(so_na_atual),
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
    print(f"\n✅ NÚMEROS EM COMUM ({primeira['Qtd_Comum']}):")
    print(f"   {primeira['Em_Comum']}")
    print(f"\n❌ SAEM da referência ({len(primeira['Saem'])}):")
    print(f"   {primeira['Saem']}")
    print(f"\n➕ ENTRAM na nova combinação ({len(primeira['Entram'])}):")
    print(f"   {primeira['Entram']}")
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
            print(f"{i:2d}. {combo['Combinacao']}")
            print(f"    Saem: {combo['Saem']} → Entram: {combo['Entram']}")
        
        if len(combinacoes_encontradas) > 10:
            print(f"\n... e mais {len(combinacoes_encontradas) - 10} combinações")
else:
    print("⚠️ Nenhuma combinação encontrada com 9 números iguais!")

print("\n" + "="*70)

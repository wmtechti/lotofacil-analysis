"""
Filtrar combinações com composição específica 4-2-3-2-4
do arquivo combinacoes_soma_195.csv
"""

import pandas as pd
from pathlib import Path

# Definir grupos
grupos = {
    'c1': list(range(1, 6)),     # 1-5
    'c2': list(range(6, 11)),    # 6-10
    'c3': list(range(11, 16)),   # 11-15
    'c4': list(range(16, 21)),   # 16-20
    'c5': list(range(21, 26))    # 21-25
}

# Composição alvo
composicao_alvo = (4, 2, 3, 2, 4)

print("="*70)
print("FILTRANDO COMBINAÇÕES COM COMPOSIÇÃO 4-2-3-2-4")
print("="*70)
print(f"\nComposição alvo:")
print(f"  c1 (1-5):   {composicao_alvo[0]} números")
print(f"  c2 (6-10):  {composicao_alvo[1]} números")
print(f"  c3 (11-15): {composicao_alvo[2]} números")
print(f"  c4 (16-20): {composicao_alvo[3]} números")
print(f"  c5 (21-25): {composicao_alvo[4]} números")

# Ler arquivo
arquivo_entrada = Path('data/combinacoes_soma_195.csv')
df = pd.read_csv(arquivo_entrada)

print(f"\n📊 Total de combinações no arquivo: {len(df):,}")

# Filtrar combinações com a composição específica
combinacoes_filtradas = []

for idx, row in df.iterrows():
    # Extrair números da combinação
    combo_str = row['Combinacao']
    numeros = [int(n) for n in combo_str.split('-')]
    
    # Contar por grupo
    c1 = sum(1 for n in numeros if n in grupos['c1'])
    c2 = sum(1 for n in numeros if n in grupos['c2'])
    c3 = sum(1 for n in numeros if n in grupos['c3'])
    c4 = sum(1 for n in numeros if n in grupos['c4'])
    c5 = sum(1 for n in numeros if n in grupos['c5'])
    
    composicao = (c1, c2, c3, c4, c5)
    
    # Verificar se corresponde à composição alvo
    if composicao == composicao_alvo:
        combinacoes_filtradas.append({
            'ID': len(combinacoes_filtradas) + 1,
            'Soma': row['Soma'],
            'Combinacao': row['Combinacao'],
            'Numeros': row['Numeros'],
            'c1': c1,
            'c2': c2,
            'c3': c3,
            'c4': c4,
            'c5': c5
        })

# Criar DataFrame com resultados
df_filtrado = pd.DataFrame(combinacoes_filtradas)

# Salvar arquivo
arquivo_saida = Path('data/combinacoes_soma_195_composicao_4_2_3_2_4.csv')
df_filtrado.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')

print(f"\n✅ Combinações filtradas: {len(combinacoes_filtradas):,}")
print(f"📁 Arquivo salvo: {arquivo_saida}")

# Mostrar primeiras 10 combinações
if len(combinacoes_filtradas) > 0:
    print(f"\n{'='*70}")
    print("PRIMEIRAS 10 COMBINAÇÕES FILTRADAS:")
    print(f"{'='*70}")
    print(df_filtrado.head(10)[['ID', 'Combinacao', 'c1', 'c2', 'c3', 'c4', 'c5']].to_string(index=False))
    
    print(f"\n{'='*70}")
    print(f"Total: {len(combinacoes_filtradas):,} combinações com composição 4-2-3-2-4")
    print(f"{'='*70}")
else:
    print("\n⚠️ Nenhuma combinação encontrada com essa composição!")

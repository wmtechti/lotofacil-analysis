import pandas as pd

df = pd.read_csv('out/lotofacil/numeros_quentes_frios.csv')

top18 = df.nlargest(18, 'freq')['numero'].tolist()
top16 = df.nlargest(16, 'freq')['numero'].tolist()

substituidos = [n for n in top18 if n not in top16]

print('='*80)
print('COMPARAÇÃO DAS ESTRATÉGIAS')
print('='*80)
print()

print('Estratégia Original (18 mais quentes):')
print(f"   {', '.join(map(str, sorted(top18)))}")
print()

print('Estratégia Otimizada (16 quentes + 2 frios):')
print(f"   {', '.join(map(str, sorted(top16 + [6, 8])))}")
print()

print('='*80)
print(f'NÚMEROS REMOVIDOS (substituídos por 6 e 8):')
print('='*80)
print()

for n in sorted(substituidos):
    row = df[df['numero'] == n].iloc[0]
    print(f"  Número {n:2d}: Freq {int(row['freq']):4d}, Desvio {row['desvio_%']:+6.2f}%, {row['categoria']}")

print()
print('='*80)
print('NÚMEROS ADICIONADOS:')
print('='*80)
print()

for n in [6, 8]:
    row = df[df['numero'] == n].iloc[0]
    print(f"  Número {n:2d}: Freq {int(row['freq']):4d}, Desvio {row['desvio_%']:+6.2f}%, {row['categoria']}")

print()

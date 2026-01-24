"""Análise de padrões de composição - Linhas 28-47"""

from collections import Counter

# Dados das linhas 28 a 47
dados = [
    (3570, [4, 2, 3, 3, 3]),
    (3571, [4, 2, 4, 2, 3]),
    (3572, [4, 2, 3, 4, 2]),
    (3573, [2, 3, 4, 3, 3]),
    (3574, [4, 2, 3, 4, 2]),
    (3575, [3, 4, 4, 1, 3]),
    (3576, [4, 3, 1, 3, 4]),
    (3577, [4, 4, 1, 3, 3]),
    (3578, [4, 4, 1, 3, 3]),
    (3579, [4, 2, 3, 3, 3]),
    (3580, [3, 3, 3, 3, 3]),
    (3581, [4, 4, 2, 3, 2]),
    (3582, [2, 5, 3, 2, 3]),
    (3583, [3, 3, 4, 0, 5]),
    (3584, [3, 3, 2, 4, 3]),
    (3585, [3, 3, 1, 4, 4]),
    (3586, [2, 2, 5, 2, 4]),
    (3587, [3, 3, 3, 5, 1]),
    (3588, [2, 3, 3, 3, 4]),
    (3589, [4, 2, 3, 2, 4]),
]

# Contar padrões exatos
padroes_exatos = Counter()
for concurso, padrao in dados:
    padrao_str = f"{padrao[0]}-{padrao[1]}-{padrao[2]}-{padrao[3]}-{padrao[4]}"
    padroes_exatos[padrao_str] += 1

# Contar padrões ordenados (independente da posição)
padroes_ordenados = Counter()
for concurso, padrao in dados:
    padrao_ordenado = tuple(sorted(padrao))
    padrao_str = f"{padrao_ordenado[0]}-{padrao_ordenado[1]}-{padrao_ordenado[2]}-{padrao_ordenado[3]}-{padrao_ordenado[4]}"
    padroes_ordenados[padrao_str] += 1

# Análise de valores individuais por coluna
valores_c1 = Counter([p[0] for _, p in dados])
valores_c2 = Counter([p[1] for _, p in dados])
valores_c3 = Counter([p[2] for _, p in dados])
valores_c4 = Counter([p[3] for _, p in dados])
valores_c5 = Counter([p[4] for _, p in dados])

print("="*70)
print("ANÁLISE DE PADRÕES - COMPOSIÇÃO LOTOFÁCIL (20 CONCURSOS)")
print("="*70)

print("\n📊 PADRÕES EXATOS MAIS FREQUENTES:")
print("-"*70)
for i, (padrao, freq) in enumerate(padroes_exatos.most_common(10), 1):
    concursos = [c for c, p in dados if f"{p[0]}-{p[1]}-{p[2]}-{p[3]}-{p[4]}" == padrao]
    pct = (freq / len(dados)) * 100
    print(f"{i:2d}. {padrao:15s} → {freq} vezes ({pct:5.1f}%) - Concursos: {concursos}")

print("\n📈 PADRÕES ORDENADOS (independente da posição):")
print("-"*70)
for i, (padrao, freq) in enumerate(padroes_ordenados.most_common(10), 1):
    pct = (freq / len(dados)) * 100
    print(f"{i:2d}. {padrao:15s} → {freq} vezes ({pct:5.1f}%)")

print("\n🎯 DISTRIBUIÇÃO POR COLUNA:")
print("-"*70)

print("\nC1 (1-5):")
for valor, freq in sorted(valores_c1.items()):
    pct = (freq / len(dados)) * 100
    bar = "█" * int(freq * 2)
    print(f"  {valor}: {freq:2d} vezes ({pct:5.1f}%) {bar}")

print("\nC2 (6-10):")
for valor, freq in sorted(valores_c2.items()):
    pct = (freq / len(dados)) * 100
    bar = "█" * int(freq * 2)
    print(f"  {valor}: {freq:2d} vezes ({pct:5.1f}%) {bar}")

print("\nC3 (11-15):")
for valor, freq in sorted(valores_c3.items()):
    pct = (freq / len(dados)) * 100
    bar = "█" * int(freq * 2)
    print(f"  {valor}: {freq:2d} vezes ({pct:5.1f}%) {bar}")

print("\nC4 (16-20):")
for valor, freq in sorted(valores_c4.items()):
    pct = (freq / len(dados)) * 100
    bar = "█" * int(freq * 2)
    print(f"  {valor}: {freq:2d} vezes ({pct:5.1f}%) {bar}")

print("\nC5 (21-25):")
for valor, freq in sorted(valores_c5.items()):
    pct = (freq / len(dados)) * 100
    bar = "█" * int(freq * 2)
    print(f"  {valor}: {freq:2d} vezes ({pct:5.1f}%) {bar}")

print("\n" + "="*70)
print("💡 INSIGHTS PRINCIPAIS:")
print("="*70)

# Encontrar o padrão mais frequente
padrao_mais_freq = padroes_exatos.most_common(1)[0]
print(f"\n✅ Padrão exato mais frequente: {padrao_mais_freq[0]} ({padrao_mais_freq[1]} vezes)")

# Encontrar o padrão ordenado mais frequente
padrao_ord_mais_freq = padroes_ordenados.most_common(1)[0]
print(f"✅ Padrão ordenado mais frequente: {padrao_ord_mais_freq[0]} ({padrao_ord_mais_freq[1]} vezes)")

# Estatísticas gerais
print(f"\n📌 Total de padrões exatos diferentes: {len(padroes_exatos)}")
print(f"📌 Total de padrões ordenados diferentes: {len(padroes_ordenados)}")

# Valores mais comuns por coluna
print(f"\n🔥 Valores mais comuns:")
print(f"   C1: {valores_c1.most_common(1)[0][0]} ({valores_c1.most_common(1)[0][1]} vezes)")
print(f"   C2: {valores_c2.most_common(1)[0][0]} ({valores_c2.most_common(1)[0][1]} vezes)")
print(f"   C3: {valores_c3.most_common(1)[0][0]} ({valores_c3.most_common(1)[0][1]} vezes)")
print(f"   C4: {valores_c4.most_common(1)[0][0]} ({valores_c4.most_common(1)[0][1]} vezes)")
print(f"   C5: {valores_c5.most_common(1)[0][0]} ({valores_c5.most_common(1)[0][1]} vezes)")

# Padrão 3-3-3-3-3 (distribuição perfeita)
qtd_distribuicao_perfeita = sum(1 for _, p in dados if p == [3, 3, 3, 3, 3])
if qtd_distribuicao_perfeita > 0:
    pct_perfeita = (qtd_distribuicao_perfeita / len(dados)) * 100
    print(f"\n⭐ Distribuição perfeita 3-3-3-3-3: {qtd_distribuicao_perfeita} vezes ({pct_perfeita:.1f}%)")

# Valores extremos
print(f"\n⚠️  Valores extremos encontrados:")
todos_valores = [v for _, p in dados for v in p]
print(f"   Mínimo: {min(todos_valores)} (grupos com menos números)")
print(f"   Máximo: {max(todos_valores)} (grupos com mais números)")

print("\n" + "="*70)

import csv

# Resultado do concurso 3592
resultado_concurso = {1, 4, 5, 6, 7, 9, 12, 13, 17, 18, 20, 21, 22, 23, 25}

print("=" * 80)
print("ANÁLISE DO CONCURSO 3592")
print(f"Números sorteados: {sorted(resultado_concurso)}")
print("=" * 80)
print()

# Conjuntos a analisar (do arquivo jogar.csv)
conjuntos = [
    "01-02-03-04-05-06-07-08-10-20-21-22-23-24-25",
    "01-02-03-04-08-09-12-13-15-17-20-21-22-24-25",
    "01-02-03-04-05-06-07-08-11-20-21-22-23-24-25",
    "01-02-03-04-06-07-11-14-15-18-20-22-23-24-25",
    "01-02-03-04-06-08-11-12-13-16-17-21-22-23-24",
    "01-02-03-04-06-08-13-14-15-16-18-22-23-24-25",
    "01-02-03-04-06-10-12-13-15-16-19-21-23-24-25",
    "01-02-03-04-06-10-12-13-15-17-19-21-23-24-25",
    "01-02-03-04-06-07-11-14-15-18-20-22-23-24-25",
    "01-02-03-04-07-10-12-13-15-17-19-21-23-24-25",
    "01-02-03-04-08-09-12-13-15-16-20-21-23-24-25",
    "01-02-03-04-06-07-11-14-15-18-20-22-23-24-25",
    "02-04-05-08-09-10-13-14-15-18-19-20-23-24-25",
    "01-02-03-04-05-06-17-18-19-20-21-22-23-24-25",
    "03-04-05-08-09-10-13-14-15-18-19-20-23-24-25",
    "01-02-03-04-06-07-11-14-15-18-20-22-23-24-25",
    "01-04-05-08-10-12-13-14-15-18-19-20-23-24-25",
    "01-04-05-09-10-12-13-14-15-18-19-20-23-24-25",
    "02-03-05-09-10-12-13-14-15-18-19-20-23-24-25",
    "01-02-03-04-05-09-17-18-19-20-21-22-23-24-25",
    "03-04-05-08-10-12-13-14-15-18-19-20-23-24-25",
    "01-02-03-04-05-10-17-18-19-20-21-22-23-24-25",
    "01-02-06-07-08-11-14-15-16-19-21-22-23-24-25",
    "01-02-03-04-05-11-17-18-19-20-21-22-23-24-25",
    "01-02-06-07-08-12-14-15-16-19-21-22-23-24-25",
    "01-02-03-04-05-12-17-18-19-20-21-22-23-24-25",
    "01-02-06-07-10-11-13-15-16-20-21-22-23-24-25",
    "01-02-03-04-05-13-17-18-19-20-21-22-23-24-25",
    "01-02-06-07-09-12-14-15-16-20-21-22-23-24-25"
]

# Resultados por quantidade de acertos
resultados_por_acertos = {}

# Analisar cada conjunto
for i, conjunto_str in enumerate(conjuntos, 1):
    # Converter para conjunto de inteiros
    numeros = set(int(n) for n in conjunto_str.split('-'))
    
    # Contar acertos
    acertos = len(resultado_concurso & numeros)
    numeros_acertados = sorted(resultado_concurso & numeros)
    numeros_errados = sorted(numeros - resultado_concurso)
    
    # Organizar por quantidade de acertos
    if acertos not in resultados_por_acertos:
        resultados_por_acertos[acertos] = []
    
    resultados_por_acertos[acertos].append({
        'numero': i,
        'conjunto': conjunto_str,
        'acertos': acertos,
        'numeros_acertados': numeros_acertados,
        'numeros_errados': numeros_errados
    })

# Exibir resultados organizados por quantidade de acertos (do maior para o menor)
print("RESULTADOS (ordenados por acertos):")
print("=" * 80)

total_jogos = len(conjuntos)
jogos_11_mais = 0

for acertos in sorted(resultados_por_acertos.keys(), reverse=True):
    jogos = resultados_por_acertos[acertos]
    
    if acertos >= 11:
        jogos_11_mais += len(jogos)
        print(f"\n🎯 {acertos} ACERTOS ({len(jogos)} jogo(s))")
    else:
        print(f"\n⭐ {acertos} ACERTOS ({len(jogos)} jogo(s))")
    
    print("-" * 80)
    
    for item in jogos:
        print(f"\nJogo #{item['numero']:02d}: {item['conjunto']}")
        print(f"  Acertou ({acertos}): {','.join(map(str, item['numeros_acertados']))}")
        print(f"  Errou   ({15-acertos}): {','.join(map(str, item['numeros_errados']))}")

# Resumo
print("\n" + "=" * 80)
print("RESUMO:")
print(f"  Total de jogos analisados: {total_jogos}")
print(f"  Jogos com 11+ acertos: {jogos_11_mais}")
print(f"  Melhor resultado: {max(resultados_por_acertos.keys())} acertos")
print(f"  Pior resultado: {min(resultados_por_acertos.keys())} acertos")
print("=" * 80)

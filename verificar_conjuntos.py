import csv

# Resultado do concurso 3592
resultado_concurso = {1, 4, 5, 6, 7, 9, 12, 13, 17, 18, 20, 21, 22, 23, 25}

print("=" * 80)
print("ANÁLISE DO CONCURSO 3592")
print(f"Números sorteados: {sorted(resultado_concurso)}")
print("=" * 80)
print()

# Conjuntos a verificar
conjuntos = [
    "3,7,9,10,11,12,13,16,18,19,20,21,22,23,24",
    "1,2,4,5,6,8,11,14,16,18,19,22,23,24,25",
    "1,2,3,9,10,11,13,16,17,19,21,22,23,24,25",
    "3,4,5,7,8,11,12,13,14,15,16,17,21,24,25",
    "2,3,5,6,8,10,11,12,13,14,15,16,21,24,25",
    "1,2,3,5,9,11,12,13,16,17,18,19,21,23,24",
    "3,4,5,6,7,11,12,13,16,18,20,21,22,23,25",
    "1,3,5,7,9,11,13,14,15,16,20,21,22,23,25",
    "1,2,5,7,9,11,15,16,17,18,19,21,22,23,25",
    "3,4,5,8,10,11,13,14,16,18,19,21,22,23,25"
]

# Analisar cada conjunto
resultados_11_mais = []

for i, conjunto_str in enumerate(conjuntos, 1):
    # Converter para conjunto de inteiros
    conjunto = set(int(n.strip()) for n in conjunto_str.split(','))
    
    # Contar acertos
    acertos = len(resultado_concurso & conjunto)
    numeros_acertados = sorted(resultado_concurso & conjunto)
    numeros_errados = sorted(conjunto - resultado_concurso)
    
    if acertos >= 11:
        resultados_11_mais.append({
            'numero': i,
            'conjunto': conjunto_str,
            'acertos': acertos,
            'numeros_acertados': numeros_acertados,
            'numeros_errados': numeros_errados
        })

# Resumo
print("=" * 80)
if resultados_11_mais:
    print(f"\n🎯 RESULTADOS COM 11 OU MAIS ACERTOS: {len(resultados_11_mais)} conjunto(s)\n")
    print("-" * 80)
    
    for item in resultados_11_mais:
        print(f"\nConjunto {item['numero']}: {item['acertos']} acertos")
        print(f"  Jogo:    {item['conjunto']}")
        print(f"  Acertou: {','.join(map(str, item['numeros_acertados']))}")
        print(f"  Errou:   {','.join(map(str, item['numeros_errados']))}")
else:
    print("\nNenhum conjunto teve 11 ou mais acertos.")

print("\n" + "=" * 80)

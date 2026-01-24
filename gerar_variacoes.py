import random
import csv

# Conjunto original
conjunto_original = [1, 2, 3, 4, 6, 7, 10, 11, 13, 14, 15, 17, 18, 19, 20]

# Números que NÃO estão no conjunto original (1-25)
numeros_disponiveis = [5, 8, 9, 12, 16, 21, 22, 23, 24, 25]

# Gerar 10 combinações
combinacoes = []

# Para garantir variação, vamos embaralhar o conjunto original e pegar grupos diferentes
random.seed(42)  # Para reprodutibilidade

for i in range(10):
    # Embaralhar o conjunto original
    conjunto_embaralhado = conjunto_original.copy()
    random.shuffle(conjunto_embaralhado)
    
    # Pegar 8 números base (diferentes posições a cada iteração)
    inicio = (i * 2) % 8  # Variar o ponto de início
    numeros_base = conjunto_embaralhado[inicio:inicio+8]
    
    # Se não tiver 8, completar do início
    if len(numeros_base) < 8:
        numeros_base.extend(conjunto_embaralhado[:8-len(numeros_base)])
    
    # Embaralhar os números disponíveis
    disponiveis_embaralhados = numeros_disponiveis.copy()
    random.shuffle(disponiveis_embaralhados)
    
    # Pegar 7 números aleatórios
    numeros_aleatorios = disponiveis_embaralhados[:7]
    
    # Combinar e ordenar
    combinacao = sorted(numeros_base + numeros_aleatorios)
    
    combinacoes.append(combinacao)
    
    # Mostrar a combinação
    print(f"Combinação {i+1}:")
    print(f"  Base (do original): {sorted(numeros_base)}")
    print(f"  Aleatórios: {sorted(numeros_aleatorios)}")
    print(f"  Completa: {combinacao}")
    print()

# Salvar no arquivo novo_jogo.csv
with open('data/novo_jogo.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Combinacao'])  # Cabeçalho
    
    for i, combinacao in enumerate(combinacoes, 1):
        # Formatar como string separada por vírgulas
        combinacao_str = ','.join(map(str, combinacao))
        writer.writerow([combinacao_str])

print(f"\n✓ 10 combinações salvas em data/novo_jogo.csv")

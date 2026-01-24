import csv

# Ler o arquivo novo_jogo.csv
with open('data/novo_jogo.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Pular o cabeçalho
    
    print("SOMATÓRIOS DOS CONJUNTOS:\n")
    
    for i, row in enumerate(reader, 1):
        # Pegar a string de números e converter para lista de inteiros
        numeros_str = row[0].replace('"', '')
        numeros = [int(n) for n in numeros_str.split(',')]
        
        # Calcular a soma
        soma = sum(numeros)
        
        print(f"Conjunto {i:2d}: {numeros_str}")
        print(f"            Soma = {soma}")
        print()

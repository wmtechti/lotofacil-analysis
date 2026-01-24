import random
import csv

# Resultado do concurso 3592 (números sorteados)
resultado_concurso = [1, 4, 5, 6, 7, 9, 12, 13, 17, 18, 20, 21, 22, 23, 25]

# Números que NÃO foram sorteados no concurso 3592 (1-25)
numeros_nao_sorteados = [2, 3, 8, 10, 11, 14, 15, 16, 19, 24]

print("=" * 80)
print("GERADOR DE COMBINAÇÕES BASEADO NO CONCURSO 3592")
print("=" * 80)
print(f"Números sorteados no 3592: {resultado_concurso}")
print(f"Números NÃO sorteados: {numeros_nao_sorteados}")
print()

# Gerar 10 combinações
combinacoes = []

random.seed(2026)  # Para reprodutibilidade

for i in range(10):
    # Embaralhar o resultado do concurso
    resultado_embaralhado = resultado_concurso.copy()
    random.shuffle(resultado_embaralhado)
    
    # Pegar 8 números do resultado (variando quais)
    inicio = (i * 2) % 8  # Variar o ponto de início
    numeros_fixos = resultado_embaralhado[inicio:inicio+8]
    
    # Se não tiver 8, completar do início
    if len(numeros_fixos) < 8:
        numeros_fixos.extend(resultado_embaralhado[:8-len(numeros_fixos)])
    
    # Embaralhar os números não sorteados
    nao_sorteados_embaralhados = numeros_nao_sorteados.copy()
    random.shuffle(nao_sorteados_embaralhados)
    
    # Pegar 7 números dos não sorteados
    numeros_novos = nao_sorteados_embaralhados[:7]
    
    # Combinar e ordenar
    combinacao = sorted(numeros_fixos + numeros_novos)
    
    combinacoes.append(combinacao)
    
    # Mostrar a combinação
    print(f"Combinação {i+1}:")
    print(f"  Fixos (do 3592): {sorted(numeros_fixos)}")
    print(f"  Novos (não sorteados): {sorted(numeros_novos)}")
    print(f"  Completa: {combinacao}")
    print()

# Salvar no arquivo combinacoes_3592.csv
with open('data/combinacoes_3592.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Combinacao'])  # Cabeçalho
    
    for i, combinacao in enumerate(combinacoes, 1):
        # Formatar como string separada por vírgulas
        combinacao_str = ','.join(map(str, combinacao))
        writer.writerow([combinacao_str])

print("\n" + "=" * 80)
print(f"✓ 10 combinações salvas em data/combinacoes_3592.csv")
print("=" * 80)

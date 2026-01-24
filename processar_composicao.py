"""
Script para processar dados de composição da Lotofácil
Agrupa os 25 números em 5 grupos de 5 e conta quantos números de cada grupo foram sorteados
"""

import csv

# Definir os grupos
grupos = {
    'c1': list(range(1, 6)),     # 1-5
    'c2': list(range(6, 11)),    # 6-10
    'c3': list(range(11, 16)),   # 11-15
    'c4': list(range(16, 21)),   # 16-20
    'c5': list(range(21, 26))    # 21-25
}

def processar_linha_concurso(linha):
    """
    Processa uma linha do CSV e extrai os números sorteados
    """
    concurso = linha[0]
    numeros_sorteados = []
    
    # Extrair números das colunas 1 a 25 (índices 1 a 25 no CSV)
    for i in range(1, 26):
        if i < len(linha) and linha[i].strip():  # Se não está vazio
            try:
                num = int(linha[i])
                numeros_sorteados.append(num)
            except ValueError:
                pass  # Ignora valores não numéricos
    
    return concurso, numeros_sorteados

def contar_por_grupos(numeros):
    """
    Conta quantos números de cada grupo foram sorteados
    """
    contagens = {}
    
    for grupo_nome, grupo_numeros in grupos.items():
        contagem = sum(1 for num in numeros if num in grupo_numeros)
        contagens[grupo_nome] = contagem
    
    return contagens

# Ler o arquivo original
arquivo_entrada = r'f:\projetos\2026\lotofacil\data\analise_composicao.csv'

resultados = []

with open(arquivo_entrada, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    linhas = list(reader)
    
    print(f"Total de linhas no arquivo: {len(linhas)}")
    print(f"Primeira linha (exemplo): {linhas[0] if linhas else 'vazio'}")
    
    # Processar linhas 2 a 21 (índices 1 a 20 - linha 2 é índice 1)
    for i in range(0, 20):  # Linhas 1 a 20 (índice 0 a 19)
        if i < len(linhas):
            linha = linhas[i]
            print(f"\nProcessando linha {i+1} (índice {i}): concurso={linha[0] if linha else 'vazio'}")
            concurso, numeros = processar_linha_concurso(linha)
            print(f"  Números sorteados: {numeros}")
            contagens = contar_por_grupos(numeros)
            print(f"  Contagens: {contagens}")
            
            resultado = f"{concurso},{contagens['c1']},{contagens['c2']},{contagens['c3']},{contagens['c4']},{contagens['c5']}"
            resultados.append(resultado)

# Gerar saída
print("\n" + "="*60)
print("DADOS PARA ADICIONAR A PARTIR DA LINHA 29:")
print("="*60)
print("concurso,c1,c2,c3,c4,c5")
for resultado in resultados:
    print(resultado)

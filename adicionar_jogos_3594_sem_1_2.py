import csv
import random
from pathlib import Path

# Resultado do concurso 3594
RESULTADO_3594 = [1, 2, 4, 5, 7, 8, 9, 11, 14, 15, 18, 20, 21, 23, 24]

# Remove os números 1 e 2 do resultado
RESULTADO_SEM_1_2 = [n for n in RESULTADO_3594 if n not in [1, 2]]

# Seleciona 8 números fixos (primeiros 8 após remover 1 e 2)
FIXOS = set(RESULTADO_SEM_1_2[:8])  # {4, 5, 7, 8, 9, 11, 14, 15}

# Todos os números da Lotofácil
TODOS_NUMEROS = set(range(1, 26))

# Números disponíveis para sortear (excluindo os fixos)
DISPONIVEIS = sorted(TODOS_NUMEROS - FIXOS)

def gerar_jogo_com_fixos():
    """Gera um jogo com os 8 números fixos + 7 aleatórios"""
    # Sorteia 7 números dos disponíveis
    aleatorios = random.sample(DISPONIVEIS, 7)
    
    # Combina fixos + aleatórios e ordena
    jogo = sorted(list(FIXOS) + aleatorios)
    
    return jogo

def main():
    arquivo = Path(r'f:\projetos\2026\lotofacil\data\jogar.csv')
    
    # Lê o arquivo atual
    linhas_existentes = []
    if arquivo.exists():
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas_existentes = f.readlines()
    
    print(f"Arquivo atual tem {len(linhas_existentes)} linhas")
    print(f"\nConcurso 3594: {','.join(map(str, RESULTADO_3594))}")
    print(f"Resultado sem 1 e 2: {','.join(map(str, RESULTADO_SEM_1_2))}")
    print(f"Números fixos (8 primeiros): {sorted(FIXOS)}")
    print(f"Gerando 10 novos jogos...")
    print("=" * 80)
    
    # Gera 10 novos jogos
    novos_jogos = []
    for i in range(10):
        jogo = gerar_jogo_com_fixos()
        novos_jogos.append(jogo)
        print(f"Jogo {i+1}: {','.join(map(str, jogo))}")
    
    # Adiciona os novos jogos ao arquivo
    with open(arquivo, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for jogo in novos_jogos:
            writer.writerow(jogo)
    
    print("=" * 80)
    print(f"✓ 10 jogos adicionados com sucesso ao arquivo jogar.csv")
    print(f"Total de linhas agora: {len(linhas_existentes) + 10}")

if __name__ == '__main__':
    main()

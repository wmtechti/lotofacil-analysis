import csv
import random
from pathlib import Path

# Números fixos
FIXOS = {1, 4, 7, 9, 18, 23}

# Todos os números da Lotofácil
TODOS_NUMEROS = set(range(1, 26))

# Números disponíveis para sortear (excluindo os fixos)
DISPONIVEIS = sorted(TODOS_NUMEROS - FIXOS)

def gerar_jogo_com_fixos():
    """Gera um jogo com os 6 números fixos + 9 aleatórios"""
    # Sorteia 9 números dos disponíveis
    aleatorios = random.sample(DISPONIVEIS, 9)
    
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
    print(f"\nNúmeros fixos: {sorted(FIXOS)}")
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

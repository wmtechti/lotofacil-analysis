import csv
import random
from pathlib import Path

# Resultado do concurso 3594
RESULTADO_3594 = [1, 2, 4, 5, 7, 8, 9, 11, 14, 15, 18, 20, 21, 23, 24]

# Remove os números 1 e 2 do resultado
RESULTADO_SEM_1_2 = [n for n in RESULTADO_3594 if n not in [1, 2]]

# Seleciona 8 números fixos (primeiros 8 após remover 1 e 2)
FIXOS = set(RESULTADO_SEM_1_2[:8])  # {4, 5, 7, 8, 9, 11, 14, 15}

# Todos os números da Lotofácil EXCETO 1 e 2
TODOS_NUMEROS = set(range(3, 26))

# Números disponíveis para sortear (excluindo os fixos)
DISPONIVEIS = sorted(TODOS_NUMEROS - FIXOS)

def gerar_jogo_com_fixos():
    """Gera um jogo com os 8 números fixos + 7 aleatórios (sem 1 e 2)"""
    # Sorteia 7 números dos disponíveis
    aleatorios = random.sample(DISPONIVEIS, 7)
    
    # Combina fixos + aleatórios e ordena
    jogo = sorted(list(FIXOS) + aleatorios)
    
    return jogo

def main():
    arquivo = Path(r'f:\projetos\2026\lotofacil\data\jogar.csv')
    
    # Lê todas as linhas
    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    print(f"Arquivo tem {len(linhas)} linhas")
    print(f"\nConcurso 3594 (sem 1 e 2): {','.join(map(str, RESULTADO_SEM_1_2))}")
    print(f"Números fixos (8 primeiros): {sorted(FIXOS)}")
    print(f"\nRemovendo números 1 e 2 dos últimos 10 jogos e regenerando...")
    print("=" * 80)
    
    # Mantém todas as linhas exceto as últimas 10
    linhas_mantidas = linhas[:-10]
    
    # Gera 10 novos jogos SEM os números 1 e 2
    novos_jogos = []
    for i in range(10):
        jogo = gerar_jogo_com_fixos()
        novos_jogos.append(jogo)
        print(f"Jogo {i+1}: {','.join(map(str, jogo))}")
    
    # Reescreve o arquivo
    with open(arquivo, 'w', encoding='utf-8', newline='') as f:
        # Escreve as linhas mantidas
        f.writelines(linhas_mantidas)
        
        # Adiciona os novos jogos
        writer = csv.writer(f)
        for jogo in novos_jogos:
            writer.writerow(jogo)
    
    print("=" * 80)
    print(f"✓ Últimos 10 jogos atualizados sem os números 1 e 2")
    print(f"Total de linhas: {len(linhas_mantidas) + 10}")

if __name__ == '__main__':
    main()

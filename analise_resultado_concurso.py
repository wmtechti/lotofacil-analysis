import csv
import os
from pathlib import Path

# Resultado do concurso 3592
resultado_concurso = {1, 4, 5, 6, 7, 9, 12, 13, 17, 18, 20, 21, 22, 23, 25}

print("=" * 80)
print("ANÁLISE DO CONCURSO 3592")
print(f"Números sorteados: {sorted(resultado_concurso)}")
print("=" * 80)
print()

# Diretórios para analisar
data_dir = Path('data')
out_dir = Path('out')

# Dicionário para armazenar resultados por quantidade de acertos
resultados = {15: [], 14: [], 13: [], 12: [], 11: []}

# Contador de arquivos e combinações
arquivos_analisados = 0
combinacoes_analisadas = 0

# Lista de todos os diretórios a serem analisados
diretorios = [data_dir, out_dir]

# Percorrer todos os arquivos CSV nos diretórios (incluindo subpastas)
for diretorio in diretorios:
    if not diretorio.exists():
        continue
    
    # Usar rglob para buscar recursivamente em subpastas
    for csv_file in sorted(diretorio.rglob('*.csv')):
        arquivos_analisados += 1
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                # Pular o cabeçalho (primeira linha)
                try:
                    header = next(reader)
                except StopIteration:
                    continue
                
                # Processar cada linha
                for linha_num, row in enumerate(reader, start=2):  # Começa em 2 porque linha 1 é cabeçalho
                    if not row or not row[0]:
                        continue
                    
                    try:
                        # Extrair números da combinação
                        numeros_str = row[0].replace('"', '').strip()
                        
                        # Ignorar linhas com comentários ou texto
                        if not numeros_str or any(c.isalpha() for c in numeros_str.replace(',', '')):
                            continue
                        
                        # Converter para conjunto de inteiros
                        combinacao = set(int(n.strip()) for n in numeros_str.split(','))
                        
                        combinacoes_analisadas += 1
                        
                        # Contar acertos
                        acertos = len(resultado_concurso & combinacao)
                        
                        # Armazenar apenas se tiver 11 ou mais acertos
                        if acertos >= 11 and acertos <= 15:
                            resultados[acertos].append({
                                'arquivo': str(csv_file.relative_to(Path('.'))),
                                'linha': linha_num,
                                'combinacao': sorted(combinacao),
                                'acertos': acertos,
                                'numeros_acertados': sorted(resultado_concurso & combinacao),
                                'numeros_errados': sorted(combinacao - resultado_concurso)
                            })
                    
                    except (ValueError, IndexError) as e:
                        # Ignorar linhas com formato inválido
                        continue
        
        except Exception as e:
            pass

# Exibir resultados
print("\nRESULTADOS DA ANÁLISE:")
print("=" * 80)

total_encontrado = 0

for acertos in [15, 14, 13, 12, 11]:
    if resultados[acertos]:
        print(f"\n{'🎯' if acertos == 15 else '⭐'} {acertos} ACERTOS ({len(resultados[acertos])} jogos encontrados)")
        print("-" * 80)
        
        for item in resultados[acertos]:
            total_encontrado += 1
            print(f"\n✓ ACERTOS: {item['acertos']} pontos")
            print(f"  Arquivo: {item['arquivo']}")
            print(f"  Linha:   {item['linha']}")
            print(f"  Jogo:    {','.join(map(str, item['combinacao']))}")
            print(f"  Acertou: {','.join(map(str, item['numeros_acertados']))}")
            print(f"  Errou:   {','.join(map(str, item['numeros_errados']))}")

if total_encontrado == 0:
    print("\nNenhum jogo com 11 ou mais acertos foi encontrado.")
else:
    print("\n" + "=" * 80)
    print(f"TOTAL: {total_encontrado} jogos com 11 ou mais acertos encontrados")
    print("=" * 80)

print(f"\nArquivos analisados: {arquivos_analisados}")
print(f"Combinações analisadas: {combinacoes_analisadas}")

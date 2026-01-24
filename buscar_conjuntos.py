import csv
from pathlib import Path

# Conjuntos a procurar
conjuntos_buscar = [
    "3,4,5,6,7,11,12,13,16,18,20,21,22,23,25",
    "1,2,3,4,5,6,17,18,19,20,21,22,23,24,25",
    "1,2,3,4,5,12,17,18,19,20,21,22,23,24,25",
    "1,2,3,4,5,9,17,18,19,20,21,22,23,24,25",
    "1,4,5,6,7,8,9,10,12,15,17,19,21,23,25",
    "1,2,3,4,5,13,17,18,19,20,21,22,23,24,25"
]

# Normalizar conjuntos (remover espaços e criar set para comparação)
conjuntos_normalizados = []
for conj in conjuntos_buscar:
    numeros = set(int(n.strip()) for n in conj.split(','))
    conjuntos_normalizados.append((conj, numeros))

print("=" * 80)
print("BUSCA DE CONJUNTOS ESPECÍFICOS")
print("=" * 80)
print("\nProcurando pelos seguintes conjuntos:")
for i, (conj_str, _) in enumerate(conjuntos_normalizados, 1):
    print(f"  {i}. {conj_str}")
print()

# Resultados
resultados = {conj: [] for conj, _ in conjuntos_normalizados}

# Diretórios para procurar
diretorios = [Path('data'), Path('out'), Path('.')]

# Contador
arquivos_analisados = 0
linhas_analisadas = 0

# Buscar em arquivos CSV
for diretorio in diretorios:
    if not diretorio.exists():
        continue
    
    # Buscar CSV
    for arquivo in sorted(diretorio.rglob('*.csv')):
        arquivos_analisados += 1
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                for num_linha, linha in enumerate(f, 1):
                    linhas_analisadas += 1
                    linha_limpa = linha.strip().replace('"', '').replace(' ', '')
                    
                    # Tentar extrair números da linha
                    if not linha_limpa or any(c.isalpha() and c not in 'Combinacao' for c in linha_limpa):
                        continue
                    
                    # Verificar se contém números separados por vírgula
                    if ',' in linha_limpa:
                        try:
                            # Extrair apenas a parte com números
                            partes = linha_limpa.split(',')
                            numeros_str_list = []
                            
                            for parte in partes:
                                # Pegar apenas dígitos
                                digitos = ''.join(c for c in parte if c.isdigit())
                                if digitos:
                                    numeros_str_list.append(digitos)
                            
                            if len(numeros_str_list) == 15:  # Lotofácil tem 15 números
                                numeros_conjunto = set(int(n) for n in numeros_str_list if int(n) <= 25)
                                
                                if len(numeros_conjunto) == 15:
                                    # Comparar com os conjuntos procurados
                                    for conj_str, conj_set in conjuntos_normalizados:
                                        if numeros_conjunto == conj_set:
                                            caminho_relativo = str(arquivo.relative_to(Path('.')))
                                            resultados[conj_str].append({
                                                'arquivo': caminho_relativo,
                                                'linha': num_linha,
                                                'conteudo': linha.strip()
                                            })
                        except (ValueError, IndexError):
                            continue
        except Exception as e:
            pass
    
    # Buscar TXT
    for arquivo in sorted(diretorio.rglob('*.txt')):
        arquivos_analisados += 1
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                for num_linha, linha in enumerate(f, 1):
                    linhas_analisadas += 1
                    linha_limpa = linha.strip().replace('"', '').replace(' ', '')
                    
                    if not linha_limpa:
                        continue
                    
                    # Verificar se contém números separados por vírgula
                    if ',' in linha_limpa:
                        try:
                            # Extrair apenas a parte com números
                            partes = linha_limpa.split(',')
                            numeros_str_list = []
                            
                            for parte in partes:
                                # Pegar apenas dígitos
                                digitos = ''.join(c for c in parte if c.isdigit())
                                if digitos:
                                    numeros_str_list.append(digitos)
                            
                            if len(numeros_str_list) == 15:
                                numeros_conjunto = set(int(n) for n in numeros_str_list if int(n) <= 25)
                                
                                if len(numeros_conjunto) == 15:
                                    # Comparar com os conjuntos procurados
                                    for conj_str, conj_set in conjuntos_normalizados:
                                        if numeros_conjunto == conj_set:
                                            caminho_relativo = str(arquivo.relative_to(Path('.')))
                                            resultados[conj_str].append({
                                                'arquivo': caminho_relativo,
                                                'linha': num_linha,
                                                'conteudo': linha.strip()[:100]  # Limitar tamanho
                                            })
                        except (ValueError, IndexError):
                            continue
        except Exception as e:
            pass

# Exibir resultados
print("\n" + "=" * 80)
print("RESULTADOS DA BUSCA")
print("=" * 80)

total_encontrado = 0

for i, (conj_str, _) in enumerate(conjuntos_normalizados, 1):
    encontrados = resultados[conj_str]
    
    if encontrados:
        print(f"\n✓ CONJUNTO {i}: {conj_str}")
        print(f"  Encontrado em {len(encontrados)} local(is):")
        print("-" * 80)
        
        for item in encontrados:
            total_encontrado += 1
            print(f"  Arquivo: {item['arquivo']}")
            print(f"  Linha:   {item['linha']}")
            print(f"  Conteúdo: {item['conteudo']}")
            print()
    else:
        print(f"\n✗ CONJUNTO {i}: {conj_str}")
        print(f"  NÃO ENCONTRADO")

print("\n" + "=" * 80)
print(f"RESUMO:")
print(f"  Arquivos analisados: {arquivos_analisados}")
print(f"  Linhas analisadas: {linhas_analisadas}")
print(f"  Total de ocorrências encontradas: {total_encontrado}")
print("=" * 80)

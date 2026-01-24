"""
Script para separar o arquivo analise_somas_209_211_completa.csv
em três arquivos separados por soma (209, 210, 211)
"""

# Caminhos dos arquivos
arquivo_entrada = r'f:\projetos\2026\lotofacil\data\analise_somas_209_211_completa.csv'
arquivo_209 = r'f:\projetos\2026\lotofacil\data\analise_soma_209.csv'
arquivo_210 = r'f:\projetos\2026\lotofacil\data\analise_soma_210.csv'
arquivo_211 = r'f:\projetos\2026\lotofacil\data\analise_soma_211.csv'

# Contadores
count_209 = 0
count_210 = 0
count_211 = 0

print("Processando arquivo...")

# Ler o arquivo e separar por soma
with open(arquivo_entrada, 'r', encoding='utf-8') as f_entrada:
    # Ler o cabeçalho
    cabecalho = f_entrada.readline()
    
    # Abrir os três arquivos de saída
    with open(arquivo_209, 'w', encoding='utf-8') as f_209, \
         open(arquivo_210, 'w', encoding='utf-8') as f_210, \
         open(arquivo_211, 'w', encoding='utf-8') as f_211:
        
        # Escrever cabeçalho em todos os arquivos
        f_209.write(cabecalho)
        f_210.write(cabecalho)
        f_211.write(cabecalho)
        
        # Processar cada linha
        for linha in f_entrada:
            if linha.startswith('209,'):
                f_209.write(linha)
                count_209 += 1
            elif linha.startswith('210,'):
                f_210.write(linha)
                count_210 += 1
            elif linha.startswith('211,'):
                f_211.write(linha)
                count_211 += 1

print("\n" + "="*70)
print("SEPARAÇÃO DE ARQUIVOS CONCLUÍDA!")
print("="*70)
print(f"\n📄 Arquivo 209: {arquivo_209}")
print(f"   → {count_209:,} linhas escritas")

print(f"\n📄 Arquivo 210: {arquivo_210}")
print(f"   → {count_210:,} linhas escritas")

print(f"\n📄 Arquivo 211: {arquivo_211}")
print(f"   → {count_211:,} linhas escritas")

print(f"\n📊 TOTAL: {count_209 + count_210 + count_211:,} linhas processadas")
print("="*70)

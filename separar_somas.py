"""
Script para separar o arquivo analise_somas_181_ate_183_completa.csv
em três arquivos separados por soma (181, 182, 183)
"""

# Caminhos dos arquivos
arquivo_entrada = r'f:\projetos\2026\lotofacil\data\analise_somas_181_ate_183_completa.csv'
arquivo_181 = r'f:\projetos\2026\lotofacil\data\analise_soma_181.csv'
arquivo_182 = r'f:\projetos\2026\lotofacil\data\analise_soma_182.csv'
arquivo_183 = r'f:\projetos\2026\lotofacil\data\analise_soma_183.csv'

# Contadores
count_181 = 0
count_182 = 0
count_183 = 0

print("Processando arquivo...")

# Ler o arquivo e separar por soma
with open(arquivo_entrada, 'r', encoding='utf-8') as f_entrada:
    # Ler o cabeçalho
    cabecalho = f_entrada.readline()
    
    # Abrir os três arquivos de saída
    with open(arquivo_181, 'w', encoding='utf-8') as f_181, \
         open(arquivo_182, 'w', encoding='utf-8') as f_182, \
         open(arquivo_183, 'w', encoding='utf-8') as f_183:
        
        # Escrever cabeçalho em todos os arquivos
        f_181.write(cabecalho)
        f_182.write(cabecalho)
        f_183.write(cabecalho)
        
        # Processar cada linha
        for linha in f_entrada:
            if linha.startswith('181,'):
                f_181.write(linha)
                count_181 += 1
            elif linha.startswith('182,'):
                f_182.write(linha)
                count_182 += 1
            elif linha.startswith('183,'):
                f_183.write(linha)
                count_183 += 1

print("\n" + "="*70)
print("SEPARAÇÃO DE ARQUIVOS CONCLUÍDA!")
print("="*70)
print(f"\n📄 Arquivo 181: {arquivo_181}")
print(f"   → {count_181:,} linhas escritas")

print(f"\n📄 Arquivo 182: {arquivo_182}")
print(f"   → {count_182:,} linhas escritas")

print(f"\n📄 Arquivo 183: {arquivo_183}")
print(f"   → {count_183:,} linhas escritas")

print(f"\n📊 TOTAL: {count_181 + count_182 + count_183:,} linhas processadas")
print("="*70)

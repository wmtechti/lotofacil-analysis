import csv
from pathlib import Path
from collections import defaultdict

# Combinações para buscar
COMBINACOES_BUSCAR = [
    "1,2,3,4,5,6,7,8,10,20,21,22,23,24,25",
    "1,2,3,4,5,8,9,12,13,15,17,20,21,22,24,25",
    "1,2,6,7,10,11,13,15,16,20,21,22,23,24,25",
    "1,2,3,4,8,9,12,13,15,16,20,21,23,24,25",
    "1,2,3,4,8,9,12,13,15,17,20,21,22,24,25",
    "1,2,3,4,5,6,7,8,10,20,21,22,23,23,25",
    "1,2,4,5,6,7,9,10,11,14,15,17,20,22,23",
    "1,2,4,5,8,9,10,13,15,18,29,20,23,24,25",
    "1,2,3,4,6,11,14,15,18,20,21,22,23,24,25",
    "1,2,3,4,6,7,11,14,15,18,20,22,23,24,25",
    "1,2,3,4,6,7,11,13,14,15,28,20,22,23,24",
    "1,5,7,8,11,12,13,14,15,16,18,19,21,23,24",
    "1,2,5,6,8,9,10,11,12,13,15,18,19,23,24",
    "1,4,5,9,10,12,13,14,15,18,19,20,23,24,25",
    "3,4,5,8,10,12,13,14,15,18,19,20,23,24,25",
    "1,4,5,8,10,12,13,14,15,18,19,20,23,24,25",
    "1,2,3,4,7,10,12,13,15,17,19,21,23,24,25",
    "1,2,3,4,6,10,12,13,15,17,19,21,23,24,25",
    "3,4,5,6,7,11,12,13,16,18,20,21,22,23,25",
    "1,2,3,4,5,6,17,18,19,20,21,22,23,24,25",
    "1,2,3,4,5,12,17,18,19,20,21,22,23,24,25",
    "1,4,5,6,7,8,9,10,12,15,17,19,21,23,25",
    "1,2,3,4,5,13,17,18,19,20,21,22,23,24,25",
    "1,2,3,4,5,9,17,18,19,20,21,22,23,24,25",
]

def normalizar_combinacao(comb_str):
    """Normaliza uma combinação para comparação"""
    try:
        nums = sorted([int(n.strip()) for n in comb_str.replace(' ', '').split(',') if n.strip().isdigit()])
        return ','.join(map(str, nums))
    except:
        return None

def buscar_em_csv(arquivo):
    """Busca combinações em um arquivo CSV"""
    encontrados = defaultdict(list)
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for idx, row in enumerate(reader, 1):
                if not row:
                    continue
                
                # Tenta diferentes formatos
                # Formato 1: linha completa é uma combinação (15 números)
                if len(row) >= 15:
                    try:
                        # Pega os primeiros 15 valores numéricos
                        nums = []
                        for val in row:
                            if val.strip().isdigit():
                                nums.append(int(val.strip()))
                                if len(nums) == 15:
                                    break
                        
                        if len(nums) == 15:
                            comb_norm = ','.join(map(str, sorted(nums)))
                            if comb_norm in COMBINACOES_BUSCAR:
                                encontrados[comb_norm].append(idx)
                    except:
                        pass
                
                # Formato 2: célula única com a combinação
                for cell in row:
                    if ',' in cell and cell.count(',') >= 14:
                        comb_norm = normalizar_combinacao(cell)
                        if comb_norm and comb_norm in COMBINACOES_BUSCAR:
                            encontrados[comb_norm].append(idx)
                            
    except Exception as e:
        pass
    
    return encontrados

def main():
    base_dir = Path(r'f:\projetos\2026\lotofacil')
    diretorios = [
        base_dir / 'data',
        base_dir / 'out'
    ]
    
    # Adiciona subpastas do out
    out_dir = base_dir / 'out'
    if out_dir.exists():
        for item in out_dir.rglob('*'):
            if item.is_dir():
                diretorios.append(item)
    
    print("=" * 100)
    print("BUSCA DE COMBINAÇÕES ESPECÍFICAS EM ARQUIVOS CSV")
    print("=" * 100)
    print(f"Total de combinações para buscar: {len(COMBINACOES_BUSCAR)}")
    print()
    
    # Dicionário para armazenar onde cada combinação foi encontrada
    resultados_por_combinacao = defaultdict(list)
    
    # Busca em todos os CSVs
    for diretorio in diretorios:
        if not diretorio.exists():
            continue
        
        for arquivo_csv in diretorio.glob('*.csv'):
            encontrados = buscar_em_csv(arquivo_csv)
            
            if encontrados:
                caminho_rel = arquivo_csv.relative_to(base_dir)
                for comb, linhas in encontrados.items():
                    for linha in linhas:
                        resultados_por_combinacao[comb].append({
                            'arquivo': str(caminho_rel),
                            'linha': linha,
                            'nome': arquivo_csv.name
                        })
    
    # Exibe resultados organizados por combinação
    total_encontradas = 0
    combinacoes_encontradas = 0
    
    for i, comb in enumerate(COMBINACOES_BUSCAR, 1):
        if comb in resultados_por_combinacao:
            combinacoes_encontradas += 1
            print(f"\n{'='*100}")
            print(f"COMBINAÇÃO #{i}: {comb}")
            print(f"{'='*100}")
            
            # Agrupa por arquivo
            por_arquivo = defaultdict(list)
            for item in resultados_por_combinacao[comb]:
                por_arquivo[item['arquivo']].append(item['linha'])
            
            for arquivo, linhas in sorted(por_arquivo.items()):
                total_encontradas += len(linhas)
                linhas_str = ', '.join(map(str, sorted(linhas)))
                print(f"  📄 {arquivo}")
                print(f"     Linhas: {linhas_str}")
    
    print(f"\n{'='*100}")
    print(f"RESUMO:")
    print(f"  • Combinações buscadas: {len(COMBINACOES_BUSCAR)}")
    print(f"  • Combinações encontradas: {combinacoes_encontradas}")
    print(f"  • Total de ocorrências: {total_encontradas}")
    print(f"{'='*100}")
    
    # Lista combinações NÃO encontradas
    nao_encontradas = [comb for comb in COMBINACOES_BUSCAR if comb not in resultados_por_combinacao]
    if nao_encontradas:
        print(f"\n⚠️  COMBINAÇÕES NÃO ENCONTRADAS ({len(nao_encontradas)}):")
        for i, comb in enumerate(nao_encontradas, 1):
            print(f"  {i}. {comb}")

if __name__ == '__main__':
    main()

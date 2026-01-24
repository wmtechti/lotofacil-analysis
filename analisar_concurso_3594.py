import os
import csv
from pathlib import Path

# Resultado do concurso 3594
resultado_3594 = {1, 2, 4, 5, 7, 8, 9, 11, 14, 15, 18, 20, 21, 23, 24}

def contar_acertos(combinacao, resultado):
    """Conta quantos acertos uma combinação tem com o resultado"""
    try:
        # Tenta diferentes formatos de parsing
        if isinstance(combinacao, str):
            # Remove espaços e divide por vírgula
            nums = set(int(n.strip()) for n in combinacao.replace(' ', '').split(',') if n.strip())
        elif isinstance(combinacao, list):
            nums = set(int(n) for n in combinacao)
        else:
            return 0
        
        return len(nums & resultado)
    except:
        return 0

def analisar_csv(arquivo):
    """Analisa um arquivo CSV procurando por combinações com > 10 acertos"""
    resultados = []
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            # Tenta ler como CSV
            try:
                reader = csv.reader(f)
                for idx, row in enumerate(reader, 1):
                    if not row:
                        continue
                    
                    # Tenta diferentes formatos
                    # Formato 1: linha completa é uma combinação
                    if len(row) >= 15:
                        # Pega os primeiros 15 números da linha
                        try:
                            nums = set(int(row[i]) for i in range(min(15, len(row))) if row[i].strip().isdigit())
                            if len(nums) == 15:
                                acertos = len(nums & resultado_3594)
                                if acertos > 10:
                                    resultados.append((idx, row[:15], acertos))
                        except:
                            pass
                    
                    # Formato 2: uma célula contém toda a combinação
                    for cell in row:
                        if ',' in cell:
                            acertos = contar_acertos(cell, resultado_3594)
                            if acertos > 10:
                                resultados.append((idx, cell, acertos))
                                
            except:
                # Se falhar, tenta ler linha por linha
                f.seek(0)
                for idx, linha in enumerate(f, 1):
                    linha = linha.strip()
                    if not linha or linha.startswith('#'):
                        continue
                    
                    # Procura por padrões de números separados por vírgula
                    if ',' in linha:
                        acertos = contar_acertos(linha, resultado_3594)
                        if acertos > 10:
                            resultados.append((idx, linha, acertos))
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")
    
    return resultados

def main():
    # Diretórios para buscar
    base_dir = Path(r'f:\projetos\2026\lotofacil')
    diretorios = [
        base_dir / 'data',
        base_dir / 'out'
    ]
    
    # Adiciona subpastas do out
    out_dir = base_dir / 'out'
    if out_dir.exists():
        for item in out_dir.iterdir():
            if item.is_dir():
                diretorios.append(item)
    
    print("=" * 80)
    print(f"ANÁLISE DO CONCURSO 3594")
    print(f"Resultado: {sorted(resultado_3594)}")
    print("=" * 80)
    print()
    
    total_encontrados = 0
    
    for diretorio in diretorios:
        if not diretorio.exists():
            continue
        
        print(f"\nAnalisando diretório: {diretorio.relative_to(base_dir)}")
        print("-" * 80)
        
        # Procura por todos os arquivos .csv
        for arquivo_csv in diretorio.glob('*.csv'):
            resultados = analisar_csv(arquivo_csv)
            
            if resultados:
                print(f"\n📄 Arquivo: {arquivo_csv.name}")
                print(f"   Caminho: {arquivo_csv.relative_to(base_dir)}")
                
                for linha, combinacao, acertos in resultados:
                    total_encontrados += 1
                    print(f"   ✓ Linha {linha}: {acertos} acertos")
                    if isinstance(combinacao, list):
                        print(f"     Combinação: {','.join(map(str, combinacao))}")
                    else:
                        # Limita o tamanho da exibição
                        comb_str = str(combinacao)
                        if len(comb_str) > 100:
                            comb_str = comb_str[:100] + "..."
                        print(f"     Combinação: {comb_str}")
    
    print()
    print("=" * 80)
    print(f"TOTAL DE COMBINAÇÕES ENCONTRADAS COM > 10 ACERTOS: {total_encontrados}")
    print("=" * 80)

if __name__ == '__main__':
    main()

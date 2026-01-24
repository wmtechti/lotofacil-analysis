import json
from pathlib import Path

# Combinações para buscar (as 16 não encontradas)
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
    "1,4,5,9,10,12,13,14,15,18,19,20,23,24,25",
    "3,4,5,8,10,12,13,14,15,18,19,20,23,24,25",
    "1,4,5,8,10,12,13,14,15,18,19,20,23,24,25",
    "1,2,3,4,7,10,12,13,15,17,19,21,23,24,25",
    "1,2,3,4,6,10,12,13,15,17,19,21,23,24,25",
]

def buscar_em_notebook(notebook_path):
    """Busca combinações em um notebook"""
    encontrados = []
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Procura em todas as células
        for cell_idx, cell in enumerate(notebook.get('cells', []), 1):
            cell_type = cell.get('cell_type', '')
            source = cell.get('source', [])
            
            # Converte source para string
            if isinstance(source, list):
                content = ''.join(source)
            else:
                content = str(source)
            
            # Busca cada combinação no conteúdo
            for comb in COMBINACOES_BUSCAR:
                # Remove espaços e tenta diferentes formatos
                comb_sem_espaco = comb.replace(' ', '')
                comb_com_espaco = comb.replace(',', ', ')
                
                if comb in content or comb_sem_espaco in content or comb_com_espaco in content:
                    encontrados.append({
                        'celula': cell_idx,
                        'tipo': cell_type,
                        'combinacao': comb,
                        'trecho': content[:200]  # Primeiros 200 chars
                    })
    except Exception as e:
        print(f"Erro ao processar {notebook_path}: {e}")
    
    return encontrados

def main():
    base_dir = Path(r'f:\projetos\2026\lotofacil')
    
    # Lista de notebooks
    notebooks = list(base_dir.glob('**/*.ipynb'))
    
    print("=" * 100)
    print("BUSCA DE COMBINAÇÕES EM NOTEBOOKS")
    print("=" * 100)
    print(f"Total de notebooks encontrados: {len(notebooks)}")
    print(f"Total de combinações para buscar: {len(COMBINACOES_BUSCAR)}")
    print()
    
    total_encontrados = 0
    notebooks_com_resultados = 0
    
    for notebook_path in notebooks:
        resultados = buscar_em_notebook(notebook_path)
        
        if resultados:
            notebooks_com_resultados += 1
            total_encontrados += len(resultados)
            
            print(f"\n📓 {notebook_path.relative_to(base_dir)}")
            print("-" * 100)
            
            for res in resultados:
                print(f"   Célula {res['celula']} ({res['tipo']}): {res['combinacao']}")
    
    print()
    print("=" * 100)
    if total_encontrados == 0:
        print("❌ Nenhuma das 16 combinações foi encontrada nos notebooks")
    else:
        print(f"✅ Total de ocorrências encontradas: {total_encontrados}")
        print(f"   Notebooks com resultados: {notebooks_com_resultados}")
    print("=" * 100)

if __name__ == '__main__':
    main()

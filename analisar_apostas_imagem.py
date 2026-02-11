#!/usr/bin/env python3
"""
Script para analisar apostas da Lotofácil a partir de uma imagem.
Extrai os números dos jogos da imagem e compara com o resultado do concurso.

Uso:
    python analisar_apostas_imagem.py <caminho_da_imagem> <numero_concurso> <numeros_resultado>
    
Exemplo:
    python analisar_apostas_imagem.py minha_aposta.jpg 3610 "01,03,05,07,08,10,13,14,17,20,21,22,23,24,25"
"""

import sys
import re
from pathlib import Path
from lotofacil_utils import determinar_nivel_premiacao

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Erro: Bibliotecas não instaladas.")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)


def extrair_numeros_de_imagem(caminho_imagem):
    """
    Extrai números de uma imagem usando OCR.
    
    Args:
        caminho_imagem: Caminho para o arquivo de imagem
        
    Returns:
        Lista de conjuntos de números (cada conjunto é um jogo)
    """
    try:
        # Abrir a imagem
        imagem = Image.open(caminho_imagem)
        
        # Extrair texto da imagem usando OCR
        texto = pytesseract.image_to_string(imagem, config='--psm 6')
        
        # Procurar por sequências de números separados por vírgula, espaço ou hífen
        # Padrão para encontrar sequências como "01,02,03" ou "01 02 03" ou "01-02-03"
        jogos = []
        linhas = texto.split('\n')
        
        for linha in linhas:
            # Remover caracteres especiais, mantendo apenas números, vírgulas, espaços e hífens
            linha_limpa = re.sub(r'[^\d,\s\-]', '', linha)
            
            # Procurar por números (1 ou 2 dígitos)
            numeros = re.findall(r'\b\d{1,2}\b', linha_limpa)
            
            # Converter para inteiros e filtrar números válidos (1-25)
            numeros_validos = []
            for num in numeros:
                try:
                    n = int(num)
                    if 1 <= n <= 25:
                        numeros_validos.append(n)
                except ValueError:
                    continue
            
            # Na Lotofácil, pode-se apostar de 15 a 20 números (desdobramento)
            # Se encontrou entre 15 e 20 números, considera como um jogo válido
            if 15 <= len(numeros_validos) <= 20:
                jogos.append(set(numeros_validos))
        
        return jogos
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_imagem}' não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return []


def entrada_manual_jogos():
    """
    Permite ao usuário entrar manualmente com os jogos caso o OCR não funcione.
    
    Returns:
        Lista de conjuntos de números
    """
    print("\nO OCR não conseguiu extrair os jogos automaticamente.")
    print("Por favor, entre manualmente com seus jogos.")
    print("Digite os números de cada jogo separados por vírgula (ex: 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15)")
    print("Digite 'fim' quando terminar.\n")
    
    jogos = []
    contador = 1
    
    while True:
        entrada = input(f"Jogo {contador}: ").strip()
        
        if entrada.lower() == 'fim':
            break
        
        try:
            # Remover espaços e separar por vírgula
            numeros_str = entrada.replace(' ', '').split(',')
            numeros = [int(n) for n in numeros_str if n]
            
            # Validar números
            if not all(1 <= n <= 25 for n in numeros):
                print("  ⚠️  Erro: Todos os números devem estar entre 1 e 25.")
                continue
            
            if len(numeros) < 15:
                print("  ⚠️  Erro: Um jogo deve ter pelo menos 15 números.")
                continue
            
            if len(numeros) > 20:
                print("  ⚠️  Erro: Um jogo pode ter no máximo 20 números.")
                continue
            
            if len(numeros) != len(set(numeros)):
                print("  ⚠️  Erro: Números duplicados encontrados.")
                continue
            
            jogos.append(set(numeros))
            print(f"  ✓ Jogo {contador} registrado com {len(numeros)} números")
            contador += 1
            
        except ValueError:
            print("  ⚠️  Erro: Formato inválido. Use apenas números separados por vírgula.")
    
    return jogos


def analisar_jogos(jogos, resultado_concurso, numero_concurso):
    """
    Analisa os jogos comparando com o resultado do concurso.
    
    Args:
        jogos: Lista de conjuntos de números (cada conjunto é um jogo)
        resultado_concurso: Conjunto com os números do resultado
        numero_concurso: Número do concurso
    """
    if not jogos:
        print("\nNenhum jogo para analisar.")
        return
    
    print("\n" + "=" * 80)
    print(f"ANÁLISE DE APOSTAS - CONCURSO {numero_concurso}")
    print(f"Resultado: {', '.join(map(lambda x: f'{x:02d}', sorted(resultado_concurso)))}")
    print("=" * 80)
    
    for i, jogo in enumerate(jogos, 1):
        acertos = resultado_concurso & jogo
        erros = jogo - resultado_concurso
        num_acertos = len(acertos)
        premiacao = determinar_nivel_premiacao(num_acertos)
        
        print(f"\n{'─' * 80}")
        print(f"JOGO {i}")
        print(f"{'─' * 80}")
        print(f"Números apostados: {', '.join(map(lambda x: f'{x:02d}', sorted(jogo)))}")
        print(f"\nRESULTADO: {premiacao} ({num_acertos} acertos)")
        print(f"\nAcertos ({num_acertos}): {', '.join(map(lambda x: f'{x:02d}', sorted(acertos)))}")
        if erros:
            print(f"Erros   ({len(erros)}): {', '.join(map(lambda x: f'{x:02d}', sorted(erros)))}")
    
    print("\n" + "=" * 80)
    print(f"TOTAL DE JOGOS ANALISADOS: {len(jogos)}")
    print("=" * 80)


def main():
    """Função principal."""
    print("=" * 80)
    print("ANALISADOR DE APOSTAS DA LOTOFÁCIL")
    print("=" * 80)
    
    # Verificar se foi passado como argumento
    if len(sys.argv) >= 4:
        caminho_imagem = sys.argv[1]
        numero_concurso = sys.argv[2]
        numeros_str = sys.argv[3]
        
        # Processar números do resultado
        try:
            numeros_resultado = [int(n.strip()) for n in numeros_str.replace(' ', '').split(',')]
            resultado_concurso = set(numeros_resultado)
        except ValueError:
            print("Erro: Formato inválido para números do resultado.")
            return
    else:
        # Modo interativo
        print("\nModo Interativo")
        print("-" * 80)
        
        # Perguntar se deseja usar imagem ou entrada manual
        usar_imagem = input("\nDeseja extrair jogos de uma imagem? (s/n): ").strip().lower()
        
        if usar_imagem == 's':
            caminho_imagem = input("Caminho da imagem: ").strip()
        else:
            caminho_imagem = None
        
        numero_concurso = input("Número do concurso: ").strip()
        numeros_str = input("Números do resultado (separados por vírgula): ").strip()
        
        # Processar números do resultado
        try:
            numeros_resultado = [int(n.strip()) for n in numeros_str.replace(' ', '').split(',')]
            resultado_concurso = set(numeros_resultado)
        except ValueError:
            print("Erro: Formato inválido para números do resultado.")
            return
    
    # Validar resultado
    if len(resultado_concurso) != 15:
        print(f"Erro: O resultado deve ter exatamente 15 números. Você forneceu {len(resultado_concurso)}.")
        return
    
    if not all(1 <= n <= 25 for n in resultado_concurso):
        print("Erro: Todos os números devem estar entre 1 e 25.")
        return
    
    # Extrair jogos
    jogos = []
    
    if caminho_imagem and Path(caminho_imagem).exists():
        print(f"\nExtraindo jogos da imagem: {caminho_imagem}")
        print("Aguarde...")
        jogos = extrair_numeros_de_imagem(caminho_imagem)
        
        if jogos:
            print(f"\n✓ {len(jogos)} jogo(s) extraído(s) da imagem com sucesso!")
        else:
            print("\n⚠️  Não foi possível extrair jogos da imagem automaticamente.")
            usar_manual = input("Deseja entrar manualmente com os jogos? (s/n): ").strip().lower()
            if usar_manual == 's':
                jogos = entrada_manual_jogos()
    else:
        # Entrada manual
        jogos = entrada_manual_jogos()
    
    # Analisar jogos
    if jogos:
        analisar_jogos(jogos, resultado_concurso, numero_concurso)
    else:
        print("\nNenhum jogo foi fornecido para análise.")


if __name__ == "__main__":
    main()

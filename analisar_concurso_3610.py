#!/usr/bin/env python3
"""
Script rápido para analisar apostas do concurso 3610.
Execute este script e digite seus jogos quando solicitado.
"""

from lotofacil_utils import determinar_nivel_premiacao

# Resultado do concurso 3610
RESULTADO_3610 = {1, 3, 5, 7, 8, 10, 13, 14, 17, 20, 21, 22, 23, 24, 25}

def analisar_jogo(jogo, resultado):
    """Analisa um jogo e retorna os acertos."""
    acertos = jogo & resultado
    erros = jogo - resultado
    num_acertos = len(acertos)
    nivel = determinar_nivel_premiacao(num_acertos)
    
    return {
        'nivel': nivel,
        'acertos': acertos,
        'erros': erros,
        'num_acertos': num_acertos
    }

def main():
    print("=" * 80)
    print("ANÁLISE DE APOSTAS - CONCURSO 3610")
    print("=" * 80)
    print(f"\nResultado: {', '.join(map(lambda x: f'{x:02d}', sorted(RESULTADO_3610)))}")
    print("\n" + "─" * 80)
    
    # Coletar jogos
    jogos = []
    
    print("\nDigite seus jogos (números separados por vírgula):")
    print("Exemplo: 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15")
    print("Digite 'fim' quando terminar.\n")
    
    contador = 1
    while True:
        entrada = input(f"Jogo {contador}: ").strip()
        
        if entrada.lower() == 'fim':
            break
        
        try:
            # Processar entrada
            numeros_str = entrada.replace(' ', '').split(',')
            numeros = [int(n) for n in numeros_str if n]
            
            # Validar
            # Na Lotofácil, pode-se apostar de 15 a 20 números
            if not (15 <= len(numeros) <= 20):
                print(f"  ⚠️  Erro: Um jogo deve ter entre 15 e 20 números. Você digitou {len(numeros)}.")
                continue
            
            if not all(1 <= n <= 25 for n in numeros):
                print("  ⚠️  Erro: Todos os números devem estar entre 1 e 25.")
                continue
            
            if len(numeros) != len(set(numeros)):
                print("  ⚠️  Erro: Números duplicados encontrados.")
                continue
            
            jogos.append(set(numeros))
            print(f"  ✓ Jogo {contador} registrado")
            contador += 1
            
        except ValueError:
            print("  ⚠️  Erro: Formato inválido. Use apenas números separados por vírgula.")
    
    # Analisar jogos
    if not jogos:
        print("\nNenhum jogo foi fornecido.")
        return
    
    print("\n" + "=" * 80)
    print("RESULTADOS DA ANÁLISE")
    print("=" * 80)
    
    for i, jogo in enumerate(jogos, 1):
        resultado = analisar_jogo(jogo, RESULTADO_3610)
        
        print(f"\n{'─' * 80}")
        print(f"JOGO {i}")
        print(f"{'─' * 80}")
        print(f"Números: {', '.join(map(lambda x: f'{x:02d}', sorted(jogo)))}")
        print(f"\n{resultado['nivel']} ({resultado['num_acertos']} acertos)")
        print(f"\nAcertou: {', '.join(map(lambda x: f'{x:02d}', sorted(resultado['acertos'])))}")
        if resultado['erros']:
            print(f"Errou:   {', '.join(map(lambda x: f'{x:02d}', sorted(resultado['erros'])))}")
    
    print("\n" + "=" * 80)
    print(f"TOTAL: {len(jogos)} jogo(s) analisado(s)")
    print("=" * 80)

if __name__ == "__main__":
    main()

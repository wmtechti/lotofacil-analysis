"""
Compara os jogos otimizados com os resultados dos últimos sorteios
"""

import pandas as pd
from pathlib import Path

def load_optimized_games():
    """Carrega os jogos otimizados"""
    games_file = Path('out/optimized/jogos_18_quentes_otimizados.csv')
    df = pd.read_csv(games_file)
    
    # Converte a coluna de números para lista de inteiros
    games = []
    for _, row in df.iterrows():
        numbers = [int(x) for x in row['numeros'].split(',')]
        games.append({
            'jogo_id': row['jogo_id'],
            'numbers': set(numbers),
            'score': row['score'],
            'dispersao': row['dispersao']
        })
    
    return games

def load_recent_draws(n=20):
    """Carrega os últimos N sorteios"""
    draws_file = Path('data/lotofacil_sorteios.csv')
    df = pd.read_csv(draws_file)
    
    # Pega os últimos N sorteios
    recent = df.tail(n)
    
    draws = []
    for _, row in recent.iterrows():
        # Colunas Bola1 a Bola15
        numbers = set()
        for i in range(1, 16):
            numbers.add(int(row[f'Bola{i}']))
        
        draws.append({
            'concurso': int(row['Concurso']),
            'data': row['Data Sorteio'],
            'numbers': numbers,
            'ganhadores_15': row['Ganhadores 15 acertos']
        })
    
    return draws

def compare_games_with_draws(games, draws):
    """Compara cada jogo com cada sorteio"""
    results = []
    
    for game in games:
        game_results = {
            'jogo_id': game['jogo_id'],
            'score': game['score'],
            'total_11': 0,
            'total_12': 0,
            'total_13': 0,
            'total_14': 0,
            'total_15': 0,
            'melhor_resultado': 0,
            'concurso_melhor': None,
            'detalhes': []
        }
        
        for draw in draws:
            # Conta quantos números do jogo estão no sorteio
            matches = len(game['numbers'] & draw['numbers'])
            
            # Atualiza contadores
            if matches == 11:
                game_results['total_11'] += 1
            elif matches == 12:
                game_results['total_12'] += 1
            elif matches == 13:
                game_results['total_13'] += 1
            elif matches == 14:
                game_results['total_14'] += 1
            elif matches == 15:
                game_results['total_15'] += 1
            
            # Atualiza melhor resultado
            if matches > game_results['melhor_resultado']:
                game_results['melhor_resultado'] = matches
                game_results['concurso_melhor'] = draw['concurso']
            
            # Guarda detalhes para jogos com 11+ acertos
            if matches >= 11:
                game_results['detalhes'].append({
                    'concurso': draw['concurso'],
                    'data': draw['data'],
                    'acertos': matches
                })
        
        results.append(game_results)
    
    return results

def analyze_results(results):
    """Analisa os resultados gerais"""
    total_games = len(results)
    
    # Estatísticas gerais
    stats = {
        'total_11': sum(r['total_11'] for r in results),
        'total_12': sum(r['total_12'] for r in results),
        'total_13': sum(r['total_13'] for r in results),
        'total_14': sum(r['total_14'] for r in results),
        'total_15': sum(r['total_15'] for r in results),
    }
    
    # Jogos que ganharam
    jogos_com_11 = sum(1 for r in results if r['total_11'] > 0)
    jogos_com_12 = sum(1 for r in results if r['total_12'] > 0)
    jogos_com_13 = sum(1 for r in results if r['total_13'] > 0)
    jogos_com_14 = sum(1 for r in results if r['total_14'] > 0)
    jogos_com_15 = sum(1 for r in results if r['total_15'] > 0)
    
    # Melhores jogos
    best_games = sorted(results, key=lambda x: (
        x['total_15'],
        x['total_14'],
        x['total_13'],
        x['total_12'],
        x['total_11']
    ), reverse=True)[:10]
    
    return stats, {
        'jogos_com_11': jogos_com_11,
        'jogos_com_12': jogos_com_12,
        'jogos_com_13': jogos_com_13,
        'jogos_com_14': jogos_com_14,
        'jogos_com_15': jogos_com_15,
    }, best_games

def main():
    print("="*80)
    print("🎯 COMPARAÇÃO DOS JOGOS OTIMIZADOS COM RESULTADOS REAIS")
    print("="*80)
    print()
    
    # Carrega dados
    print("📥 Carregando jogos otimizados...")
    games = load_optimized_games()
    print(f"   ✓ {len(games)} jogos carregados")
    print()
    
    print("📥 Carregando últimos 20 sorteios...")
    draws = load_recent_draws(20)
    print(f"   ✓ Sorteios {draws[-1]['concurso']} a {draws[0]['concurso']}")
    print()
    
    # Compara
    print("🔍 Comparando jogos com sorteios...")
    results = compare_games_with_draws(games, draws)
    print()
    
    # Analisa
    stats, game_stats, best_games = analyze_results(results)
    
    # Exibe resultados
    print("="*80)
    print("📊 RESULTADOS GERAIS")
    print("="*80)
    print(f"Total de jogos analisados: {len(games)}")
    print(f"Total de sorteios analisados: {len(draws)}")
    print(f"Total de comparações: {len(games) * len(draws):,}")
    print()
    
    print("🎁 PRÊMIOS CONQUISTADOS (nos últimos 20 sorteios):")
    print("-"*80)
    print(f"  15 acertos: {stats['total_15']:3d} prêmios | {game_stats['jogos_com_15']} jogos diferentes")
    print(f"  14 acertos: {stats['total_14']:3d} prêmios | {game_stats['jogos_com_14']} jogos diferentes")
    print(f"  13 acertos: {stats['total_13']:3d} prêmios | {game_stats['jogos_com_13']} jogos diferentes")
    print(f"  12 acertos: {stats['total_12']:3d} prêmios | {game_stats['jogos_com_12']} jogos diferentes")
    print(f"  11 acertos: {stats['total_11']:3d} prêmios | {game_stats['jogos_com_11']} jogos diferentes")
    print()
    
    total_premios = sum(stats.values())
    total_jogos_premiados = len([r for r in results if r['total_11'] + r['total_12'] + r['total_13'] + r['total_14'] + r['total_15'] > 0])
    
    print(f"📈 RESUMO:")
    print(f"  Total de prêmios: {total_premios}")
    print(f"  Jogos que ganharam pelo menos 1 prêmio: {total_jogos_premiados} ({total_jogos_premiados/len(games)*100:.1f}%)")
    print(f"  Taxa de premiação: {total_premios/(len(games)*len(draws))*100:.2f}%")
    print()
    
    # Top 10 melhores jogos
    print("="*80)
    print("🏆 TOP 10 MELHORES JOGOS")
    print("="*80)
    for i, game in enumerate(best_games, 1):
        total_premios_jogo = game['total_11'] + game['total_12'] + game['total_13'] + game['total_14'] + game['total_15']
        print(f"\n{i:2d}. Jogo #{game['jogo_id']} (Score: {game['score']}/10)")
        print(f"    Prêmios: 15={game['total_15']}, 14={game['total_14']}, 13={game['total_13']}, 12={game['total_12']}, 11={game['total_11']} | Total: {total_premios_jogo}")
        
        if game['detalhes']:
            print(f"    Detalhes dos acertos:")
            for detail in game['detalhes']:
                print(f"      - Concurso {detail['concurso']} ({detail['data']}): {detail['acertos']} acertos")
    
    print()
    print("="*80)
    
    # Salva resultados detalhados
    output_dir = Path('out/optimized')
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # CSV com todos os resultados
    results_df = pd.DataFrame([{
        'jogo_id': r['jogo_id'],
        'score': r['score'],
        'total_premios': r['total_11'] + r['total_12'] + r['total_13'] + r['total_14'] + r['total_15'],
        'acertos_15': r['total_15'],
        'acertos_14': r['total_14'],
        'acertos_13': r['total_13'],
        'acertos_12': r['total_12'],
        'acertos_11': r['total_11'],
        'melhor_resultado': r['melhor_resultado'],
        'concurso_melhor': r['concurso_melhor']
    } for r in results])
    
    results_file = output_dir / 'comparacao_resultados.csv'
    results_df.to_csv(results_file, index=False)
    print(f"💾 Resultados detalhados salvos em: {results_file}")
    
    # Relatório detalhado
    report_file = output_dir / 'relatorio_comparacao.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RELATÓRIO DETALHADO - COMPARAÇÃO COM RESULTADOS REAIS\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Jogos analisados: {len(games)}\n")
        f.write(f"Sorteios analisados: {len(draws)} (concursos {draws[-1]['concurso']} a {draws[0]['concurso']})\n\n")
        
        f.write("PRÊMIOS CONQUISTADOS:\n")
        f.write(f"  15 acertos: {stats['total_15']}\n")
        f.write(f"  14 acertos: {stats['total_14']}\n")
        f.write(f"  13 acertos: {stats['total_13']}\n")
        f.write(f"  12 acertos: {stats['total_12']}\n")
        f.write(f"  11 acertos: {stats['total_11']}\n")
        f.write(f"  Total: {total_premios}\n\n")
        
        f.write("JOGOS COM MAIS PRÊMIOS:\n")
        f.write("-"*80 + "\n")
        for i, game in enumerate(best_games, 1):
            total_premios_jogo = game['total_11'] + game['total_12'] + game['total_13'] + game['total_14'] + game['total_15']
            f.write(f"\n{i}. Jogo #{game['jogo_id']} (Score: {game['score']}/10)\n")
            f.write(f"   Total de prêmios: {total_premios_jogo}\n")
            f.write(f"   15 acertos: {game['total_15']}\n")
            f.write(f"   14 acertos: {game['total_14']}\n")
            f.write(f"   13 acertos: {game['total_13']}\n")
            f.write(f"   12 acertos: {game['total_12']}\n")
            f.write(f"   11 acertos: {game['total_11']}\n")
            
            if game['detalhes']:
                f.write(f"\n   Detalhes:\n")
                for detail in game['detalhes']:
                    f.write(f"     Concurso {detail['concurso']} ({detail['data']}): {detail['acertos']} acertos\n")
    
    print(f"💾 Relatório completo salvo em: {report_file}")
    print()

if __name__ == '__main__':
    main()

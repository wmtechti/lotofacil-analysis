"""
Script de simulação Monte Carlo e teste de estratégias da Lotofácil.
"""
from __future__ import annotations

import os
import sys
import json
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.io_data import load_draws_csv
from src.game_generator import LotofacilGameGenerator
from src.monte_carlo import MonteCarloSimulator


def main():
    """Executa simulações Monte Carlo e testa estratégias."""
    print("="*80)
    print("🎲 SIMULAÇÃO MONTE CARLO - LOTOFÁCIL")
    print("="*80)
    
    os.makedirs("out", exist_ok=True)
    
    # 1. Carrega dados
    print("\n📂 Carregando dados...")
    df, ball_cols = load_draws_csv("data/lotofacil_sorteios.csv")
    hot_cold_df = pd.read_csv("out/numeros_quentes_frios.csv")
    pares_forca = pd.read_csv("out/pares_forca.csv")
    trends_df = pd.read_csv("out/tendencias_temporais.csv")
    
    with open("out/bias_borda_centro.json") as f:
        bias = json.load(f)
    
    print(f"   ✓ {len(df)} sorteios carregados")
    
    # 2. Inicializa gerador
    print("\n🎯 Inicializando gerador de jogos...")
    generator = LotofacilGameGenerator(hot_cold_df, pares_forca, trends_df, bias)
    
    # 3. Gera jogos com diferentes estratégias
    print("\n🎨 Gerando jogos com 6 estratégias (5 jogos cada)...")
    strategy_games = generator.generate_all_strategies(n_numbers=15, games_per_strategy=5)
    
    for strategy, games in strategy_games.items():
        print(f"\n   📋 {strategy}:")
        for i, game in enumerate(games, 1):
            print(f"      Jogo {i}: {game}")
    
    # 4. Salva jogos gerados
    all_games = []
    for strategy, games in strategy_games.items():
        for i, game in enumerate(games, 1):
            all_games.append({
                'estrategia': strategy,
                'jogo_id': i,
                'numeros': str(game)
            })
    
    pd.DataFrame(all_games).to_csv("out/jogos_gerados.csv", index=False)
    print("\n   ✓ Jogos salvos em: out/jogos_gerados.csv")
    
    # 5. Inicializa simulador
    print("\n🎰 Inicializando simulador Monte Carlo...")
    simulator = MonteCarloSimulator(df, ball_cols)
    
    # 6. Simula estratégias contra histórico
    print("\n📊 Testando estratégias contra histórico completo...")
    results_df = simulator.simulate_all_strategies(strategy_games)
    results_df.to_csv("out/resultados_estrategias.csv", index=False)
    print("   ✓ Resultados salvos em: out/resultados_estrategias.csv")
    
    # 7. Compara estratégias
    print("\n📈 Comparando performance das estratégias...")
    comparison = simulator.compare_strategies(results_df)
    comparison.to_csv("out/comparacao_estrategias.csv")
    
    print("\n" + "="*80)
    print("🏆 RANKING DE ESTRATÉGIAS")
    print("="*80)
    print(comparison.to_string())
    
    # 8. Melhores jogos
    print("\n" + "="*80)
    print("⭐ TOP 10 MELHORES JOGOS")
    print("="*80)
    best_games = simulator.validate_best_games(results_df, top_n=10)
    print(best_games.to_string(index=False))
    best_games.to_csv("out/melhores_jogos.csv", index=False)
    
    # 9. Monte Carlo puro (jogos aleatórios)
    print("\n" + "="*80)
    print("🎲 SIMULAÇÃO MONTE CARLO PURA (10.000 JOGOS ALEATÓRIOS)")
    print("="*80)
    mc_stats = simulator.monte_carlo_random(n_simulations=10000, n_numbers=15)
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Média de acertos: {mc_stats['media_acertos']:.2f} ± {mc_stats['desvio_acertos']:.2f}")
    print(f"   Min-Max acertos: {mc_stats['min_acertos']} - {mc_stats['max_acertos']}")
    print(f"\n🎁 PRÊMIOS (em {mc_stats['n_simulacoes']:,} simulações):")
    print(f"   11 acertos: {mc_stats['premios_11']:,} ({mc_stats['prob_11_acertos_%']:.3f}%)")
    print(f"   12 acertos: {mc_stats['premios_12']:,} ({mc_stats['prob_12_acertos_%']:.3f}%)")
    print(f"   13 acertos: {mc_stats['premios_13']:,} ({mc_stats['prob_13_acertos_%']:.3f}%)")
    print(f"   14 acertos: {mc_stats['premios_14']:,} ({mc_stats['prob_14_acertos_%']:.4f}%)")
    print(f"   15 acertos: {mc_stats['premios_15']:,} ({mc_stats['prob_15_acertos_%']:.6f}%)")
    print(f"\n   TOTAL de prêmios: {mc_stats['total_premios']:,}")
    print(f"   Probabilidade de ganhar algo: {mc_stats['prob_qualquer_premio_%']:.3f}%")
    
    # Salva estatísticas Monte Carlo
    with open("out/monte_carlo_stats.json", "w", encoding="utf-8") as f:
        json.dump(mc_stats, f, ensure_ascii=False, indent=2)
    
    # 10. Relatório final
    print("\n" + "="*80)
    print("💡 INSIGHTS FINAIS")
    print("="*80)
    
    best_strategy = comparison.index[0]
    best_avg = comparison.iloc[0]['media_acertos']
    best_prizes = comparison.iloc[0]['total_premios']
    
    print(f"\n✨ Melhor estratégia: {best_strategy}")
    print(f"   Média de acertos: {best_avg:.2f}")
    print(f"   Total de prêmios no histórico: {int(best_prizes)}")
    print(f"   Taxa de prêmio: {comparison.iloc[0]['taxa_premio_%']:.2f}%")
    
    print(f"\n📊 Comparado com jogos aleatórios:")
    print(f"   Aleatório: {mc_stats['media_acertos']:.2f} acertos")
    print(f"   Melhor estratégia: {best_avg:.2f} acertos")
    print(f"   Ganho: {best_avg - mc_stats['media_acertos']:+.2f} acertos")
    
    print("\n" + "="*80)
    print("✅ SIMULAÇÃO CONCLUÍDA!")
    print("="*80)
    print(f"\n📁 Arquivos gerados em out/:")
    print(f"   - jogos_gerados.csv")
    print(f"   - resultados_estrategias.csv")
    print(f"   - comparacao_estrategias.csv")
    print(f"   - melhores_jogos.csv")
    print(f"   - monte_carlo_stats.json")


if __name__ == "__main__":
    main()

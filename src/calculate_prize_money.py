"""
Calcula os valores monetários dos prêmios conquistados
"""

import pandas as pd
from pathlib import Path
import re

def parse_money(value):
    """Converte string de dinheiro para float"""
    if pd.isna(value) or value == 'NaN':
        return 0.0
    
    # Remove R$, pontos de milhar e substitui vírgula por ponto
    value_str = str(value).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(value_str)
    except:
        return 0.0

def load_prize_values(n=20):
    """Carrega os valores de prêmio dos últimos N sorteios"""
    draws_file = Path('data/lotofacil_sorteios.csv')
    df = pd.read_csv(draws_file)
    
    # Pega os últimos N sorteios
    recent = df.tail(n)
    
    prize_data = {
        '15': [],
        '14': [],
        '13': [],
        '12': [],
        '11': []
    }
    
    for _, row in recent.iterrows():
        # Valores de cada categoria
        value_15 = parse_money(row['Rateio 15 acertos'])
        value_14 = parse_money(row['Rateio 14 acertos'])
        value_13 = parse_money(row['Rateio 13 acertos'])
        value_12 = parse_money(row['Rateio 12 acertos'])
        value_11 = parse_money(row['Rateio 11 acertos'])
        
        # Só adiciona se teve ganhadores (valor > 0)
        if value_15 > 0:
            prize_data['15'].append(value_15)
        if value_14 > 0:
            prize_data['14'].append(value_14)
        if value_13 > 0:
            prize_data['13'].append(value_13)
        if value_12 > 0:
            prize_data['12'].append(value_12)
        if value_11 > 0:
            prize_data['11'].append(value_11)
    
    return prize_data

def calculate_average_prizes(prize_data):
    """Calcula a média de cada categoria"""
    averages = {}
    for category, values in prize_data.items():
        if values:
            averages[category] = sum(values) / len(values)
        else:
            averages[category] = 0.0
    
    return averages

def load_comparison_results():
    """Carrega os resultados da comparação"""
    results_file = Path('out/optimized/comparacao_resultados.csv')
    df = pd.read_csv(results_file)
    
    # Soma total de cada categoria
    totals = {
        '15': df['acertos_15'].sum(),
        '14': df['acertos_14'].sum(),
        '13': df['acertos_13'].sum(),
        '12': df['acertos_12'].sum(),
        '11': df['acertos_11'].sum(),
    }
    
    return totals

def main():
    print("="*80)
    print("💰 CÁLCULO DE PRÊMIOS EM DINHEIRO")
    print("="*80)
    print()
    
    # Carrega valores dos sorteios
    print("📊 Analisando valores dos últimos 20 sorteios...")
    prize_data = load_prize_values(20)
    
    # Calcula médias
    averages = calculate_average_prizes(prize_data)
    
    print()
    print("💵 VALORES MÉDIOS POR CATEGORIA (últimos 20 sorteios):")
    print("-"*80)
    print(f"  15 acertos: R$ {averages['15']:>12,.2f} (baseado em {len(prize_data['15'])} sorteios)")
    print(f"  14 acertos: R$ {averages['14']:>12,.2f} (baseado em {len(prize_data['14'])} sorteios)")
    print(f"  13 acertos: R$ {averages['13']:>12,.2f} (baseado em {len(prize_data['13'])} sorteios)")
    print(f"  12 acertos: R$ {averages['12']:>12,.2f} (baseado em {len(prize_data['12'])} sorteios)")
    print(f"  11 acertos: R$ {averages['11']:>12,.2f} (baseado em {len(prize_data['11'])} sorteios)")
    print()
    
    # Carrega resultados da comparação
    print("📋 Carregando resultados dos seus jogos...")
    totals = load_comparison_results()
    
    print()
    print("🎁 PRÊMIOS CONQUISTADOS (últimos 20 sorteios):")
    print("-"*80)
    print(f"  15 acertos: {totals['15']:4d} prêmios")
    print(f"  14 acertos: {totals['14']:4d} prêmios")
    print(f"  13 acertos: {totals['13']:4d} prêmios")
    print(f"  12 acertos: {totals['12']:4d} prêmios")
    print(f"  11 acertos: {totals['11']:4d} prêmios")
    print()
    
    # Calcula valores totais
    print("="*80)
    print("💸 CÁLCULO DOS GANHOS")
    print("="*80)
    print()
    
    earnings = {}
    total_earnings = 0.0
    
    for category in ['15', '14', '13', '12', '11']:
        value = totals[category] * averages[category]
        earnings[category] = value
        total_earnings += value
        
        print(f"  {category} acertos: {totals[category]:4d} prêmios × R$ {averages[category]:>10,.2f} = R$ {value:>15,.2f}")
    
    print("-"*80)
    print(f"  {'TOTAL DE GANHOS:':47s} R$ {total_earnings:>15,.2f}")
    print()
    
    # Investimento
    num_games = 333
    price_per_game = 3.50
    total_investment = num_games * price_per_game
    
    print("="*80)
    print("📊 ANÁLISE FINANCEIRA")
    print("="*80)
    print()
    print(f"  Investimento total: {num_games} jogos × R$ {price_per_game:.2f} = R$ {total_investment:>12,.2f}")
    print(f"  Total de ganhos:                              R$ {total_earnings:>12,.2f}")
    print("-"*80)
    
    profit = total_earnings - total_investment
    roi = (profit / total_investment) * 100 if total_investment > 0 else 0
    
    if profit > 0:
        print(f"  💚 LUCRO:                                      R$ {profit:>12,.2f}")
        print(f"  📈 ROI (Retorno sobre Investimento):          {roi:>12,.1f}%")
    else:
        print(f"  ❌ PREJUÍZO:                                   R$ {abs(profit):>12,.2f}")
        print(f"  📉 ROI (Retorno sobre Investimento):          {roi:>12,.1f}%")
    
    print()
    print("="*80)
    print("💡 OBSERVAÇÕES")
    print("="*80)
    print()
    print("  • Estes cálculos são baseados nos VALORES MÉDIOS dos últimos 20 sorteios")
    print("  • Os valores reais variam a cada sorteio conforme a arrecadação")
    print("  • Esta é uma análise RETROATIVA (o que teria acontecido)")
    print("  • Resultados passados NÃO garantem resultados futuros")
    print(f"  • Período analisado: {len(prize_data['11'])} sorteios recentes")
    print()
    
    # Projeção por sorteio
    if len(prize_data['11']) > 0:
        earnings_per_draw = total_earnings / len(prize_data['11'])
        investment_per_draw = total_investment / len(prize_data['11'])
        profit_per_draw = earnings_per_draw - investment_per_draw
        
        print("="*80)
        print("📊 MÉDIA POR SORTEIO")
        print("="*80)
        print()
        print(f"  Investimento por sorteio:       R$ {investment_per_draw:>10,.2f}")
        print(f"  Ganhos médios por sorteio:      R$ {earnings_per_draw:>10,.2f}")
        print(f"  {'Lucro' if profit_per_draw > 0 else 'Prejuízo'} médio por sorteio:       R$ {abs(profit_per_draw):>10,.2f}")
        print()
    
    # Salva relatório
    output_dir = Path('out/optimized')
    report_file = output_dir / 'relatorio_financeiro.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RELATÓRIO FINANCEIRO - ANÁLISE DE GANHOS\n")
        f.write("="*80 + "\n\n")
        
        f.write("VALORES MÉDIOS POR CATEGORIA:\n")
        for category in ['15', '14', '13', '12', '11']:
            f.write(f"  {category} acertos: R$ {averages[category]:,.2f}\n")
        f.write("\n")
        
        f.write("PRÊMIOS CONQUISTADOS:\n")
        for category in ['15', '14', '13', '12', '11']:
            f.write(f"  {category} acertos: {totals[category]} prêmios\n")
        f.write("\n")
        
        f.write("CÁLCULO DOS GANHOS:\n")
        for category in ['15', '14', '13', '12', '11']:
            f.write(f"  {category} acertos: {totals[category]} × R$ {averages[category]:,.2f} = R$ {earnings[category]:,.2f}\n")
        f.write(f"\nTOTAL DE GANHOS: R$ {total_earnings:,.2f}\n\n")
        
        f.write("ANÁLISE FINANCEIRA:\n")
        f.write(f"  Investimento: R$ {total_investment:,.2f}\n")
        f.write(f"  Ganhos: R$ {total_earnings:,.2f}\n")
        f.write(f"  {'Lucro' if profit > 0 else 'Prejuízo'}: R$ {abs(profit):,.2f}\n")
        f.write(f"  ROI: {roi:.1f}%\n")
    
    print(f"💾 Relatório financeiro salvo em: {report_file}")
    print()

if __name__ == '__main__':
    main()

"""
Análise dos 15 Números Mais Frios da Lotofácil

Este script analisa os 15 números que menos saíram na Lotofácil e
gera jogos otimizados EVITANDO esses números ou testando estratégias
que os incluem para verificar se há oportunidade.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json


class ColdNumbersAnalysis:
    """Análise focada nos números mais frios"""
    
    def __init__(self, top_n=15):
        self.top_n = top_n
        self.cold_numbers = []
        self.hot_numbers = []
        self.all_stats = None
        
    def load_data(self):
        """Carregar dados de frequência"""
        print("=" * 80)
        print(f"❄️  ANÁLISE DOS {self.top_n} NÚMEROS MAIS FRIOS - LOTOFÁCIL")
        print("=" * 80)
        
        # Carregar números quentes/frios
        df = pd.read_csv('out/lotofacil/numeros_quentes_frios.csv')
        self.all_stats = df
        
        # Ordenar por frequência (menor para maior)
        df_sorted = df.sort_values('freq', ascending=True)
        
        # Os N mais frios
        self.cold_numbers = list(df_sorted.head(self.top_n)['numero'].values)
        
        # Os N mais quentes (para comparação)
        self.hot_numbers = list(df.sort_values('freq', ascending=False).head(self.top_n)['numero'].values)
        
        print(f"\n❄️  OS {self.top_n} NÚMEROS MAIS FRIOS (que menos saíram):")
        print("-" * 80)
        
        for idx, row in df_sorted.head(self.top_n).iterrows():
            print(f"  {row['numero']:2d} - Frequência: {row['freq']:4d} | "
                  f"Esperado: {row['esperado']:.0f} | "
                  f"Desvio: {row['desvio_%']:+6.2f}% | {row['categoria']}")
        
        print(f"\n🔥 OS {self.top_n} NÚMEROS MAIS QUENTES (para comparação):")
        print("-" * 80)
        
        for idx, row in df.sort_values('freq', ascending=False).head(self.top_n).iterrows():
            print(f"  {row['numero']:2d} - Frequência: {row['freq']:4d} | "
                  f"Esperado: {row['esperado']:.0f} | "
                  f"Desvio: {row['desvio_%']:+6.2f}% | {row['categoria']}")
    
    def analyze_cold_presence(self):
        """Analisar presença dos números frios nos sorteios históricos"""
        print(f"\n" + "=" * 80)
        print("📊 ANÁLISE DE PRESENÇA DOS NÚMEROS FRIOS NOS SORTEIOS")
        print("=" * 80)
        
        # Carregar sorteios históricos
        df_draws = pd.read_csv('data/lotofacil_sorteios.csv')
        
        # Contar quantos números frios aparecem em cada sorteio
        cold_counts = []
        hot_counts = []
        
        for _, row in df_draws.iterrows():
            numbers = [int(row[f'Bola{i}']) for i in range(1, 16)]
            
            cold_in_draw = sum(1 for n in numbers if n in self.cold_numbers)
            hot_in_draw = sum(1 for n in numbers if n in self.hot_numbers)
            
            cold_counts.append(cold_in_draw)
            hot_counts.append(hot_in_draw)
        
        # Estatísticas
        print(f"\n📈 Estatísticas de Presença (em {len(df_draws)} sorteios):")
        print(f"\n  NÚMEROS FRIOS ({self.cold_numbers}):")
        print(f"    • Média por sorteio: {np.mean(cold_counts):.2f} números")
        print(f"    • Mínimo: {min(cold_counts)} números")
        print(f"    • Máximo: {max(cold_counts)} números")
        print(f"    • Sorteios sem nenhum frio: {sum(1 for c in cold_counts if c == 0)}")
        print(f"    • Sorteios com 3+ frios: {sum(1 for c in cold_counts if c >= 3)}")
        
        print(f"\n  NÚMEROS QUENTES ({self.hot_numbers}):")
        print(f"    • Média por sorteio: {np.mean(hot_counts):.2f} números")
        print(f"    • Mínimo: {min(hot_counts)} números")
        print(f"    • Máximo: {max(hot_counts)} números")
        print(f"    • Sorteios sem nenhum quente: {sum(1 for c in hot_counts if c == 0)}")
        print(f"    • Sorteios com 3+ quentes: {sum(1 for c in hot_counts if c >= 3)}")
        
        return cold_counts, hot_counts
    
    def analyze_cold_combinations(self):
        """Analisar pares entre números frios"""
        print(f"\n" + "=" * 80)
        print("🔗 ANÁLISE DE PARES ENTRE NÚMEROS FRIOS")
        print("=" * 80)
        
        # Carregar dados de pares
        df_pairs = pd.read_csv('out/lotofacil/pares_forca.csv')
        
        # Filtrar pares onde ambos são números frios
        cold_pairs = []
        for _, row in df_pairs.iterrows():
            if int(row['a']) in self.cold_numbers and int(row['b']) in self.cold_numbers:
                cold_pairs.append({
                    'par': f"{row['a']}-{row['b']}",
                    'count': row['count'],
                    'forca_%': row['forca_%'],
                    'categoria': row['categoria']
                })
        
        if cold_pairs:
            df_cold_pairs = pd.DataFrame(cold_pairs).sort_values('count', ascending=False)
            
            print(f"\n  Total de pares frios-frios: {len(df_cold_pairs)}")
            print(f"\n  TOP 10 Pares Mais Frequentes entre Números Frios:")
            print(df_cold_pairs.head(10).to_string(index=False))
        else:
            print("  Nenhum par significativo encontrado entre números frios.")
    
    def create_visualizations(self, cold_counts, hot_counts):
        """Criar visualizações comparativas"""
        print(f"\n📊 Gerando visualizações...")
        
        Path('out/cold_analysis').mkdir(exist_ok=True)
        
        # Figura 1: Comparação de frequências
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Números frios
        cold_stats = self.all_stats[self.all_stats['numero'].isin(self.cold_numbers)].sort_values('freq')
        axes[0].barh(cold_stats['numero'].astype(str), cold_stats['freq'], color='#3498db', edgecolor='black')
        axes[0].axvline(cold_stats['esperado'].iloc[0], color='red', linestyle='--', linewidth=2, label='Esperado')
        axes[0].set_xlabel('Frequência Total', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Número', fontsize=12, fontweight='bold')
        axes[0].set_title('7 Números Mais FRIOS', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3, axis='x')
        
        # Números quentes
        hot_stats = self.all_stats[self.all_stats['numero'].isin(self.hot_numbers)].sort_values('freq')
        axes[1].barh(hot_stats['numero'].astype(str), hot_stats['freq'], color='#e74c3c', edgecolor='black')
        axes[1].axvline(hot_stats['esperado'].iloc[0], color='red', linestyle='--', linewidth=2, label='Esperado')
        axes[1].set_xlabel('Frequência Total', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Número', fontsize=12, fontweight='bold')
        axes[1].set_title('7 Números Mais QUENTES', fontsize=14, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3, axis='x')
        
        plt.suptitle('Comparação: Números Mais Frios vs Mais Quentes', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig('out/cold_analysis/comparacao_frios_quentes.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Figura 2: Distribuição de presença nos sorteios
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Histograma números frios
        axes[0].hist(cold_counts, bins=range(0, 8), color='#3498db', alpha=0.7, edgecolor='black')
        axes[0].axvline(np.mean(cold_counts), color='red', linestyle='--', linewidth=2,
                       label=f'Média: {np.mean(cold_counts):.2f}')
        axes[0].set_xlabel('Quantidade de Números Frios no Sorteio', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Frequência', fontsize=12, fontweight='bold')
        axes[0].set_title('Distribuição: Números Frios por Sorteio', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3, axis='y')
        
        # Histograma números quentes
        axes[1].hist(hot_counts, bins=range(0, 8), color='#e74c3c', alpha=0.7, edgecolor='black')
        axes[1].axvline(np.mean(hot_counts), color='red', linestyle='--', linewidth=2,
                       label=f'Média: {np.mean(hot_counts):.2f}')
        axes[1].set_xlabel('Quantidade de Números Quentes no Sorteio', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Frequência', fontsize=12, fontweight='bold')
        axes[1].set_title('Distribuição: Números Quentes por Sorteio', fontsize=14, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.suptitle('Presença em Sorteios Históricos', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig('out/cold_analysis/distribuicao_presenca.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("  ✅ Visualizações salvas em: out/cold_analysis/")
    
    def generate_strategies(self):
        """Gerar estratégias baseadas nos números frios"""
        print(f"\n" + "=" * 80)
        print("🎯 ESTRATÉGIAS RECOMENDADAS")
        print("=" * 80)
        
        print(f"\n1️⃣ ESTRATÉGIA CONSERVADORA (Evitar Frios):")
        print(f"   • EVITAR os {self.top_n} números mais frios: {self.cold_numbers}")
        print(f"   • FOCAR nos {25 - self.top_n} números restantes")
        if self.top_n == 15:
            print(f"   • ⚠️ ATENÇÃO: Como você quer evitar 15 números e precisa selecionar 15,")
            print(f"   •            você só pode escolher os 10 números MAIS QUENTES!")
            print(f"   • Números disponíveis (10 mais quentes): {self.hot_numbers[:10]}")
        else:
            print(f"   • Selecionar 15 números dentre os {25 - self.top_n} mais frequentes")
        print(f"   • Aplicar dispersão espacial e equilíbrio regional")
        
        print(f"\n2️⃣ ESTRATÉGIA OPORTUNISTA (Apostar em Reversão):")
        print(f"   • INCLUIR 2-3 números frios (teoria de reversão à média)")
        print(f"   • Completar com 12-13 números quentes/médios")
        print(f"   • Números frios podem estar 'devendo' aparições")
        print(f"   • ⚠️ Risco maior, mas pode compensar se houver reversão")
        
        print(f"\n3️⃣ ESTRATÉGIA BALANCEADA (Híbrida):")
        print(f"   • INCLUIR 1 número frio")
        print(f"   • INCLUIR 2-3 números quentes")
        print(f"   • Completar com 11-12 números médios")
        print(f"   • Equilibrar risco e oportunidade")
        
        print(f"\n4️⃣ ESTRATÉGIA BASEADA EM DADOS (Melhor Histórico):")
        print(f"   • Usar números com desvio entre -2% e +2%")
        print(f"   • EVITAR extremos (muito quente OU muito frio)")
        print(f"   • Selecionar da faixa 'normal' de distribuição")
        print(f"   • Aplicar co-ocorrência e dispersão espacial")
        
        # Gerar exemplos de jogos
        print(f"\n" + "=" * 80)
        print("🎮 EXEMPLOS DE JOGOS")
        print("=" * 80)
        
        # Estratégia 1: Sem frios
        available = [n for n in range(1, 26) if n not in self.cold_numbers]
        if len(available) >= 15:
            game1 = sorted(np.random.choice(available, 15, replace=False))
            print(f"\n  Jogo 1 (SEM os {self.top_n} frios): {game1}")
            print(f"  Estratégia: Conservadora (usando {len(available)} números disponíveis)")
        else:
            print(f"\n  ⚠️ IMPOSSÍVEL gerar jogo SEM os {self.top_n} frios!")
            print(f"  Apenas {len(available)} números disponíveis (precisa de 15)")
            game1 = sorted(self.hot_numbers[:15])  # Usar os 15 mais quentes
            print(f"\n  Jogo 1 (15 MAIS QUENTES): {game1}")
            print(f"  Estratégia: Usar APENAS os números mais frequentes")
        
        # Estratégia 2: Com 3 frios
        available_non_cold = [n for n in range(1, 26) if n not in self.cold_numbers]
        if len(available_non_cold) >= 12 and len(self.cold_numbers) >= 3:
            game2 = sorted(
                list(np.random.choice(self.cold_numbers, 3, replace=False)) +
                list(np.random.choice(available_non_cold, 12, replace=False))
            )
            print(f"\n  Jogo 2 (COM 3 frios): {game2}")
            print(f"  Estratégia: Oportunista (reversão à média)")
        else:
            print(f"\n  ⚠️ Não há números suficientes para gerar jogo com 3 frios")
            print(f"  Disponíveis não-frios: {len(available_non_cold)} (precisa de 12)")
        
        # Estratégia 3: Balanceado
        available_medium = [n for n in range(1, 26) if n not in self.cold_numbers and n not in self.hot_numbers]
        if len(available_medium) >= 11:
            game3 = sorted(
                list(np.random.choice(self.cold_numbers, 1, replace=False)) +
                list(np.random.choice(self.hot_numbers, 3, replace=False)) +
                list(np.random.choice(available_medium, 11, replace=False))
            )
            print(f"\n  Jogo 3 (BALANCEADO): {game3}")
            print(f"  Estratégia: Híbrida (1 frio + 3 quentes + médios)")
        else:
            print(f"\n  ⚠️ Overlap detectado: alguns números estão em múltiplas categorias")
            print(f"  Gerando jogo alternativo...")
            game3 = sorted(
                list(np.random.choice(self.cold_numbers[:5], 3, replace=False)) +
                list(np.random.choice(self.hot_numbers[:5], 5, replace=False)) +
                list(np.random.choice(range(1, 26), 7, replace=False))
            )
            print(f"\n  Jogo 3 (ALTERNATIVO): {game3}")
            print(f"  Estratégia: Mix de frios, quentes e aleatórios")
    
    def save_report(self):
        """Salvar relatório completo"""
        print(f"\n💾 Salvando relatório...")
        
        report = f"""
RELATÓRIO: ANÁLISE DOS {self.top_n} NÚMEROS MAIS FRIOS - LOTOFÁCIL
{'=' * 80}

📊 NÚMEROS MAIS FRIOS (que menos saíram):
{self.all_stats.sort_values('freq').head(self.top_n).to_string(index=False)}

🔥 NÚMEROS MAIS QUENTES (para comparação):
{self.all_stats.sort_values('freq', ascending=False).head(self.top_n).to_string(index=False)}
{'=' * 80}

📊 NÚMEROS MAIS FRIOS (que menos saíram):
{self.all_stats.sort_values('freq').head(7).to_string(index=False)}

🔥 NÚMEROS MAIS QUENTES (para comparação):
{self.all_stats.sort_values('freq', ascending=False).head(7).to_string(index=False)}

💡 CONCLUSÕES:

1. Os {self.top_n} números mais frios representam {self.top_n/25*100:.0f}% do total de números
2. Desvios observados em relação ao esperado
3. {'⚠️ CRÍTICO: Evitar 15 números deixa apenas 10 disponíveis!' if self.top_n == 15 else 'Diferenças são estatisticamente PEQUENAS'}
4. Padrões de frequência podem não persistir no futuro

⚠️ AVISOS:

• Não há garantia de que números frios "devem" sair mais
• Desvios observados estão dentro do esperado para eventos aleatórios
• A "reversão à média" pode levar centenas de sorteios para ocorrer
• Estratégias baseadas apenas em frequência têm eficácia limitada

🎯 RECOMENDAÇÃO FINAL:

Combine a análise de números frios/quentes com:
• Dispersão espacial (distribuição no grid 5×5)
• Equilíbrio regional (linhas e colunas)
• Super pares (co-ocorrência comprovada)
• Evitar muitos números adjacentes

Arquivos gerados:
• out/cold_analysis/comparacao_frios_quentes.png
• out/cold_analysis/distribuicao_presenca.png
• out/cold_analysis/relatorio_numeros_frios.txt
"""
        
        with open('out/cold_analysis/relatorio_numeros_frios.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("  ✅ Relatório salvo em: out/cold_analysis/relatorio_numeros_frios.txt")


def main():
    """Executar análise completa"""
    analyzer = ColdNumbersAnalysis(top_n=15)  # Analisar 15 números mais frios
    
    # Carregar dados
    analyzer.load_data()
    
    # Analisar presença nos sorteios
    cold_counts, hot_counts = analyzer.analyze_cold_presence()
    
    # Analisar combinações
    analyzer.analyze_cold_combinations()
    
    # Criar visualizações
    analyzer.create_visualizations(cold_counts, hot_counts)
    
    # Gerar estratégias
    analyzer.generate_strategies()
    
    # Salvar relatório
    analyzer.save_report()
    
    print("\n" + "=" * 80)
    print("✅ ANÁLISE DOS NÚMEROS FRIOS CONCLUÍDA!")
    print("=" * 80)


if __name__ == '__main__':
    main()

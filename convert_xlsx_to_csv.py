"""
Script para converter o arquivo XLSX para CSV.
"""
import pandas as pd

# Ler o arquivo Excel
df = pd.read_excel('data/lotofacil_sorteios.xlsx')

# Salvar como CSV
df.to_csv('data/lotofacil_sorteios.csv', index=False, encoding='utf-8')

print("✅ Arquivo convertido com sucesso!")
print(f"📊 Total de linhas: {len(df)}")
print(f"📋 Colunas: {list(df.columns)}")
print("\nPrimeiras linhas:")
print(df.head())

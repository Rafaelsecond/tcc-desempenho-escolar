from pathlib import Path
import pandas as pd

pasta_inep = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\raw\2. INEP — Indicadores Educacionais (Fatores Docentes e Socioeconômicos)"
)

# Caminhos dos arquivos de 2023
arq_inse = pasta_inep / "D. Nível Socioeconômico (INSE)" / "INSE_2023" / "INSE_2023_escolas.xlsx"
arq_ird = (
    pasta_inep
    / "A. Regularidade do Corpo Docente (IRD)"
    / "2023 Regularidade do Corpo Docente"
    / "IRD_2023_ESCOLAS"
    / "IRD_ESCOLAS_2023.xlsx"
)

print("==================================================")
print("1. INSPECIONANDO CABEÇALHO DO INSE 2023")
print("==================================================")
# Lemos as primeiras 12 linhas sem definir header para ver onde ele começa
df_inse_raw = pd.read_excel(arq_inse, nrows=12, header=None)
for idx, row in df_inse_raw.iterrows():
    # Exibe os primeiros 6 valores não nulos de cada linha
    valores = [str(v) for v in row.values if pd.notna(v)][:6]
    print(f"Linha {idx}: {valores}")

print("\n==================================================")
print("2. INSPECIONANDO CABEÇALHO DO IRD 2023")
print("==================================================")
df_ird_raw = pd.read_excel(arq_ird, nrows=12, header=None)
for idx, row in df_ird_raw.iterrows():
    valores = [str(v) for v in row.values if pd.notna(v)][:6]
    print(f"Linha {idx}: {valores}")
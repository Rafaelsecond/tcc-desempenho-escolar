from pathlib import Path
import pandas as pd

pasta_inep = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\raw\2. INEP — Indicadores Educacionais (Fatores Docentes e Socioeconômicos)"
)

arq_inse = (
    pasta_inep
    / "D. Nível Socioeconômico (INSE)"
    / "INSE_2023"
    / "INSE_2023_escolas.xlsx"
)
arq_ird = (
    pasta_inep
    / "A. Regularidade do Corpo Docente (IRD)"
    / "2023 Regularidade do Corpo Docente"
    / "IRD_2023_ESCOLAS"
    / "IRD_ESCOLAS_2023.xlsx"
)

# -------------------------------------------------------------------------
# 1. DETALHANDO INSE 2023
# -------------------------------------------------------------------------
print("==================================================")
print("1. COLUNAS E AMOSTRA DO INSE 2023 (header=0)")
print("==================================================")
df_inse = pd.read_excel(arq_inse, header=0, nrows=100)

print(f"Total de colunas no INSE: {len(df_inse.columns)}")
print("Lista de colunas:")
for col in df_inse.columns:
    print(f" - {col}")

# Filtra uma amostra de SP para vermos os valores reais
df_inse_sp = df_inse[df_inse["SG_UF"] == "SP"]
if not df_inse_sp.empty:
    print("\nExemplo de linha de SP no INSE:")
    print(df_inse_sp.iloc[0].to_dict())
else:
    print("\nPrimeira linha geral (RO):")
    print(df_inse.iloc[0].to_dict())

# -------------------------------------------------------------------------
# 2. DETALHANDO IRD 2023
# -------------------------------------------------------------------------
print("\n==================================================")
print("2. COLUNAS E AMOSTRA DO IRD 2023 (header=10)")
print("==================================================")
df_ird = pd.read_excel(arq_ird, header=10, nrows=100)

print(f"Total de colunas no IRD: {len(df_ird.columns)}")
print("Lista de colunas:")
for col in df_ird.columns:
    print(f" - {col}")

df_ird_sp = df_ird[df_ird["SG_UF"] == "SP"]
if not df_ird_sp.empty:
    print("\nExemplo de linha de SP no IRD:")
    print(df_ird_sp.iloc[0].to_dict())
else:
    print("\nPrimeira linha geral (RO):")
    print(df_ird.iloc[0].to_dict())
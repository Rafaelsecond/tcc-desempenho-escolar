from pathlib import Path
import pandas as pd

pasta_inep = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\raw\2. INEP — Indicadores Educacionais (Fatores Docentes e Socioeconômicos)"
)

arq_ied = (
    pasta_inep
    / "B. Esforço Docente (IED)"
    / "2023 IED"
    / "IED_2023_ESCOLAS"
    / "IED_ESCOLAS_2023.xlsx"
)

# Lemos com header=10 e apenas 5 linhas
df_ied = pd.read_excel(arq_ied, header=10, nrows=5)

print(f"Total de colunas no IED: {len(df_ied.columns)}")
print("\nLista de todas as colunas técnicas do IED:")
for col in df_ied.columns:
    print(f" - {col}")
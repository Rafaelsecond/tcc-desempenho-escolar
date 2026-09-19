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

print(f"Inspecionando: {arq_ied.name}\n")

# Lemos as primeiras 12 linhas sem header para detectar a linha correta
df_raw = pd.read_excel(arq_ied, nrows=12, header=None)
for idx, row in df_raw.iterrows():
    valores = [str(v) for v in row.values if pd.notna(v)][:6]
    print(f"Linha {idx}: {valores}")
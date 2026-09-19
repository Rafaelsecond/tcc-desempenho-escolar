from pathlib import Path
import pandas as pd

pasta_inep = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\raw\2. INEP — Indicadores Educacionais (Fatores Docentes e Socioeconômicos)"
)
pasta_silver = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\silver"
)

arq_base = pasta_silver / "01_escolas_base.parquet"
arq_ird = (
    pasta_inep
    / "A. Regularidade do Corpo Docente (IRD)"
    / "2023 Regularidade do Corpo Docente"
    / "IRD_2023_ESCOLAS"
    / "IRD_ESCOLAS_2023.xlsx"
)

# 1. Ver como estão as chaves na Base de Escolas (Passo 1)
df_base = pd.read_parquet(arq_base)
print("--- Amostra de chaves da 01_escolas_base.parquet ---")
print(df_base["CO_ENTIDADE"].head(5).tolist())

# 2. Ler uma amostra do IRD 2023
df_ird = pd.read_excel(arq_ird, header=10, nrows=100)
print("\n--- Amostra de colunas e dados brutos do IRD 2023 ---")
print("Colunas lidas:", df_ird.columns.tolist()[:6])
print("Tipos de dados:\n", df_ird[["CO_ENTIDADE", "EDU_BAS_CAT_0"]].dtypes)
print(
    "\nAmostra de CO_ENTIDADE brutos no IRD:",
    df_ird["CO_ENTIDADE"].head(5).tolist(),
)
print(
    "Amostra de EDU_BAS_CAT_0 no IRD:", df_ird["EDU_BAS_CAT_0"].head(5).tolist()
)

# 3. Ler mais linhas do IRD para verificar o range de valores de EDU_BAS_CAT_0 em SP
df_ird_sp = pd.read_excel(
    arq_ird, header=10, usecols=["SG_UF", "CO_ENTIDADE", "EDU_BAS_CAT_0"]
)
df_ird_sp = df_ird_sp[df_ird_sp["SG_UF"] == "SP"]
print("\n--- Estatísticas do IRD em SP ---")
print(f"Total de linhas em SP: {len(df_ird_sp)}")
print(
    f"Valores únicos estranhos ou nulos em EDU_BAS_CAT_0: {df_ird_sp['EDU_BAS_CAT_0'].isna().sum()} nulos"
)
valores_invalidos = df_ird_sp[
    (df_ird_sp["EDU_BAS_CAT_0"] < 1.0) | (df_ird_sp["EDU_BAS_CAT_0"] > 5.0)
]
print(f"Total de valores fora de [1.0, 5.0]: {len(valores_invalidos)}")
if not valores_invalidos.empty:
    print("Exemplos de valores fora da escala:")
    print(valores_invalidos.head(5))
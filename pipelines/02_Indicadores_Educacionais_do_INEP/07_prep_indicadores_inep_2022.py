"""PIPELINE 02 (2022): PROCESSAMENTO DOS INDICADORES INEP (IRD E IED 2022)

Camada: Bronze -> Silver
Indicadores:
  - IRD: Indicador de Regularidade do Corpo Docente (2022)
  - IED: Indicador de Esforço Docente - Ensino Médio (2022)
Saída:
  - data/silver/02_indicadores_inep_2022.parquet
"""

from pathlib import Path
import numpy as np
import pandas as pd

DIRETORIO_RAIZ = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
PASTA_INEP = (
    DIRETORIO_RAIZ
    / "data"
    / "raw"
    / "2. INEP — Indicadores Educacionais (Fatores Docentes e Socioeconômicos)"
)
PASTA_SILVER = DIRETORIO_RAIZ / "data" / "silver"

ARQ_IRD = (
    PASTA_INEP
    / "A. Regularidade do Corpo Docente (IRD)"
    / "2022 Regularidade do Corpo Docente"
    / "IRD_2022_ESCOLAS"
    / "IRD_ESCOLAS_2022.xlsx"
)
ARQ_IED = (
    PASTA_INEP
    / "B. Esforço Docente (IED)"
    / "2022 IED"
    / "IED_2022_ESCOLAS"
    / "IED_ESCOLAS_2022.xlsx"
)

ARQ_ESCOLAS_BASE_2022 = PASTA_SILVER / "01_escolas_base_2022.parquet"
ARQUIVO_SAIDA = PASTA_SILVER / "02_indicadores_inep_2022.parquet"

print("=================================================================")
print("INICIANDO PIPELINE 02 (2022): INDICADORES EDUCACIONAIS DO INEP")
print("=================================================================\n")


def formatar_codigo_inep(serie):
    return serie.astype(str).str.split(".").str[0].str.strip().str.zfill(8)


# 1. PROCESSAMENTO DO IRD 2022
print("1. Lendo e processando IRD 2022...")
cols_ird = ["SG_UF", "CO_ENTIDADE", "EDU_BAS_CAT_0"]
df_ird = pd.read_excel(ARQ_IRD, header=10, usecols=cols_ird)
df_ird = df_ird[df_ird["SG_UF"] == "SP"].dropna(subset=["CO_ENTIDADE"]).copy()

df_ird["CO_ENTIDADE"] = formatar_codigo_inep(df_ird["CO_ENTIDADE"])
df_ird["IRD_MEDIO"] = pd.to_numeric(df_ird["EDU_BAS_CAT_0"], errors="coerce")

df_ird = df_ird[["CO_ENTIDADE", "IRD_MEDIO"]].drop_duplicates(
    subset=["CO_ENTIDADE"]
)
print(f"   -> Escolas de SP com IRD 2022: {len(df_ird):,}")

# 2. PROCESSAMENTO DO IED 2022
print("\n2. Lendo e processando IED 2022...")
cols_ied = [
    "SG_UF",
    "CO_ENTIDADE",
    "MED_CAT_1",
    "MED_CAT_2",
    "MED_CAT_3",
    "MED_CAT_4",
    "MED_CAT_5",
    "MED_CAT_6",
]
df_ied = pd.read_excel(ARQ_IED, header=10, usecols=cols_ied)
df_ied = df_ied[df_ied["SG_UF"] == "SP"].dropna(subset=["CO_ENTIDADE"]).copy()

df_ied["CO_ENTIDADE"] = formatar_codigo_inep(df_ied["CO_ENTIDADE"])

for i in range(1, 7):
    df_ied[f"MED_CAT_{i}"] = pd.to_numeric(
        df_ied[f"MED_CAT_{i}"], errors="coerce"
    )

df_ied["IED_SCORE_MEDIO"] = (
    1 * df_ied["MED_CAT_1"].fillna(0)
    + 2 * df_ied["MED_CAT_2"].fillna(0)
    + 3 * df_ied["MED_CAT_3"].fillna(0)
    + 4 * df_ied["MED_CAT_4"].fillna(0)
    + 5 * df_ied["MED_CAT_5"].fillna(0)
    + 6 * df_ied["MED_CAT_6"].fillna(0)
) / 100.0

df_ied["IED_ESFORCO_ALTO"] = df_ied["MED_CAT_5"].fillna(0) + df_ied[
    "MED_CAT_6"
].fillna(0)

df_ied = df_ied[
    [
        "CO_ENTIDADE",
        "IED_SCORE_MEDIO",
        "IED_ESFORCO_ALTO",
        "MED_CAT_1",
        "MED_CAT_2",
        "MED_CAT_3",
        "MED_CAT_4",
        "MED_CAT_5",
        "MED_CAT_6",
    ]
].drop_duplicates(subset=["CO_ENTIDADE"])
print(f"   -> Escolas de SP com IED 2022: {len(df_ied):,}")

# 3. JUNÇÃO DOS INDICADORES 2022
print("\n3. Consolidando indicadores 2022...")
df_indicadores_2022 = pd.merge(df_ird, df_ied, on="CO_ENTIDADE", how="outer")
print(
    f"   -> Total de escolas únicas de SP com indicadores: {len(df_indicadores_2022):,}"
)

# 4. QUALITY GATES & COBERTURA COM A BASE DE 2022
print("\n4. Executando Quality Gates de Validação contra a Base 2022...")
df_base_2022 = pd.read_parquet(ARQ_ESCOLAS_BASE_2022)
total_escolas = len(df_base_2022)

df_cobertura = pd.merge(
    df_base_2022[["CO_ENTIDADE"]], df_indicadores_2022, on="CO_ENTIDADE", how="left"
)
cob_ird = df_cobertura["IRD_MEDIO"].notna().sum()
cob_ied = df_cobertura["IED_SCORE_MEDIO"].notna().sum()

print(
    f"   [COBERTURA 2022] IRD: {cob_ird}/{total_escolas} escolas ({cob_ird/total_escolas*100:.1f}%)"
)
print(
    f"   [COBERTURA 2022] IED: {cob_ied}/{total_escolas} escolas ({cob_ied/total_escolas*100:.1f}%)"
)

ird_valid = df_indicadores_2022["IRD_MEDIO"].dropna()
assert (
    (ird_valid >= 0.0) & (ird_valid <= 5.0)
).all(), "Erro: IRD 2022 fora do limite [0.0, 5.0]!"
print("   [PASS] IRD 2022 dentro do limite [0.0, 5.0].")

ied_valid = df_indicadores_2022["IED_SCORE_MEDIO"].dropna()
assert (
    (ied_valid >= 0.0) & (ied_valid <= 6.0)
).all(), "Erro: IED Score 2022 fora do limite [0.0, 6.0]!"
print("   [PASS] IED Score 2022 dentro do limite [0.0, 6.0].")

# 5. EXPORTAÇÃO
df_indicadores_2022.to_parquet(ARQUIVO_SAIDA, index=False, engine="pyarrow")
print(
    f"\n[SUCESSO] Base Silver de Indicadores 2022 gerada: {ARQUIVO_SAIDA.name}"
)
print(
    f"   Dimensões: {df_indicadores_2022.shape[0]} linhas x {df_indicadores_2022.shape[1]} colunas\n"
)
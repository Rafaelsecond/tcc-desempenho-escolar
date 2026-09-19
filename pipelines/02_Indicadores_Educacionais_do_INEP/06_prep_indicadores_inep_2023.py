"""PIPELINE 02: PROCESSAMENTO DOS INDICADORES EDUCACIONAIS DO INEP (2023) - CORRIGIDO

Camada: Bronze -> Silver
Indicadores:
  - INSE: Nível Socioeconômico das Escolas
  - IRD: Indicador de Regularidade do Corpo Docente
  - IED: Indicador de Esforço Docente (Ensino Médio)
Saída:
  - data/silver/02_indicadores_inep.parquet
"""

from pathlib import Path
import numpy as np
import pandas as pd

# -------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DE CAMINHOS
# -------------------------------------------------------------------------
DIRETORIO_RAIZ = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
PASTA_INEP = (
    DIRETORIO_RAIZ
    / "data"
    / "raw"
    / "2. INEP — Indicadores Educacionais (Fatores Docentes e Socioeconômicos)"
)
PASTA_SILVER = DIRETORIO_RAIZ / "data" / "silver"

ARQ_INSE = (
    PASTA_INEP
    / "D. Nível Socioeconômico (INSE)"
    / "INSE_2023"
    / "INSE_2023_escolas.xlsx"
)
ARQ_IRD = (
    PASTA_INEP
    / "A. Regularidade do Corpo Docente (IRD)"
    / "2023 Regularidade do Corpo Docente"
    / "IRD_2023_ESCOLAS"
    / "IRD_ESCOLAS_2023.xlsx"
)
ARQ_IED = (
    PASTA_INEP
    / "B. Esforço Docente (IED)"
    / "2023 IED"
    / "IED_2023_ESCOLAS"
    / "IED_ESCOLAS_2023.xlsx"
)

ARQ_ESCOLAS_BASE = PASTA_SILVER / "01_escolas_base.parquet"
ARQUIVO_SAIDA = PASTA_SILVER / "02_indicadores_inep.parquet"

print("=================================================================")
print("INICIANDO PIPELINE 02: INDICADORES EDUCACIONAIS DO INEP (SILVER)")
print("=================================================================\n")


def formatar_codigo_inep(serie):
    """Remove qualquer '.0' proveniente de floats do Excel e garante 8 dígitos."""
    return serie.astype(str).str.split(".").str[0].str.strip().str.zfill(8)


# -------------------------------------------------------------------------
# 2. PROCESSAMENTO DO INSE 2023 (NÍVEL SOCIOECONÔMICO)
# -------------------------------------------------------------------------
print("1. Lendo e processando INSE 2023...")
cols_inse = [
    "SG_UF",
    "ID_ESCOLA",
    "QTD_ALUNOS_INSE",
    "MEDIA_INSE",
    "INSE_CLASSIFICACAO",
]
df_inse = pd.read_excel(ARQ_INSE, header=0, usecols=cols_inse)
df_inse = df_inse[df_inse["SG_UF"] == "SP"].copy()

df_inse["CO_ENTIDADE"] = formatar_codigo_inep(df_inse["ID_ESCOLA"])
df_inse["MEDIA_INSE"] = pd.to_numeric(df_inse["MEDIA_INSE"], errors="coerce")
df_inse["QTD_ALUNOS_INSE"] = pd.to_numeric(
    df_inse["QTD_ALUNOS_INSE"], errors="coerce"
)
df_inse["INSE_CLASSIFICACAO"] = df_inse["INSE_CLASSIFICACAO"].astype(str).str.strip()

df_inse = df_inse[
    ["CO_ENTIDADE", "MEDIA_INSE", "INSE_CLASSIFICACAO", "QTD_ALUNOS_INSE"]
].drop_duplicates(subset=["CO_ENTIDADE"])
print(f"   -> Escolas de SP com INSE processadas: {len(df_inse):,}")

# -------------------------------------------------------------------------
# 3. PROCESSAMENTO DO IRD 2023 (REGULARIDADE DOCENTE)
# -------------------------------------------------------------------------
print("\n2. Lendo e processando IRD 2023...")
cols_ird = ["SG_UF", "CO_ENTIDADE", "EDU_BAS_CAT_0"]
df_ird = pd.read_excel(ARQ_IRD, header=10, usecols=cols_ird)
df_ird = df_ird[df_ird["SG_UF"] == "SP"].copy()

# Remove nulos e formata código sem .0
df_ird = df_ird.dropna(subset=["CO_ENTIDADE"]).copy()
df_ird["CO_ENTIDADE"] = formatar_codigo_inep(df_ird["CO_ENTIDADE"])
df_ird["IRD_MEDIO"] = pd.to_numeric(df_ird["EDU_BAS_CAT_0"], errors="coerce")

df_ird = df_ird[["CO_ENTIDADE", "IRD_MEDIO"]].drop_duplicates(
    subset=["CO_ENTIDADE"]
)
print(f"   -> Escolas de SP com IRD processadas: {len(df_ird):,}")

# -------------------------------------------------------------------------
# 4. PROCESSAMENTO DO IED 2023 (ESFORÇO DOCENTE - ENSINO MÉDIO)
# -------------------------------------------------------------------------
print("\n3. Lendo e processando IED 2023...")
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
df_ied = df_ied[df_ied["SG_UF"] == "SP"].copy()

df_ied = df_ied.dropna(subset=["CO_ENTIDADE"]).copy()
df_ied["CO_ENTIDADE"] = formatar_codigo_inep(df_ied["CO_ENTIDADE"])

for i in range(1, 7):
    df_ied[f"MED_CAT_{i}"] = pd.to_numeric(
        df_ied[f"MED_CAT_{i}"], errors="coerce"
    )

# Feature Engineering: Média Ponderada (1.0 a 6.0) e Esforço Alto (Níveis 5 e 6)
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
print(f"   -> Escolas de SP com IED processadas: {len(df_ied):,}")

# -------------------------------------------------------------------------
# 5. JUNÇÃO DOS INDICADORES
# -------------------------------------------------------------------------
print("\n4. Consolidando os três indicadores do INEP...")
df_indicadores = pd.merge(df_inse, df_ird, on="CO_ENTIDADE", how="outer")
df_indicadores = pd.merge(df_indicadores, df_ied, on="CO_ENTIDADE", how="outer")

print(
    f"   -> Total de escolas únicas de SP com algum indicador INEP: {len(df_indicadores):,}"
)

# -------------------------------------------------------------------------
# 6. QUALITY GATES & COBERTURA COM A BASE DE ESCOLAS DO PASSO 1
# -------------------------------------------------------------------------
print("\n5. Executando Quality Gates e Verificação de Cobertura...")

df_base_escolas = pd.read_parquet(ARQ_ESCOLAS_BASE)
total_escolas_estudo = len(df_base_escolas)

df_cobertura = pd.merge(
    df_base_escolas[["CO_ENTIDADE", "NOMESC"]],
    df_indicadores,
    on="CO_ENTIDADE",
    how="left",
)

cob_inse = df_cobertura["MEDIA_INSE"].notna().sum()
cob_ird = df_cobertura["IRD_MEDIO"].notna().sum()
cob_ied = df_cobertura["IED_SCORE_MEDIO"].notna().sum()

print(
    f"   [COBERTURA] INSE: {cob_inse}/{total_escolas_estudo} escolas ({cob_inse/total_escolas_estudo*100:.1f}%)"
)
print(
    f"   [COBERTURA] IRD:  {cob_ird}/{total_escolas_estudo} escolas ({cob_ird/total_escolas_estudo*100:.1f}%)"
)
print(
    f"   [COBERTURA] IED:  {cob_ied}/{total_escolas_estudo} escolas ({cob_ied/total_escolas_estudo*100:.1f}%)"
)

# Validação dos limites estatísticos reais do INEP
ird_valid = df_indicadores["IRD_MEDIO"].dropna()
assert (
    (ird_valid >= 0.0) & (ird_valid <= 5.0)
).all(), "Erro: IRD fora do limite [0.0, 5.0]!"
print("   [PASS] IRD estritamente contido no intervalo teórico [0.0, 5.0].")

ied_valid = df_indicadores["IED_SCORE_MEDIO"].dropna()
assert (
    (ied_valid >= 0.0) & (ied_valid <= 6.0)
).all(), "Erro: IED Score fora do limite [0.0, 6.0]!"
print("   [PASS] IED Score estritamente contido no intervalo teórico [0.0, 6.0].")

# -------------------------------------------------------------------------
# 7. EXPORTAÇÃO ARTEFATO SILVER (PARQUET)
# -------------------------------------------------------------------------
df_indicadores.to_parquet(ARQUIVO_SAIDA, index=False, engine="pyarrow")
print(f"\n[SUCESSO] Base Silver de Indicadores INEP gerada com sucesso:")
print(f"   Destino: {ARQUIVO_SAIDA}")
print(
    f"   Dimensões: {df_indicadores.shape[0]} linhas x {df_indicadores.shape[1]} colunas"
)
print(f"   Tamanho do arquivo: {ARQUIVO_SAIDA.stat().st_size / 1024:.1f} KB")

# Amostra das primeiras 3 escolas
print("\n--- Amostra dos Indicadores ---")
print(
    df_indicadores[
        [
            "CO_ENTIDADE",
            "MEDIA_INSE",
            "INSE_CLASSIFICACAO",
            "IRD_MEDIO",
            "IED_SCORE_MEDIO",
            "IED_ESFORCO_ALTO",
        ]
    ].head(3)
)
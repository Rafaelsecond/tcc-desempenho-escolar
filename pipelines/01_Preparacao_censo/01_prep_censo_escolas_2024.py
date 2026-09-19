"""PIPELINE 01 (2024): PREPARAÇÃO DA BASE DE ESCOLAS (CENSO 2024 + SEDUC 2024)

Camada: Bronze -> Silver
Entradas:
  - data/raw/1. SEDUC-SP — SARESP & Cadastro de Escolas/B - Tabela de Ligação/ENDERECO_ESCOLAS_072024.csv
  - data/raw/3. INEP — Censo Escolar da Educação Básica (Infraestrutura)/2024 microdados_censo_escolar/dados/microdados_ed_basica_2024.csv
Saída:
  - data/silver/01_escolas_base_2024.parquet
"""

from pathlib import Path
import numpy as np
import pandas as pd

DIRETORIO_RAIZ = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")

ARQUIVO_SEDUC = (
    DIRETORIO_RAIZ
    / "data"
    / "raw"
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "B - Tabela de Ligação (De-Para CIE - INEP)"
    / "ENDERECO_ESCOLAS_072024.csv"
)

ARQUIVO_CENSO = (
    DIRETORIO_RAIZ
    / "data"
    / "raw"
    / "3. INEP — Censo Escolar da Educação Básica (Infraestrutura)"
    / "2024 microdados_censo_escolar"
    / "dados"
    / "microdados_ed_basica_2024.csv"
)

PASTA_SILVER = DIRETORIO_RAIZ / "data" / "silver"
PASTA_SILVER.mkdir(parents=True, exist_ok=True)
ARQUIVO_SAIDA = PASTA_SILVER / "01_escolas_base_2024.parquet"

print("=================================================================")
print("INICIANDO PIPELINE 01 (2024): PREPARAÇÃO DA BASE DE ESCOLAS")
print("=================================================================\n")

# 1. PROCESSAMENTO SEDUC 2024
print("1. Processando Cadastro SEDUC 2024...")
colunas_seduc = [
    "NOMEDEP",
    "DE",
    "MUN",
    "CD_IBGE",
    "COD_ESC",
    "CODESCMEC",
    "NOMESC",
    "DS_LATITUDE",
    "DS_LONGITUDE",
]

df_seduc = pd.read_csv(
    ARQUIVO_SEDUC,
    sep=";",
    encoding="latin1",
    usecols=lambda c: any(
        c.replace("ï»¿", "").strip() == col for col in colunas_seduc
    ),
    dtype=str,
)

df_seduc.columns = [c.replace("ï»¿", "").strip() for c in df_seduc.columns]
df_seduc = df_seduc[df_seduc["NOMEDEP"].str.strip() == "ESTADUAL - SE"].copy()

df_seduc["CODESC"] = df_seduc["COD_ESC"].str.strip().str.zfill(6)
df_seduc["CO_ENTIDADE"] = df_seduc["CODESCMEC"].str.strip().str.zfill(8)

df_seduc["DS_LATITUDE"] = pd.to_numeric(
    df_seduc["DS_LATITUDE"].str.replace(",", "."), errors="coerce"
)
df_seduc["DS_LONGITUDE"] = pd.to_numeric(
    df_seduc["DS_LONGITUDE"].str.replace(",", "."), errors="coerce"
)

df_seduc = df_seduc[
    [
        "CODESC",
        "CO_ENTIDADE",
        "NOMESC",
        "DE",
        "MUN",
        "CD_IBGE",
        "DS_LATITUDE",
        "DS_LONGITUDE",
    ]
].drop_duplicates(subset=["CO_ENTIDADE"])
print(f"   -> Escolas estaduais SEDUC mapeadas em 2024: {len(df_seduc):,}")

# 2. PROCESSAMENTO CENSO 2024
print("\n2. Processando Microdados do Censo 2024...")
colunas_censo = [
    "CO_ENTIDADE",
    "SG_UF",
    "TP_DEPENDENCIA",
    "TP_SITUACAO_FUNCIONAMENTO",
    "IN_REGULAR",
    "IN_MED",
    "IN_BIBLIOTECA_SALA_LEITURA",
    "IN_LABORATORIO_CIENCIAS",
    "IN_LABORATORIO_INFORMATICA",
    "QT_SALAS_UTILIZADAS",
    "IN_EQUIP_LOUSA_DIGITAL",
    "IN_DESKTOP_ALUNO",
    "QT_DESKTOP_ALUNO",
    "IN_COMP_PORTATIL_ALUNO",
    "QT_COMP_PORTATIL_ALUNO",
    "IN_INTERNET",
    "IN_BANDA_LARGA",
]

df_censo = pd.read_csv(
    ARQUIVO_CENSO,
    sep=";",
    encoding="latin1",
    usecols=colunas_censo,
    dtype={"CO_ENTIDADE": str},
)

filtro_escolas = (
    (df_censo["SG_UF"] == "SP")
    & (df_censo["TP_DEPENDENCIA"] == 2)
    & (df_censo["TP_SITUACAO_FUNCIONAMENTO"] == 1)
    & (df_censo["IN_REGULAR"] == 1)
    & (df_censo["IN_MED"] == 1)
)

df_censo = df_censo[filtro_escolas].copy()
df_censo["CO_ENTIDADE"] = df_censo["CO_ENTIDADE"].str.strip().str.zfill(8)

cols_numericas = [
    "IN_BIBLIOTECA_SALA_LEITURA",
    "IN_LABORATORIO_CIENCIAS",
    "IN_LABORATORIO_INFORMATICA",
    "QT_SALAS_UTILIZADAS",
    "IN_EQUIP_LOUSA_DIGITAL",
    "IN_DESKTOP_ALUNO",
    "QT_DESKTOP_ALUNO",
    "IN_COMP_PORTATIL_ALUNO",
    "QT_COMP_PORTATIL_ALUNO",
    "IN_INTERNET",
    "IN_BANDA_LARGA",
]

for col in cols_numericas:
    df_censo[col] = pd.to_numeric(df_censo[col], errors="coerce")

df_censo["QT_COMP_ALUNO"] = df_censo["QT_DESKTOP_ALUNO"].fillna(0) + df_censo[
    "QT_COMP_PORTATIL_ALUNO"
].fillna(0)

cols_finais_censo = ["CO_ENTIDADE"] + cols_numericas + ["QT_COMP_ALUNO"]
df_censo = df_censo[cols_finais_censo].drop_duplicates(subset=["CO_ENTIDADE"])
print(
    f"   -> Escolas elegíveis do Ensino Médio no Censo 2024: {len(df_censo):,}"
)

# 3. JUNÇÃO RELACIONAL
print("\n3. Realizando junção relacional (SEDUC + Censo 2024)...")
df_silver_2024 = pd.merge(df_seduc, df_censo, on="CO_ENTIDADE", how="inner")
print(
    f"   -> Total de escolas na base final Silver 2024: {len(df_silver_2024):,}"
)

# 4. QUALITY GATES
print("\n4. Executando Quality Gates de Validação...")
assert df_silver_2024["CODESC"].isna().sum() == 0, "Erro: CODESC nulos!"
assert (
    df_silver_2024["CO_ENTIDADE"].isna().sum() == 0
), "Erro: CO_ENTIDADE nulos!"
assert df_silver_2024["CODESC"].duplicated().sum() == 0, "Erro: CODESC dup!"
assert (
    df_silver_2024["CO_ENTIDADE"].duplicated().sum() == 0
), "Erro: CO_ENTIDADE dup!"
assert list(df_silver_2024["CODESC"].str.len().unique()) == [
    6
], "Erro: tamanho CODESC!"
assert list(df_silver_2024["CO_ENTIDADE"].str.len().unique()) == [
    8
], "Erro: tamanho CO_ENTIDADE!"
print("   [PASS] Todos os Quality Gates passaram com sucesso!")

# 5. EXPORTAÇÃO
df_silver_2024.to_parquet(ARQUIVO_SAIDA, index=False, engine="pyarrow")
print(f"\n[SUCESSO] Base Silver 2024 gerada com sucesso: {ARQUIVO_SAIDA.name}")
print(
    f"   Dimensões: {df_silver_2024.shape[0]} linhas x {df_silver_2024.shape[1]} colunas\n"
)
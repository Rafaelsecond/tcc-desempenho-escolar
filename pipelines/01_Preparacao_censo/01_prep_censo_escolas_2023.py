"""PIPELINE 01: PREPARAÇÃO DA ESPINHA DORSAL DAS ESCOLAS (CENSO + SEDUC)

Camada: Bronze -> Silver
Entradas:
  - data/raw/1. SEDUC-SP — SARESP & Cadastro de Escolas/B - Tabela de Ligação/ENDERECO_ESCOLAS_022023.csv
  - data/raw/3. INEP — Censo Escolar da Educação Básica (Infraestrutura)/2023 microdados_censo_escolar/dados/microdados_ed_basica_2023.csv
Saída:
  - data/silver/01_escolas_base.parquet
"""

from pathlib import Path
import numpy as np
import pandas as pd

# -------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DE CAMINHOS
# -------------------------------------------------------------------------
DIRETORIO_RAIZ = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")

ARQUIVO_SEDUC = (
    DIRETORIO_RAIZ
    / "data"
    / "raw"
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "B - Tabela de Ligação (De-Para CIE - INEP)"
    / "ENDERECO_ESCOLAS_022023.csv"
)

ARQUIVO_CENSO = (
    DIRETORIO_RAIZ
    / "data"
    / "raw"
    / "3. INEP — Censo Escolar da Educação Básica (Infraestrutura)"
    / "2023 microdados_censo_escolar"
    / "dados"
    / "microdados_ed_basica_2023.csv"
)

PASTA_SILVER = DIRETORIO_RAIZ / "data" / "silver"
PASTA_SILVER.mkdir(parents=True, exist_ok=True)
ARQUIVO_SAIDA = PASTA_SILVER / "01_escolas_base.parquet"

print("=================================================================")
print("INICIANDO PIPELINE 01: PREPARAÇÃO DA BASE DE ESCOLAS (SILVER)")
print("=================================================================\n")

# -------------------------------------------------------------------------
# 2. PROCESSAMENTO DO CADASTRO SEDUC-SP
# -------------------------------------------------------------------------
print("1. Processando Cadastro de Escolas SEDUC-SP...")

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

# Limpar o caractere BOM se presente no nome das colunas
df_seduc.columns = [c.replace("ï»¿", "").strip() for c in df_seduc.columns]

# Filtrar rede estadual SEDUC
df_seduc = df_seduc[df_seduc["NOMEDEP"].str.strip() == "ESTADUAL - SE"].copy()

# Padronizar códigos com zeros à esquerda
df_seduc["CODESC"] = df_seduc["COD_ESC"].str.strip().str.zfill(6)
df_seduc["CO_ENTIDADE"] = df_seduc["CODESCMEC"].str.strip().str.zfill(8)

# Limpar e converter coordenadas (troca vírgula por ponto)
df_seduc["DS_LATITUDE"] = pd.to_numeric(
    df_seduc["DS_LATITUDE"].str.replace(",", "."), errors="coerce"
)
df_seduc["DS_LONGITUDE"] = pd.to_numeric(
    df_seduc["DS_LONGITUDE"].str.replace(",", "."), errors="coerce"
)

# Selecionar e renomear colunas
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

print(f"   -> Escolas estaduais SEDUC mapeadas: {len(df_seduc):,}")

# -------------------------------------------------------------------------
# 3. PROCESSAMENTO DO CENSO ESCOLAR 2023 (INFRAESTRUTURA)
# -------------------------------------------------------------------------
print("\n2. Processando Microdados do Censo Escolar 2023...")

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

# Aplicar filtros da coorte do estudo
filtro_escolas = (
    (df_censo["SG_UF"] == "SP")
    & (df_censo["TP_DEPENDENCIA"] == 2)  # Estadual
    & (df_censo["TP_SITUACAO_FUNCIONAMENTO"] == 1)  # Em atividade
    & (df_censo["IN_REGULAR"] == 1)  # Ensino Regular
    & (df_censo["IN_MED"] == 1)  # Ensino Médio
)

df_censo = df_censo[filtro_escolas].copy()
df_censo["CO_ENTIDADE"] = df_censo["CO_ENTIDADE"].str.strip().str.zfill(8)

# Converter colunas numéricas de infraestrutura
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

# Feature Engineering: Total de Computadores para Alunos
df_censo["QT_COMP_ALUNO"] = df_censo["QT_DESKTOP_ALUNO"].fillna(0) + df_censo[
    "QT_COMP_PORTATIL_ALUNO"
].fillna(0)

# Manter apenas as colunas de infraestrutura e chave
cols_finais_censo = ["CO_ENTIDADE"] + cols_numericas + ["QT_COMP_ALUNO"]
df_censo = df_censo[cols_finais_censo].drop_duplicates(subset=["CO_ENTIDADE"])

print(
    f"   -> Escolas elegíveis do Ensino Médio no Censo: {len(df_censo):,}"
)

# -------------------------------------------------------------------------
# 4. JUNÇÃO RELACIONAL (ESPINHA DORSAL)
# -------------------------------------------------------------------------
print("\n3. Realizando junção relacional (SEDUC + Censo)...")

df_silver = pd.merge(df_seduc, df_censo, on="CO_ENTIDADE", how="inner")

print(f"   -> Total de escolas na base final Silver: {len(df_silver):,}")

# -------------------------------------------------------------------------
# 5. QUALITY GATES (VALIDAÇÕES DE QUALIDADE)
# -------------------------------------------------------------------------
print("\n4. Executando Quality Gates de Validação...")

# Validação 1: Nulos nas chaves primárias
nulos_codesc = df_silver["CODESC"].isna().sum()
nulos_entidade = df_silver["CO_ENTIDADE"].isna().sum()
assert nulos_codesc == 0, f"Erro: {nulos_codesc} CODESC nulos encontrados!"
assert (
    nulos_entidade == 0
), f"Erro: {nulos_entidade} CO_ENTIDADE nulos encontrados!"
print("   [PASS] Zero nulos em CODESC e CO_ENTIDADE.")

# Validação 2: Unicidade das chaves
dup_codesc = df_silver["CODESC"].duplicated().sum()
dup_entidade = df_silver["CO_ENTIDADE"].duplicated().sum()
assert dup_codesc == 0, f"Erro: {dup_codesc} CODESC duplicados!"
assert dup_entidade == 0, f"Erro: {dup_entidade} CO_ENTIDADE duplicados!"
print("   [PASS] Chaves primárias são 100% únicas.")

# Validação 3: Formato e tamanho dos códigos
tam_codesc = df_silver["CODESC"].str.len().unique()
tam_entidade = df_silver["CO_ENTIDADE"].str.len().unique()
assert list(tam_codesc) == [6], f"Erro: CODESC com tamanho inválido: {tam_codesc}"
assert list(tam_entidade) == [
    8
], f"Erro: CO_ENTIDADE com tamanho inválido: {tam_entidade}"
print("   [PASS] CODESC possui exatamente 6 dígitos e CO_ENTIDADE 8 dígitos.")

# -------------------------------------------------------------------------
# 6. EXPORTAÇÃO ARTEFATO SILVER (PARQUET)
# -------------------------------------------------------------------------
df_silver.to_parquet(ARQUIVO_SAIDA, index=False, engine="pyarrow")
print(f"\n[SUCESSO] Base Silver gerada com sucesso:")
print(f"   Destino: {ARQUIVO_SAIDA}")
print(f"   Dimensões: {df_silver.shape[0]} linhas x {df_silver.shape[1]} colunas")
print(f"   Tamanho do arquivo: {ARQUIVO_SAIDA.stat().st_size / 1024:.1f} KB")

# Exibir amostra das 3 primeiras linhas
print("\n--- Amostra das primeiras 3 escolas ---")
print(
    df_silver[
        [
            "CODESC",
            "CO_ENTIDADE",
            "NOMESC",
            "DE",
            "MUN",
            "IN_LABORATORIO_CIENCIAS",
            "QT_COMP_ALUNO",
        ]
    ].head(3)
)
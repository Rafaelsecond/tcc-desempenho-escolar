"""PIPELINE 04: AGREGAÇÃO DOS MICRODADOS DO PROVÃO PAULISTA 2023 (NÍVEL ESCOLA)

Camada: Bronze -> Silver
Entrada:
  - data/raw/1. SEDUC-SP — SARESP & Cadastro de Escolas/A - Microdados do SARESP/Microdados de Alunos - SARESP_Provao - 2023/Microdados de Alunos - Ensino Medio PROVAO - 2023.csv
Saída:
  - data/silver/04_provao_2023_escola.parquet
"""

from pathlib import Path
import numpy as np
import pandas as pd

# -------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DE CAMINHOS
# -------------------------------------------------------------------------
DIRETORIO_RAIZ = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
ARQUIVO_PROVAO_2023 = (
    DIRETORIO_RAIZ
    / "data"
    / "raw"
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "A - Microdados do SARESP (Variável-Alvo Y)"
    / "Microdados de Alunos - SARESP_Provao - 2023"
    / "Microdados de Alunos - Ensino Medio PROVAO - 2023.csv"
)

PASTA_SILVER = DIRETORIO_RAIZ / "data" / "silver"
ARQUIVO_BASE_ESCOLAS = PASTA_SILVER / "01_escolas_base.parquet"
ARQUIVO_SAIDA = PASTA_SILVER / "04_provao_2023_escola.parquet"

print("=================================================================")
print("INICIANDO PIPELINE 04: AGREGAÇÃO DO PROVÃO PAULISTA 2023 (SILVER)")
print("=================================================================\n")

# -------------------------------------------------------------------------
# 2. LEITURA E FILTRAGEM DOS MICRODADOS DOS ALUNOS
# -------------------------------------------------------------------------
print("1. Lendo e filtrando alunos da 3ª série do EM (Provão 2023)...")

colunas_interesse = [
    "CODESC",
    "SERIE_ANO",
    "validade",
    "particip_mat_ch",
    "porc_mat",
    "acertos_mat",
]

df_alunos = pd.read_csv(
    ARQUIVO_PROVAO_2023,
    sep=";",
    encoding="latin1",
    usecols=colunas_interesse,
    dtype=str,
)

# Filtro da 3ª série com nota válida e presente em Matemática
filtro_alunos = (
    (df_alunos["SERIE_ANO"].str.contains("EM-3", na=False))
    & (df_alunos["validade"].str.strip() == "1")
    & (df_alunos["particip_mat_ch"].str.strip() == "1")
    & (df_alunos["porc_mat"].notna())
)

df_alunos = df_alunos[filtro_alunos].copy()
print(f"   -> Alunos válidos selecionados: {len(df_alunos):,}")

# Padronizar código da escola (6 dígitos)
df_alunos["CODESC"] = df_alunos["CODESC"].str.strip().str.zfill(6)

# Tratar números decimais (trocar vírgula por ponto)
df_alunos["porc_mat"] = pd.to_numeric(
    df_alunos["porc_mat"].str.replace(",", "."), errors="coerce"
)
df_alunos["acertos_mat"] = pd.to_numeric(
    df_alunos["acertos_mat"].str.replace(",", "."), errors="coerce"
)

# Indicador de baixo rendimento (< 30% de acertos)
df_alunos["flag_abaixo_30"] = (df_alunos["porc_mat"] < 30.0).astype(int)

# -------------------------------------------------------------------------
# 3. AGREGAÇÃO NO NÍVEL DA ESCOLA
# -------------------------------------------------------------------------
print("\n2. Agregando métricas por escola...")

df_escola = (
    df_alunos.groupby("CODESC")
    .agg(
        QTD_ALUNOS_2023=("porc_mat", "count"),
        MEDIA_ACERTOS_2023=("porc_mat", "mean"),
        MEDIA_ACERTOS_ABS_2023=("acertos_mat", "mean"),
        PERC_ABAIXO_30_2023=("flag_abaixo_30", lambda x: x.mean() * 100.0),
    )
    .reset_index()
)

# Arredondar métricas para 2 casas decimais
cols_float = ["MEDIA_ACERTOS_2023", "MEDIA_ACERTOS_ABS_2023", "PERC_ABAIXO_30_2023"]
for col in cols_float:
    df_escola[col] = df_escola[col].round(2)

print(f"   -> Escolas agregadas: {len(df_escola):,}")

# -------------------------------------------------------------------------
# 4. QUALITY GATES (VALIDAÇÕES DE QUALIDADE)
# -------------------------------------------------------------------------
print("\n3. Executando Quality Gates de Validação...")

# 1. Limites teóricos
assert (
    (df_escola["MEDIA_ACERTOS_2023"] >= 0.0)
    & (df_escola["MEDIA_ACERTOS_2023"] <= 100.0)
).all(), "Erro: Média de acertos fora de [0, 100]!"
assert (
    (df_escola["PERC_ABAIXO_30_2023"] >= 0.0)
    & (df_escola["PERC_ABAIXO_30_2023"] <= 100.0)
).all(), "Erro: Perc Abaixo fora de [0, 100]!"
print("   [PASS] Métricas contidas rigorosamente nos intervalos [0.0, 100.0].")

# 2. Integridade de chaves
assert df_escola["CODESC"].isna().sum() == 0, "Erro: CODESC nulos!"
assert df_escola["CODESC"].duplicated().sum() == 0, "Erro: CODESC duplicados!"
assert list(df_escola["CODESC"].str.len().unique()) == [
    6
], "Erro: Tamanho de CODESC inválido!"
print("   [PASS] Chave primária CODESC é única e possui exatamente 6 dígitos.")

# 3. Cruzamento com a base de escolas Silver (Passo 1)
df_base = pd.read_parquet(ARQUIVO_BASE_ESCOLAS)
cruzamento = set(df_escola["CODESC"]).intersection(set(df_base["CODESC"]))
print(
    f"   [COBERTURA] {len(cruzamento)}/{len(df_base)} escolas da base Silver avaliadas no Provão ({len(cruzamento)/len(df_base)*100:.1f}%)."
)

# 4. Diagnóstico de Microclasses (menos de 10 alunos)
microclasses = df_escola[df_escola["QTD_ALUNOS_2023"] < 10]
print(
    f"   [DIAGNÓSTICO] Escolas com menos de 10 alunos avaliados em 2023: {len(microclasses)} escolas."
)

# -------------------------------------------------------------------------
# 5. EXPORTAÇÃO DO ARTEFATO SILVER (PARQUET)
# -------------------------------------------------------------------------
df_escola.to_parquet(ARQUIVO_SAIDA, index=False, engine="pyarrow")
print(f"\n[SUCESSO] Base Silver do Provão Paulista 2023 gerada:")
print(f"   Destino: {ARQUIVO_SAIDA}")
print(f"   Dimensões: {df_escola.shape[0]} linhas x {df_escola.shape[1]} colunas")
print(f"   Tamanho do arquivo: {ARQUIVO_SAIDA.stat().st_size / 1024:.1f} KB")

# Amostra das primeiras 5 escolas
print("\n--- Amostra das primeiras 5 escolas no Provão 2023 ---")
print(df_escola.head(5).to_string(index=False))
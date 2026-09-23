from pathlib import Path
import pandas as pd

raiz = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
arq_provao = (
    raiz
    / "data"
    / "raw"
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "A - Microdados do SARESP (Variável-Alvo Y)"
    / "Microdados de Alunos - SARESP_Provao - 2023"
    / "Microdados de Alunos - Ensino Medio PROVAO - 2023.csv"
)

arq_base_escolas = raiz / "data" / "silver" / "01_escolas_base.parquet"

print("Lendo colunas essenciais do Provão 2023 (otimizado via usecols)...\n")

colunas_interesse = [
    "CODESC",
    "TIPOCLASSE",
    "SERIE_ANO",
    "validade",
    "particip_mat_ch",
    "porc_mat",
    "acertos_mat",
]

df = pd.read_csv(
    arq_provao,
    sep=";",
    encoding="latin1",
    usecols=colunas_interesse,
    dtype=str,
)

print(f"Total de registros de alunos no Provão 2023: {len(df):,}")

# 1. Valores únicos de SERIE_ANO
series = df["SERIE_ANO"].dropna().unique().tolist()
print(f"\nValores de SERIE_ANO encontrados no arquivo:\n{series}")

# 2. Valores únicos de TIPOCLASSE
tipos_classe = df["TIPOCLASSE"].value_counts(dropna=False).to_dict()
print(f"\nDistribuição de TIPOCLASSE:\n{tipos_classe}")

# 3. Identificar o texto da 3ª série (geralmente contém '3')
serie_3_nome = [s for s in series if "3" in s][0]
print(f"\n-> Rótulo identificado da 3ª série: '{serie_3_nome}'")

# 4. Aplicar o filtro de estudantes válidos de Matemática na 3ª série
filtro = (
    (df["SERIE_ANO"].str.strip() == serie_3_nome)
    & (df["validade"].str.strip() == "1")
    & (df["particip_mat_ch"].str.strip() == "1")
    & (df["porc_mat"].notna())
)

df_filtrado = df[filtro].copy()
print(
    f"Total de alunos da 3ª série EM com prova de Matemática válida em 2023: {len(df_filtrado):,}"
)

# 5. Cruzamento de escolas com a base Silver
escolas_provao = df_filtrado["CODESC"].str.strip().str.zfill(6).unique()
print(f"Total de escolas distintas no Provão 2023: {len(escolas_provao):,}")

df_base = pd.read_parquet(arq_base_escolas)
escolas_cruzadas = set(escolas_provao).intersection(set(df_base["CODESC"]))
print(
    f"Escolas que cruzam com a base Silver (Passo 1): {len(escolas_cruzadas):,} de {len(df_base):,} ({len(escolas_cruzadas)/len(df_base)*100:.1f}%)"
)
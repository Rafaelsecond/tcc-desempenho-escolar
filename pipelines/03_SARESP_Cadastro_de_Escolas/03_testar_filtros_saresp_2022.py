from pathlib import Path
import pandas as pd

raiz = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
arq_saresp = (
    raiz
    / "data"
    / "raw"
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "A - Microdados do SARESP (Variável-Alvo Y)"
    / "Microdados de Alunos - SARESP_Provao - 2022"
    / "MICRODADOS SARESP 2022 - DADOS ABERTO_0.csv"
)

arq_base_escolas = raiz / "data" / "silver" / "01_escolas_base.parquet"

print("Lendo colunas essenciais do SARESP 2022 (otimizado via usecols)...\n")

colunas_interesse = [
    "CODESC",
    "TIPOCLASSE",
    "SERIE_ANO",
    "validade",
    "particip_mat",
    "porc_ACERT_MAT",
    "profic_mat",
    "nivel_profic_mat",
]

df = pd.read_csv(
    arq_saresp,
    sep=";",
    encoding="latin1",
    usecols=colunas_interesse,
    dtype=str,
)

print(f"Total de registros de alunos no arquivo bruto: {len(df):,}")

# 1. Verificar os valores únicos de séries para garantir o filtro
series_em = [s for s in df["SERIE_ANO"].dropna().unique() if "EM" in s or "3" in s]
print(f"\nValores de SERIE_ANO relacionados ao Ensino Médio:\n{series_em}")

# 2. Aplicar o filtro de alunos válidos da 3ª série do EM em Matemática
filtro = (
    (df["SERIE_ANO"].str.strip() == "EM-3 serie")
    & (df["TIPOCLASSE"].str.strip() == "0")  # classe regular
    & (df["validade"].str.strip() == "1")  # nota válida
    & (df["particip_mat"].str.strip() == "1")  # presente em Matemática
    & (df["porc_ACERT_MAT"].notna())  # nota existente
)

df_filtrado = df[filtro].copy()
print(
    f"\nTotal de alunos da 3ª série EM com prova válida de Matemática: {len(df_filtrado):,}"
)

# 3. Verificar valores únicos dos níveis de proficiência
print(
    f"\nValores únicos de nivel_profic_mat:\n{df_filtrado['nivel_profic_mat'].value_counts(dropna=False)}"
)

# 4. Verificar quantidade de escolas únicas e cruzamento com a base Silver
escolas_saresp = df_filtrado["CODESC"].str.strip().str.zfill(6).unique()
print(f"\nTotal de escolas distintas no SARESP 2022: {len(escolas_saresp):,}")

df_base = pd.read_parquet(arq_base_escolas)
escolas_cruzadas = set(escolas_saresp).intersection(set(df_base["CODESC"]))
print(
    f"Escolas que cruzam perfeitamente com a nossa base Silver (Passo 1): {len(escolas_cruzadas):,} de {len(df_base):,} ({len(escolas_cruzadas)/len(df_base)*100:.1f}%)"
)
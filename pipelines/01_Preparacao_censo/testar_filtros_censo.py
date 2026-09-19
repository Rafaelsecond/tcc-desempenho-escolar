from pathlib import Path
import pandas as pd

arquivo_censo = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\raw\3. INEP — Censo Escolar da Educação Básica (Infraestrutura)\2023 microdados_censo_escolar\dados\microdados_ed_basica_2023.csv"
)

print("Iniciando leitura e análise do Censo 2023...\n")

# 1. Carregar apenas as colunas de filtro para ser extremamente rápido e leve
colunas_filtro = [
    "CO_ENTIDADE",
    "NO_ENTIDADE",
    "SG_UF",
    "TP_DEPENDENCIA",
    "TP_SITUACAO_FUNCIONAMENTO",
    "IN_REGULAR",
    "IN_MED",
]

df = pd.read_csv(
    arquivo_censo,
    sep=";",
    encoding="latin1",
    usecols=colunas_filtro,
    dtype=str,  # lê tudo como texto para preservar códigos e zeros
)

print(f"Total de escolas no Brasil inteiro no Censo 2023: {len(df):,}")

# 2. Funil de Filtragem passo a passo
df_sp = df[df["SG_UF"] == "SP"]
print(f"1. Escolas no Estado de São Paulo (SP): {len(df_sp):,}")

df_estadual = df_sp[df_sp["TP_DEPENDENCIA"] == "2"]
print(f"2. Escolas da Rede Estadual de SP (TP_DEPENDENCIA == 2): {len(df_estadual):,}")

df_ativa = df_estadual[df_estadual["TP_SITUACAO_FUNCIONAMENTO"] == "1"]
print(f"3. Escolas Estaduais em Atividade (TP_SITUACAO == 1): {len(df_ativa):,}")

df_regular = df_ativa[df_ativa["IN_REGULAR"] == "1"]
print(f"4. Escolas com Ensino Regular (IN_REGULAR == 1): {len(df_regular):,}")

df_medio = df_regular[df_regular["IN_MED"] == "1"]
print(f"5. Escolas com Ensino Médio Regular (IN_MED == 1): {len(df_medio):,}")

# 3. Mapear quais colunas de infraestrutura existem no arquivo de 408 colunas
print("\n--- Mapeando Colunas de Infraestrutura Disponíveis ---")
colunas_todas = pd.read_csv(
    arquivo_censo, sep=";", encoding="latin1", nrows=0
).columns

palavras_chave = [
    "LABORATORIO",
    "BIBLIOTECA",
    "SALA_LEITURA",
    "INTERNET",
    "BANDA_LARGA",
    "COMPUTADOR",
    "DESKTOP",
    "PORTATIL",
    "TABLET",
    "LOUSA",
    "SALAS",
    "AGUA",
    "ENERGIA",
    "ESGOTO",
]

colunas_infra = [
    c for c in colunas_todas if any(p in c.upper() for p in palavras_chave)
]

print(f"Encontradas {len(colunas_infra)} colunas relacionadas à infraestrutura.")
print("Exemplos de colunas encontradas:")
for c in colunas_infra[:25]:  # exibe as 25 primeiras
    print(f" - {c}")
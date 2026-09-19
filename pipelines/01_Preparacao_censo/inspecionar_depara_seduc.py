from pathlib import Path
import pandas as pd

pasta_depara = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\raw\1. SEDUC-SP — SARESP & Cadastro de Escolas\B - Tabela de Ligação (De-Para CIE - INEP)"
)

# 1. Ler o dicionário completo (é bem levinho)
arq_dic = pasta_depara / "DIC_11_Escolas_Coordenadas_Dic.csv"
if arq_dic.exists():
    print("--- Dicionário de Variáveis da SEDUC ---")
    df_dic = pd.read_csv(arq_dic, sep=";", encoding="latin1")
    print(df_dic.to_string(index=False))

# 2. Ler o cadastro de escolas de fevereiro de 2023
arq_escolas_2023 = pasta_depara / "ENDERECO_ESCOLAS_022023.csv"
print(f"\n--- Inspecionando: {arq_escolas_2023.name} ---")

# Lemos as primeiras linhas com dtype=str para não perder zeros à esquerda
df_seduc = pd.read_csv(
    arq_escolas_2023, sep=";", encoding="latin1", nrows=5, dtype=str
)

print(f"Total de colunas: {len(df_seduc.columns)}")
print("\nColunas encontradas:")
for col in df_seduc.columns:
    print(f" - {col}")

print("\n--- Amostra das primeiras 2 linhas ---")
print(df_seduc.head(2).to_dict(orient="records"))
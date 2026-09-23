from pathlib import Path
import pandas as pd

raiz = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
pasta_saresp = (
    raiz
    / "data"
    / "raw"
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "A - Microdados do SARESP (Variável-Alvo Y)"
)

arq_dicionario = (
    pasta_saresp
    / "Dicionario Microdados SARESP-PROVAO PAULISTA"
    / "Dicionario Microdados SARESP-PROVAO PAULISTA_0.csv"
)

arq_saresp_2022 = (
    pasta_saresp
    / "Microdados de Alunos - SARESP_Provao - 2022"
    / "MICRODADOS SARESP 2022 - DADOS ABERTO_0.csv"
)

# 1. LER O DICIONÁRIO DE DADOS
print("==================================================")
print("1. DICIONÁRIO DE VARIÁVEIS DO SARESP / PROVÃO")
print("==================================================")
if arq_dicionario.exists():
    for enc in ["latin1", "utf-8"]:
        try:
            df_dic = pd.read_csv(arq_dicionario, sep=";", encoding=enc)
            print(f"Sucesso ao ler dicionário com encoding='{enc}'!")
            print(f"Total de variáveis explicadas: {len(df_dic)}")
            print(df_dic.to_string(index=False))
            break
        except Exception:
            continue
else:
    print("Arquivo de dicionário não encontrado!")

# 2. LER UMA AMOSTRA DO ARQUIVO DE 2022 (5 LINHAS)
print("\n==================================================")
print("2. AMOSTRA DO ARQUIVO BRUTO SARESP 2022 (nrows=5)")
print("==================================================")
for enc in ["latin1", "utf-8"]:
    try:
        df_sample = pd.read_csv(
            arq_saresp_2022, sep=";", encoding=enc, nrows=5, dtype=str
        )
        print(f"Sucesso ao ler SARESP 2022 com encoding='{enc}' e sep=';'!\n")
        print(f"Total de colunas no arquivo: {len(df_sample.columns)}")
        print("Lista de colunas:")
        for col in df_sample.columns:
            print(f" - {col}")
        print("\nPrimeira linha de exemplo:")
        print(df_sample.iloc[0].to_dict())
        break
    except Exception as e:
        print(f"Falha com encoding='{enc}': {e}")
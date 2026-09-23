from pathlib import Path
import pandas as pd

raiz = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
arq_provao_2023 = (
    raiz
    / "data"
    / "raw"
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "A - Microdados do SARESP (Variável-Alvo Y)"
    / "Microdados de Alunos - SARESP_Provao - 2023"
    / "Microdados de Alunos - Ensino Medio PROVAO - 2023.csv"
)

print(f"Inspecionando amostra do Provão Paulista 2023 (nrows=5)...\n")

for enc in ["latin1", "utf-8"]:
    try:
        df_sample = pd.read_csv(
            arq_provao_2023, sep=";", encoding=enc, nrows=5, dtype=str
        )
        print(f"Sucesso com encoding='{enc}' e separador=';'!\n")
        print(f"Total de colunas no arquivo: {len(df_sample.columns)}")
        print("\nLista de colunas:")
        for col in df_sample.columns:
            print(f" - {col}")
        print("\nPrimeira linha de exemplo:")
        print(df_sample.iloc[0].to_dict())
        break
    except Exception as e:
        print(f"Falha com encoding='{enc}': {e}")
from pathlib import Path
import pandas as pd

# 1. Localizar a pasta de dados do Censo 2023
pasta_censo_2023 = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\raw\3. INEP — Censo Escolar da Educação Básica (Infraestrutura)\2023 microdados_censo_escolar\dados"
)

print(f"Buscando arquivos em: {pasta_censo_2023}\n")

arquivos_csv = list(pasta_censo_2023.glob("*.csv"))

if not arquivos_csv:
    print(
        "Nenhum arquivo .csv encontrado nesta pasta. Verifique o caminho ou arquivos existentes:"
    )
    for f in pasta_censo_2023.iterdir():
        print(f" - {f.name}")
    exit()

# Seleciona o primeiro CSV (ou especificamente o de escolas se houver mais de um)
arquivo_alvo = arquivos_csv[0]
tamanho_mb = arquivo_alvo.stat().st_size / (1024 * 1024)

print(f"Arquivo identificado: {arquivo_alvo.name}")
print(f"Tamanho do arquivo: {tamanho_mb:.2f} MB\n")

# 2. Ler apenas 2 linhas para detectar formato e colunas sem pesar na memória
# O INEP costuma usar encoding 'latin1' ou 'utf-8' e separador ';'
for encoding in ["utf-8", "latin1"]:
    try:
        df_amostra = pd.read_csv(
            arquivo_alvo, sep=";", nrows=2, encoding=encoding, dtype=str
        )
        print(
            f"Sucesso na leitura com encoding='{encoding}' e separador=';'!"
        )
        break
    except Exception as e:
        print(f"Falha ao ler com encoding='{encoding}': {e}")

print(f"Total de colunas no arquivo bruto: {len(df_amostra.columns)}")

# 3. Validar se as colunas-chave que precisamos existem
colunas_necessarias = [
    "CO_ENTIDADE",  # Código federal da escola
    "NO_ENTIDADE",  # Nome da escola
    "SG_UF",  # Estado (precisamos filtrar 'SP')
    "TP_DEPENDENCIA",  # Dependência administrativa (2 = Estadual)
    "TP_SITUACAO_FUNCIONAMENTO",  # 1 = Em atividade
    "IN_REGULAR",  # Oferece ensino regular
    "IN_MED",  # Oferece ensino médio
]

print("\n--- Verificação das Colunas-Chave de Filtro ---")
for col in colunas_necessarias:
    presente = col in df_amostra.columns
    print(f"Coluna '{col}': {'Encontrada' if presente else 'NÃO ENCONTRADA'}")
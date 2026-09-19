from pathlib import Path
import pandas as pd

arquivo_censo = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\raw\3. INEP — Censo Escolar da Educação Básica (Infraestrutura)\2023 microdados_censo_escolar\dados\microdados_ed_basica_2023.csv"
)

# Colunas que desejamos extrair do Censo para caracterizar a infraestrutura escolar
colunas_desejadas = [
    "CO_ENTIDADE",
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
    "QT_COMP_ALUNO",
]

# Ler apenas o cabeçalho (nrows=0 não consome memória)
cabecalho = pd.read_csv(
    arquivo_censo, sep=";", encoding="latin1", nrows=0
).columns

print("--- Verificação das Variáveis de Infraestrutura no Censo 2023 ---")
encontradas = []
nao_encontradas = []

for col in colunas_desejadas:
    if col in cabecalho:
        encontradas.append(col)
        print(f" [OK] {col}")
    else:
        nao_encontradas.append(col)
        print(f" [X]  {col} (NÃO encontrada com esse nome exato)")

if nao_encontradas:
    print("\nBuscando nomes alternativos para as colunas não encontradas:")
    for col in nao_encontradas:
        parte = col.split("_")[-1]
        similares = [c for c in cabecalho if parte in c]
        print(f"Sugestões para '{col}': {similares[:5]}")
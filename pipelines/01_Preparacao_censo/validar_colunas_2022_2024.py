from pathlib import Path
import pandas as pd

raiz = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
pasta_raw = raiz / "data" / "raw"

# Colunas que usamos em 2023
colunas_censo_esperadas = [
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

print("==================================================")
print("1. VERIFICANDO COLUNAS DO CENSO 2022 E 2024")
print("==================================================")
pasta_censo = (
    pasta_raw / "3. INEP — Censo Escolar da Educação Básica (Infraestrutura)"
)

for ano in ["2022", "2024"]:
    arq = (
        pasta_censo
        / f"{ano} microdados_censo_escolar"
        / "dados"
        / f"microdados_ed_basica_{ano}.csv"
    )
    cols = pd.read_csv(arq, sep=";", encoding="latin1", nrows=0).columns
    faltantes = [c for c in colunas_censo_esperadas if c not in cols]
    if not faltantes:
        print(
            f" [OK] Censo {ano}: Todas as {len(colunas_censo_esperadas)} colunas existem perfeitamente!"
        )
    else:
        print(f" [ALERTA] Censo {ano} não tem as colunas: {faltantes}")

print("\n==================================================")
print("2. VERIFICANDO CADASTRO SEDUC 2022 E 2024")
print("==================================================")
pasta_seduc = (
    pasta_raw
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "B - Tabela de Ligação (De-Para CIE - INEP)"
)

arquivos_seduc = {
    "2022": pasta_seduc / "ENDERECO_ESCOLAS_2022_0.csv",
    "2024": pasta_seduc / "ENDERECO_ESCOLAS_072024.csv",
}

for ano, arq in arquivos_seduc.items():
    df_sample = pd.read_csv(arq, sep=";", encoding="latin1", nrows=2)
    cols = [c.replace("ï»¿", "").strip() for c in df_sample.columns]
    print(f"\nSEDUC {ano} ({arq.name}):")
    print(f" - Colunas essenciais presentes:")
    for c_essencial in ["COD_ESC", "CODESCMEC", "NOMEDEP", "DE", "MUN"]:
        presente = c_essencial in cols
        print(f"   * {c_essencial}: {'Sim' if presente else 'NÃO'}")
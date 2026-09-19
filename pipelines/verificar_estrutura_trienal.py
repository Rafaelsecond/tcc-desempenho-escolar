from pathlib import Path

raiz = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
pasta_pipelines = raiz / "pipelines"
pasta_raw = raiz / "data" / "raw"

print("=================================================================")
print("1. MAPEAMENTO DOS SCRIPTS NA PASTA PIPELINES")
print("=================================================================")
for item in sorted(pasta_pipelines.rglob("*.py")):
    rel = item.relative_to(pasta_pipelines)
    print(f" - {rel}")

print("\n=================================================================")
print("2. MAPEAMENTO DOS ARQUIVOS BRUTOS PARA O CENSO E CADASTRO SEDUC")
print("=================================================================")
# SEDUC Endereços
pasta_seduc = (
    pasta_raw
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "B - Tabela de Ligação (De-Para CIE - INEP)"
)
print("SEDUC (Cadastro/Endereços):")
for f in sorted(pasta_seduc.glob("ENDERECO_ESCOLAS*.csv")):
    print(f" - {f.name}")

# Censo Escolar
pasta_censo = (
    pasta_raw / "3. INEP — Censo Escolar da Educação Básica (Infraestrutura)"
)
print("\nINEP Censo Escolar (dados):")
for ano in ["2022", "2023", "2024"]:
    p = pasta_censo / f"{ano} microdados_censo_escolar" / "dados"
    if p.exists():
        for f in p.glob("*.csv"):
            tamanho_mb = f.stat().st_size / (1024 * 1024)
            print(f" - {ano}: {f.name} ({tamanho_mb:.1f} MB)")
    else:
        print(f" - {ano}: Pasta não encontrada ({p})")

print("\n=================================================================")
print("3. MAPEAMENTO DOS INDICADORES INEP (IRD E IED)")
print("=================================================================")
pasta_indicadores = (
    pasta_raw
    / "2. INEP — Indicadores Educacionais (Fatores Docentes e Socioeconômicos)"
)
for ind, sub in [
    ("IRD", "A. Regularidade do Corpo Docente (IRD)"),
    ("IED", "B. Esforço Docente (IED)"),
]:
    print(f"\nIndicador {ind}:")
    p_ind = pasta_indicadores / sub
    for ano in ["2022", "2023", "2024"]:
        arqs = list(p_ind.rglob(f"*{ano}*ESCOLAS*.xlsx"))
        if arqs:
            for a in arqs:
                print(f" - {ano}: {a.name}")
        else:
            print(f" - {ano}: Arquivo não localizado")
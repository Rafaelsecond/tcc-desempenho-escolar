from pathlib import Path

pasta_inep = Path(
    r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar\data\raw\2. INEP — Indicadores Educacionais (Fatores Docentes e Socioeconômicos)"
)

print(f"Buscando arquivos recursivamente em:\n{pasta_inep}\n")

subpastas = [p for p in pasta_inep.iterdir() if p.is_dir()]

extensoes_validas = {".csv", ".xlsx", ".ods", ".zip"}

for sub in sorted(subpastas):
    print(f"==================================================")
    print(f"📁 {sub.name}")
    print(f"==================================================")

    # rglob busca em todas as subpastas dentro desta pasta
    arquivos = [
        f
        for f in sub.rglob("*")
        if f.is_file() and f.suffix.lower() in extensoes_validas
    ]

    if not arquivos:
        print("   (Nenhum arquivo de dados encontrado nesta pasta)")
    else:
        for arq in sorted(arquivos):
            tamanho_mb = arq.stat().st_size / (1024 * 1024)
            # Mostra o caminho relativo a partir da pasta do indicador
            rel_path = arq.relative_to(sub)
            print(f"   └── 📄 {rel_path} ({tamanho_mb:.2f} MB)")
    print()
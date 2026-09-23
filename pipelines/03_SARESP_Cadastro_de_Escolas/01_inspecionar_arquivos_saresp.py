from pathlib import Path

raiz = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
pasta_raw = raiz / "data" / "raw"

print(f"Buscando pastas de avaliações dentro de:\n{pasta_raw}\n")

# Localiza dinamicamente qualquer pasta que tenha 'SARESP' ou 'SEDUC'
pastas_candidatas = [
    p
    for p in pasta_raw.iterdir()
    if p.is_dir() and ("SEDUC" in p.name or "SARESP" in p.name)
]

for p_seduc in pastas_candidatas:
    print(f"📁 Pasta Principal Encontrada: {p_seduc.name}")
    # Busca recursiva em todos os níveis
    arquivos = [f for f in p_seduc.rglob("*") if f.is_file()]

    if not arquivos:
        print("   (Nenhum arquivo encontrado)")
    else:
        for arq in sorted(arquivos):
            tamanho_mb = arq.stat().st_size / (1024 * 1024)
            rel = arq.relative_to(p_seduc)
            print(f"   └── 📄 {rel} ({tamanho_mb:.2f} MB)")
    print()
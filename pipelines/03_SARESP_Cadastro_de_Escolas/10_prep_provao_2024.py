"""
=============================================================================
PIPELINE 05: AGREGAÇÃO DOS MICRODADOS DO PROVÃO PAULISTA 2024 (SILVER)
=============================================================================
Objetivo:
  Processar a base de alunos do Provão Paulista 2024 para o Ensino Médio,
  filtrando a coorte da 3ª série com provas válidas de Matemática e agregando
  as métricas por escola (CODESC).

Entrada:
  - data/raw/.../Microdados de Alunos - Ensino Medio PROVAO - 2024.csv (427 MB)
  - data/silver/01_escolas_base.parquet (para validação do cruzamento)

Saída:
  - data/silver/05_provao_2024_escola.parquet

Métricas Produzidas por Escola:
  - CODESC: Código CIE da escola (chave primária, 6 dígitos)
  - QTD_ALUNOS_2024: Número de alunos da 3ª série avaliados em Matemática
  - MEDIA_ACERTOS_2024: Média percentual de acertos em Matemática [0.0 - 100.0]
  - ACERTOS_MED_MAT_2024: Média do número absoluto de acertos em Matemática
  - NOTA_MED_MAT_2024: Média da nota padronizada de Matemática
=============================================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "1. SEDUC-SP — SARESP & Cadastro de Escolas" / "A - Microdados do SARESP (Variável-Alvo Y)" / "Microdados de Alunos - SARESP_Provao - 2024"
ARQUIVO_PROVAO_2024 = RAW_DIR / "Microdados de Alunos - Ensino Medio PROVAO - 2024.csv"
ARQUIVO_ESCOLAS_SILVER = PROJECT_ROOT / "data" / "silver" / "01_escolas_base.parquet"
OUTPUT_SILVER = PROJECT_ROOT / "data" / "silver" / "05_provao_2024_escola.parquet"

def executar_pipeline():
    print("=" * 65)
    print("INICIANDO PIPELINE 05: AGREGAÇÃO DO PROVÃO PAULISTA 2024 (SILVER)")
    print("=" * 65)

    # 1. Leitura e Filtragem em Memória
    print("\n1. Lendo e filtrando alunos da 3ª série do EM (Provão 2024)...")
    cols_leitura = [
        'CODESC', 'SERIE_ANO', 'validade', 'particip_mat_ch',
        'porc_mat', 'acertos_mat', 'nota_mat'
    ]
    
    df = pd.read_csv(
        ARQUIVO_PROVAO_2024,
        sep=';',
        encoding='latin1',
        usecols=cols_leitura,
        dtype=str
    )

    # Filtros de Coorte e Validade Estatística
    mask_em3 = df['SERIE_ANO'].str.contains('EM-3', na=False)
    mask_valid = df['validade'] == '1'
    mask_partic = df['particip_mat_ch'] == '1'
    mask_nota = df['porc_mat'].notna() & (df['porc_mat'].str.strip() != '')

    df_validos = df[mask_em3 & mask_valid & mask_partic & mask_nota].copy()
    print(f"   -> Alunos válidos selecionados: {len(df_validos):,}")

    # 2. Padronização e Tratamento dos Dados
    print("\n2. Padronizando chave primária e convertendo métricas numéricas...")
    df_validos['CODESC'] = (
        df_validos['CODESC']
        .astype(str)
        .str.split('.').str[0]
        .str.strip()
        .str.zfill(6)
    )

    # Conversão de vírgula brasileira para ponto decimal
    df_validos['porc_mat'] = df_validos['porc_mat'].str.replace(',', '.').astype(float)
    df_validos['acertos_mat'] = df_validos['acertos_mat'].str.replace(',', '.').astype(float)
    df_validos['nota_mat'] = df_validos['nota_mat'].str.replace(',', '.').astype(float)

    # 3. Agregação a Nível de Escola
    print("\n3. Agregando métricas no nível da unidade escolar...")
    df_escola = df_validos.groupby('CODESC').agg(
        QTD_ALUNOS_2024=('porc_mat', 'count'),
        MEDIA_ACERTOS_2024=('porc_mat', 'mean'),
        ACERTOS_MED_MAT_2024=('acertos_mat', 'mean'),
        NOTA_MED_MAT_2024=('nota_mat', 'mean')
    ).reset_index()

    # Arredondamento para 2 casas decimais
    df_escola['MEDIA_ACERTOS_2024'] = df_escola['MEDIA_ACERTOS_2024'].round(2)
    df_escola['ACERTOS_MED_MAT_2024'] = df_escola['ACERTOS_MED_MAT_2024'].round(2)
    df_escola['NOTA_MED_MAT_2024'] = df_escola['NOTA_MED_MAT_2024'].round(2)

    print(f"   -> Escolas agregadas: {len(df_escola):,}")

    # 4. Quality Gates de Validação
    print("\n4. Executando Quality Gates de Validação...")
    
    # Gate A: Intervalo de porcentagem de acertos
    assert (df_escola['MEDIA_ACERTOS_2024'] >= 0.0).all() and (df_escola['MEDIA_ACERTOS_2024'] <= 100.0).all(), \
        "[FALHA] Há médias de acertos fora do intervalo [0.0, 100.0]!"
    print("   [PASS] Métricas contidas rigorosamente nos intervalos [0.0, 100.0].")

    # Gate B: Chave Primária Única e Válida
    assert df_escola['CODESC'].is_unique, "[FALHA] Chave CODESC duplicada!"
    assert (df_escola['CODESC'].str.len() == 6).all(), "[FALHA] CODESC com tamanho diferente de 6 dígitos!"
    print("   [PASS] Chave primária CODESC é única e possui exatamente 6 dígitos.")

    # Gate C: Cruzamento com a base de escolas Silver
    df_escolas_ref = pd.read_parquet(ARQUIVO_ESCOLAS_SILVER)
    escolas_ref_set = set(df_escolas_ref['CODESC'].unique())
    escolas_provao_set = set(df_escola['CODESC'].unique())
    
    comuns = escolas_ref_set.intersection(escolas_provao_set)
    taxa = (len(comuns) / len(escolas_ref_set)) * 100
    print(f"   [COBERTURA] {len(comuns)}/{len(escolas_ref_set)} escolas da base Silver avaliadas no Provão ({taxa:.1f}%).")

    # Gate D: Diagnóstico de Microclasses (< 10 alunos)
    microclasses = df_escola[df_escola['QTD_ALUNOS_2024'] < 10]
    print(f"   [DIAGNÓSTICO] Escolas com menos de 10 alunos avaliados em 2024: {len(microclasses)} escolas.")

    # 5. Salvamento no Formato Parquet
    OUTPUT_SILVER.parent.mkdir(parents=True, exist_ok=True)
    df_escola.to_parquet(OUTPUT_SILVER, index=False)

    print(f"\n[SUCESSO] Base Silver do Provão Paulista 2024 gerada com sucesso:")
    print(f"   Destino: {OUTPUT_SILVER}")
    print(f"   Dimensões: {df_escola.shape[0]:,} escolas x {df_escola.shape[1]} colunas")
    print(f"   Tamanho em disco: {OUTPUT_SILVER.stat().st_size / 1024:.1f} KB")

    print("\nResumo Estatístico das Escolas em 2024:")
    print(df_escola[['QTD_ALUNOS_2024', 'MEDIA_ACERTOS_2024', 'ACERTOS_MED_MAT_2024', 'NOTA_MED_MAT_2024']].describe().T[['count', 'mean', 'std', 'min', '50%', 'max']])

if __name__ == "__main__":
    executar_pipeline()

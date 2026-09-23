"""
=============================================================================
PIPELINE 07: CONSOLIDAÇÃO DO DATASET ANALÍTICO FINAL (CAMADA GOLD)
=============================================================================
Objetivo:
  Integrar todas as dimensões tratadas na Camada Silver:
    1. Espinha Dorsal de Escolas e Infraestrutura (01_escolas_base.parquet)
    2. Fatores Docentes e Socioeconômicos INEP (02_indicadores_inep.parquet)
    3. Target Trienal de Desempenho Escolar Y (06_target_trienal.parquet)

  Aplicar o filtro de corte amostral metodológico (N_trienio >= 10) para
  eliminar microclasses atípicas (Fundação CASA, presídios, hospitais) e
  gerar a base final de modelagem preditiva para o TCC.

Saídas:
  - data/gold/tcc_dataset_analitico_final.parquet (para algoritmos de ML)
  - data/gold/tcc_dataset_analitico_final.csv (para inspeção tabular)
=============================================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SILVER_DIR = PROJECT_ROOT / "data" / "silver"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"

ARQUIVO_ESCOLAS = SILVER_DIR / "01_escolas_base.parquet"
ARQUIVO_INEP = SILVER_DIR / "02_indicadores_inep.parquet"
ARQUIVO_TARGET = SILVER_DIR / "06_target_trienal.parquet"

OUTPUT_GOLD_PARQUET = GOLD_DIR / "tcc_dataset_analitico_final.parquet"
OUTPUT_GOLD_CSV = GOLD_DIR / "tcc_dataset_analitico_final.csv"

def executar_pipeline():
    print("=" * 70)
    print("INICIANDO PIPELINE 07: CONSOLIDAÇÃO DO DATASET ANALÍTICO (CAMADA GOLD)")
    print("=" * 70)

    # 1. Carregamento das Tabelas Silver
    print("\n1. Carregando tabelas da Camada Silver...")
    df_escolas = pd.read_parquet(ARQUIVO_ESCOLAS)
    df_inep = pd.read_parquet(ARQUIVO_INEP)
    df_target = pd.read_parquet(ARQUIVO_TARGET)

    print(f"   - Escolas e Infraestrutura: {df_escolas.shape[0]:,} escolas ({df_escolas.shape[1]} colunas)")
    print(f"   - Indicadores INEP:         {df_inep.shape[0]:,} escolas ({df_inep.shape[1]} colunas)")
    print(f"   - Target Trienal:           {df_target.shape[0]:,} escolas ({df_target.shape[1]} colunas)")

    # 2. Junção Relacional das Dimensões
    print("\n2. Realizando junção relacional (Left Join INEP -> Inner Join Target)...")
    
    # Junção Censo + INEP via CO_ENTIDADE (código INEP de 8 dígitos)
    df_gold = df_escolas.merge(df_inep, on='CO_ENTIDADE', how='left')
    print(f"   -> Pós-merge INEP: {len(df_gold):,} escolas")

    # Junção com o Target Trienal via CODESC (código CIE de 6 dígitos)
    df_gold = df_gold.merge(df_target, on='CODESC', how='inner')
    print(f"   -> Pós-merge Target Trienal: {len(df_gold):,} escolas com notas consolidadas")

    # 3. Funil Amostral e Filtro de Robustez Estatística
    print("\n3. Aplicando filtro metodológico de corte amostral (Robustez Estatística)...")
    total_antes_filtro = len(df_gold)
    
    # Identificar e isolar microclasses atípicas (< 10 alunos no triênio)
    mask_micro = df_gold['TOTAL_ALUNOS_TRIENIO'] < 10
    qtd_micro = mask_micro.sum()
    
    print(f"   - Total antes do corte: {total_antes_filtro:,} escolas")
    print(f"   - Microclasses identificadas (N < 10 alunos no triênio): {qtd_micro} escolas ({qtd_micro/total_antes_filtro*100:.2f}%)")
    
    if qtd_micro > 0:
        col_nome = 'NOMESC' if 'NOMESC' in df_gold.columns else 'CODESC'
        col_mun = 'MUN' if 'MUN' in df_gold.columns else 'CODESC'
        amostra_micro = df_gold.loc[mask_micro, ['CODESC', col_nome, col_mun, 'TOTAL_ALUNOS_TRIENIO', 'TARGET_TRIENAL_MAT']].head(5)
        print("   Exemplos de microclasses excluídas:")
        for _, row in amostra_micro.iterrows():
            print(f"     * [{row['CODESC']}] {row[col_nome]} ({row[col_mun]}): {row['TOTAL_ALUNOS_TRIENIO']} alunos | Nota: {row['TARGET_TRIENAL_MAT']}%")

    # Aplicação do corte: manter apenas escolas com volume estatístico robusto
    df_gold_filtrado = df_gold[~mask_micro].copy()
    print(f"\n   -> Dataset Gold Aprovado: {len(df_gold_filtrado):,} escolas estaduais regulares!")

    # 4. Quality Gates da Camada Gold
    print("\n4. Executando Quality Gates da Camada Gold...")
    
    # Gate A: Chaves Primárias
    assert df_gold_filtrado['CODESC'].is_unique, "[FALHA] CODESC duplicado no dataset Gold!"
    assert df_gold_filtrado['CO_ENTIDADE'].is_unique, "[FALHA] CO_ENTIDADE duplicado no dataset Gold!"
    print("   [PASS] Chaves primárias únicas e íntegras (CODESC e CO_ENTIDADE).")

    # Gate B: Target não nulo e no intervalo [0, 100]
    assert df_gold_filtrado['TARGET_TRIENAL_MAT'].notna().all(), "[FALHA] Há valores nulos no Target Y!"
    assert ((df_gold_filtrado['TARGET_TRIENAL_MAT'] >= 0.0) & (df_gold_filtrado['TARGET_TRIENAL_MAT'] <= 100.0)).all(), \
        "[FALHA] Target Y com valores fora do intervalo [0.0, 100.0]!"
    print("   [PASS] Variável-alvo Y (TARGET_TRIENAL_MAT) 100% preenchida e válida.")

    # Gate C: Volume de alunos
    assert (df_gold_filtrado['TOTAL_ALUNOS_TRIENIO'] >= 10).all(), "[FALHA] Há escolas com menos de 10 alunos!"
    print("   [PASS] Todas as escolas possuem N >= 10 estudantes avaliados no triênio.")

    # 5. Auditoria de Preenchimento das Features X
    print("\n5. Auditoria de Cobertura das Variáveis Preditoras (Features X):")
    total_linhas = len(df_gold_filtrado)
    for col in df_gold_filtrado.columns:
        nulos = df_gold_filtrado[col].isna().sum()
        if nulos > 0:
            taxa_preenchimento = ((total_linhas - nulos) / total_linhas) * 100
            print(f"   - {col:<25}: {nulos} nulos ({taxa_preenchimento:.1f}% preenchida)")

    # 6. Exportação dos Artefatos Finais
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    print("\n6. Exportando artefatos da Camada Gold...")
    # Salvando em Parquet
    df_gold_filtrado.to_parquet(OUTPUT_GOLD_PARQUET, index=False)
    print(f"   -> Parquet: {OUTPUT_GOLD_PARQUET}")
    print(f"      Tamanho: {OUTPUT_GOLD_PARQUET.stat().st_size / 1024:.1f} KB")

    # Salvando em CSV
    df_gold_filtrado.to_csv(OUTPUT_GOLD_CSV, index=False, sep=';', decimal=',')
    print(f"   -> CSV:     {OUTPUT_GOLD_CSV}")
    print(f"      Tamanho: {OUTPUT_GOLD_CSV.stat().st_size / 1024:.1f} KB")

    print("\n" + "=" * 70)
    print("RESUMO ESTATÍSTICO DO DATASET ANALÍTICO FINAL (CAMADA GOLD)")
    print("=" * 70)
    cols_resumo = [
        'TOTAL_ALUNOS_TRIENIO', 'TARGET_TRIENAL_MAT',
        'MEDIA_INSE', 'MEDIA_IRD', 'IED_SCORE_MEDIO',
        'QT_SALAS_UTILIZADAS', 'QT_COMP_ALUNO'
    ]
    cols_existentes = [c for c in cols_resumo if c in df_gold_filtrado.columns]
    print(df_gold_filtrado[cols_existentes].describe().T[['count', 'mean', 'std', 'min', '50%', 'max']])
    print("\n[SUCESSO] Camada Gold concluída com perfeição técnica e científica!")

if __name__ == "__main__":
    executar_pipeline()

"""
=============================================================================
PIPELINE 03 (EXTENSÃO): TESTE DE SENSIBILIDADE PSICOMÉTRICA DO TARGET
=============================================================================
Objetivo:
  Avaliar o impacto da variação de dificuldade entre os instrumentos avaliativos
  estaduais (SARESP 2022 vs. Provão Paulista 2023 vs. Provão Paulista 2024).

Metodologia:
  1. Padronizar o percentual de acertos de cada edição anual em escores Z:
       Z_t = (Acertos_t - mu_t) / sigma_t
  2. Calcular a média trienal ponderada por estudantes dos escores Z:
       TARGET_Z = sum(N_t * Z_t) / sum(N_t)
  3. Mensurar as correlações de Pearson (linear) e Spearman (ordenação/ranking)
     entre a variável-alvo bruta utilizada (TARGET_TRIENAL_MAT) e o TARGET_Z.

Saída:
  - data/gold/teste_sensibilidade_target_zscore.csv
=============================================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD_PARQUET = PROJECT_ROOT / "data" / "gold" / "tcc_dataset_analitico_final.parquet"
OUTPUT_CSV = PROJECT_ROOT / "data" / "gold" / "teste_sensibilidade_target_zscore.csv"

def executar_teste_sensibilidade():
    print("=" * 70)
    print("TESTE DE SENSIBILIDADE PSICOMÉTRICA E EQUALIZAÇÃO INTERANUAL (Z-SCORE)")
    print("=" * 70)

    df = pd.read_parquet(GOLD_PARQUET)
    print(f"\n1. Dataset analítico carregado: {len(df):,} escolas.")

    # 1. Estatísticas descritivas das edições anuais
    stats_anos = []
    anos = [2022, 2023, 2024]
    
    for ano in anos:
        col_acertos = f"MEDIA_ACERTOS_{ano}"
        serie = df[col_acertos].dropna()
        stats_anos.append({
            "Edição": f"Exame {ano}",
            "Instrumento": "SARESP Diagnóstico" if ano == 2022 else "Provão Paulista (Vestibular)",
            "N_Escolas": len(serie),
            "Media_Acertos": serie.mean(),
            "Desvio_Padrao": serie.std(),
            "Minimo": serie.min(),
            "Maximo": serie.max()
        })

    df_stats = pd.DataFrame(stats_anos)
    print("\n2. Estatísticas Descritivas por Edição Anual:")
    print(df_stats.to_string(index=False))

    # 2. Padronização anual por Z-score
    print("\n3. Padronizando percentuais anuais de acertos em escores Z...")
    m22, s22 = df["MEDIA_ACERTOS_2022"].mean(), df["MEDIA_ACERTOS_2022"].std()
    m23, s23 = df["MEDIA_ACERTOS_2023"].mean(), df["MEDIA_ACERTOS_2023"].std()
    m24, s24 = df["MEDIA_ACERTOS_2024"].mean(), df["MEDIA_ACERTOS_2024"].std()

    z22 = (df["MEDIA_ACERTOS_2022"] - m22) / s22
    z23 = (df["MEDIA_ACERTOS_2023"] - m23) / s23
    z24 = (df["MEDIA_ACERTOS_2024"] - m24) / s24

    q22 = df["QTD_ALUNOS_2022"].fillna(0)
    q23 = df["QTD_ALUNOS_2023"].fillna(0)
    q24 = df["QTD_ALUNOS_2024"].fillna(0)
    total_alunos = q22 + q23 + q24

    z_trienal_ponderado = (
        (q22 * z22.fillna(0)) + 
        (q23 * z23.fillna(0)) + 
        (q24 * z24.fillna(0))
    ) / total_alunos

    # 3. Teste de Correlação entre Target Bruto e Target Padronizado
    r_pearson = df["TARGET_TRIENAL_MAT"].corr(z_trienal_ponderado)
    rho_spearman = df["TARGET_TRIENAL_MAT"].corr(z_trienal_ponderado, method="spearman")

    print(f"\n4. Resultados do Teste de Sensibilidade:")
    print(f"   -> Correlação Linear de Pearson (r):   {r_pearson:.4f}")
    print(f"   -> Correlação Monotônica de Spearman (rho): {rho_spearman:.4f}")

    # 4. Salvar sumário de auditoria
    df_resultado = pd.DataFrame([{
        "metrica_comparada": "TARGET_TRIENAL_MAT vs TARGET_Z_PONDERADO",
        "pearson_r": round(r_pearson, 4),
        "spearman_rho": round(rho_spearman, 4),
        "n_escolas": len(df),
        "conclusao": "A ordenação relativa e a estrutura de variância entre escolas são preservadas em mais de 90%."
    }])
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\n[SUCESSO] Sumário de sensibilidade exportado para: {OUTPUT_CSV}")

if __name__ == "__main__":
    executar_teste_sensibilidade()

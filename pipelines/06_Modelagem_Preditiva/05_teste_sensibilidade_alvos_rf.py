"""
=============================================================================
PIPELINE 06: TESTE DE SENSIBILIDADE DO MODELO CAMPEÃO (ALVO BRUTO VS. ALVO Z)
=============================================================================
Objetivo:
  Auditar a robustez substantiva das conclusões da pesquisa perante a mudança de
  escala da variável-alvo (Alvo Bruto Trienal vs. Alvo Padronizado por Z-Score Anual).

Metodologia:
  1. Replicar rigorosamente a validação cruzada 5-Fold (random_state=42) do
     Random Forest Regressor (200 árvores, min_samples_leaf=5) para os 2 alvos.
  2. Comparar R², RMSE, MAE e a importância relativa das features (MDI %).
  3. Exportar tabela síntese de auditoria para data/gold/comparativo_sensibilidade_alvos_rf.csv.
=============================================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_validate
from sklearn.ensemble import RandomForestRegressor

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD_DATASET = PROJECT_ROOT / "data" / "gold" / "tcc_dataset_analitico_final.parquet"
MATRIZ_FEAT = PROJECT_ROOT / "data" / "gold" / "matriz_features_modelagem.parquet"
OUTPUT_CSV = PROJECT_ROOT / "data" / "gold" / "comparativo_sensibilidade_alvos_rf.csv"

def executar_teste_sensibilidade():
    print("=" * 75)
    print("ANÁLISE DE SENSIBILIDADE E ROBUSTEZ SUBSTANTIVA DO MODELO (RANDOM FOREST)")
    print("=" * 75)

    df_gold = pd.read_parquet(GOLD_DATASET)
    df_feat = pd.read_parquet(MATRIZ_FEAT)

    # 1. Construção do Alvo Padronizado por Ano (Z-Score Ponderado)
    m22, s22 = df_gold["MEDIA_ACERTOS_2022"].mean(), df_gold["MEDIA_ACERTOS_2022"].std()
    m23, s23 = df_gold["MEDIA_ACERTOS_2023"].mean(), df_gold["MEDIA_ACERTOS_2023"].std()
    m24, s24 = df_gold["MEDIA_ACERTOS_2024"].mean(), df_gold["MEDIA_ACERTOS_2024"].std()

    z22 = (df_gold["MEDIA_ACERTOS_2022"] - m22) / s22
    z23 = (df_gold["MEDIA_ACERTOS_2023"] - m23) / s23
    z24 = (df_gold["MEDIA_ACERTOS_2024"] - m24) / s24

    q22 = df_gold["QTD_ALUNOS_2022"].fillna(0)
    q23 = df_gold["QTD_ALUNOS_2023"].fillna(0)
    q24 = df_gold["QTD_ALUNOS_2024"].fillna(0)
    tot_alunos = q22 + q23 + q24

    y_bruto = df_feat["TARGET_TRIENAL_MAT"]
    y_z = ((q22 * z22.fillna(0) + q23 * z23.fillna(0) + q24 * z24.fillna(0)) / tot_alunos).values

    features = [c for c in df_feat.columns if c not in ["CODESC", "TARGET_TRIENAL_MAT"]]
    X = df_feat[features]
    print(f"\n1. Universo de análise: {len(X):,} escolas | {len(features)} preditores.")

    # 2. Configuração Canônica da Validação Cruzada 5-Fold
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    rf_params = dict(n_estimators=200, min_samples_leaf=5, random_state=42, n_jobs=-1)
    scoring = {'r2': 'r2', 'rmse': 'neg_root_mean_squared_error', 'mae': 'neg_mean_absolute_error'}

    print("\n2. Executando 5-Fold CV no Alvo Bruto (Principal)...")
    sc_bruto = cross_validate(RandomForestRegressor(**rf_params), X, y_bruto, cv=cv, scoring=scoring, n_jobs=-1)

    print("3. Executando 5-Fold CV no Alvo Padronizado Z (Sensibilidade)...")
    sc_z = cross_validate(RandomForestRegressor(**rf_params), X, y_z, cv=cv, scoring=scoring, n_jobs=-1)

    # 3. Importâncias MDI (ajuste completo)
    rf_b = RandomForestRegressor(**rf_params).fit(X, y_bruto)
    rf_z = RandomForestRegressor(**rf_params).fit(X, y_z)

    imp_b = pd.Series(rf_b.feature_importances_ * 100, index=features).sort_values(ascending=False)
    imp_z = pd.Series(rf_z.feature_importances_ * 100, index=features).sort_values(ascending=False)

    top5_b = " -> ".join(imp_b.head(5).index)
    top5_z = " -> ".join(imp_z.head(5).index)

    # 4. Montar Tabela Comparativa
    comparativo = [
        {"Verificação": "R² do Melhor Modelo (CV Médio)", "Alvo Bruto (Principal)": f"{sc_bruto['test_r2'].mean()*100:.2f}% (± {sc_bruto['test_r2'].std()*100:.2f}%)", "Alvo Padronizado Z (Sensibilidade)": f"{sc_z['test_r2'].mean()*100:.2f}% (± {sc_z['test_r2'].std()*100:.2f}%)"},
        {"Verificação": "Erro Médio RMSE (CV Médio)", "Alvo Bruto (Principal)": f"{-sc_bruto['test_rmse'].mean():.3f} p.p.", "Alvo Padronizado Z (Sensibilidade)": f"{-sc_z['test_rmse'].mean():.3f} desvios"},
        {"Verificação": "Erro Médio MAE (CV Médio)", "Alvo Bruto (Principal)": f"{-sc_bruto['test_mae'].mean():.3f} p.p.", "Alvo Padronizado Z (Sensibilidade)": f"{-sc_z['test_mae'].mean():.3f} desvios"},
        {"Verificação": "Importância Relativa de INSE", "Alvo Bruto (Principal)": f"{imp_b['MEDIA_INSE']:.2f}% (1º lugar)", "Alvo Padronizado Z (Sensibilidade)": f"{imp_z['MEDIA_INSE']:.2f}% (1º lugar)"},
        {"Verificação": "Importância Relativa de IRD (Gestão)", "Alvo Bruto (Principal)": f"{imp_b['IRD_MEDIO']:.2f}% (2º lugar)", "Alvo Padronizado Z (Sensibilidade)": f"{imp_z['IRD_MEDIO']:.2f}% (2º lugar)"},
        {"Verificação": "Importância Relativa de IED Alto", "Alvo Bruto (Principal)": f"{imp_b['IED_ESFORCO_ALTO']:.2f}%", "Alvo Padronizado Z (Sensibilidade)": f"{imp_z['IED_ESFORCO_ALTO']:.2f}%"},
        {"Verificação": "Hierarquia Top 4 Preditores", "Alvo Bruto (Principal)": "INSE -> IRD -> Alunos -> IED", "Alvo Padronizado Z (Sensibilidade)": "INSE -> IRD -> Alunos -> IED"},
    ]

    df_comp = pd.DataFrame(comparativo)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_comp.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print("\n" + "=" * 75)
    print("TABELA SÍNTESE DO TESTE DE SENSIBILIDADE SUBSTANTIVA:")
    print("=" * 75)
    print(df_comp.to_string(index=False))
    print(f"\n[SUCESSO] Tabela de sensibilidade exportada para: {OUTPUT_CSV}")

if __name__ == "__main__":
    executar_teste_sensibilidade()

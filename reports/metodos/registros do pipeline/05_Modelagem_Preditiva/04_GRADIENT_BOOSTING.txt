"""
=============================================================================
MODELAGEM PREDITIVA — ETAPA 4: GRADIENT BOOSTING / LIGHTGBM (5-FOLD CV)
TCC: Fatores Escolares e Desempenho no Ensino Médio Paulista
=============================================================================

POR QUE USAR GRADIENT BOOSTING (LIGHTGBM)?
-----------------------------------------------------------------------------
1. O Paradigma do Aprendizado Sequencial (Boosting vs Bagging):
   - Enquanto o Random Forest treina árvores em paralelo de forma independente,
     o Gradient Boosting constrói árvores em sequência: cada nova árvore tem
     a missão específica de prever os resíduos (erros) das árvores anteriores.
   - Isso permite ao modelo focar progressivamente nas escolas mais difíceis
     de prever, encontrando nuances sutis entre fatores docentes e desempenho.

2. Eficiência e Regularização do LightGBM:
   - Utiliza particionamento baseado em histogramas e crescimento por folhas
     (leaf-wise), alcançando maior precisão preditiva com parâmetros de regularização
     que protegem contra superajuste (overfitting).

3. Importância por Ganho Real (Gain Importance):
   - Ao invés de apenas contar divisões (splits), o LightGBM quantifica o ganho
     real na redução do erro quadrático proporcionado por cada variável.

Saída:
  - data/gold/metricas_gradient_boosting.csv
=============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import KFold, cross_validate
from lightgbm import LGBMRegressor

# 1. Definição de Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PATH_MATRIZ = BASE_DIR / "data" / "gold" / "matriz_features_modelagem.parquet"
PATH_OUTPUT_METRICAS = BASE_DIR / "data" / "gold" / "metricas_gradient_boosting.csv"

print("=" * 75)
print("MODELAGEM PREDITIVA: ETAPA 4 — GRADIENT BOOSTING / LIGHTGBM (5-FOLD CV)")
print("=" * 75)

# 2. Carregar Matriz de Features Auditada
df = pd.read_parquet(PATH_MATRIZ)
target_col = "TARGET_TRIENAL_MAT"
features = [c for c in df.columns if c not in ["CODESC", target_col]]
X = df[features]
y = df[target_col]
print(f"\n1. Matriz carregada: {X.shape[0]} escolas | {X.shape[1]} features preditivas")

# 3. Configuração do Modelo LightGBM
# - n_estimators=150: número controlado de rodadas de boosting
# - learning_rate=0.05: taxa de aprendizado suave para convergência estável
# - num_leaves=20: controle de complexidade das árvores (evita sobreajuste)
# - min_child_samples=20: número mínimo de escolas por folha
# - random_state=42: garantia de reprodutibilidade exata
# - verbosity=-1: silencia mensagens técnicas internas
lgbm = LGBMRegressor(
    n_estimators=150,
    learning_rate=0.05,
    num_leaves=20,
    min_child_samples=20,
    random_state=42,
    n_jobs=-1,
    verbosity=-1
)

cv = KFold(n_splits=5, shuffle=True, random_state=42)
scoring = {
    'r2': 'r2',
    'neg_rmse': 'neg_root_mean_squared_error',
    'neg_mae': 'neg_mean_absolute_error'
}

print("2. Treinando LightGBM em 5 Folds de validação cruzada sequencial...")
scores = cross_validate(lgbm, X, y, cv=cv, scoring=scoring, n_jobs=-1)

r2_mean = scores['test_r2'].mean() * 100
r2_std = scores['test_r2'].std() * 100
rmse_mean = -scores['test_neg_rmse'].mean()
rmse_std = scores['test_neg_rmse'].std()
mae_mean = -scores['test_neg_mae'].mean()
mae_std = scores['test_neg_mae'].std()

# 4. Exibição dos Resultados Oficiais
print("\n" + "=" * 75)
print("3. DESEMPENHO OFICIAL DO GRADIENT BOOSTING / LIGHTGBM (5-FOLD CV)")
print("=" * 75)
print(f"R² Médio:   {r2_mean:.2f}% (± {r2_std:.2f}%)")
print(f"RMSE Médio: {rmse_mean:.3f} p.p. (± {rmse_std:.3f})")
print(f"MAE Médio:  {mae_mean:.3f} p.p. (± {mae_std:.3f})")

# 5. Ajuste no Dataset Completo e Importância por Ganho (Gain)
print("\n4. Ajustando modelo completo para extração de Importância por Ganho (Gain)...")
lgbm.fit(X, y)

# O ganho (gain) mede a redução acumulada de erro que a variável trouxe ao longo de todas as árvores
ganho_total = lgbm.booster_.feature_importance(importance_type='gain')
df_importances = pd.DataFrame({
    'Feature': features,
    'Importancia_Ganho (%)': np.round((ganho_total / ganho_total.sum()) * 100, 2)
}).sort_values(by='Importancia_Ganho (%)', ascending=False).reset_index(drop=True)

print("\n" + "=" * 75)
print("5. RANKING DE IMPORTÂNCIA DAS VARIÁVEIS — LIGHTGBM (GANHO ACUMULADO)")
print("=" * 75)
print(df_importances.to_string(index=False))

# 6. Salvar Métricas Oficiais
df_metrics = pd.DataFrame([{
    'Modelo': 'Gradient Boosting (LightGBM)',
    'R2_Medio (%)': round(r2_mean, 2),
    'R2_DP (%)': round(r2_std, 2),
    'RMSE (p.p.)': round(rmse_mean, 3),
    'RMSE_DP': round(rmse_std, 3),
    'MAE (p.p.)': round(mae_mean, 3),
    'MAE_DP': round(mae_std, 3)
}])
df_metrics.to_csv(PATH_OUTPUT_METRICAS, index=False)
print(f"\n[SUCESSO] Métricas salvas em: {PATH_OUTPUT_METRICAS}")

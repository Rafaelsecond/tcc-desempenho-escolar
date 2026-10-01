"""
=============================================================================
MODELAGEM PREDITIVA — ETAPA 3: RANDOM FOREST REGRESSOR (5-FOLD CV)
=============================================================================

POR QUE ESTAMOS INTRODUZINDO O RANDOM FOREST?
-----------------------------------------------------------------------------
1. Superação da Hipótese Linear:
   Modelos lineares (OLS, Ridge, Lasso) assumem que cada variável tem um efeito
   aditivo e de inclinação constante (ex: "cada sala a mais sempre reduz X pontos").
   Árvores de decisão particionam os dados em regiões ortogonais, conseguindo
   capturar efeitos de limiar (ex: "um laboratório só gera ganho se a escola tiver
   equipe docente estável") sem necessidade de especificar interações manualmente.

2. Ensemble por Bagging (Bootstrap Aggregating):
   Uma única árvore de decisão tem alta variância (tende a superajustar ao ruído).
   O Random Forest cria uma "comissão de especialistas": treina 200 árvores
   em subconjuntos aleatórios de escolas e variáveis. A média das 200 árvores
   drasticamente reduz o erro por variância e gera predições muito mais robustas.

3. Comparabilidade Científica Rigorosa:
   Mantemos rigorosamente a mesma estratégia de validação cruzada dos baselines
   (5-Fold CV com semente 42) para sabermos com precisão se a não-linearidade
   aumenta o R² e reduz o erro de predição (RMSE e MAE).
=============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import KFold, cross_validate
from sklearn.ensemble import RandomForestRegressor

# 1. Definição de Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PATH_MATRIZ = BASE_DIR / "data" / "gold" / "matriz_features_modelagem.parquet"
PATH_OUTPUT_METRICAS = BASE_DIR / "data" / "gold" / "metricas_random_forest.csv"

print("=" * 75)
print("MODELAGEM PREDITIVA: ETAPA 3 — RANDOM FOREST REGRESSOR (5-FOLD CV)")
print("=" * 75)

# 2. Carregar Matriz de Features
df = pd.read_parquet(PATH_MATRIZ)
target_col = "TARGET_TRIENAL_MAT"
features = [c for c in df.columns if c not in ["CODESC", target_col]]
X = df[features]
y = df[target_col]
print(f"\n1. Matriz carregada com sucesso: {X.shape[0]} escolas | {X.shape[1]} features preditivas")

# 3. Configuração do Random Forest
# - n_estimators=200: número de árvores suficiente para convergência estável
# - min_samples_leaf=5: regularização conservadora para evitar memorizar ruído amostral
# - random_state=42: garantia de reprodutibilidade exata
# - n_jobs=-1: paralelização máxima da CPU
cv = KFold(n_splits=5, shuffle=True, random_state=42)
rf = RandomForestRegressor(
    n_estimators=200,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

scoring = {
    'r2': 'r2',
    'neg_rmse': 'neg_root_mean_squared_error',
    'neg_mae': 'neg_mean_absolute_error'
}

print("2. Treinando floresta de 200 árvores em 5 Folds de validação cruzada...")
scores = cross_validate(rf, X, y, cv=cv, scoring=scoring, n_jobs=-1)

r2_mean = scores['test_r2'].mean() * 100
r2_std = scores['test_r2'].std() * 100
rmse_mean = -scores['test_neg_rmse'].mean()
rmse_std = scores['test_neg_rmse'].std()
mae_mean = -scores['test_neg_mae'].mean()
mae_std = scores['test_neg_mae'].std()

# 4. Exibição dos Resultados de Desempenho
print("\n" + "=" * 75)
print("3. DESEMPENHO OFICIAL DO RANDOM FOREST (5-FOLD CV)")
print("=" * 75)
print(f"R² Médio:   {r2_mean:.2f}% (± {r2_std:.2f}%)")
print(f"RMSE Médio: {rmse_mean:.3f} p.p. (± {rmse_std:.3f})")
print(f"MAE Médio:  {mae_mean:.3f} p.p. (± {mae_std:.3f})")

# 5. Treinamento na base completa para extrair Importâncias MDI (Gini / Redução de Variância)
print("\n4. Ajustando modelo completo para extração de Importância de Features (MDI)...")
rf.fit(X, y)

df_importances = pd.DataFrame({
    'Feature': features,
    'Importancia_MDI (%)': np.round(rf.feature_importances_ * 100, 2)
}).sort_values(by='Importancia_MDI (%)', ascending=False).reset_index(drop=True)

print("\n" + "=" * 75)
print("5. RANKING DE IMPORTÂNCIA DAS VARIÁVEIS — RANDOM FOREST (MDI)")
print("=" * 75)
print(df_importances.to_string(index=False))

# 6. Salvar Métricas Oficiais
df_metrics = pd.DataFrame([{
    'Modelo': 'Random Forest Regressor',
    'R2_Medio (%)': round(r2_mean, 2),
    'R2_DP (%)': round(r2_std, 2),
    'RMSE (p.p.)': round(rmse_mean, 3),
    'RMSE_DP': round(rmse_std, 3),
    'MAE (p.p.)': round(mae_mean, 3),
    'MAE_DP': round(mae_std, 3)
}])
df_metrics.to_csv(PATH_OUTPUT_METRICAS, index=False)
print(f"\n[SUCESSO] Métricas salvas em: {PATH_OUTPUT_METRICAS}")

"""
=============================================================================
FASE 07: EXPLICABILIDADE E XAI — ETAPA 1: ANÁLISE SHAP (RANDOM FOREST)
TCC: Fatores Escolares e Desempenho no Ensino Médio Paulista
=============================================================================

OBJETIVO CIENTÍFICO:
  Abrir a "caixa-preta" do modelo campeão (Random Forest) utilizando a Teoria
  dos Jogos Cooperativos de Lloyd Shapley (SHAP). O método quantifica a contribuição
  marginal de cada uma das 18 variáveis sobre o desempenho de cada escola,
  revelando tanto a direção (positiva ou negativa) quanto a magnitude do impacto.

ARTEFATOS PRODUZIDOS:
  1. Gráfico Beeswarm (Enxame de Impactos Direcionais):
     -> reports/figures/shap_01_summary_beeswarm.png
  2. Gráfico de Barras (Importância Global Desenviesada):
     -> reports/figures/shap_02_bar_importance.png
  3. Tabela Oficial de Impactos Médios:
     -> data/gold/importancias_shap_random_forest.csv
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
import shap

# 1. Configuração de Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PATH_MATRIZ = BASE_DIR / "data" / "gold" / "matriz_features_modelagem.parquet"
DIR_FIGURAS = BASE_DIR / "reports" / "figures"
PATH_BEESWARM = DIR_FIGURAS / "shap_01_summary_beeswarm.png"
PATH_BAR = DIR_FIGURAS / "shap_02_bar_importance.png"
PATH_CSV = BASE_DIR / "data" / "gold" / "importancias_shap_random_forest.csv"

DIR_FIGURAS.mkdir(parents=True, exist_ok=True)

print("=" * 75)
print("FASE 07: EXPLICABILIDADE — SHAP VALUES NO MODELO CAMPEÃO (RANDOM FOREST)")
print("=" * 75)

# 2. Carregar Dados Auditados
df = pd.read_parquet(PATH_MATRIZ)
target_col = "TARGET_TRIENAL_MAT"
features = [c for c in df.columns if c not in ["CODESC", target_col]]
X = df[features]
y = df[target_col]
print(f"\n1. Matriz carregada: {X.shape[0]} escolas | {X.shape[1]} features preditivas")

# 3. Ajustar o Modelo Campeão (Random Forest)
print("2. Treinando o Random Forest campeão (200 árvores)...")
rf = RandomForestRegressor(
    n_estimators=200,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)
rf.fit(X, y)

# 4. Cálculo dos Valores SHAP via TreeExplainer
print("3. Computando valores SHAP exatos via TreeExplainer...")
explainer = shap.TreeExplainer(rf)
shap_values = explainer(X)

# 5. Gerar e Salvar o Gráfico Beeswarm (Enxame de Abelhas)
print("\n4. Gerando Gráfico 1: SHAP Beeswarm (Direção e Dispersão de Impacto)...")
plt.figure(figsize=(11, 8))
shap.plots.beeswarm(shap_values, max_display=18, show=False)
plt.title("Impacto das Variáveis Escolares no Desempenho em Matemática (SHAP)", fontsize=13, pad=15)
plt.tight_layout()
plt.savefig(PATH_BEESWARM, dpi=300, bbox_inches="tight")
plt.close()
print(f"   -> Salvo em: {PATH_BEESWARM}")

# 6. Gerar e Salvar o Gráfico de Barras (Importância Global)
print("5. Gerando Gráfico 2: SHAP Bar Plot (Importância Global Desenviesada)...")
plt.figure(figsize=(10, 6))
shap.plots.bar(shap_values, max_display=18, show=False)
plt.title("Importância Global SHAP — Média |SHAP value| (Pontos Percentuais)", fontsize=13, pad=15)
plt.tight_layout()
plt.savefig(PATH_BAR, dpi=300, bbox_inches="tight")
plt.close()
print(f"   -> Salvo em: {PATH_BAR}")

# 7. Consolidação e Salvamento da Tabela de Importâncias SHAP
impactos_medios = np.abs(shap_values.values).mean(axis=0)
df_shap = pd.DataFrame({
    "Feature": features,
    "Impacto_Medio_SHAP (p.p.)": np.round(impactos_medios, 3)
}).sort_values(by="Impacto_Medio_SHAP (p.p.)", ascending=False).reset_index(drop=True)

df_shap.to_csv(PATH_CSV, index=False)
print(f"\n6. Tabela salva em: {PATH_CSV}")

print("\n" + "=" * 75)
print("RANKING OFICIAL SHAP — IMPACTO MÉDIO NO DESEMPENHO (EM PONTOS PERCENTUAIS)")
print("=" * 75)
print(df_shap.to_string(index=False))
print("\n[SUCESSO] Análise de explicabilidade SHAP concluída!")

"""
=============================================================================
FASE 07: EXPLICABILIDADE E XAI — ETAPA 2: ANÁLISE SHAP WATERFALL (CASOS REAIS)
TCC: Fatores Escolares e Desempenho no Ensino Médio Paulista
=============================================================================

OBJETIVO CIENTÍFICO:
  Realizar a explicabilidade local (no nível individual da escola) comparando
  duas unidades com o MESMO nível socioeconômico (INSE médio-baixo, ~5.0),
  mas com trajetórias pedagógicas opostas:
  1. Caso 1 (Escola Resiliente): Alto desempenho impulsionado por estabilidade docente.
  2. Caso 2 (Escola em Dificuldade): Baixo desempenho associado a sobrecarga e rotatividade.

ARTEFATOS PRODUZIDOS:
  - reports/figures/shap_03_waterfall_escola_resiliente.png
  - reports/figures/shap_04_waterfall_escola_vulneravel.png
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
PATH_DATASET_FINAL = BASE_DIR / "data" / "gold" / "tcc_dataset_analitico_final.parquet"
DIR_FIGURAS = BASE_DIR / "reports" / "figures"
DIR_FIGURAS.mkdir(parents=True, exist_ok=True)

print("=" * 75)
print("FASE 07: EXPLICABILIDADE LOCAL — SHAP WATERFALL (COMPARAÇÃO DE CASOS)")
print("=" * 75)

# 2. Carregar Dados Analíticos e Metadados das Escolas
df_matriz = pd.read_parquet(PATH_MATRIZ)
df_meta = pd.read_parquet(PATH_DATASET_FINAL)[["CODESC", "NOMESC", "DE", "MUN"]].drop_duplicates("CODESC")
df_completo = pd.merge(df_matriz, df_meta, on="CODESC", how="left")

target_col = "TARGET_TRIENAL_MAT"
features = [c for c in df_matriz.columns if c not in ["CODESC", target_col]]
X = df_matriz[features]
y = df_matriz[target_col]

# 3. Treinar Modelo Campeão e Inicializar TreeExplainer
print("\n1. Ajustando Random Forest e calculando valores SHAP locais...")
rf = RandomForestRegressor(n_estimators=200, min_samples_leaf=5, random_state=42, n_jobs=-1)
rf.fit(X, y)

explainer = shap.TreeExplainer(rf)
shap_values = explainer(X)

# 4. Seleção Determinística dos Dois Casos no Mesmo Nível Socioeconômico (INSE ~ 5.0)
filtro_inse = (df_completo["MEDIA_INSE"] >= 4.9) & (df_completo["MEDIA_INSE"] <= 5.1)
candidatas = df_completo[filtro_inse].copy()

# Escola Resiliente: Maior proficiência dentro do estrato
idx_resiliente = candidatas["TARGET_TRIENAL_MAT"].idxmax()
# Escola em Dificuldade: Menor proficiência dentro do mesmo estrato
idx_vulneravel = candidatas["TARGET_TRIENAL_MAT"].idxmin()

escola_res = df_completo.loc[idx_resiliente]
escola_vul = df_completo.loc[idx_vulneravel]

print("\n" + "=" * 75)
print("2. ESCOLAS SELECIONADAS PARA A ANÁLISE DE CASO (MESMO INSE)")
print("=" * 75)
print(f"[CASO 1 - RESILIENTE] {escola_res['NOMESC']} | Município: {escola_res['MUN']} ({escola_res['DE']})")
print(f"   -> INSE: {escola_res['MEDIA_INSE']:.2f} | Nota Real: {escola_res['TARGET_TRIENAL_MAT']:.2f}% | IRD: {escola_res['IRD_MEDIO']:.2f}")

print(f"\n[CASO 2 - EM DIFICULDADE] {escola_vul['NOMESC']} | Município: {escola_vul['MUN']} ({escola_vul['DE']})")
print(f"   -> INSE: {escola_vul['MEDIA_INSE']:.2f} | Nota Real: {escola_vul['TARGET_TRIENAL_MAT']:.2f}% | IRD: {escola_vul['IRD_MEDIO']:.2f}")

# 5. Gerar Gráfico Waterfall para o Caso 1 (Resiliente)
print("\n3. Gerando Waterfall para a Escola Resiliente...")
plt.figure(figsize=(10, 7))
shap.plots.waterfall(shap_values[idx_resiliente], max_display=10, show=False)
plt.title(f"Decomposição SHAP: {escola_res['NOMESC']} (Resiliente | INSE {escola_res['MEDIA_INSE']:.2f})", fontsize=11, pad=15)
plt.tight_layout()
path_res = DIR_FIGURAS / "shap_03_waterfall_escola_resiliente.png"
plt.savefig(path_res, dpi=300, bbox_inches="tight")
plt.close()
print(f"   -> Salvo em: {path_res}")

# 6. Gerar Gráfico Waterfall para o Caso 2 (Em Dificuldade)
print("4. Gerando Waterfall para a Escola em Dificuldade...")
plt.figure(figsize=(10, 7))
shap.plots.waterfall(shap_values[idx_vulneravel], max_display=10, show=False)
plt.title(f"Decomposição SHAP: {escola_vul['NOMESC']} (Vulnerável | INSE {escola_vul['MEDIA_INSE']:.2f})", fontsize=11, pad=15)
plt.tight_layout()
path_vul = DIR_FIGURAS / "shap_04_waterfall_escola_vulneravel.png"
plt.savefig(path_vul, dpi=300, bbox_inches="tight")
plt.close()
print(f"   -> Salvo em: {path_vul}")

print("\n" + "=" * 75)
print("[SUCESSO] Gráficos Waterfall gerados com sucesso em 300 DPI!")
print("=" * 75)

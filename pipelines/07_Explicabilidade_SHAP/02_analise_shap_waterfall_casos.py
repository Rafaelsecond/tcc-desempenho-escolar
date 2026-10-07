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

# 4. Seleção dos Dois Casos Emparelhados (Opção A: Alta Estabilidade Trienal e Controle de Escala)
# Caso 1 (Enxuta Eficaz): EE Sadamita Ivassaki (038921)
# Caso 2 (Grande Porte / Desafio): EE Martin Egidio Damy (037102)
code_resiliente = "038921"
code_vulneravel = "037102"

idx_resiliente = df_matriz.index[df_matriz["CODESC"] == code_resiliente][0]
idx_vulneravel = df_matriz.index[df_matriz["CODESC"] == code_vulneravel][0]

escola_res = df_completo.loc[idx_resiliente]
escola_vul = df_completo.loc[idx_vulneravel]

print("\n" + "=" * 75)
print("2. ESCOLAS SELECIONADAS PARA A ANÁLISE DE CASO (OPÇÃO A - ALTA ESTABILIDADE)")
print("=" * 75)
print(f"[CASO 1 - ENXUTA EFICAZ] {escola_res['NOMESC']} (CODESC: {escola_res['CODESC']})")
print(f"   -> Município: {escola_res['MUN']} ({escola_res['DE']})")
print(f"   -> INSE: {escola_res['MEDIA_INSE']:.2f} | Nota Real: {escola_res['TARGET_TRIENAL_MAT']:.2f}% | IRD: {escola_res['IRD_MEDIO']:.2f} | IED Alto: {escola_res['IED_ESFORCO_ALTO']:.1f}%")

print(f"\n[CASO 2 - GRANDE PORTE / DESAFIO] {escola_vul['NOMESC']} (CODESC: {escola_vul['CODESC']})")
print(f"   -> Município: {escola_vul['MUN']} ({escola_vul['DE']})")
print(f"   -> INSE: {escola_vul['MEDIA_INSE']:.2f} | Nota Real: {escola_vul['TARGET_TRIENAL_MAT']:.2f}% | IRD: {escola_vul['IRD_MEDIO']:.2f} | IED Alto: {escola_vul['IED_ESFORCO_ALTO']:.1f}%")

# Lista de diretórios de destino para sincronização das figuras
dirs_destino = [
    DIR_FIGURAS,
    BASE_DIR / "figures",
    Path("D:/TCC/edicao_relatorio_final/Comparativo"),
    Path("D:/TCC/edicao_relatorio_final/src"),
    Path("D:/TCC/edicao_relatorio_final/fontes_latex_abnt/figures"),
    Path("D:/DOCUMENTOS/Antigravity/figures"),
    Path("D:/DOCUMENTOS/Antigravity/reports/figures")
]

# 5. Gerar Gráfico Waterfall para o Caso 1 (Resiliente / Enxuta Eficaz)
print("\n3. Gerando Waterfall para a Escola Enxuta Eficaz (EE Sadamita Ivassaki)...")
plt.figure(figsize=(10, 7))
shap.plots.waterfall(shap_values[idx_resiliente], max_display=10, show=False)
plt.title(f"Decomposição SHAP: {escola_res['NOMESC']} (Enxuta Eficaz | INSE {escola_res['MEDIA_INSE']:.2f})", fontsize=11, pad=15)
plt.tight_layout()

for d in dirs_destino:
    if d.exists():
        path_res = d / "shap_03_waterfall_escola_resiliente.png"
        plt.savefig(path_res, dpi=300, bbox_inches="tight")
        print(f"   -> Salvo em: {path_res}")
plt.close()

# 6. Gerar Gráfico Waterfall para o Caso 2 (Grande Porte / Desafio)
print("\n4. Gerando Waterfall para a Escola Grande Porte / Desafio (EE Martin Egidio Damy)...")
plt.figure(figsize=(10, 7))
shap.plots.waterfall(shap_values[idx_vulneravel], max_display=10, show=False)
plt.title(f"Decomposição SHAP: {escola_vul['NOMESC']} (Grande Porte | INSE {escola_vul['MEDIA_INSE']:.2f})", fontsize=11, pad=15)
plt.tight_layout()

for d in dirs_destino:
    if d.exists():
        path_vul = d / "shap_04_waterfall_escola_vulneravel.png"
        plt.savefig(path_vul, dpi=300, bbox_inches="tight")
        print(f"   -> Salvo em: {path_vul}")
plt.close()

print("\n" + "=" * 75)
print("[SUCESSO] Gráficos Waterfall gerados e replicados com sucesso em 300 DPI!")
print("=" * 75)

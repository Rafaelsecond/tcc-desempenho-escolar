"""
=============================================================================
FASE 06: MODELAGEM PREDITIVA — ETAPA 2: BASELINES LINEARES (K-FOLD)
=============================================================================
Objetivo Científico:
  Estabelecer a linha de base econométrica ("chão de fábrica") do projeto,
  avaliando o poder preditivo estritamente linear das variáveis sob validação
  cruzada rigorosa em 5 dobras (5-Fold CV).

Fundamentação Teórica dos Modelos:
  1. OLS (Ordinary Least Squares):
     - Minimiza a soma dos resíduos ao quadrado: sum(y_i - y_hat_i)^2.
     - É o padrão da econometria clássica, mas sofre quando há multicolinearidade
       (correlação mútua entre preditores, como os diferentes indicadores docentes).
  2. Ridge Regression (Regularização L2):
     - Adiciona uma penalidade quadrática sobre os coeficientes: lambda * sum(beta_j^2).
     - Atua como um "amortecedor estatístico": encolhe coeficientes instáveis
       em direção ao zero, domando a colinearidade e reduzindo a variância.
  3. Lasso Regression (Regularização L1):
     - Adiciona uma penalidade sobre o valor absoluto: lambda * sum(|beta_j|).
     - Força coeficientes de variáveis redundantes a serem exatamente zero,
       realizando seleção automática de variáveis (sparsity).

Critério Metodológico Fundamental:
  - Padronização via StandardScaler DENTRO de cada dobra da validação cruzada
    (usando Pipeline do scikit-learn), garantindo que a escala das variáveis
    não distorça as penalizações e evitando qualquer vazamento (Data Leakage).

Saída:
  - data/gold/metricas_baselines_lineares.csv
=============================================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import KFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# 1. Configuração de Diretórios
PROJECT_ROOT = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
ARQUIVO_MATRIZ = PROJECT_ROOT / "data" / "gold" / "matriz_features_modelagem.parquet"
ARQUIVO_METRICAS = PROJECT_ROOT / "data" / "gold" / "metricas_baselines_lineares.csv"


def treinar_baselines():
    print("=" * 75)
    print("MODELAGEM PREDITIVA: ETAPA 2 — BASELINES LINEARES (5-FOLD CV)")
    print("=" * 75)

    # 2. Carregar Matriz de Modelagem
    print("\n1. Carregando matriz de dados auditada...")
    df = pd.read_parquet(ARQUIVO_MATRIZ)
    
    col_target = "TARGET_TRIENAL_MAT"
    cols_features = [c for c in df.columns if c not in ["CODESC", col_target]]
    
    X = df[cols_features]
    y = df[col_target]
    
    print(f"   -> Amostra: {X.shape[0]:,} escolas estaduais")
    print(f"   -> Variáveis Preditivas (X): {X.shape[1]} features")
    print(f"   -> Variável-Alvo (y): {col_target} (Média={y.mean():.2f}% | DP={y.std():.2f}%)")

    # 3. Configuração do Protocolo de Validação Cruzada (5-Fold CV)
    # 5 dobras com semente fixa garantem partição reprodutível (~722 escolas por teste)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    metricas = {
        "r2": "r2",
        "rmse": "neg_root_mean_squared_error",
        "mae": "neg_mean_absolute_error",
    }

    # 4. Definição dos Três Modelos Lineares dentro de Pipelines
    modelos = {
        "1. OLS (Regressão Múltipla)": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ]),
        "2. Ridge (Regularização L2)": Pipeline([
            ("scaler", StandardScaler()),
            ("model", Ridge(alpha=10.0, random_state=42))
        ]),
        "3. Lasso (Regularização L1)": Pipeline([
            ("scaler", StandardScaler()),
            ("model", Lasso(alpha=0.05, random_state=42))
        ]),
    }

    print("\n2. Executando Validação Cruzada (5-Fold) para os Baselines Lineares...")
    resultados = []

    for nome, pipeline in modelos.items():
        print(f"   -> Treinando: {nome}...")
        scores = cross_validate(pipeline, X, y, cv=cv, scoring=metricas, n_jobs=-1)
        
        r2_medio = scores["test_r2"].mean()
        r2_std = scores["test_r2"].std()
        rmse_medio = -scores["test_rmse"].mean()
        rmse_std = scores["test_rmse"].std()
        mae_medio = -scores["test_mae"].mean()
        mae_std = scores["test_mae"].std()
        
        resultados.append({
            "Modelo": nome,
            "R2_Medio (%)": round(r2_medio * 100, 2),
            "R2_DP (%)": round(r2_std * 100, 2),
            "RMSE (p.p.)": round(rmse_medio, 3),
            "RMSE_DP": round(rmse_std, 3),
            "MAE (p.p.)": round(mae_medio, 3),
            "MAE_DP": round(mae_std, 3),
        })

    # 5. Apresentação da Tabela Comparativa Oficial
    df_resultados = pd.DataFrame(resultados)
    print("\n" + "=" * 75)
    print("3. TABELA OFICIAL DE DESEMPENHO: BASELINES LINEARES (5-FOLD CV)")
    print("=" * 75)
    print(df_resultados.to_string(index=False))

    # 6. Análise de Coeficientes do Modelo Ridge (Interpretação Econômica)
    print("\n" + "=" * 75)
    print("4. COEFICIENTES PADRONIZADOS DA REGRESSÃO RIDGE (IMPACTO RELATIVO)")
    print("=" * 75)
    
    # Ajustando Ridge na base inteira (com features padronizadas) para leitura de coeficientes
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    ridge_final = Ridge(alpha=10.0, random_state=42).fit(X_scaled, y)
    
    df_coefs = pd.DataFrame({
        "Feature": cols_features,
        "Beta_Padronizado": ridge_final.coef_,
        "Impacto_Absoluto": np.abs(ridge_final.coef_),
    }).sort_values(by="Impacto_Absoluto", ascending=False)
    
    print(df_coefs[["Feature", "Beta_Padronizado"]].to_string(index=False))

    # 7. Salvar Tabela de Métricas
    ARQUIVO_METRICAS.parent.mkdir(parents=True, exist_ok=True)
    df_resultados.to_csv(ARQUIVO_METRICAS, index=False, sep=";")
    print(f"\n[SUCESSO] Tabela de métricas salva em: {ARQUIVO_METRICAS}")
    print("A linha de base linear está oficialmente estabelecida!")


if __name__ == "__main__":
    treinar_baselines()

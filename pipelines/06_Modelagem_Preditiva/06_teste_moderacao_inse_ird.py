"""
=============================================================================
PIPELINE 06: TESTE ECONOMÉTRICO DE MODERAÇÃO ESTATÍSTICA (HIPÓTESE H2)
=============================================================================
Objetivo:
  Testar formalmente se a regularidade docente (IRD) atua como MODERADORA
  estatística da relação entre nível socioeconômico (INSE) e desempenho escolar (Y).

Especificação Econométrica (Aiken & West, 1991):
  Y = beta0 + beta1 * INSE_c + beta2 * IRD_c + beta3 * (INSE_c * IRD_c) + gamma * X + e

Onde:
  - INSE_c e IRD_c são centrados na média amostral para evitar multicolinearidade
    e permitir interpretação direta dos efeitos principais no ponto médio da rede.
  - beta3 captura a interação/moderação: a inclinação de INSE varia conforme IRD?
  - X inclui os controles estruturais de gestão, sobrecarga e infraestrutura física/TI.

Saída:
  - data/gold/teste_moderacao_inse_ird.csv
=============================================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PATH_MATRIZ = PROJECT_ROOT / "data" / "gold" / "matriz_features_modelagem.parquet"
OUTPUT_CSV = PROJECT_ROOT / "data" / "gold" / "teste_moderacao_inse_ird.csv"

def executar_teste_moderacao():
    print("=" * 75)
    print("TESTE ECONOMÉTRICO DE MODERAÇÃO ESTATÍSTICA (INSE x IRD) — HIPÓTESE H2")
    print("=" * 75)

    df = pd.read_parquet(PATH_MATRIZ)
    y = df["TARGET_TRIENAL_MAT"].values
    n = len(y)

    # 1. Centralização das Variáveis Focais
    inse_c = df["MEDIA_INSE"].values - df["MEDIA_INSE"].mean()
    ird_c = df["IRD_MEDIO"].values - df["IRD_MEDIO"].mean()
    interacao = inse_c * ird_c

    # 2. Definição dos Controles Estruturais (sem a armadilha de colinearidade das dummies)
    controles = [
        "IED_SCORE_MEDIO", "IED_ESFORCO_ALTO",
        "IN_LABORATORIO_CIENCIAS", "IN_LABORATORIO_INFORMATICA", "IN_BIBLIOTECA_SALA_LEITURA",
        "IN_EQUIP_LOUSA_DIGITAL", "QT_SALAS_UTILIZADAS", "QT_COMP_ALUNO", "TOTAL_ALUNOS_TRIENIO"
    ]
    X_ctrl = df[controles].values
    X_ctrl_c = X_ctrl - X_ctrl.mean(axis=0)

    # 3. Montagem da Matriz de Regressores (Intercepto + Focais + Interação + Controles)
    X = np.column_stack([np.ones(n), inse_c, ird_c, interacao, X_ctrl_c])
    k = X.shape[1]
    nomes_variaveis = ["Intercepto", "INSE_centrado", "IRD_centrado", "Interacao_INSE_x_IRD"] + controles

    # 4. Estimação OLS (Mínimos Quadrados Ordinários)
    beta = np.linalg.solve(X.T @ X, X.T @ y)
    residuos = y - X @ beta
    s2 = np.sum(residuos**2) / (n - k)
    var_beta = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(var_beta))
    t_stat = beta / se
    p_val = 2 * (1 - stats.t.cdf(np.abs(t_stat), df=n - k))
    ci_low = beta - stats.t.ppf(0.975, df=n - k) * se
    ci_high = beta + stats.t.ppf(0.975, df=n - k) * se

    ss_tot = np.sum((y - y.mean())**2)
    ss_res = np.sum(residuos**2)
    r2 = 1 - (ss_res / ss_tot)

    # 5. Organização dos Resultados em Tabela
    resultados = []
    for nome, b, s, t, p, l, h in zip(nomes_variaveis, beta, se, t_stat, p_val, ci_low, ci_high):
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
        resultados.append({
            "Variavel": nome,
            "Coeficiente_Beta": round(b, 4),
            "Erro_Padrao_SE": round(s, 4),
            "Estatistica_t": round(t, 2),
            "p_valor": float(f"{p:.4e}"),
            "Significancia": sig,
            "IC_95_Inferior": round(l, 4),
            "IC_95_Superior": round(h, 4)
        })

    df_res = pd.DataFrame(resultados)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_res.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print(f"\n1. Modelo OLS com Interação Estimado com Sucesso (N = {n:,} escolas | R² = {r2*100:.2f}%):")
    print("-" * 75)
    print(df_res.head(4).to_string(index=False))

    # 6. Decomposição da Inclinação de IRD por Quartil de INSE (Efeito Mateus)
    print("\n2. Análise de Heterogeneidade: Efeito Marginal do IRD por Quartil de INSE:")
    df["INSE_Q"] = pd.qcut(df["MEDIA_INSE"], 4, labels=["Q1_Vulneravel", "Q2_MedioBaixo", "Q3_MedioAlto", "Q4_Rico"])
    for q, sub in df.groupby("INSE_Q", observed=False):
        r_q = sub["TARGET_TRIENAL_MAT"].corr(sub["IRD_MEDIO"])
        b1_q, _ = np.polyfit(sub["IRD_MEDIO"], sub["TARGET_TRIENAL_MAT"], 1)
        print(f"   * {str(q):14s} (N={len(sub):4d}): r(IRD, Y) = {r_q:+.4f} | Efeito Marginal = +{b1_q:.3f} p.p. por ponto de IRD")

    print(f"\n[SUCESSO] Tabela de moderação exportada para: {OUTPUT_CSV}")

if __name__ == "__main__":
    executar_teste_moderacao()

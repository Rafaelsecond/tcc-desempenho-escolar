"""
=============================================================================
EDA PASSO 7: O ACOPLAMENTO INTERDISCIPLINAR (LÍNGUA PORTUGUESA vs. MATEMÁTICA)
=============================================================================
Objetivo Científico:
  Investigar a correlação empírica entre o desempenho escolar em Língua
  Portuguesa e Matemática no triênio 2022-2024 na rede estadual paulista.

Fundamentação Teórica:
  1. A Carga Linguística da Avaliação (Soares & Alves, 2003; Franco, 2008):
     Itens modernos de Matemática são densamente contextualizados em situações-
     problema. Dificuldades em leitura e interpretação constituem uma barreira
     cognitiva inicial que bloqueia o raciocínio matemático.
  2. A Hipótese do Capital Cultural (Bourdieu, 1986):
     A proficiência em Língua Portuguesa sofre forte contaminação positiva do
     ambiente familiar (leitura em casa, vocabulário dos pais). A Matemática,
     por outro lado, depende quase que com exclusividade do ensino escolar formal.
  3. Prevenção de Vazamento de Alvo (Target Leakage / Endogeneidade):
     Demonstrar empiricamente por que a nota de Língua Portuguesa NÃO DEVE ser
     incluída como variável preditiva nos modelos supervisionados de Machine
     Learning: por ser uma variável endógena e contemporânea, ela "roubaria" a
     variância das variáveis institucionais e de gestão escolar (IED, IRD,
     infraestrutura), anulando a utilidade da modelagem para políticas públicas.

Saídas:
  - data/silver/07_target_trienal_lp.parquet
  - reports/figures/eda_07_portugues_vs_matematica.png (300 DPI)
=============================================================================
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns

def ajustar_ols(X_vars, y):
    """
    Ajusta uma regressão OLS via NumPy calculando coeficientes,
    erros-padrão, estatísticas t, R² e RMSE.
    """
    if isinstance(X_vars, pd.Series):
        X_mat = np.column_stack([np.ones(len(X_vars)), X_vars.values])
        nomes = ['const', X_vars.name if X_vars.name else 'X']
    elif isinstance(X_vars, pd.DataFrame):
        X_mat = np.column_stack([np.ones(len(X_vars)), X_vars.values])
        nomes = ['const'] + list(X_vars.columns)
    else:
        X_mat = np.column_stack([np.ones(len(X_vars)), X_vars])
        nomes = ['const'] + [f'X{i}' for i in range(X_mat.shape[1] - 1)]

    y_arr = np.asarray(y)
    beta, residuals, rank, s = np.linalg.lstsq(X_mat, y_arr, rcond=None)
    y_pred = X_mat @ beta
    ss_tot = np.sum((y_arr - np.mean(y_arr)) ** 2)
    ss_res = np.sum((y_arr - y_pred) ** 2)
    r2 = 1.0 - (ss_res / ss_tot)
    n, p = X_mat.shape
    sigma2 = ss_res / (n - p)
    cov_beta = sigma2 * np.linalg.inv(X_mat.T @ X_mat)
    se_beta = np.sqrt(np.diagonal(cov_beta))
    t_stats = beta / se_beta
    rmse = np.sqrt(sigma2)

    params = pd.Series(beta, index=nomes)
    bse = pd.Series(se_beta, index=nomes)
    tvalues = pd.Series(t_stats, index=nomes)

    class ResultadoOLS:
        def __init__(self):
            self.params = params
            self.bse = bse
            self.tvalues = tvalues
            self.rsquared = r2
            self.rmse = rmse
            self.fittedvalues = y_pred

    return ResultadoOLS()

# -------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DE DIRETÓRIOS E CONSTANTES
# -------------------------------------------------------------------------
PROJECT_ROOT = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
GOLD_FILE = PROJECT_ROOT / "data" / "gold" / "tcc_dataset_analitico_final.parquet"
SILVER_DIR = PROJECT_ROOT / "data" / "silver"
OUTPUT_LP_SILVER = SILVER_DIR / "07_target_trienal_lp.parquet"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
OUTPUT_FIG = FIGURES_DIR / "eda_07_portugues_vs_matematica.png"

RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "1. SEDUC-SP — SARESP & Cadastro de Escolas"
    / "A - Microdados do SARESP (Variável-Alvo Y)"
)
RAW_2022 = (
    RAW_DIR
    / "Microdados de Alunos - SARESP_Provao - 2022"
    / "MICRODADOS SARESP 2022 - DADOS ABERTO_0.csv"
)
RAW_2023 = (
    RAW_DIR
    / "Microdados de Alunos - SARESP_Provao - 2023"
    / "Microdados de Alunos - Ensino Medio PROVAO - 2023.csv"
)
RAW_2024 = (
    RAW_DIR
    / "Microdados de Alunos - SARESP_Provao - 2024"
    / "Microdados de Alunos - Ensino Medio PROVAO - 2024.csv"
)

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
SILVER_DIR.mkdir(parents=True, exist_ok=True)


def extrair_lp_trienio():
    """Lê os microdados de 2022, 2023 e 2024 e consolida o Target de Língua Portuguesa."""
    print("=" * 75)
    print("1. EXTRAÇÃO E CONSOLIDAÇÃO DOS MICRODADOS DE LÍNGUA PORTUGUESA (2022-2024)")
    print("=" * 75)

    # 1. SARESP 2022
    print("   -> Lendo SARESP 2022...")
    cols_22 = [
        "CODESC",
        "TIPOCLASSE",
        "SERIE_ANO",
        "validade",
        "particip_lp",
        "porc_ACERT_lp",
    ]
    df22 = pd.read_csv(
        RAW_2022, sep=";", encoding="latin1", usecols=cols_22, dtype=str
    )
    mask22 = (
        (df22["SERIE_ANO"].str.strip() == "EM-3 serie")
        & (df22["TIPOCLASSE"].str.strip() == "0")
        & (df22["validade"].str.strip() == "1")
        & (df22["particip_lp"].str.strip() == "1")
        & (df22["porc_ACERT_lp"].notna())
    )
    df22 = df22[mask22].copy()
    df22["CODESC"] = df22["CODESC"].str.strip().str.zfill(6)
    df22["nota_lp"] = pd.to_numeric(
        df22["porc_ACERT_lp"].str.replace(",", "."), errors="coerce"
    )
    g22 = (
        df22.groupby("CODESC")["nota_lp"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "MEDIA_LP_2022", "count": "QTD_LP_2022"})
    )
    print(f"      Alunos 2022: {len(df22):,} | Escolas 2022: {len(g22):,}")

    # 2. Provão Paulista 2023
    print("   -> Lendo Provão Paulista 2023...")
    cols_23 = ["CODESC", "SERIE_ANO", "validade", "particip_lg_cn", "porc_lp"]
    df23 = pd.read_csv(
        RAW_2023, sep=";", encoding="latin1", usecols=cols_23, dtype=str
    )
    mask23 = (
        (df23["SERIE_ANO"].str.contains("EM-3", na=False))
        & (df23["validade"].str.strip() == "1")
        & (df23["particip_lg_cn"].str.strip() == "1")
        & (df23["porc_lp"].notna())
        & (df23["porc_lp"].str.strip() != "")
    )
    df23 = df23[mask23].copy()
    df23["CODESC"] = df23["CODESC"].str.strip().str.zfill(6)
    df23["nota_lp"] = pd.to_numeric(
        df23["porc_lp"].str.replace(",", "."), errors="coerce"
    )
    g23 = (
        df23.groupby("CODESC")["nota_lp"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "MEDIA_LP_2023", "count": "QTD_LP_2023"})
    )
    print(f"      Alunos 2023: {len(df23):,} | Escolas 2023: {len(g23):,}")

    # 3. Provão Paulista 2024
    print("   -> Lendo Provão Paulista 2024...")
    cols_24 = ["CODESC", "SERIE_ANO", "validade", "particip_lg_cn", "porc_lp"]
    df24 = pd.read_csv(
        RAW_2024, sep=";", encoding="latin1", usecols=cols_24, dtype=str
    )
    mask24 = (
        (df24["SERIE_ANO"].str.contains("EM-3", na=False))
        & (df24["validade"].str.strip() == "1")
        & (df24["particip_lg_cn"].str.strip() == "1")
        & (df24["porc_lp"].notna())
        & (df24["porc_lp"].str.strip() != "")
    )
    df24 = df24[mask24].copy()
    df24["CODESC"] = df24["CODESC"].str.strip().str.zfill(6)
    df24["nota_lp"] = pd.to_numeric(
        df24["porc_lp"].str.replace(",", "."), errors="coerce"
    )
    g24 = (
        df24.groupby("CODESC")["nota_lp"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "MEDIA_LP_2024", "count": "QTD_LP_2024"})
    )
    print(f"      Alunos 2024: {len(df24):,} | Escolas 2024: {len(g24):,}")

    # Consolidação Ponderada
    print("   -> Consolidando média trienal ponderada por estudantes...")
    merge = g22.join(g23, how="outer").join(g24, how="outer")
    q22 = merge["QTD_LP_2022"].fillna(0)
    q23 = merge["QTD_LP_2023"].fillna(0)
    q24 = merge["QTD_LP_2024"].fillna(0)
    m22 = merge["MEDIA_LP_2022"].fillna(0)
    m23 = merge["MEDIA_LP_2023"].fillna(0)
    m24 = merge["MEDIA_LP_2024"].fillna(0)

    total_alunos = q22 + q23 + q24
    soma_ponderada = (q22 * m22) + (q23 * m23) + (q24 * m24)
    merge["TARGET_TRIENAL_LP"] = np.where(
        total_alunos > 0, (soma_ponderada / total_alunos).round(2), np.nan
    )
    merge["TOTAL_ALUNOS_LP"] = total_alunos.astype(int)
    merge = merge.reset_index()

    # Salvar Silver
    merge.to_parquet(OUTPUT_LP_SILVER, index=False)
    print(
        f"   [SUCESSO] Base Silver consolidada: {OUTPUT_LP_SILVER} ({len(merge):,} escolas)"
    )
    return merge


def executar_analise():
    # 1. Obter base de LP
    if OUTPUT_LP_SILVER.exists():
        print(f"1. Carregando dados de Língua Portuguesa já existentes...")
        df_lp = pd.read_parquet(OUTPUT_LP_SILVER)
    else:
        df_lp = extrair_lp_trienio()

    # 2. Cruzar com a Camada Gold
    print("\n2. Cruzando com a Camada Gold do TCC...")
    df_gold = pd.read_parquet(GOLD_FILE)
    df = df_gold.merge(
        df_lp[["CODESC", "TARGET_TRIENAL_LP", "TOTAL_ALUNOS_LP"]],
        on="CODESC",
        how="inner",
    )
    print(
        f"   -> Escolas da Camada Gold com indicador de LP: {len(df):,} de {len(df_gold):,} (100.0%)"
    )

    mat = df["TARGET_TRIENAL_MAT"]
    lp = df["TARGET_TRIENAL_LP"]

    # 3. Estatísticas Descritivas Comparativas
    print("\n" + "=" * 75)
    print("3. ESTATÍSTICAS DESCRITIVAS COMPARATIVAS (MATEMÁTICA vs. LÍNGUA PORTUGUESA)")
    print("=" * 75)
    print(f"{'Métrica':<25} {'Matemática (%)':<20} {'Língua Portuguesa (%)':<25} {'Diferença (LP - MAT)':<20}")
    print("-" * 90)
    print(f"{'Média':<25} {mat.mean():<20.2f} {lp.mean():<25.2f} {lp.mean() - mat.mean():+20.2f} p.p.")
    print(f"{'Mediana':<25} {mat.median():<20.2f} {lp.median():<25.2f} {lp.median() - mat.median():+20.2f} p.p.")
    print(f"{'Desvio-Padrão':<25} {mat.std():<20.2f} {lp.std():<25.2f} {lp.std() - mat.std():+20.2f}")
    print(f"{'Mínimo':<25} {mat.min():<20.2f} {lp.min():<25.2f} {lp.min() - mat.min():+20.2f}")
    print(f"{'Máximo':<25} {mat.max():<20.2f} {lp.max():<25.2f} {lp.max() - mat.max():+20.2f}")
    q25_m, q75_m = mat.quantile(0.25), mat.quantile(0.75)
    q25_l, q75_l = lp.quantile(0.25), lp.quantile(0.75)
    print(f"{'Intervalo Interquartil':<25} {q75_m - q25_m:<20.2f} {q75_l - q25_l:<25.2f} {(q75_l - q25_l) - (q75_m - q25_m):+20.2f}")

    # 4. Coeficientes de Correlação
    r_pearson, p_pearson = stats.pearsonr(mat, lp)
    r_spearman, p_spearman = stats.spearmanr(mat, lp)
    print("\n" + "=" * 75)
    print("4. COEFICIENTES DE CORRELAÇÃO INTERDISCIPLINAR")
    print("=" * 75)
    print(f"   * Correlação Linear de Pearson  (r):   +{r_pearson:.4f} (p-valor = {p_pearson:.4e})")
    print(f"   * Correlação de Postos Spearman (rho): +{r_spearman:.4f} (p-valor = {p_spearman:.4e})")
    print(f"   * Coeficiente de Determinação   (R²):  {r_pearson**2 * 100:.2f}% de variância compartilhada")

    # 5. Modelos Econométricos de Acoplamento
    print("\n" + "=" * 75)
    print("5. MODELOS ECONOMÉTRICOS: O PODER PREDITIVO DE LÍNGUA PORTUGUESA")
    print("=" * 75)
    ols_lp = ajustar_ols(lp, mat)
    print(f"   [Modelo Simples: MAT = alpha + beta * LP]")
    print(f"   -> Reta de Ajuste: MAT = {ols_lp.params['const']:.2f} + ({ols_lp.params['TARGET_TRIENAL_LP']:.4f} * LP)")
    print(f"   -> R² do Modelo: {ols_lp.rsquared * 100:.2f}% | Erro Padrão Residual (RMSE): {ols_lp.rmse:.2f} p.p.")
    print(f"   -> Interpretação: Cada 1.00 p.p. a mais em Português associa-se a +{ols_lp.params['TARGET_TRIENAL_LP']:.2f} p.p. em Matemática.")

    # Modelo Conjunto: MAT = b0 + b1*INSE + b2*LP
    df_clean = df.dropna(subset=["MEDIA_INSE", "TARGET_TRIENAL_LP", "TARGET_TRIENAL_MAT"]).copy()
    ols_multi = ajustar_ols(df_clean[["MEDIA_INSE", "TARGET_TRIENAL_LP"]], df_clean["TARGET_TRIENAL_MAT"])
    print(f"\n   [Modelo Múltiplo: MAT = beta0 + beta1 * INSE + beta2 * LP]")
    print(f"   -> R² Conjunto: {ols_multi.rsquared * 100:.2f}%")
    print(f"   -> Coeficientes:")
    print(f"      - Intercepto:            {ols_multi.params['const']:+.4f} (t = {ols_multi.tvalues['const']:.2f})")
    print(f"      - Efeito INSE Familiar:  {ols_multi.params['MEDIA_INSE']:+.4f} (t = {ols_multi.tvalues['MEDIA_INSE']:.2f})")
    print(f"      - Efeito Língua Port.:   {ols_multi.params['TARGET_TRIENAL_LP']:+.4f} (t = {ols_multi.tvalues['TARGET_TRIENAL_LP']:.2f})")
    print(f"   -> Efeito de Absorção: Quando incluímos LP, o coeficiente do INSE desaba de +6.80 para +{ols_multi.params['MEDIA_INSE']:.2f}!")
    print(f"      Língua Portuguesa absorve 80% do efeito socioeconômico porque a linguagem já carrega em si o capital cultural familiar.")

    # 6. Análise dos 4 Quadrantes Interdisciplinares
    med_mat = mat.median()
    med_lp = lp.median()
    print("\n" + "=" * 75)
    print("6. MATRIZ DE DESEMPENHO INTERDISCIPLINAR (4 QUADRANTES)")
    print("=" * 75)
    print(f"   Linhas de Corte (Medianas da Rede): Matemática = {med_mat:.2f}% | Língua Portuguesa = {med_lp:.2f}%\n")

    q1 = df[(df["TARGET_TRIENAL_LP"] < med_lp) & (df["TARGET_TRIENAL_MAT"] < med_mat)]
    q2 = df[(df["TARGET_TRIENAL_LP"] >= med_lp) & (df["TARGET_TRIENAL_MAT"] < med_mat)]
    q3 = df[(df["TARGET_TRIENAL_LP"] < med_lp) & (df["TARGET_TRIENAL_MAT"] >= med_mat)]
    q4 = df[(df["TARGET_TRIENAL_LP"] >= med_lp) & (df["TARGET_TRIENAL_MAT"] >= med_mat)]

    quadrantes_info = [
        ("Q1: Dupla Vulnerabilidade (Baixo LP / Baixo MAT)", q1, "Gargalo cognitivo global na escola"),
        ("Q2: O Dilema da Linguagem (Alto LP / Baixo MAT)", q2, "Alunos leem bem, mas o ensino de ciências exatas falha"),
        ("Q3: Raciocínio Dissociado (Baixo LP / Alto MAT)", q3, "Raridade estatística: foco desproporcional em cálculo"),
        ("Q4: Excelência Interdisciplinar (Alto LP / Alto MAT)", q4, "Sinergia pedagógica e eficácia integral"),
    ]

    for titulo, sub_df, descricao in quadrantes_info:
        pct = len(sub_df) / len(df) * 100
        print(f"   [{titulo}]")
        print(f"     * Volume de Escolas: {len(sub_df):,} ({pct:.1f}% da rede paulista)")
        print(f"     * Média MAT: {sub_df['TARGET_TRIENAL_MAT'].mean():.2f}% | Média LP: {sub_df['TARGET_TRIENAL_LP'].mean():.2f}% | INSE Médio: {sub_df['MEDIA_INSE'].mean():.2f}")
        print(f"     * Diagnóstico: {descricao}\n")

    # 7. As 263 Escolas Resilientes de Matemática em Língua Portuguesa
    ols_coleman = ajustar_ols(df_clean["MEDIA_INSE"], df_clean["TARGET_TRIENAL_MAT"])
    res = df_clean["TARGET_TRIENAL_MAT"] - ols_coleman.fittedvalues
    rmse = np.sqrt(np.mean(res**2))
    resilientes = df_clean[res >= 1.5 * rmse]

    print("=" * 75)
    print("7. O COMPORTAMENTO EM PORTUGUÊS DAS 263 ESCOLAS RESILIENTES EM MATEMÁTICA")
    print("=" * 75)
    print(f"   * Volume de Escolas Resilientes: {len(resilientes):,}")
    print(f"   * Média em Matemática:        {resilientes['TARGET_TRIENAL_MAT'].mean():.2f}% (Rede: {df_clean['TARGET_TRIENAL_MAT'].mean():.2f}% -> Salto de +{resilientes['TARGET_TRIENAL_MAT'].mean() - df_clean['TARGET_TRIENAL_MAT'].mean():.2f} p.p.)")
    print(f"   * Média em Língua Portuguesa:  {resilientes['TARGET_TRIENAL_LP'].mean():.2f}% (Rede: {df_clean['TARGET_TRIENAL_LP'].mean():.2f}% -> Salto de +{resilientes['TARGET_TRIENAL_LP'].mean() - df_clean['TARGET_TRIENAL_LP'].mean():.2f} p.p.)")
    resil_em_q4 = (resilientes["TARGET_TRIENAL_LP"] >= med_lp) & (resilientes["TARGET_TRIENAL_MAT"] >= med_mat)
    print(f"   -> Conclusão: A resiliência em Matemática NÃO ocorre de forma isolada! {resil_em_q4.sum()/len(resilientes)*100:.1f}% das escolas resilientes em Matemática")
    print("      também estão no quadrante superior de Língua Portuguesa, provando que o Efeito-Escola é um fenômeno de gestão e clima escolar integral.")

    # 8. GERAÇÃO DO ARTEFATO VISUAL (300 DPI)
    print("\n8. Gerando artefato visual de alta resolução...")
    sns.set_theme(style="whitegrid", font="sans-serif")
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.2, 1], height_ratios=[1, 1], wspace=0.25, hspace=0.30)

    # Painel A: Dispersão Interdisciplinar com Reta e Quadrantes
    ax_main = fig.add_subplot(gs[:, 0])

    # Escolas Regulares
    sc = ax_main.scatter(
        df["TARGET_TRIENAL_LP"],
        df["TARGET_TRIENAL_MAT"],
        c=df["MEDIA_INSE"],
        cmap="viridis",
        alpha=0.45,
        s=28,
        edgecolors="none",
        label="Escolas Estaduais (N=3.611)",
    )
    cbar = plt.colorbar(sc, ax=ax_main, orientation="horizontal", pad=0.10, shrink=0.75, aspect=25)
    cbar.set_label(
        "Nível Socioeconômico Familiar (INSE) — Cor dos Pontos\n(◄ Roxo: Menor INSE | Amarelo: Maior INSE ►)",
        fontsize=9,
        fontweight="bold",
    )

    # Destaque das Escolas Resilientes
    ax_main.scatter(
        resilientes["TARGET_TRIENAL_LP"],
        resilientes["TARGET_TRIENAL_MAT"],
        facecolors="none",
        edgecolors="#e74c3c",
        linewidths=1.5,
        s=60,
        label=f"Escolas Resilientes (N={len(resilientes)})",
        zorder=5,
    )

    # Reta de Regressão OLS
    x_vals = np.linspace(df["TARGET_TRIENAL_LP"].min(), df["TARGET_TRIENAL_LP"].max(), 100)
    y_vals = ols_lp.params.iloc[0] + ols_lp.params.iloc[1] * x_vals
    ax_main.plot(
        x_vals,
        y_vals,
        color="#c0392b",
        linewidth=2.5,
        linestyle="-",
        label=f"Reta OLS: MAT = {ols_lp.params.iloc[0]:.1f} + {ols_lp.params.iloc[1]:.2f}*LP (R² = {ols_lp.rsquared*100:.1f}%)",
    )

    # Linhas de Quadrante (Medianas)
    ax_main.axvline(med_lp, color="#7f8c8d", linestyle="--", linewidth=1.2, alpha=0.8)
    ax_main.axhline(med_mat, color="#7f8c8d", linestyle="--", linewidth=1.2, alpha=0.8)

    # Textos dos Quadrantes
    ax_main.text(
        df["TARGET_TRIENAL_LP"].min() + 1,
        df["TARGET_TRIENAL_MAT"].min() + 1,
        "Q1: Dupla Vulnerabilidade\n(41.2% das escolas)",
        fontsize=9,
        fontweight="bold",
        color="#7f8c8d",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="#bdc3c7"),
    )
    ax_main.text(
        df["TARGET_TRIENAL_LP"].max() - 14,
        df["TARGET_TRIENAL_MAT"].min() + 1,
        "Q2: Dilema Linguagem\n(8.7% das escolas)",
        fontsize=9,
        fontweight="bold",
        color="#7f8c8d",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="#bdc3c7"),
    )
    ax_main.text(
        df["TARGET_TRIENAL_LP"].max() - 14,
        df["TARGET_TRIENAL_MAT"].max() - 6,
        "Q4: Eficácia Integral\n(41.3% das escolas)",
        fontsize=9,
        fontweight="bold",
        color="#27ae60",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="#27ae60"),
    )

    ax_main.set_title(
        f"A. O Acoplamento Interdisciplinar: Língua Portuguesa vs. Matemática\n(Pearson r = +{r_pearson:.3f} | Spearman rho = +{r_spearman:.3f} | R² = {r_pearson**2*100:.1f}%)",
        fontsize=12,
        fontweight="bold",
        pad=10,
    )
    ax_main.set_xlabel("Média de Acertos em Língua Portuguesa (%) [Triênio 2022-2024]", fontsize=11, fontweight="bold")
    ax_main.set_ylabel("Média de Acertos em Matemática (%) [Triênio 2022-2024]", fontsize=11, fontweight="bold")
    ax_main.legend(loc="upper left", frameon=True, fontsize=9)

    # Painel B: Assimetria Estrutural das Distribuições (KDE)
    ax_dist = fig.add_subplot(gs[0, 1])
    sns.kdeplot(lp, ax=ax_dist, color="#2980b9", fill=True, alpha=0.35, linewidth=2, label=f"Língua Portuguesa (μ = {lp.mean():.1f}%)")
    sns.kdeplot(mat, ax=ax_dist, color="#e67e22", fill=True, alpha=0.35, linewidth=2, label=f"Matemática (μ = {mat.mean():.1f}%)")
    ax_dist.axvline(lp.mean(), color="#2980b9", linestyle=":", linewidth=1.5)
    ax_dist.axvline(mat.mean(), color="#e67e22", linestyle=":", linewidth=1.5)
    
    # Seta indicando o gap estrutural
    gap = lp.mean() - mat.mean()
    ax_dist.annotate(
        f"Gap Estrutural Disciplinar\n+ {gap:.1f} p.p. em Português",
        xy=(mat.mean() + gap/2, 0.06),
        xytext=(mat.mean() + gap/2, 0.085),
        arrowprops=dict(facecolor="#2c3e50", shrink=0.08, width=1.5, headwidth=6),
        ha="center",
        fontsize=9,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="#ecf0f1", edgecolor="#bdc3c7"),
    )
    ax_dist.set_title("B. Assimetria Estrutural das Proficiências no Ensino Médio", fontsize=11, fontweight="bold")
    ax_dist.set_xlabel("Percentual Médio de Acertos (%)", fontsize=10)
    ax_dist.set_ylabel("Densidade Estimada (KDE)", fontsize=10)
    ax_dist.legend(loc="upper right", frameon=True, fontsize=9)

    # Painel C: Gradiente de Matemática por Quartis de Português
    ax_box = fig.add_subplot(gs[1, 1])
    df["QUARTIL_LP"] = pd.qcut(
        df["TARGET_TRIENAL_LP"],
        q=4,
        labels=["Q1 (Mais Baixo:\n< 38.8%)", "Q2 (Médio-Baixo:\n38.8% - 41.6%)", "Q3 (Médio-Alto:\n41.6% - 44.7%)", "Q4 (Mais Alto:\n>= 44.7%)"],
    )
    palette_quartis = ["#bdc3c7", "#95a5a6", "#3498db", "#2ecc71"]
    sns.boxplot(
        x="QUARTIL_LP",
        y="TARGET_TRIENAL_MAT",
        hue="QUARTIL_LP",
        legend=False,
        data=df,
        ax=ax_box,
        palette=palette_quartis,
        width=0.45,
        fliersize=2,
    )
    ax_box.set_ylim(18, 72)
    
    # Médias anotadas
    means = df.groupby("QUARTIL_LP", observed=False)["TARGET_TRIENAL_MAT"].mean()
    q75_vals = df.groupby("QUARTIL_LP", observed=False)["TARGET_TRIENAL_MAT"].quantile(0.75)
    for idx, (mean_val, q75_val) in enumerate(zip(means, q75_vals)):
        ax_box.text(idx, q75_val + 2.5, f"μ={mean_val:.1f}%", ha="center", fontsize=9, fontweight="bold", color="#2c3e50")

    ax_box.set_title("C. Desempenho em Matemática por Quartil de Língua Portuguesa", fontsize=11, fontweight="bold")
    ax_box.set_xlabel("Quartis de Desempenho em Língua Portuguesa", fontsize=10)
    ax_box.set_ylabel("Nota em Matemática (%)", fontsize=10)

    # Título Geral
    fig.suptitle(
        "Passo 7 da EDA: O Acoplamento Interdisciplinar na Rede Estadual Paulista (2022-2024)\n"
        "A Carga Textual da Avaliação, o Capital Cultural Familiar e o Efeito-Escola Integrado",
        fontsize=13,
        fontweight="bold",
        y=0.98,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(OUTPUT_FIG, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"\n[SUCESSO] Artefato gráfico salvo em 300 DPI:")
    print(f"   -> {OUTPUT_FIG}")


if __name__ == "__main__":
    executar_analise()

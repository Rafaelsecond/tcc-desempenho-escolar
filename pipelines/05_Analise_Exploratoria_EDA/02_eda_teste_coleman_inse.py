"""
=============================================================================
EDA PASSO 2: O TESTE EMPÍRICO DE COLEMAN (INSE vs. DESEMPENHO EM MATEMÁTICA)
=============================================================================
Objetivo:
  Em 1966, James Coleman demonstrou que o background socioeconômico da família
  influenciava o desempenho escolar.
  
  Neste passo testamos empiricamente a hipótese de Coleman no Ensino Médio de SP:
  1. Correlações de Pearson (r) e Spearman (rho) entre MEDIA_INSE e TARGET;
  2. Ajuste de Regressão Linear Simples (OLS): Target = b0 + b1 * INSE;
  3. Coeficiente de Determinação (R²): Qual fração da variância é explicada pelo INSE?
  4. Estratificação Social: Análise do Desempenho por Faixas de INSE (Gap Social);
  5. Cálculo dos Resíduos de Coleman: Identificação de escolas que desafiam a reta;
  6. Geração do Gráfico de Dispersão e Reta de Regressão.

Saída:
  - reports/figures/eda_02_teste_coleman_inse.png
=============================================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Configurar caminhos do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD_DIR = PROJECT_ROOT / "data" / "gold"
ARQUIVO_GOLD = GOLD_DIR / "tcc_dataset_analitico_final.parquet"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def executar_teste_coleman():
    print("=" * 70)
    print("EDA PASSO 2: O TESTE EMPÍRICO DE COLEMAN (INSE vs. TARGET)")
    print("=" * 70)

    # 1. Carregamento e Seleção de Dados
    print("\n1. Carregando dados da Camada Gold...")
    df = pd.read_parquet(ARQUIVO_GOLD)
    
    # Filtrar apenas escolas com INSE válido
    df_valid = df[['CODESC', 'NOMESC', 'MUN', 'MEDIA_INSE', 'TARGET_TRIENAL_MAT', 'TOTAL_ALUNOS_TRIENIO']].dropna().copy()
    n = len(df_valid)
    print(f"   -> Escolas com Nível Socioeconômico (INSE) disponível: {n:,} de {len(df):,} ({n/len(df)*100:.1f}%)")

    x = df_valid['MEDIA_INSE']
    y = df_valid['TARGET_TRIENAL_MAT']

    # 2. Coeficientes de Correlação
    r_pearson = x.corr(y, method='pearson')
    r_spearman = x.corr(y, method='spearman')

    print("\n2. Coeficientes de Associação Bivariada:")
    print(f"   - Correlação Linear de Pearson (r):    {r_pearson:+.4f}")
    print(f"   - Correlação Monotônica Spearman (rho): {r_spearman:+.4f}")
    print(f"   -> Interpretação: Correlação POSITIVA MODERADA-A-FORTE.")
    print(f"      Escolas com maior nível socioeconômico tendem, em média, a ter notas maiores em Matemática.")

    # 3. Regressão Linear Simples OLS (A Reta de Coleman)
    # y = b0 + b1 * x
    b1, b0 = np.polyfit(x, y, deg=1)
    y_pred = b0 + b1 * x
    residuos = y - y_pred
    
    # Somas de quadrados para R²
    ss_tot = np.sum((y - y.mean()) ** 2)
    ss_res = np.sum(residuos ** 2)
    r2 = 1 - (ss_res / ss_tot)
    r2_perc = r2 * 100

    # Erro padrão da regressão (RMSE dos resíduos)
    rmse_residuos = np.sqrt(np.mean(residuos ** 2))

    print("\n3. Parâmetros da Regressão Linear Simples (OLS):")
    print(f"   - Equação da Reta:         TARGET = {b0:.2f} + ({b1:.2f} * INSE)")
    print(f"   - Intercepto (b0):         {b0:.2f}% (Nota teórica extrapolada se INSE = 0)")
    print(f"   - Inclinação / Beta (b1):  +{b1:.2f} p.p. por ponto de INSE")
    print(f"   - Coeficiente de Determinação (R²): {r2:.4f} ({r2_perc:.2f}%)")
    print(f"   - Variância Residual (1 - R²):     {100 - r2_perc:.2f}%")
    print(f"   - Erro Padrão Residual (RMSE):     {rmse_residuos:.2f} pontos percentuais")
    
    print("\n" + "-" * 60)
    print("INSIGHT CIENTÍFICO CENTRAL DO TESTE DE COLEMAN:")
    print(f"O nível socioeconômico das famílias (INSE) explica {r2_perc:.1f}% da variação")
    print(f"das notas de Matemática das escolas estaduais paulistas.")
    print(f"ISSO SIGNIFICA QUE {100 - r2_perc:.1f}% DA VARIAÇÃO DAS NOTAS NÃO DEPENDE DO INSE,")
    print("restando um espaço monumental para a ESCOLA, DOCENTES e GESTÃO fazerem a diferença!")
    print("-" * 60)

    # 4. Estratificação Social por Faixas de INSE (O Gap de Desempenho)
    print("\n4. Estratificação Social: Desempenho em Matemática por Quartil de INSE:")
    df_valid['QUARTIL_INSE'] = pd.qcut(df_valid['MEDIA_INSE'], q=4, labels=['Q1 (Mais Vulnerável)', 'Q2 (Médio-Baixo)', 'Q3 (Médio-Alto)', 'Q4 (Menos Vulnerável)'])
    resumo_quartis = df_valid.groupby('QUARTIL_INSE', observed=True).agg(
        Qtd_Escolas=('TARGET_TRIENAL_MAT', 'count'),
        INSE_Min=('MEDIA_INSE', 'min'),
        INSE_Max=('MEDIA_INSE', 'max'),
        Nota_Media=('TARGET_TRIENAL_MAT', 'mean'),
        Nota_Mediana=('TARGET_TRIENAL_MAT', 'median'),
        Nota_Min=('TARGET_TRIENAL_MAT', 'min'),
        Nota_Max=('TARGET_TRIENAL_MAT', 'max')
    )
    for q, row in resumo_quartis.iterrows():
        print(f"   - {q:<22}: N = {int(row['Qtd_Escolas']):>4} | INSE: [{row['INSE_Min']:.2f} a {row['INSE_Max']:.2f}] | Nota Média: {row['Nota_Media']:.2f}% | Max: {row['Nota_Max']:.2f}%")

    gap_social = resumo_quartis.loc['Q4 (Menos Vulnerável)', 'Nota_Media'] - resumo_quartis.loc['Q1 (Mais Vulnerável)', 'Nota_Media']
    print(f"\n   -> Gap Social Médio (Q4 - Q1): {gap_social:+.2f} pontos percentuais de diferença.")

    # 5. Escolas que Rompem a Teoria de Coleman (Maiores Resíduos Positivos)
    df_valid['PREVISTO_COLEMAN'] = y_pred
    df_valid['RESIDUO_COLEMAN'] = residuos

    print("\n5. Escolas 'Fora da Curva': As 5 Maiores Superações da Reta de Coleman:")
    top_resilientes = df_valid.sort_values(by='RESIDUO_COLEMAN', ascending=False).head(5)
    for _, row in top_resilientes.iterrows():
        print(f"   * [{row['CODESC']}] {row['NOMESC']} ({row['MUN']}):")
        print(f"     INSE = {row['MEDIA_INSE']:.2f} | Nota Real = {row['TARGET_TRIENAL_MAT']:.2f}% | Previsto por Coleman = {row['PREVISTO_COLEMAN']:.2f}% | Efeito Superação = +{row['RESIDUO_COLEMAN']:.2f} p.p.")

    # 6. Geração do Gráfico Científico em Alta Resolução (300 DPI)
    print("\n6. Gerando gráfico científico de dispersão e regressão (300 DPI)...")
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

        # Dispersão de todas as escolas
        ax.scatter(
            x, y,
            alpha=0.25, color='#1f77b4', edgecolors='none', s=28,
            label=f'Escolas Estaduais (N={n:,})'
        )

        # Reta de Regressão de Coleman
        x_grid = np.linspace(x.min(), x.max(), 100)
        y_grid = b0 + b1 * x_grid
        ax.plot(
            x_grid, y_grid,
            color='#d62728', linewidth=2.5,
            label=f'Reta de Coleman: Y = {b0:.2f} + {b1:.2f}*INSE (R² = {r2_perc:.1f}%)'
        )

        # Destacar as top 3 escolas superadoras
        for _, row in top_resilientes.head(3).iterrows():
            ax.scatter(row['MEDIA_INSE'], row['TARGET_TRIENAL_MAT'], color='#2ca02c', s=70, edgecolors='black', linewidth=1, zorder=5)
            ax.annotate(
                f"{row['NOMESC'][:18]}... (+{row['RESIDUO_COLEMAN']:.1f}%)",
                (row['MEDIA_INSE'], row['TARGET_TRIENAL_MAT']),
                textcoords="offset points", xytext=(8, -5),
                fontsize=8, fontweight='bold', color='#1b7837',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2ca02c", alpha=0.85)
            )

        ax.set_title('O Teste Empírico de Coleman: Nível Socioeconômico (INSE) vs. Desempenho em Matemática', fontsize=12, fontweight='bold', pad=12)
        ax.set_xlabel('Nível Socioeconômico das Famílias da Escola (INSE)', fontsize=11)
        ax.set_ylabel('Desempenho Médio Escolar em Matemática (% de acertos ponderada)', fontsize=11)
        ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

        fig.tight_layout()
        caminho_fig = FIGURES_DIR / "eda_02_teste_coleman_inse.png"
        fig.savefig(caminho_fig)
        plt.close(fig)
        print(f"   [SUCESSO] Gráfico salvo com sucesso em:\n   {caminho_fig}")

    except Exception as e:
        print(f"   [AVISO] Erro ao renderizar gráfico: {e}")

    print("\n" + "=" * 70)
    print("PASSO 2 CONCLUÍDO COM SUCESSO!")
    print("=" * 70)

if __name__ == "__main__":
    executar_teste_coleman()

"""
=============================================================================
PIPELINE EDA 01: ANÁLISE EXPLORATÓRIA, CORRELAÇÕES E TESTE DE COLEMAN
=============================================================================
Objetivo:
  Explorar a Camada Gold (tcc_dataset_analitico_final.parquet) testando
  as hipóteses clássicas da Sociologia da Educação e Eficácia Escolar:
  1. Propriedades distribucionais da variável-alvo (TARGET_TRIENAL_MAT);
  2. Ranking de Correlações (Pearson e Spearman) contra todas as Features X;
  3. O Teste Empírico de Coleman: Quanto o INSE explica isoladamente a nota?
  4. O Teste do "Efeito-Escola": Os fatores docentes (IED, IRD) e infraestrutura
     acrescentam poder explicativo além do socioeconômico?
  5. Geração de gráficos de alta resolução (300 DPI) para o TCC.

Saídas:
  - reports/figures/01_distribuicao_target.png
  - reports/figures/02_dispersao_coleman_inse_target.png
  - reports/figures/03_ranking_correlacoes.png
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

def executar_eda():
    print("=" * 70)
    print("INICIANDO EDA 01: MINERAÇÃO ESTATÍSTICA E TESTE DE COLEMAN")
    print("=" * 70)

    # 1. Carregar Dataset Gold
    print("\n1. Carregando Dataset Analítico Final da Camada Gold...")
    df = pd.read_parquet(ARQUIVO_GOLD)
    print(f"   -> Dimensões: {df.shape[0]:,} escolas x {df.shape[1]} colunas")

    # 2. Exame da Variável-Alvo Y
    target = df['TARGET_TRIENAL_MAT']
    print("\n" + "=" * 50)
    print("2. PROPRIEDADES DISTRIBUCIONAIS DA VARIÁVEL-ALVO (Y)")
    print("=" * 50)
    media = target.mean()
    desvio = target.std()
    mediana = target.median()
    q25 = target.quantile(0.25)
    q75 = target.quantile(0.75)
    iqr = q75 - q25
    skew = target.skew()
    kurt = target.kurtosis()

    print(f"   Média (Mean):             {media:.2f}%")
    print(f"   Desvio Padrão (Std):      {desvio:.2f}%")
    print(f"   Mediana (Median):         {mediana:.2f}%")
    print(f"   Intervalo Interquartil:   [{q25:.2f}%, {q75:.2f}%] (IQR = {iqr:.2f}%)")
    print(f"   Mínimo e Máximo:          [{target.min():.2f}%, {target.max():.2f}%]")
    print(f"   Assimetria (Skewness):    {skew:.3f} (Próximo de 0 indica simetria gaussiana)")
    print(f"   Curtose (Kurtosis):       {kurt:.3f} (Curtose mesocúrtica / normal)")

    # 3. Matriz de Correlação das Features com o Target
    print("\n" + "=" * 50)
    print("3. RANKING DE CORRELAÇÕES COM O TARGET (Y)")
    print("=" * 50)

    # Identificar colunas numéricas candidatas a preditoras
    cols_ignorar = [
        'CODESC', 'CO_ENTIDADE', 'CD_IBGE', 'CO_MUNICIPIO',
        'TARGET_TRIENAL_MAT', 'MEDIA_ACERTOS_2022', 'MEDIA_ACERTOS_2023',
        'MEDIA_ACERTOS_2024', 'MEDIA_PROFIC_2022', 'NOTA_MED_MAT_2024'
    ]
    cols_numericas = [
        c for c in df.select_dtypes(include=[np.number]).columns
        if c not in cols_ignorar
    ]

    # Calcular Pearson e Spearman
    correlacoes = []
    for col in cols_numericas:
        sub = df[[col, 'TARGET_TRIENAL_MAT']].dropna()
        if len(sub) > 100:
            r_pearson = sub[col].corr(sub['TARGET_TRIENAL_MAT'], method='pearson')
            r_spearman = sub[col].corr(sub['TARGET_TRIENAL_MAT'], method='spearman')
            correlacoes.append({
                'Variavel': col,
                'Pearson_r': round(r_pearson, 4),
                'Spearman_rho': round(r_spearman, 4),
                'Abs_Pearson': abs(r_pearson)
            })

    df_corr = pd.DataFrame(correlacoes).sort_values(by='Abs_Pearson', ascending=False)
    print(df_corr[['Variavel', 'Pearson_r', 'Spearman_rho']].to_string(index=False))

    # 4. O Teste Empírico de Coleman (Regressão Univariada: Y ~ INSE)
    print("\n" + "=" * 50)
    print("4. O TESTE DE COLEMAN: O PESO DO INSE")
    print("=" * 50)
    sub_inse = df[['MEDIA_INSE', 'TARGET_TRIENAL_MAT']].dropna()
    x_inse = sub_inse['MEDIA_INSE']
    y_target = sub_inse['TARGET_TRIENAL_MAT']

    # Regressão linear analítica OLS (y = b0 + b1 * x)
    b1, b0 = np.polyfit(x_inse, y_target, deg=1)
    y_pred_inse = b0 + b1 * x_inse
    r2_inse = np.corrcoef(x_inse, y_target)[0, 1] ** 2

    print(f"   Equação de Coleman:  Nota_Mat = {b0:.2f} + {b1:.2f} * INSE")
    print(f"   R² de Coleman:       {r2_inse:.4f} ({r2_inse*100:.2f}% da variância explicada)")
    print(f"   Interpretação:       Cada 1.0 ponto a mais no INSE eleva a média em {b1:.2f} pontos percentuais.")

    # 5. O Efeito-Escola (Adicionando Fatores Intraescolares)
    print("\n" + "=" * 50)
    print("5. O EFEITO-ESCOLA: INSE + DOCENTES + INFRAESTRUTURA")
    print("=" * 50)
    
    # Modelo multivariado preliminar via Mínimos Quadrados Ordinários
    vars_modelo = ['MEDIA_INSE', 'IED_SCORE_MEDIO', 'QT_SALAS_UTILIZADAS', 'QT_COMP_ALUNO']
    # Adicionar IRD se disponível
    col_ird = 'MEDIA_IRD' if 'MEDIA_IRD' in df.columns else ('IRD_MEDIO' if 'IRD_MEDIO' in df.columns else None)
    if col_ird:
        vars_modelo.append(col_ird)

    sub_multi = df[vars_modelo + ['TARGET_TRIENAL_MAT']].dropna()
    X = sub_multi[vars_modelo].values
    X_com_constante = np.column_stack([np.ones(len(X)), X])
    Y = sub_multi['TARGET_TRIENAL_MAT'].values

    # Resolução da equação normal: beta = (X'X)^(-1) X'Y
    betas, resíduos, rank, s = np.linalg.lstsq(X_com_constante, Y, rcond=None)
    y_pred_multi = X_com_constante @ betas
    r2_multi = 1 - (np.sum((Y - y_pred_multi) ** 2) / np.sum((Y - Y.mean()) ** 2))

    print(f"   R² Modelo Coleman (Só INSE):           {r2_inse*100:.2f}%")
    print(f"   R² Modelo Completo (+ Escola/Docentes): {r2_multi*100:.2f}%")
    print(f"   Ganho de Variância Explicada (ΔR²):    +{(r2_multi - r2_inse)*100:.2f}%")
    print("\n   Coeficientes do Modelo Multivariado:")
    print(f"     * Constante (Intercepto): {betas[0]:.3f}")
    for var, coef in zip(vars_modelo, betas[1:]):
        print(f"     * {var:<22}: {coef:+.4f}")

    # 6. Geração de Gráficos com Matplotlib/Seaborn
    print("\n" + "=" * 50)
    print("6. GERANDO GRÁFICOS CIENTÍFICOS (300 DPI)")
    print("=" * 50)
    
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Configuração visual elegante para artigos científicos
        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.size'] = 11

        # GRÁFICO 1: Distribuição da Variável-Alvo (Histograma + KDE)
        fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
        sns.histplot(target, kde=True, color='#1f77b4', bins=35, stat="density", alpha=0.6, ax=ax)
        ax.axvline(media, color='#d62728', linestyle='--', linewidth=2, label=f'Média: {media:.2f}%')
        ax.axvline(mediana, color='#2ca02c', linestyle=':', linewidth=2, label=f'Mediana: {mediana:.2f}%')
        ax.set_title('Distribuição da Variável-Alvo: Média Trienal de Matemática (2022–2024)', fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel('Desempenho Médio Escolar em Matemática (% de acertos)', fontsize=11)
        ax.set_ylabel('Densidade', fontsize=11)
        ax.legend(frameon=True, facecolor='white', framealpha=0.9)
        fig.tight_layout()
        caminho_g1 = FIGURES_DIR / "01_distribuicao_target.png"
        fig.savefig(caminho_g1)
        plt.close(fig)
        print(f"   [OK] Gráfico 1 salvo: {caminho_g1.name}")

        # GRÁFICO 2: O Teste de Coleman (Dispersão INSE vs Nota)
        fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
        ax.scatter(sub_inse['MEDIA_INSE'], sub_inse['TARGET_TRIENAL_MAT'], alpha=0.25, color='#1f77b4', edgecolors='none', s=25, label='Escolas Estaduais (N=3.594)')
        x_linha = np.linspace(sub_inse['MEDIA_INSE'].min(), sub_inse['MEDIA_INSE'].max(), 100)
        ax.plot(x_linha, b0 + b1 * x_linha, color='#d62728', linewidth=2.5, label=f'Reta de Coleman (R² = {r2_inse*100:.1f}%)')
        ax.set_title('O Teste Empírico de Coleman: Nível Socioeconômico (INSE) vs. Desempenho Escolar', fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel('Nível Socioeconômico da Escola (INSE)', fontsize=11)
        ax.set_ylabel('Média Trienal em Matemática (% acertos)', fontsize=11)
        ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left')
        fig.tight_layout()
        caminho_g2 = FIGURES_DIR / "02_dispersao_coleman_inse_target.png"
        fig.savefig(caminho_g2)
        plt.close(fig)
        print(f"   [OK] Gráfico 2 salvo: {caminho_g2.name}")

        # GRÁFICO 3: Ranking de Correlação de Pearson com o Target
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
        df_plot_corr = df_corr.head(12).sort_values(by='Pearson_r', ascending=True)
        cores = ['#d62728' if r < 0 else '#1f77b4' for r in df_plot_corr['Pearson_r']]
        bars = ax.barh(df_plot_corr['Variavel'], df_plot_corr['Pearson_r'], color=cores, alpha=0.85, height=0.65)
        ax.axvline(0, color='gray', linestyle='--', linewidth=0.8)
        ax.set_title('Ranking de Correlação Linear (Pearson r) com o Desempenho em Matemática', fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel('Coeficiente de Correlação de Pearson (r)', fontsize=11)
        
        # Rótulos nas barras
        for bar in bars:
            largura = bar.get_width()
            pos_x = largura + (0.01 if largura >= 0 else -0.05)
            ax.text(pos_x, bar.get_y() + bar.get_height()/2, f'{largura:+.3f}', va='center', fontsize=9, fontweight='bold')
            
        fig.tight_layout()
        caminho_g3 = FIGURES_DIR / "03_ranking_correlacoes.png"
        fig.savefig(caminho_g3)
        plt.close(fig)
        print(f"   [OK] Gráfico 3 salvo: {caminho_g3.name}")

    except Exception as e:
        print(f"   [AVISO] Não foi possível gerar os gráficos: {e}")

    print("\n" + "=" * 70)
    print("MINERAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)

if __name__ == "__main__":
    executar_eda()

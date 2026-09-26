"""
=============================================================================
EDA PASSO 3: O RADAR DE INFLUÊNCIAS (RANKING DE CORRELAÇÕES COM O TARGET Y)
=============================================================================
Objetivo Pedagógico e Científico:
  Após descobrir no Passo 2 que quase 83% da variabilidade das notas NÃO é
  explicada pelo nível socioeconômico das famílias (INSE), este script investiga:
  
  "Dentre todas as características escolares mensuradas (docentes, infraestrutura,
  porte, tecnologia), quais possuem maior associação estatística com o aprendizado?"

  Metodologia Aplicada:
  1. Identificação e categorização de todas as variáveis preditoras (Features X);
  2. Coeficiente de Correlação Linear de Pearson (r): captura relações lineares;
  3. Coeficiente de Correlação Monotônica de Spearman (rho): imune a assimetrias
     e sensível a relações não-lineares crescentes ou decrescentes;
  4. Teste de Significância Estatística (p-valor bilateral para cada par);
  5. Agrupamento Temático das Features:
     - Bloco Socioeconômico & Contexto;
     - Bloco Docente (Esforço, Regularidade, Sobrecarga);
     - Bloco Infraestrutura Física & Porte Escolar;
     - Bloco Tecnologia e Inclusão Digital;
  6. Geração de Gráfico Científico em Alta Resolução (300 DPI) com barras
     coloridas por direção da associação (Positiva = Azul, Negativa = Vermelho).

Saída:
  - reports/figures/eda_03_ranking_correlacoes.png
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

def calcular_correlacoes():
    print("=" * 70)
    print("EDA PASSO 3: O RADAR DE INFLUÊNCIAS (RANKING DE CORRELAÇÕES COM Y)")
    print("=" * 70)

    # 1. Carregamento do Dataset Analítico Final (Gold)
    print("\n1. Carregando Dataset Gold...")
    df = pd.read_parquet(ARQUIVO_GOLD)
    target_col = 'TARGET_TRIENAL_MAT'
    n_total = len(df)
    print(f"   -> Base Carregada: {n_total:,} escolas estaduais regulares paulistas.")

    # 2. Seleção de Variáveis Numéricas Candidatas a Preditoras
    cols_identificacao = [
        'CODESC', 'CO_ENTIDADE', 'CD_IBGE', 'CO_MUNICIPIO', 'NOMESC', 'MUN', 'DE',
        'INSE_CLASSIFICACAO'
    ]
    cols_alvo_e_intermediarias = [
        target_col,
        'MEDIA_ACERTOS_2022', 'QTD_ALUNOS_2022', 'MEDIA_PROFIC_2022', 'PERC_ABAIXO_2022', 'PERC_ADEQ_AVANC_2022',
        'MEDIA_ACERTOS_2023', 'QTD_ALUNOS_2023', 'ACERTOS_MED_MAT_2023',
        'MEDIA_ACERTOS_2024', 'QTD_ALUNOS_2024', 'ACERTOS_MED_MAT_2024', 'NOTA_MED_MAT_2024',
        'ANOS_AVALIADOS'
    ]
    
    # Colunas de features puras
    cols_candidatas = [
        c for c in df.select_dtypes(include=[np.number]).columns
        if c not in cols_identificacao and c not in cols_alvo_e_intermediarias
    ]

    print(f"\n2. Variáveis Preditoras Identificadas para o Radar ({len(cols_candidatas)} métricas):")
    for i, c in enumerate(cols_candidatas, 1):
        print(f"   [{i:02d}] {c}")

    # 3. Cálculo de Pearson, Spearman e p-valores
    resultados = []
    from scipy import stats

    for col in cols_candidatas:
        sub = df[[col, target_col]].dropna()
        n_obs = len(sub)
        if n_obs >= 50:
            # Pearson
            r_pearson, p_pearson = stats.pearsonr(sub[col], sub[target_col])
            # Spearman
            rho_spearman, p_spearman = stats.spearmanr(sub[col], sub[target_col])
            
            resultados.append({
                'Variavel': col,
                'N_Obs': n_obs,
                'Pearson_r': r_pearson,
                'p_Pearson': p_pearson,
                'Spearman_rho': rho_spearman,
                'p_Spearman': p_spearman,
                'Abs_Pearson': abs(r_pearson)
            })

    df_corr = pd.DataFrame(resultados).sort_values(by='Abs_Pearson', ascending=False).reset_index(drop=True)

    # 4. Exibição Tabular Formatada do Ranking
    print("\n" + "=" * 70)
    print("3. RANKING GERAL DE CORRELAÇÃO COM O DESEMPENHO EM MATEMÁTICA (Y)")
    print("=" * 70)
    print(f"{'Pos':<4} {'Variável':<28} {'Pearson (r)':<14} {'Spearman (ρ)':<14} {'Significância (p)'}")
    print("-" * 70)

    for idx, row in df_corr.iterrows():
        sig = "***" if row['p_Pearson'] < 0.001 else ("**" if row['p_Pearson'] < 0.01 else ("*" if row['p_Pearson'] < 0.05 else "ns"))
        print(f"{idx+1:<4} {row['Variavel']:<28} {row['Pearson_r']:>+8.4f}      {row['Spearman_rho']:>+8.4f}      p < 0.001 {sig}" if row['p_Pearson'] < 0.001 else f"{idx+1:<4} {row['Variavel']:<28} {row['Pearson_r']:>+8.4f}      {row['Spearman_rho']:>+8.4f}      p = {row['p_Pearson']:.4f} {sig}")

    print("\nLegenda de Significância Estatística: *** p < 0.001 | ** p < 0.01 | * p < 0.05 | ns = não significante")

    # 5. Destaques Temáticos Estratégicos
    print("\n" + "=" * 70)
    print("4. DESTAQUES ANALÍTICOS POR DIMENSÃO TEMÁTICA")
    print("=" * 70)

    # A) Fatores Docentes
    vars_docentes = [c for c in df_corr['Variavel'] if any(k in c for k in ['IED', 'IRD', 'MED_CAT'])]
    print("\n[A] DIMENSÃO DOCENTE (SOBRECARGA & REGULARIDADE):")
    for v in vars_docentes:
        linha = df_corr[df_corr['Variavel'] == v].iloc[0]
        sentido = "PREJUDICA o desempenho (relação inversa)" if linha['Pearson_r'] < 0 else "FAVORECE o desempenho (relação direta)"
        print(f"   * {v:<22}: r = {linha['Pearson_r']:+.4f} | rho = {linha['Spearman_rho']:+.4f} -> {sentido}")

    # B) Infraestrutura e Tecnologia
    vars_infra = [c for c in df_corr['Variavel'] if any(k in c for k in ['COMP', 'LAB', 'BIBLIO', 'SALAS', 'INTERNET', 'BANDA'])]
    print("\n[B] DIMENSÃO INFRAESTRUTURA & TECNOLOGIA:")
    for v in vars_infra:
        linha = df_corr[df_corr['Variavel'] == v].iloc[0]
        sentido = "associação positiva" if linha['Pearson_r'] > 0 else "associação negativa"
        print(f"   * {v:<25}: r = {linha['Pearson_r']:+.4f} | rho = {linha['Spearman_rho']:+.4f} -> {sentido}")

    # 6. Geração do Gráfico Científico em Alta Resolução (300 DPI)
    print("\n" + "=" * 70)
    print("5. GERANDO GRÁFICO CIENTÍFICO: RADAR DE CORRELAÇÕES (300 DPI)")
    print("=" * 70)

    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        
        # Selecionar top variáveis mais expressivas para o gráfico
        df_plot = df_corr.head(14).sort_values(by='Pearson_r', ascending=True)

        fig, ax = plt.subplots(figsize=(10, 7), dpi=300)

        # Cores: Azul para correlações positivas, Vermelho para negativas
        cores = ['#d62728' if r < 0 else '#1f77b4' for r in df_plot['Pearson_r']]
        bars = ax.barh(df_plot['Variavel'], df_plot['Pearson_r'], color=cores, alpha=0.85, height=0.65)
        
        # Linha zero de referência
        ax.axvline(0, color='black', linestyle='--', linewidth=0.9, alpha=0.7)

        # Rótulos de dados nas barras
        for bar in bars:
            w = bar.get_width()
            desloc = 0.015 if w >= 0 else -0.06
            ax.text(w + desloc, bar.get_y() + bar.get_height()/2, f'{w:+.3f}', va='center', fontsize=9.5, fontweight='bold', color='#111111')

        ax.set_title('Radar de Influências: Ranking de Correlação Linear (Pearson r) com a Nota de Matemática', fontsize=12, fontweight='bold', pad=15)
        ax.set_xlabel('Coeficiente de Correlação de Pearson (r) com o Desempenho Escolar', fontsize=10.5)
        ax.set_xlim(min(df_plot['Pearson_r'].min() - 0.08, -0.20), max(df_plot['Pearson_r'].max() + 0.08, 0.50))
        
        # Legenda customizada
        import matplotlib.patches as mpatches
        patch_pos = mpatches.Patch(color='#1f77b4', label='Associação Positiva (Alavanca de Desempenho)')
        patch_neg = mpatches.Patch(color='#d62728', label='Associação Negativa (Gargalo / Sobrecarga)')
        ax.legend(handles=[patch_pos, patch_neg], loc='lower right', frameon=True, facecolor='white', framealpha=0.9)

        fig.tight_layout()
        caminho_fig = FIGURES_DIR / "eda_03_ranking_correlacoes.png"
        fig.savefig(caminho_fig)
        plt.close(fig)
        print(f"   [SUCESSO] Gráfico salvo com sucesso em:\n   {caminho_fig}")

    except Exception as e:
        print(f"   [AVISO] Erro ao renderizar gráfico: {e}")

    print("\n" + "=" * 70)
    print("PASSO 3 CONCLUÍDO COM SUCESSO!")
    print("=" * 70)

if __name__ == "__main__":
    calcular_correlacoes()

"""
=============================================================================
EDA PASSO 1: A ANATOMIA DA VARIÁVEL-ALVO (TARGET_TRIENAL_MAT)
=============================================================================
Objetivo:
  Antes de Machine Learning, analisar a variável alvo (Y).
  
  Neste passo investigamos:
  1. Tendência Central: Média vs. Mediana;
  2. Dispersão e Variabilidade: Desvio Padrão e Intervalo Interquartil;
  3. Formato da Distribuição: Assimetria e Curtose;
  4. Presença de Outliers (Regra de Tukey: 1.5 * IQR);
  5. Identificação das Escolas Líderes do Estado (Top 5 da rede);
  6. Geração do Gráfico de Diagnóstico (Histograma + KDE + Boxplot).

Saída:
  - reports/figures/eda_01_distribuicao_target.png
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

def analisar_target():
    print("=" * 70)
    print("EDA PASSO 1: DIAGNÓSTICO ESTATÍSTICO DA VARIÁVEL-ALVO (Y)")
    print("=" * 70)

    # 1. Carregamento da Camada Gold
    print("\n1. Carregando a Camada Gold...")
    df = pd.read_parquet(ARQUIVO_GOLD)
    y = df['TARGET_TRIENAL_MAT']
    n = len(y)
    print(f"   -> Universo Analisado: {n:,} escolas estaduais regulares paulistas.")

    # 2. Medidas de Tendência Central e Posição
    media = y.mean()
    mediana = y.median()
    q25 = y.quantile(0.25)
    q75 = y.quantile(0.75)
    iqr = q75 - q25
    minimo = y.min()
    maximo = y.max()

    print("\n2. Medidas de Tendência Central e Posição:")
    print(f"   - Média Aritmética:       {media:.2f}% de acertos")
    print(f"   - Mediana (P50):          {mediana:.2f}% de acertos")
    print(f"   - 1º Quartil (P25):       {q25:.2f}% (25% das escolas tiram menos que isso)")
    print(f"   - 3º Quartil (P75):       {q75:.2f}% (25% das escolas tiram mais que isso)")
    print(f"   - Distância Interquartil: {iqr:.2f} p.p. (onde se concentram os 50% centrais da rede)")
    print(f"   - Amplitude Total:        [{minimo:.2f}%, {maximo:.2f}%] (Diferença de {maximo - minimo:.2f} p.p.)")

    # 3. Medidas de Dispersão e Forma (Geometria da Distribuição)
    desvio = y.std()
    variancia = y.var()
    cv = (desvio / media) * 100
    skewness = y.skew()
    kurtosis = y.kurtosis()

    print("\n3. Medidas de Dispersão e Geometria da Curva:")
    print(f"   - Variância:              {variancia:.2f}")
    print(f"   - Desvio Padrão:          {desvio:.2f} p.p.")
    print(f"   - Coeficiente de Variação:{cv:.2f}% (CV < 20% indica dispersão moderada e controlada)")
    print(f"   - Assimetria (Skewness):  {skewness:+.3f}")
    if abs(skewness) < 0.5:
        print("     -> Interpretação: Distribuição aproximadamente SIMÉTRICA (Excelente para modelos lineares).")
    elif skewness > 0.5:
        print("     -> Interpretação: Assimetria positiva (cauda alongada à direita, poucas escolas com notas muito altas).")
    else:
        print("     -> Interpretação: Assimetria negativa (cauda alongada à esquerda).")

    print(f"   - Curtose (Kurtosis):     {kurtosis:+.3f}")
    if abs(kurtosis) < 1.0:
        print("     -> Interpretação: Curva Mesocúrtica (caudas normais, comportamento próximo de uma Gaussiana).")
    elif kurtosis > 1.0:
        print("     -> Interpretação: Curva Leptocúrtica (pico pronunciado no centro e caudas pesadas).")

    # 4. Detecção de Outliers pela Regra de Tukey
    limite_inferior = q25 - 1.5 * iqr
    limite_superior = q75 + 1.5 * iqr
    outliers_abaixo = df[df['TARGET_TRIENAL_MAT'] < limite_inferior]
    outliers_acima = df[df['TARGET_TRIENAL_MAT'] > limite_superior]

    print("\n4. Diagnóstico de Outliers (Regra de Tukey: Q ± 1.5 * IQR):")
    print(f"   - Limite Inferior Teórico: {limite_inferior:.2f}%")
    print(f"   - Limite Superior Teórico: {limite_superior:.2f}%")
    print(f"   - Escolas abaixo do limite (Outliers Inferiores): {len(outliers_abaixo)} escolas ({len(outliers_abaixo)/n*100:.2f}%)")
    print(f"   - Escolas acima do limite (Outliers Superiores):  {len(outliers_acima)} escolas ({len(outliers_acima)/n*100:.2f}%)")
    
    if len(outliers_acima) > 0:
        print("\n   Top 5 Escolas Destaque no Topo da Curva (Outliers Positivos):")
        col_nome = 'NOMESC' if 'NOMESC' in df.columns else 'CODESC'
        col_mun = 'MUN' if 'MUN' in df.columns else 'CODESC'
        top5 = outliers_acima.sort_values(by='TARGET_TRIENAL_MAT', ascending=False)[
            ['CODESC', col_nome, col_mun, 'MEDIA_INSE', 'TOTAL_ALUNOS_TRIENIO', 'TARGET_TRIENAL_MAT']
        ].head(5)
        for _, row in top5.iterrows():
            print(f"     * [{row['CODESC']}] {row[col_nome]} ({row[col_mun]}): Nota = {row['TARGET_TRIENAL_MAT']:.2f}% | INSE = {row['MEDIA_INSE']} | Alunos = {row['TOTAL_ALUNOS_TRIENIO']}")

    # 5. Geração de Gráfico Científico Conjugado (Histograma + KDE + Boxplot)
    print("\n5. Gerando painel gráfico científico de alta resolução (300 DPI)...")
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        fig, (ax_box, ax_hist) = plt.subplots(
            2, 1, figsize=(10, 7), dpi=300, sharex=True,
            gridspec_kw={'height_ratios': [0.25, 0.75]}
        )

        # Painel Superior: Boxplot
        sns.boxplot(x=y, ax=ax_box, color='#6baed6', fliersize=4, flierprops={'markerfacecolor': '#d62728', 'alpha': 0.6})
        ax_box.axvline(media, color='#d62728', linestyle='--', linewidth=1.5, label='Média')
        ax_box.axvline(mediana, color='#2ca02c', linestyle='-', linewidth=2, label='Mediana')
        ax_box.set(xlabel='')
        ax_box.set_title('Painel de Diagnóstico da Variável-Alvo: Média Trienal de Matemática (2022–2024)', fontsize=12, fontweight='bold', pad=10)
        ax_box.legend(loc='upper right', frameon=True, facecolor='white')

        # Painel Inferior: Histograma + Densidade KDE
        sns.histplot(y, kde=True, ax=ax_hist, color='#1f77b4', bins=40, stat="density", alpha=0.55)
        ax_hist.axvline(media, color='#d62728', linestyle='--', linewidth=1.8, label=f'Média: {media:.2f}%')
        ax_hist.axvline(mediana, color='#2ca02c', linestyle='-', linewidth=2, label=f'Mediana: {mediana:.2f}%')
        ax_hist.axvline(q25, color='gray', linestyle=':', linewidth=1.2, label=f'P25: {q25:.2f}%')
        ax_hist.axvline(q75, color='gray', linestyle=':', linewidth=1.2, label=f'P75: {q75:.2f}%')
        
        ax_hist.set_xlabel('Desempenho Médio Escolar em Matemática (% de acertos ponderada)', fontsize=11)
        ax_hist.set_ylabel('Densidade de Probabilidade', fontsize=11)
        ax_hist.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)

        fig.tight_layout()
        caminho_fig = FIGURES_DIR / "eda_01_distribuicao_target.png"
        fig.savefig(caminho_fig)
        plt.close(fig)
        print(f"   [SUCESSO] Gráfico salvo com sucesso em:\n   {caminho_fig}")

    except Exception as e:
        print(f"   [AVISO] Erro ao renderizar gráfico com matplotlib: {e}")

    print("\n" + "=" * 70)
    print("PASSO 1 CONCLUÍDO! Pronto para interpretação e reflexão teórica.")
    print("=" * 70)

if __name__ == "__main__":
    analisar_target()

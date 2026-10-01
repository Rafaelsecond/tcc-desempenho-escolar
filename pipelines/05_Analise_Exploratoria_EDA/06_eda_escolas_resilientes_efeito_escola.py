"""
=============================================================================
EDA PASSO 6: O MAPEAMENTO SISTEMÁTICO DAS ESCOLAS RESILIENTES (EFEITO-ESCOLA)
=============================================================================
Objetivo Pedagógico e Científico:
  Em Eficácia Escolar (School Effectiveness Research), uma questão importante é:
  "Quais escolas públicas conseguem entregar alta aprendizagem mesmo atendendo
   estudantes de famílias em situação de vulnerabilidade socioeconômica?"

  Metodologia Aplicada:
  1. Cálculo do Resíduo de Coleman para as 3.594 escolas com INSE:
     Resíduo (e_i) = Nota Real (Y_i) - Nota Prevista pelo INSE (Y_chapéu)
  2. Classificação em Três Regimes de Eficácia Escolar:
     - Escolas Resilientes (Alta Eficácia): Resíduo >= +1.5 * RMSE (+5.18 p.p.)
     - Escolas Típicas / Alinhadas: Resíduo entre -1.5 * RMSE e +1.5 * RMSE
     - Escolas em Subdesempenho Crítico: Resíduo <= -1.5 * RMSE
  3. Mapeamento dos Polos Geográficos de Resiliência:
     - Diretorias de Ensino (DEs) e Municípios com maior concentração de resiliência;
  4. Raio-X Comparativo do Perfil das Escolas Resilientes vs. Rede em Geral:
     - Fator Docente (IED e IRD);
     - Porte Físico e Volume de Estudantes;
     - Recursos de Infraestrutura;
  5. Top 15 Escolas Resilientes do Estado de São Paulo;
  6. Geração de Gráfico Científico em 300 DPI (Dispersão com Faixas de Resíduo).

Saída:
  - reports/figures/eda_06_escolas_resilientes_efeito_escola.png
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

def mapear_escolas_resilientes():
    print("=" * 75)
    print("EDA PASSO 6: O MAPEAMENTO DAS ESCOLAS RESILIENTES (EFEITO-ESCOLA)")
    print("=" * 75)

    # 1. Carregamento de Dados
    print("\n1. Carregando dados da Camada Gold...")
    df = pd.read_parquet(ARQUIVO_GOLD)
    target_col = 'TARGET_TRIENAL_MAT'
    
    # Filtrar escolas com INSE válido
    df_valid = df.dropna(subset=['MEDIA_INSE', target_col]).copy()
    n_total = len(df_valid)
    print(f"   -> Escolas com INSE analisadas: {n_total:,}")

    # 2. Ajuste da Reta de Coleman e Cálculo dos Resíduos
    x = df_valid['MEDIA_INSE'].values
    y = df_valid[target_col].values

    b1, b0 = np.polyfit(x, y, deg=1)
    y_pred = b0 + b1 * x
    residuos = y - y_pred
    rmse = np.sqrt(np.mean(residuos ** 2))

    df_valid['PREVISTO_COLEMAN'] = y_pred
    df_valid['RESIDUO_COLEMAN'] = residuos

    limiar_resiliencia = 1.5 * rmse
    limiar_critico = -1.5 * rmse

    print(f"\n2. Parâmetros da Linha de Base de Coleman:")
    print(f"   - Reta de Referência: Target = {b0:.2f} + {b1:.2f} * INSE")
    print(f"   - Erro Padrão Residual (RMSE): {rmse:.2f} pontos percentuais")
    print(f"   - Limiar de Alta Eficácia (Resíduo >= +1.5*RMSE):  +{limiar_resiliencia:.2f} p.p. acima do previsto")
    print(f"   - Limiar de Subdesempenho (Resíduo <= -1.5*RMSE):  {limiar_critico:.2f} p.p. abaixo do previsto")

    # 3. Classificação dos Regimes de Eficácia
    def classificar_regime(res):
        if res >= limiar_resiliencia:
            return "Escola Resiliente (Alta Eficácia)"
        elif res <= limiar_critico:
            return "Subdesempenho Crítico"
        else:
            return "Desempenho Típico (Alinhado ao INSE)"

    df_valid['REGIME_EFICACIA'] = df_valid['RESIDUO_COLEMAN'].apply(classificar_regime)

    print("\n3. Distribuição dos Regimes de Eficácia Escolar na Rede Paulista:")
    contagem_regimes = df_valid['REGIME_EFICACIA'].value_counts()
    for reg, qtd in contagem_regimes.items():
        print(f"   - {reg:<36}: {qtd:>4} escolas ({qtd/n_total*100:>5.2f}%)")

    # Isolar Escolas Resilientes
    df_resilientes = df_valid[df_valid['REGIME_EFICACIA'] == "Escola Resiliente (Alta Eficácia)"].copy()
    n_resilientes = len(df_resilientes)

    # 4. Raio-X Comparativo: Escolas Resilientes vs. Rede em Geral
    print("\n" + "=" * 70)
    print("4. RAIO-X COMPARATIVO: ESCOLAS RESILIENTES vs. REDE GERAL")
    print("=" * 70)

    indicadores_comparar = [
        ('TARGET_TRIENAL_MAT', 'Nota Média em Matemática (%)'),
        ('MEDIA_INSE', 'Nível Socioeconômico (INSE)'),
        ('IED_SCORE_MEDIO', 'Esforço Docente (IED: 1 a 6)'),
        ('IED_ESFORCO_ALTO', 'Sobrecarga Alta (% Cat 5 e 6)'),
        ('IRD_MEDIO', 'Regularidade Docente (IRD: 0 a 5)'),
        ('QT_SALAS_UTILIZADAS', 'Salas de Aula Utilizadas'),
        ('TOTAL_ALUNOS_TRIENIO', 'Alunos Avaliados no Triênio'),
        ('QT_COMP_ALUNO', 'Computadores para Alunos'),
        ('IN_LABORATORIO_CIENCIAS', 'Laboratório de Ciências (%)')
    ]

    print(f"{'Indicador':<32} {'Rede Geral (μ)':<16} {'Resilientes (μ)':<16} {'Diferença (Δ)'}")
    print("-" * 75)

    for col, nome in indicadores_comparar:
        if col in df_valid.columns:
            m_geral = df_valid[col].mean()
            m_resil = df_resilientes[col].mean()
            if col == 'IN_LABORATORIO_CIENCIAS':
                m_geral *= 100
                m_resil *= 100
                dif = m_resil - m_geral
                print(f"{nome:<32} {m_geral:>12.1f}%    {m_resil:>12.1f}%    {dif:>+12.1f} p.p.")
            else:
                dif = m_resil - m_geral
                print(f"{nome:<32} {m_geral:>14.2f}      {m_resil:>14.2f}      {dif:>+14.2f}")

    # 5. Concentração Geográfica das Escolas Resilientes (Polos Regionais)
    print("\n" + "=" * 70)
    print("5. POLOS REGIONAIS: TOP DIRETORIAS DE ENSINO (DEs) EM RESILIÊNCIA")
    print("=" * 70)
    
    top_de = df_resilientes['DE'].value_counts().head(8)
    for de, qtd in top_de.items():
        total_escolas_de = len(df_valid[df_valid['DE'] == de])
        taxa_resil = (qtd / total_escolas_de) * 100
        print(f"   * DE {de:<32}: {qtd:>2} escolas resilientes de {total_escolas_de} na DE ({taxa_resil:>4.1f}% da diretoria!)")

    # 6. Top 15 Escolas de Maior Eficácia e Superação do Estado de São Paulo
    print("\n" + "=" * 70)
    print("6. TOP 15 ESCOLAS RESILIENTES DO ESTADO DE SÃO PAULO")
    print("=" * 70)
    
    top15 = df_resilientes.sort_values(by='RESIDUO_COLEMAN', ascending=False).head(15)
    cols_top = ['CODESC', 'NOMESC', 'MUN', 'DE', 'MEDIA_INSE', 'TARGET_TRIENAL_MAT', 'PREVISTO_COLEMAN', 'RESIDUO_COLEMAN', 'IED_SCORE_MEDIO', 'IRD_MEDIO']
    
    for i, (_, row) in enumerate(top15[cols_top].iterrows(), 1):
        print(f"[{i:02d}] {row['NOMESC'][:32]:<32} | {row['MUN']:<18} | INSE: {row['MEDIA_INSE']:.2f} | Nota: {row['TARGET_TRIENAL_MAT']:>5.2f}% | Previsto: {row['PREVISTO_COLEMAN']:>5.2f}% | Superação: +{row['RESIDUO_COLEMAN']:>5.2f} p.p.")

    # 7. Geração de Gráfico Científico em Alta Resolução (300 DPI)
    print("\n7. Gerando gráfico científico de resiliência escolar (300 DPI)...")
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

        # Plotar escolas típicas
        mask_tipicas = df_valid['REGIME_EFICACIA'] == "Desempenho Típico (Alinhado ao INSE)"
        ax.scatter(
            df_valid.loc[mask_tipicas, 'MEDIA_INSE'], df_valid.loc[mask_tipicas, target_col],
            color='#9ecae1', alpha=0.35, s=25, edgecolors='none', label='Escolas Típicas (N=3.308)'
        )

        # Plotar subdesempenho
        mask_critico = df_valid['REGIME_EFICACIA'] == "Subdesempenho Crítico"
        ax.scatter(
            df_valid.loc[mask_critico, 'MEDIA_INSE'], df_valid.loc[mask_critico, target_col],
            color='#fc9272', alpha=0.6, s=35, edgecolors='none', label='Subdesempenho Crítico'
        )

        # Plotar Escolas Resilientes
        ax.scatter(
            df_resilientes['MEDIA_INSE'], df_resilientes[target_col],
            color='#2ca02c', alpha=0.85, s=55, edgecolors='#1b7837', linewidth=0.8,
            label=f'Escolas Resilientes (N={n_resilientes})', zorder=4
        )

        # Reta de Coleman
        x_linha = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_linha, b0 + b1 * x_linha, color='#d62728', linewidth=2.2, label=f'Reta de Coleman (Esperado pelo INSE)')
        
        # Linha pontilhada do limiar de resiliência (+1.5 RMSE)
        ax.plot(x_linha, b0 + b1 * x_linha + limiar_resiliencia, color='#2ca02c', linestyle='--', linewidth=1.5, label='Limiar de Alta Eficácia (+1.5x RMSE)')

        # Destacar com anotação as top 4
        for _, row in top15.head(4).iterrows():
            ax.annotate(
                f"{row['NOMESC'][:18]} (+{row['RESIDUO_COLEMAN']:.1f}%)",
                (row['MEDIA_INSE'], row[target_col]),
                textcoords="offset points", xytext=(8, -4),
                fontsize=8.5, fontweight='bold', color='#1b7837',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2ca02c", alpha=0.9)
            )

        ax.set_title('Mapeamento das Escolas Resilientes: O Efeito-Escola Puro no Ensino Médio Paulista', fontsize=12.5, fontweight='bold', pad=15)
        ax.set_xlabel('Nível Socioeconômico das Famílias da Escola (INSE)', fontsize=10.5)
        ax.set_ylabel('Média Trienal de Matemática (% de acertos ponderada)', fontsize=10.5)
        ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

        fig.tight_layout()
        caminho_fig = FIGURES_DIR / "eda_06_escolas_resilientes_efeito_escola.png"
        fig.savefig(caminho_fig)
        plt.close(fig)
        print(f"   [SUCESSO] Gráfico salvo com sucesso em:\n   {caminho_fig}")

    except Exception as e:
        print(f"   [AVISO] Erro ao renderizar gráfico: {e}")

    print("\n" + "=" * 75)
    print("PASSO 6 CONCLUÍDO COM SUCESSO!")
    print("=" * 75)

if __name__ == "__main__":
    mapear_escolas_resilientes()

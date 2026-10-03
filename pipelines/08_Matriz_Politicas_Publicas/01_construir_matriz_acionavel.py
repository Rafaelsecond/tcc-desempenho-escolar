"""
=============================================================================
FASE 08: SÍNTESE ESTRATÉGICA — ETAPA 1: MATRIZ ACIONÁVEL DE POLÍTICAS PÚBLICAS
TCC: Fatores Escolares e Desempenho no Ensino Médio Paulista
=============================================================================

OBJETIVO:
  Traduzir os valores de impacto SHAP e descobertas econométricas em uma
  Matriz de Decisão Executiva para a Secretaria da Educação (SEDUC-SP).
  Cruza o Retorno Pedagógico Real (Eixo Y: Impacto SHAP) com o Custo e
  Complexidade de Implementação (Eixo X) em quatro quadrantes de ação.

ARTEFATOS PRODUZIDOS:
  - reports/figures/matriz_01_politicas_publicas.png (Gráfico Executivo 2x2)
  - data/gold/matriz_priorizacao_politicas_publicas.csv (Tabela de Decisão)
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Configuração de Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DIR_FIGURAS = BASE_DIR / "reports" / "figures"
DIR_GOLD = BASE_DIR / "data" / "gold"
DIR_FIGURAS.mkdir(parents=True, exist_ok=True)

PATH_FIGURA = DIR_FIGURAS / "matriz_01_politicas_publicas.png"
PATH_CSV = DIR_GOLD / "matriz_priorizacao_politicas_publicas.csv"

print("=" * 75)
print("FASE 08: CONSTRUÇÃO DA MATRIZ ACIONÁVEL DE POLÍTICAS PÚBLICAS (SEDUC-SP)")
print("=" * 75)

# 2. Definição das Intervenções e Cruzamento SHAP vs Custo/Esforço
# Custo/Esforço (Escala 1 a 5: 1=Muito Baixo/Regulatório, 5=Altíssimo Custo Financeiro)
dados_matriz = [
    {
        "Politica": "Fixação Docente (Permanência)",
        "Feature_Base": "IRD_MEDIO",
        "Impacto_SHAP": 0.370,
        "Custo_Esforco": 2.2,
        "Quadrante": "Q1: Prioridade Estrutural (Alto Retorno)",
        "Acao_Recomendada": "Criar bônus de permanência e pontuação de carreira para fixação na mesma unidade."
    },
    {
        "Politica": "Teto de Sobrecarga Docente",
        "Feature_Base": "IED_ESFORCO_ALTO",
        "Impacto_SHAP": 0.327,
        "Custo_Esforco": 2.5,
        "Quadrante": "Q1: Prioridade Estrutural (Alto Retorno)",
        "Acao_Recomendada": "Limitar a atribuição a no máximo 2-3 turmas por professor em unidades de vulnerabilidade."
    },
    {
        "Politica": "Desmassificação Escolar (Escala Humana)",
        "Feature_Base": "TOTAL_ALUNOS / QT_SALAS",
        "Impacto_SHAP": 0.149,
        "Custo_Esforco": 4.5,
        "Quadrante": "Q2: Estruturante de Longo Prazo",
        "Acao_Recomendada": "Modular novas escolas com menos de 500 alunos ou criar subunidades pedagógicas."
    },
    {
        "Politica": "Laboratório de Ciências Ativo",
        "Feature_Base": "IN_LABORATORIO_CIENCIAS",
        "Impacto_SHAP": 0.055,
        "Custo_Esforco": 1.8,
        "Quadrante": "Q3: Eficiência Marginal / Manutenção",
        "Acao_Recomendada": "Fornecer kits de experimentos e protocolos curriculares ativos."
    },
    {
        "Politica": "Salas de Leitura e Mediação",
        "Feature_Base": "IN_BIBLIOTECA_SALA_LEITURA",
        "Impacto_SHAP": 0.008,
        "Custo_Esforco": 1.5,
        "Quadrante": "Q3: Eficiência Marginal / Manutenção",
        "Acao_Recomendada": "Integrar a leitura à interpretação de enunciados matemáticos (EDA Passo 7)."
    },
    {
        "Politica": "Aquisição Massiva de Computadores",
        "Feature_Base": "QT_COMP_ALUNO",
        "Impacto_SHAP": 0.085,
        "Custo_Esforco": 4.6,
        "Quadrante": "Q4: Baixa Relação Custo-Efetividade",
        "Acao_Recomendada": "Condicionar aquisições à prévia formação docente e projeto pedagógico estruturado."
    },
    {
        "Politica": "Instalação de Lousas Digitais",
        "Feature_Base": "IN_EQUIP_LOUSA_DIGITAL",
        "Impacto_SHAP": 0.033,
        "Custo_Esforco": 4.2,
        "Quadrante": "Q4: Baixa Relação Custo-Efetividade",
        "Acao_Recomendada": "Priorizar formação em metodologias ativas antes de novos pregões de hardware."
    },
    {
        "Politica": "Laboratórios Tradicionais de TI",
        "Feature_Base": "IN_LABORATORIO_INFORMATICA",
        "Impacto_SHAP": 0.011,
        "Custo_Esforco": 3.8,
        "Quadrante": "Q4: Baixa Relação Custo-Efetividade",
        "Acao_Recomendada": "Reavaliar espaços ociosos e readequar para convivência e reforço pedagógico."
    }
]

df_matriz = pd.DataFrame(dados_matriz)
df_matriz.to_csv(PATH_CSV, index=False, sep=";")
print(f"1. Tabela executiva salva em: {PATH_CSV}")

# 3. Construção Gráfica da Matriz de Decisão 2x2
print("2. Gerando Gráfico Executivo da Matriz Acionável (300 DPI)...")
fig, ax = plt.subplots(figsize=(11, 8.5))

cores_quadrante = {
    "Q1: Prioridade Estrutural (Alto Retorno)": "#2E7D32",      # Verde escuro
    "Q2: Estruturante de Longo Prazo": "#1565C0",              # Azul
    "Q3: Eficiência Marginal / Manutenção": "#F57F17",         # Amarelo/Laranja
    "Q4: Baixa Relação Custo-Efetividade": "#C62828"            # Vermelho escuro
}

# Linhas divisórias dos Quadrantes
ax.axhline(y=0.12, color="gray", linestyle="--", linewidth=1.2, alpha=0.7)
ax.axvline(x=3.0, color="gray", linestyle="--", linewidth=1.2, alpha=0.7)

# Fundo sutil para os quadrantes
ax.axvspan(0.8, 3.0, ymin=0.30, ymax=1.0, color="#E8F5E9", alpha=0.3)  # Q1 Verde claro
ax.axvspan(3.0, 5.3, ymin=0.30, ymax=1.0, color="#E3F2FD", alpha=0.3)  # Q2 Azul claro
ax.axvspan(0.8, 3.0, ymin=0.0, ymax=0.30, color="#FFF8E1", alpha=0.3)   # Q3 Amarelo claro
ax.axvspan(3.0, 5.3, ymin=0.0, ymax=0.30, color="#FFEBEE", alpha=0.3)   # Q4 Vermelho claro

# Rótulos dos Quadrantes (em posições sem colisão)
ax.text(0.9, 0.42, "QUADRANTE 1: PRIORIDADE ESTRUTURAL\n• Alto Retorno Pedagógico | Custo de Gestão/Regulatório",
        fontsize=9.5, weight="bold", color="#1B5E20", va="top")
ax.text(3.1, 0.42, "QUADRANTE 2: ESTRUTURANTE DE LONGO PRAZO\n• Alto Retorno Pedagógico | Alto Custo / Obras",
        fontsize=9.5, weight="bold", color="#0D47A1", va="top")
ax.text(0.9, 0.115, "QUADRANTE 3: EFICIÊNCIA MARGINAL / MANUTENÇÃO\n• Retorno Específico | Baixo Custo Orçamentário",
        fontsize=9.5, weight="bold", color="#E65100", va="top")
ax.text(3.1, 0.115, "QUADRANTE 4: BAIXA RELAÇÃO CUSTO-EFETIVIDADE\n• Retorno Prático Residual | Alto Custo de Aquisição",
        fontsize=9.5, weight="bold", color="#B71C1C", va="top")

# Anotações manuais inteligentes de cada ponto para evitar colisões
offsets = {
    "Fixação Docente (Permanência)": (10, -5),
    "Teto de Sobrecarga Docente": (10, -5),
    "Desmassificação Escolar (Escala Humana)": (-15, 12),
    "Laboratório de Ciências Ativo": (10, 4),
    "Salas de Leitura e Mediação": (10, -6),
    "Aquisição Massiva de Computadores": (-25, -20),
    "Instalação de Lousas Digitais": (10, -4),
    "Laboratórios Tradicionais de TI": (10, -5)
}

for _, row in df_matriz.iterrows():
    cor = cores_quadrante[row["Quadrante"]]
    ax.scatter(row["Custo_Esforco"], row["Impacto_SHAP"], color=cor, s=170, zorder=5, edgecolor="black", linewidth=1.2)
    ox, oy = offsets.get(row["Politica"], (10, 0))
    ax.annotate(
        row["Politica"],
        (row["Custo_Esforco"], row["Impacto_SHAP"]),
        xytext=(ox, oy), textcoords="offset points",
        fontsize=9, weight="bold", color="#212121",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="gray", alpha=0.9, lw=0.5)
    )

ax.set_title("Matriz de Priorização de Políticas Públicas Educacionais (SEDUC-SP)\nCruzamento Empírico: Impacto SHAP (Retorno Pedagógico) vs. Custo/Esforço de Implementação",
             fontsize=12.5, weight="bold", pad=20)
ax.set_xlabel("Custo Financeiro e Esforço de Implementação (1 = Regulatório/Gestão ➔ 5 = Obras/Hardware)", fontsize=10.5, labelpad=10)
ax.set_ylabel("Retorno Pedagógico Real (Impacto Médio SHAP em p.p.)", fontsize=10.5, labelpad=10)
ax.set_xlim(0.8, 5.3)
ax.set_ylim(-0.02, 0.44)
ax.grid(True, linestyle=":", alpha=0.6, zorder=1)

plt.tight_layout()
plt.savefig(PATH_FIGURA, dpi=300, bbox_inches="tight")
plt.close()
print(f"3. Gráfico salvo em: {PATH_FIGURA}")

print("\n" + "=" * 75)
print("TABELA EXECUTIVA DA MATRIZ DE POLÍTICAS PÚBLICAS")
print("=" * 75)
for q in cores_quadrante.keys():
    print(f"\n>>> {q.upper()}:")
    sub = df_matriz[df_matriz["Quadrante"] == q]
    for _, r in sub.iterrows():
        print(f"  • {r['Politica']} (SHAP: +{r['Impacto_SHAP']:.3f} p.p. | Custo: {r['Custo_Esforco']}/5)")
        print(f"    -> Recomendação: {r['Acao_Recomendada']}")

print("\n[SUCESSO] Matriz acionável concluída com êxito!")

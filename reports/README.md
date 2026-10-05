# Documentação Acadêmica, Relatórios e Catálogo de Evidências Visuais (TCC UNIVESP)

Esta pasta centraliza os documentos acadêmicos, relatórios metodológicos, notas de auditoria e todo o aparato gráfico analítico produzido para o Trabalho de Conclusão de Curso:

> **Título:** Eficácia Escolar e Fatores de Gestão no Desempenho em Matemática do Ensino Médio Paulista: Uma Abordagem Preditiva e Explicável (2022–2024)  
> **População:** Universo Censitário de $N = 3.611$ Escolas Estaduais Paulistas  
> **Bases Integradas:** Microdados do Censo Escolar (INEP), Indicadores Educacionais (INEP) e SARESP (SEDUC-SP)  

---

## 📄 Documentos Monográficos e Relatórios Oficiais

| Arquivo | Descrição e Finalidade | Público-Alvo / Uso |
| :--- | :--- | :--- |
| [`relatorio_final_tcc.md`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/relatorio_final_tcc.md) | **Monografia Completa do TCC**: Texto acadêmico estruturado conforme as normas ABNT e diretrizes da UNIVESP. Contém introdução, marco teórico, metodologia, resultados econométricos/preditivos, discussão à luz da eficácia escolar e subsídios para políticas públicas. | Banca examinadora, avaliadores e publicação acadêmica. |
| [`relatorio_metodologico_tcc.md`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/relatorio_metodologico_tcc.md) | **Caderno de Governança Metodológica e Auditoria**: Registro longitudinal e cumulativo de cada pipeline (01 a 08). Estruturado nos 5 pilares obrigatórios: Métodos Utilizados, Motivações Estratégicas, Resumo das Métricas, Descobertas/Auditoria de Erros e Fundamentação Teórica. | Cientistas de dados, auditores de pesquisa e reprodutibilidade FAIR. |
| [`fundamentacao_teorica.md`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/fundamentacao_teorica.md) | **Marco Teórico-Conceitual de Eficácia Escolar**: Síntese bibliográfica detalhada abordando a teoria de Coleman (1966), a sociologia da reprodução de Bourdieu (1970/1983) e os modelos de eficácia escolar de Soares & Alves (2003) e Franco (2007). | Aprofundamento teórico e fundamentação sociológica. |
| [`validacao_estabilidade_trienal.md`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/validacao_estabilidade_trienal.md) | **Auditoria de Consistência Temporal dos Indicadores**: Avaliação empírica da coerência estrutural das variáveis docentes e socioeconômicas entre 2022 e 2024. | Validação econométrica de estabilidade de painel. |

---

## 🖼️ Catálogo de Gráficos e Evidências Visuais (`reports/figures/`)

Todas as figuras foram produzidas a partir dos pipelines oficiais de dados e exportadas em **alta resolução (300 DPI)** com padronização visual consistente:

### 1. Análise Exploratória de Dados (Pipeline 05)
1. [`eda_00_estabilidade_docente_trienal.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/eda_00_estabilidade_docente_trienal.png): Validação da estabilidade temporal dos indicadores docentes (2022 vs 2024).
2. [`eda_01_distribuicao_target.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/eda_01_distribuicao_target.png): Histograma e curva de densidade do percentual de estudantes no nível adequado em Matemática.
3. [`eda_02_teste_coleman_inse.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/eda_02_teste_coleman_inse.png): Regressão bivariada entre Nível Socioeconômico (INSE) e Desempenho (Teste da Hipótese de Coleman, $R^2 = 20,4\%$).
4. [`eda_03_ranking_correlacoes.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/eda_03_ranking_correlacoes.png): Coeficientes de correlação de Pearson de todas as variáveis observadas com o desempenho em Matemática.
5. [`eda_04_fatores_docentes_ied_ird.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/eda_04_fatores_docentes_ied_ird.png): Impacto bivariado da regularidade do corpo docente (IRD) e sobrecarga de turmas (IED) sobre a proficiência.
6. [`eda_05_infraestrutura_e_tecnologia.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/eda_05_infraestrutura_e_tecnologia.png): Contraste empírico entre recursos físicos consolidados (laboratórios, bibliotecas) e aparatos digitais (lousas, computadores).
7. [`eda_06_escolas_resilientes_efeito_escola.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/eda_06_escolas_resilientes_efeito_escola.png): Identificação das escolas com desempenho superior ao esperado dado seu nível socioeconômico (Efeito Escola).
8. [`eda_07_portugues_vs_matematica.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/eda_07_portugues_vs_matematica.png): Desacoplamento entre proficiência em Língua Portuguesa e Matemática ($r = +0,793$), demonstrando a absorção do INSE por Português e justificando o isolamento metodológico contra vazamento de alvo.

### 2. Explicabilidade Preditiva por Inteligência Artificial (Pipeline 07)
9. [`shap_01_summary_beeswarm.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/shap_01_summary_beeswarm.png): Gráfico SHAP Beeswarm da Random Forest campeã, evidenciando a magnitude e a direção do impacto de cada preditor na distribuição completa das escolas.
10. [`shap_02_bar_importance.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/shap_02_bar_importance.png): Ranking de importância média absoluta ($|\text{SHAP}|$ em pontos percentuais), confirmando a primazia do INSE ($1,17$ p.p.) seguido por estabilidade docente ($0,37$ p.p.) e sobrecarga de turmas ($0,33$ p.p.).
11. [`shap_03_waterfall_escola_resiliente.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/shap_03_waterfall_escola_resiliente.png): Decomposição local SHAP da **EE Assentamento Santa Clara** (Mirante do Paranapanema), ilustrando como a estabilidade de gestão neutraliza a penalidade de alta vulnerabilidade social (+18,1 p.p. de efeito explicável).
12. [`shap_04_waterfall_escola_vulneravel.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/shap_04_waterfall_escola_vulneravel.png): Decomposição local SHAP da **EE Jardim Aracati II** (Capital), evidenciando o efeito cumulativo de rotatividade docente e superpopulação amplificando a defasagem de aprendizagem (-6,1 p.p. de penalidade explicável).

### 3. Síntese de Políticas Públicas e Tomada de Decisão (Pipeline 08)
13. [`matriz_01_politicas_publicas.png`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures/matriz_01_politicas_publicas.png): Matriz acionável $2 \times 2$ cruzando **Impacto Marginal SHAP** contra **Custo / Complexidade de Implementação**, orientando a alocação de recursos da Secretaria da Educação do Estado de São Paulo (SEDUC-SP).

---

## 📂 Pastas Auxiliares de Apoio

* **`metodos/`**: Armazena anotações técnicas, logs de transformações intermediárias e registros passo a passo da limpeza do Censo, Indicadores INEP e SARESP.
* **`planejamento/`**: Contém o histórico de sprints, planejamento metodológico das quinzenas e notas conceituais do desenho experimental da pesquisa.

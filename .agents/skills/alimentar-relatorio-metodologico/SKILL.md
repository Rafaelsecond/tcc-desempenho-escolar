---
name: alimentar-relatorio-metodologico
description: >-
  Use esta skill sempre que uma etapa, modelo ou fase de pesquisa for concluída no TCC.
  Orienta a alimentação sistemática do relatório metodológico (reports/relatorio_metodologico_tcc.md),
  estruturando formalmente os métodos utilizados, as motivações estratégicas das escolhas, o resumo
  das métricas obtidas, as descobertas empíricas e a fundamentação teórica aplicável.
---

# Protocolo de Governança: Atualização do Relatório Metodológico do TCC

Esta skill estabelece o Procedimento Operacional Padrão (SOP) para documentar cada avanço empírico e computacional da pesquisa no arquivo `reports/relatorio_metodologico_tcc.md`.

## Os 5 Pilares Obrigatórios de Cada Atualização

Ao final de cada etapa (ex: baselines lineares, random forest, gradient boosting, SHAP), a documentação no relatório deve cobrir de forma modular e concisa:

### 1. Métodos e Técnicas Utilizadas
- **Algoritmos e Bibliotecas**: Explicitar modelos (ex: Ridge, Lasso, RandomForest, LightGBM) e pacotes (`scikit-learn`, `lightgbm`, etc.).
- **Hiperparâmetros e Configuração**: Indicar valores de regularização ($\alpha$, `min_samples_leaf`, `num_leaves`), número de estimadores e sementes fixas (`random_state=42`).
- **Protocolo de Validação**: Detalhar a estratégia de particionamento (ex: 5-Fold Cross-Validation) e o pipeline de pré-processamento (`StandardScaler` isolado por dobra).

### 2. Motivações Estratégicas das Escolhas
- Justificar a razão da escolha do método em relação aos anteriores.
- Exemplo:
  * Por que OLS $\to$ Ridge/Lasso? (Controlar a multicolinearidade e testar esparsidade).
  * Por que Lineares $\to$ Random Forest? (Superar a hipótese de linearidade estrita e capturar interações entre insumos e fatores docentes).
  * Por que Random Forest $\to$ Gradient Boosting? (Testar aprendizado sequencial com foco na redução progressiva de resíduos).

### 3. Resumo Consolidado dos Resultados (Métricas)
- Apresentar tabelas de comparação com métricas padronizadas:
  * $R^2$ Médio ($\%$) $\pm$ Desvio Padrão;
  * RMSE (Root Mean Squared Error) em pontos percentuais;
  * MAE (Mean Absolute Error) em pontos percentuais;
  * Rankings de relevância (Betas padronizados, MDI ou Ganho de Redução de Erro).

### 4. Partes Descobertas e Diagnósticos Empíricos
- Interpretar o significado prático dos números para a rede escolar paulista.
- Registrar detecções metodológicas críticas ocorridas durante o processo (ex: detecção e saneamento de vazamento de ID/`CODESC`).
- Confirmar se a hierarquia das variáveis se mantém ou muda com o algoritmo.

### 5. Fundamentação Teórica e Sociológica
- Vincular os achados matemáticos aos teóricos da Eficácia Escolar:
  * **James Coleman (1966)**: Limites dos insumos materiais frente à determinação socioeconômica.
  * **Pierre Bourdieu**: Capital cultural familiar e estratificação social de partida (`MEDIA_INSE`).
  * **Soares & Alves (2003, 2013) / Crahay (2000)**: Centralidade do fator humano e estabilidade docente (`IRD_MEDIO`) como o verdadeiro "efeito-escola".
  * **Creso Franco**: Gestão escolar e capacidade de atenuar vulnerabilidades contextuais.

## Protocolo de Execução
1. Pausa e validação prévia com o pesquisador no chat.
2. Inserção modular no arquivo `reports/relatorio_metodologico_tcc.md`.
3. Verificação de integridade e clareza da redação acadêmica.

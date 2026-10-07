# Eficácia Escolar e Fatores de Gestão no Desempenho em Matemática do Ensino Médio Paulista: Uma Abordagem Preditiva e Explicável (2022–2024)

> **Trabalho de Conclusão de Curso (TCC)**  
> **Instituição:** Universidade Virtual do Estado de São Paulo (UNIVESP)  
> **População Analisada:** Universo Censitário de $N = 3.611$ Escolas Estaduais Paulistas de Ensino Médio Regular  
> **Período Focal:** Triênio 2022–2024  

---

## 📌 Visão Geral do Projeto

Este repositório abriga o pipeline de dados de ponta a ponta, a modelagem estatístico-preditiva de Machine Learning, as análises de explicabilidade por inteligência artificial (XAI - *SHAP*) e a documentação metodológica integral da pesquisa sobre os fatores determinantes do desempenho em Matemática no Sistema de Avaliação do Rendimento Escolar do Estado de São Paulo (SARESP).

Ancorado teoricamente na literatura de **Eficácia Escolar** (*School Effectiveness Research* — Coleman, Bourdieu, Soares & Alves, Franco), o projeto investiga a tensão clássica entre a primazia das condições socioeconômicas de origem dos estudantes e o papel amortecedor desempenhado por fatores intraescolares de gestão, organização do trabalho docente e infraestrutura física/tecnológica.

---

## 📁 Arquitetura do Repositório (Medallion & Modular)

O projeto adota a arquitetura de dados em camadas (*Medallion Architecture*) para assegurar governança estrita, rastreabilidade, imutabilidade dos dados brutos e total reprodutibilidade científica (Princípios *FAIR*):

```text
tcc_desempenho_escolar/
├── .agents/                               # Skills e protocolos de governança do agente IA
├── .venv/                                 # Ambiente virtual Python isolado
├── data/
│   ├── raw/                               # Microdados brutos imutáveis [ignorado no Git]
│   │   ├── 1. SEDUC-SP - SARESP & Cadastro de Escolas/
│   │   ├── 2. INEP - Indicadores Educacionais (Fluxo, Docentes, INSE)/
│   │   └── 3. INEP - Censo Escolar da Educação Básica (2022 e 2024)/
│   ├── silver/                            # Dados limpos, normalizados e padronizados (.parquet)
│   └── gold/                              # Bases consolidadas, matrizes analíticas e saídas de ML
│       ├── tcc_dataset_analitico_final.parquet (.csv) # Base analítica consolidada (N=3.611)
│       ├── matriz_features_modelagem.parquet          # Matriz de treino/teste de ML
│       ├── importancias_shap_random_forest.csv        # Contribuições marginais médias (|SHAP|)
│       └── matriz_priorizacao_politicas_publicas.csv  # Matriz acionável 2x2 para a SEDUC-SP
├── pipelines/                             # Códigos modulares de processamento e análise
│   ├── 01_Preparacao_censo/               # Extração, tipagem e filtros censitários
│   ├── 02_Indicadores_Educacionais_do_INEP/ # Tratamento de INSE, IRD, IED, AFD, ATU e ICU
│   ├── 03_SARESP_Cadastro_de_Escolas/     # Microdados de proficiência e cadastro SEDUC-SP
│   ├── 04_Consolidacao_Gold/              # Enriquecimento e merge determinístico (N=3.611)
│   ├── 05_Analise_Exploratoria_EDA/       # 7 etapas modulares de EDA e testes de hipóteses
│   ├── 06_Modelagem_Preditiva/            # Treinamento e validação de Baselines, RF e LightGBM
│   ├── 07_Explicabilidade_SHAP/           # Interpretabilidade global (Beeswarm) e local (Waterfall)
│   └── 08_Matriz_Politicas_Publicas/      # Síntese executiva e cruzamento Impacto vs Custo
├── reports/                               # Documentação monográfica e aparato visual
│   ├── figures/                           # 13 gráficos analíticos em alta resolução (300 DPI)
│   ├── metodos/                           # Cadernos de auditoria detalhada dos pipelines
│   ├── planejamento/                      # Planejamento estratégico e notas técnicas
│   ├── fundamentacao_teorica.md           # Marco teórico-conceitual de Eficácia Escolar
│   ├── relatorio_metodologico_tcc.md      # Registro formal de governança metodológica
│   ├── relatorio_final_tcc.md             # Monografia completa do TCC (Normas ABNT)
│   └── README.md                          # Guia de navegação interna da pasta reports
├── .gitignore
├── GEMINI.md                              # Protocolo de governança e cadência de pequenos passos
├── requirements.txt                       # Dependências exatas pinadas para o ambiente
└── README.md                              # Este arquivo
```

---

## ⚙️ Pré-requisitos e Configuração do Ambiente

O projeto foi construído utilizando **Python 3.10+** (validado até 3.14). Recomenda-se rigorosamente o uso de ambiente virtual isolado para prevenir inconsistências de pacotes.

### 1. Clonagem e Configuração do Ambiente Virtual (PowerShell no Windows)

```powershell
# 1. Navegar até a raiz do repositório
cd "D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar"

# 2. Criar o ambiente virtual isolado (.venv)
python -m venv .venv

# 3. Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

# 4. Atualizar o gerenciador de pacotes e instalar as dependências pinadas
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Principais Dependências Pinadas

* **Manipulação de Dados:** `pandas==3.0.6`, `pyarrow==25.0.1`, `numpy==2.5.3`
* **Modelagem Estatística e ML:** `scikit-learn==1.9.1`, `lightgbm==4.7.0`, `scipy==1.18.1`
* **Explicabilidade (XAI):** `shap==0.52.0`, `numba==0.67.0`
* **Visualização Gráfica:** `matplotlib==3.11.2`, `seaborn==0.13.2`

---

## 🚀 Guia de Reprodutibilidade Passo a Passo

Para reproduzir integralmente os tratamentos, análises exploratórias, modelos preditivos e matrizes acionáveis a partir dos dados originais, execute os scripts na ordem sequencial abaixo:

### Etapa 1: Consolidação da Camada Silver
```powershell
python pipelines/01_Preparacao_censo/01_limpar_censo_2022.py
python pipelines/01_Preparacao_censo/02_limpar_censo_2024.py
python pipelines/02_Indicadores_Educacionais_do_INEP/01_processar_indicadores_2022.py
python pipelines/02_Indicadores_Educacionais_do_INEP/02_processar_indicadores_2024.py
python pipelines/03_SARESP_Cadastro_de_Escolas/01_processar_saresp_proficiencia.py
```

### Etapa 2: Integração e Auditoria da Camada Gold
```powershell
python pipelines/04_Consolidacao_Gold/01_consolidar_base_gold.py
python pipelines/verificar_estrutura_trienal.py
```
*Saída gerada:* `data/gold/tcc_dataset_analitico_final.parquet` e `.csv` ($N = 3.611$ escolas estaduais).

### Etapa 3: Análise Exploratória de Dados (EDA Modular em 7 Passos)
```powershell
python pipelines/05_Analise_Exploratoria_EDA/01_distribuicao_target.py
python pipelines/05_Analise_Exploratoria_EDA/02_teste_hipotese_coleman_inse.py
python pipelines/05_Analise_Exploratoria_EDA/03_ranking_correlacoes.py
python pipelines/05_Analise_Exploratoria_EDA/04_fatores_docentes_ied_ird.py
python pipelines/05_Analise_Exploratoria_EDA/05_infraestrutura_e_tecnologia.py
python pipelines/05_Analise_Exploratoria_EDA/06_escolas_resilientes_efeito_escola.py
python pipelines/05_Analise_Exploratoria_EDA/07_portugues_vs_matematica.py
```
*Saídas geradas:* Figuras `eda_01` a `eda_07` salvas em `reports/figures/` (300 DPI).

### Etapa 4: Modelagem Preditiva e Benchmark de Algoritmos
```powershell
python pipelines/06_Modelagem_Preditiva/01_preparar_matriz_modelagem.py
python pipelines/06_Modelagem_Preditiva/02_treinar_baselines_lineares.py
python pipelines/06_Modelagem_Preditiva/03_treinar_random_forest.py
python pipelines/06_Modelagem_Preditiva/04_treinar_gradient_boosting.py
python pipelines/06_Modelagem_Preditiva/05_teste_sensibilidade_alvos_rf.py
```
*Métricas geradas:* Tabela comparativa, arquivo `data/gold/metricas_random_forest.csv` e `data/gold/comparativo_sensibilidade_alvos_rf.csv`.

### Etapa 5: Explicabilidade por SHAP (Interpretabilidade Global e Local)
```powershell
python pipelines/07_Explicabilidade_SHAP/01_analise_shap_random_forest.py
python pipelines/07_Explicabilidade_SHAP/02_analise_shap_waterfall_casos.py
```
*Saídas geradas:* Gráficos `shap_01` (Beeswarm), `shap_02` (Barras de Importância), `shap_03` e `shap_04` (Waterfall) em `reports/figures/`.

### Etapa 6: Construção da Matriz Acionável de Políticas Públicas
```powershell
python pipelines/08_Matriz_Politicas_Publicas/01_construir_matriz_acionavel.py
```
*Saídas geradas:* Gráfico executivo `matriz_01_politicas_publicas.png` e tabela `matriz_priorizacao_politicas_publicas.csv`.

---

## 📊 Síntese dos Resultados e Modelo Campeão

### 1. Benchmark Preditivo dos Modelos (Validação Cruzada 5-Fold Estratificada)

| Algoritmo | $R^2$ Médio | Desvio Padrão ($R^2$) | RMSE Médio | MAE Médio | Veredito Metodológico |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **OLS (Mínimos Quadrados)** | 23,09% | $\pm 0,0091$ | 3,385 | 2,429 | Baseline Linear Paramétrico |
| **Ridge Regression ($L_2$)** | 23,09% | $\pm 0,0091$ | 3,385 | 2,429 | Controle estrito de multicolinearidade |
| **Lasso Regression ($L_1$)** | 23,14% | $\pm 0,0090$ | 3,384 | 2,427 | Seleção esparsa de variáveis |
| **LightGBM Regressor** | 22,72% | $\pm 0,0194$ | 3,393 | 2,437 | Penalizado por ruído comportamental |
| 🏆 **Random Forest Regressor** | **24,08%** | **$\pm 0,0089$** | **3,363** | **2,398** | **Modelo Campeão Oficial** |

*Nota Epistemológica:* O modelo não-linear de *bagging* (Random Forest) superou as formulações lineares e o gradiente boosting, demonstrando robustez contra o ruído estocástico das avaliações censitárias em larga escala.

### 2. Hierarquia de Preditores Acionáveis (Importância Marginal Média via SHAP)

1. **Nível Socioeconômico Médio (`MEDIA_INSE`):** $+1,170$ p.p. no percentual de alunos no nível adequado de Matemática (ancoragem teórica em Coleman e Bourdieu).
2. **Índice de Regularidade Docente (`IRD_MEDIO`):** $+0,370$ p.p. — maior alavanca de gestão sob controle direto do Estado (estabilidade do corpo docente).
3. **Esforço Docente / Sobrecarga de Turmas (`IED_ESFORCO_ALTO`):** $+0,327$ p.p. — penalidade estrutural associada a professores alocados em mais de 4 turmas.
4. **Escala Escolar (`NUM_ESTUDANTES`):** $+0,149$ p.p. — benefício da desmassificação e modulação em escalas menores.
5. **Infraestrutura Digital / Hardware (Computadores + Lousas + Laboratórios):** $+0,132$ p.p. combinados — impacto marginal reduzido na ausência de metodologias ativas.

### 3. Matriz de Priorização para Tomada de Decisão Pública (SEDUC-SP)

* **Prioridade Estrutural (Alto Retorno, Baixo a Médio Esforço):** Fixação de docentes em escolas vulneráveis (redução da rotatividade) e estabelecimento de tetos de turmas por professor.
* **Estruturante de Longo Prazo (Alto Retorno, Alto Esforço):** Desmassificação das unidades escolares (escala humana).
* **Eficiência Marginal / Manutenção (Baixo Retorno, Baixo Custo):** Laboratórios de ciências com protocolos ativos e integração pedagógica de salas de leitura.
* **Baixa Relação Custo-Efetividade (Baixo Retorno, Elevado Investimento):** Aquisições massivas de computadores/tablets e lousas digitais desvinculadas de formação continuada e planos pedagógicos estruturados.

---

## 🛡️ Rigor Econométrico e Salvaguardas Éticas

1. **Prevenção Estrita de Vazamento de Alvo (*Target Leakage*):** O desempenho em Língua Portuguesa foi mantido exclusivamente no campo exploratório e epistemológico (EDA Passo 7, $r = +0,793$), sendo expressamente banido da matriz de treinamento de Machine Learning para evitar a canibalização dos efeitos de gestão e infraestrutura.
2. **Neutralização de Vazamento de Identificadores:** Identificadores administrativos espúrios (`CODESC`, `COD_MUN`) foram limpos da matriz preditiva, garantindo generalização real.
3. **Visão Sistêmica 360º:** O $R^2$ de $24,08\%$ é interpretado sob a ótica da sociologia da educação: cerca de três quartos da variância escolar residem em fatores contextuais não medidos (clima familiar, motivação individual, trajetórias prévias), legitimando o papel da escola como fator relevante, mas não onipotente.

---

## 📚 Navegação pela Documentação Acadêmica

* 📄 **Monografia Completa do TCC:** [`reports/relatorio_final_tcc.md`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/relatorio_final_tcc.md)
* 📋 **Relatório Metodológico e Auditoria:** [`reports/relatorio_metodologico_tcc.md`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/relatorio_metodologico_tcc.md)
* 📖 **Marco Teórico-Conceitual:** [`reports/fundamentacao_teorica.md`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/fundamentacao_teorica.md)
* 🖼️ **Catálogo de Gráficos Analíticos (300 DPI):** [`reports/figures/`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/figures)
* 🗺️ **Índice da Pasta de Relatórios:** [`reports/README.md`](file:///D:/TCC/Quinzena%203%20-%20Material%20e%20metodo/tcc_desempenho_escolar/reports/README.md)

---

## ⚖️ Licença e Uso de Dados

Os dados originais utilizados nesta pesquisa são de domínio público, disponibilizados pelo **Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP)** e pela **Secretaria da Educação do Estado de São Paulo (SEDUC-SP)**, em conformidade com a Lei de Acesso à Informação (Lei nº 12.527/2011) e com a Lei Geral de Proteção de Dados Pessoais (LGPD - Lei nº 13.709/2018), com agregação por unidade escolar e ausência de identificação individual de estudantes.

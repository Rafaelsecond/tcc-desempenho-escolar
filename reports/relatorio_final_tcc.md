# UNIVERSIDADE VIRTUAL DO ESTADO DE SÃO PAULO
## BACHARELADO EM CIÊNCIA DE DADOS

<br>

**ADEMILSON ACOSTA CIRINO – RA: 24217736**  
**EVERSON DOS SANTOS RODRIGUES – RA: 23223574**  
**LUCAS SILVA DE AQUINO – RA: 2217680**  
**RAFAEL PEIXOTO DE CARVALHO – RA: 23211013**  
**RODRIGO MATHEUS DE OLIVEIRA KOJIMA – RA: 23228077**  
**TARIK RIBEIRO CONSTÂNCIO CAMPESTRINI – RA: 2203974**  

<br><br><br>

# PREDIÇÃO DO DESEMPENHO EM MATEMÁTICA NA EDUCAÇÃO BÁSICA A PARTIR DE INDICADORES EDUCACIONAIS E SOCIOECONÔMICOS: UMA ABORDAGEM BASEADA EM CIÊNCIA DE DADOS

<br><br><br>

> **Vídeo de Apresentação do Trabalho de Conclusão de Curso**  
> *[Link a ser inserido na entrega final]*

<br><br><br>

**SÃO PAULO – SP**  
**2026**

---

<br>

# PREDIÇÃO DO DESEMPENHO EM MATEMÁTICA NA EDUCAÇÃO BÁSICA A PARTIR DE INDICADORES EDUCACIONAIS E SOCIOECONÔMICOS: UMA ABORDAGEM BASEADA EM CIÊNCIA DE DADOS

<br><br>

Relatório Técnico-Científico apresentado na disciplina de Trabalho de Conclusão de Curso do Bacharelado em Ciência de Dados da Universidade Virtual do Estado de São Paulo (UNIVESP).

**Grupo**: TCC530 – BCD – Turma 002  
**Orientador**: Prof. Me. Cássio Silva Takarada  

<br><br><br>

**SÃO PAULO – SP**  
**2026**

---

### FICHA CATALOGRÁFICA / REFERÊNCIA DO TRABALHO

CAMPESTRINI, T. R. C.; CIRINO, A. A.; AQUINO, L. S.; RODRIGUES, E. S.; KOJIMA, R. M. O.; CARVALHO, R. P. **Predição do desempenho em Matemática na Educação Básica a partir de indicadores educacionais e socioeconômicos: uma abordagem baseada em Ciência de Dados**. Relatório Técnico-Científico. Bacharelado em Ciência de Dados – Universidade Virtual do Estado de São Paulo. Orientador: Cássio Silva Takarada. São Paulo, 2026.

---

## RESUMO

A etapa final da Educação Básica brasileira enfrenta um histórico e persistente desafio na consolidação de competências quantitativas essenciais. No Estado de São Paulo, avaliações diagnósticas padronizadas revelam que expressiva parcela dos concluintes da 3ª série do Ensino Médio da rede pública estadual permanece retida em níveis críticos de proficiência em Matemática ("Abaixo do Básico"). Embora a literatura aponte forte determinação socioeconômica sobre o rendimento acadêmico, abordagens estritamente contextuais mostram-se deterministas e pouco acionáveis para formulação de políticas escolares. Este trabalho de conclusão de curso investiga, por meio de modelos de aprendizado de máquina supervisionado acoplados ao arcabouço de Inteligência Artificial Explicável (XAI), em que magnitude os fatores intraescolares controláveis — prioritariamente a regularidade do corpo docente (IRD), a sobrecarga de trabalho docente (IED) e a infraestrutura escolar instalada — atuam na mitigação da defasagem em Matemática. A base amostral integra microdados do SARESP (2022), Provão Paulista (2023 e 2024), Censo Escolar da Educação Básica e Indicadores Educacionais do INEP para as escolas estaduais paulistas. Adotou-se a Arquitetura Medalhão para engenharia de dados, fundamentando a adoção de 2023 como ano-pivô após validação empírica da estabilidade longitudinal dos fatores escolares ($r > 0,70$). Os modelos preditivos avaliados e a subsequente decomposição de Shapley (valores SHAP) visam identificar limiares críticos de proteção docente e subsidiar a construção de uma matriz diagnóstica acionável para tomada de decisão em Diretorias de Ensino.

**Palavras-chave**: Aprendizado de Máquina, Inteligência Artificial Explicável (XAI), SHAP, Desempenho Escolar, SARESP, Fatores Intraescolares.

---

## ABSTRACT

The final stage of Brazilian Basic Education faces a historical and persistent challenge in consolidating essential quantitative skills. In the State of São Paulo, standardized diagnostic assessments reveal that a substantial portion of public secondary school seniors remains trapped at critical proficiency levels in Mathematics ("Below Basic"). Although literature highlights strong socioeconomic conditioning over student achievement, purely contextual approaches provide deterministic and non-actionable frameworks for educational management. This capstone project investigates, using supervised machine learning models combined with Explainable Artificial Intelligence (XAI), to what extent controllable within-school factors — primarily teacher regularity (IRD), teacher workload (IED), and installed educational infrastructure — mitigate critical learning deficits in Mathematics. The analytical sample integrates microdata from SARESP (2022), Provão Paulista (2023 and 2024), Basic Education School Census, and INEP Educational Indicators across São Paulo state public schools. A Medallion Architecture was employed for data engineering, confirming 2023 as a representative pivot year through empirical longitudinal stability validation ($r > 0.70$). Predictive modeling and subsequent Shapley Additive Explanations (SHAP values) aim to identify protective thresholds for teacher stability and support an actionable diagnostic decision matrix for regional educational boards.

**Keywords**: Machine Learning, Explainable Artificial Intelligence (XAI), SHAP, School Performance, SARESP, Within-school Factors.

---

## LISTA DE ILUSTRAÇÕES

*Figura 1 – Arquitetura do Pipeline de Dados e Fluxo Metodológico Ponta a Ponta*  
*Figura 2 – Diagrama da Arquitetura Medalhão de Dados (Bronze, Silver e Gold)*  
*Figura 3 – Dispersão Interanual e Correlação de Pearson dos Indicadores Docentes (2022–2024)*  
*Figura 4 – Análise Exploratória: Distribuição da Variável-Alvo Trienal (% Abaixo do Básico)* *(Em desenvolvimento)*  
*Figura 5 – Curva de Desempenho e Comparativo das Métricas dos Modelos Preditivos* *(Previsto)*  
*Figura 6 – SHAP Summary Plot: Ranqueamento Global de Importância dos Fatores Escolares* *(Previsto)*  
*Figura 7 – SHAP Dependence Plot: Interação Bivariada entre Regularidade Docente (IRD) e Vulnerabilidade (INSE)* *(Previsto)*  

---

## LISTA DE TABELAS

*Tabela 1 – Cronograma Geral de Execução e Entregas Quinzenais do TCC*  
*Tabela 2 – Síntese das Fontes de Dados Governamentais Integradas*  
*Tabela 3 – Dicionário de Variáveis das Features Independentes ($X$)*  
*Tabela 4 – Funil Amostral de Seleção das Escolas Estaduais de Ensino Médio (SP)*  
*Tabela 5 – Estatísticas Descritivas e Validação da Estabilidade Trienal (2022–2024)*  
*Tabela 6 – Matriz de Correlação Interanual de Pearson ($r$) dos Fatores Escolares*  
*Tabela 7 – Métricas de Desempenho dos Algoritmos de Aprendizado Supervisionado* *(Previsto)*  
*Tabela 8 – Matriz Diagnóstica Acionável de Recomendações para a Gestão Escolar* *(Previsto)*  

---

## LISTA DE SIGLAS E ABREVIATURAS

| Sigla | Significado |
| :--- | :--- |
| **ABNT** | Associação Brasileira de Normas Técnicas |
| **AFD** | Adequação da Formação Docente |
| **CIE** | Cadastro de Informações Educacionais (Código Estadual da Escola) |
| **EDA** | *Exploratory Data Analysis* (Análise Exploratória de Dados) |
| **ETL** | *Extract, Transform, Load* (Extração, Transformação e Carga) |
| **IED** | Indicador de Esforço Docente |
| **INEP** | Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira |
| **INSE** | Indicador de Nível Socioeconômico das Escolas |
| **IRD** | Indicador de Regularidade do Corpo Docente |
| **LAI** | Lei de Acesso à Informação (Lei nº 12.527/2011) |
| **LGPD** | Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018) |
| **LightGBM**| *Light Gradient Boosting Machine* |
| **MAE** | *Mean Absolute Error* (Erro Médio Absoluto) |
| **RMSE** | *Root Mean Squared Error* (Raiz do Erro Quadrático Médio) |
| **SAEB** | Sistema de Avaliação da Educação Básica |
| **SARESP** | Sistema de Avaliação do Rendimento Escolar do Estado de São Paulo |
| **SEDUC-SP**| Secretaria da Educação do Estado de São Paulo |
| **SHAP** | *SHapley Additive exPlanations* |
| **UNIVESP**| Universidade Virtual do Estado de São Paulo |
| **XAI** | *Explainable Artificial Intelligence* (Inteligência Artificial Explicável) |

---

## SUMÁRIO

```text
1. INTRODUÇÃO
   1.1. Contextualização da Defasagem em Matemática no Ensino Médio Paulista
   1.2. Fatores Intraescolares versus Condicionantes Socioeconômicos
   1.3. Relevância da Inteligência Artificial Explicável (XAI) na Gestão Pública
   1.4. Organização do Documento

2. DELIMITAÇÃO DO PROBLEMA E OBJETIVOS
   2.1. Formulação da Pergunta-Problema
   2.2. Critérios de Demarcação do Campo de Estudo
   2.3. Hipóteses de Pesquisa
   2.4. Objetivos
        2.4.1. Objetivo Geral
        2.4.2. Objetivos Específicos

3. MATERIAIS E AMBIENTE COMPUTACIONAL
   3.1. Fontes de Dados e Arcabouço Jurídico-Institucional (LAI e LGPD)
   3.2. Caracterização das Bases e Dicionário de Atributos
   3.3. Infraestrutura Tecnológica e Bibliotecas Utilizadas

4. METODOLOGIA E ENGENHARIA DE DADOS
   4.1. Delineamento Metodológico da Pesquisa
   4.2. Arquitetura Medalhão de Dados
   4.3. Funil Amostral e Critérios de Elegibilidade
   4.4. Padronização de Chaves Primárias Duplas e Resolução de Inconsistências
   4.5. Engenharia de Atributos e Construção das Features (X)
   4.6. Validação Científica da Estabilidade Trienal do Ano-Pivô (2023)
   4.7. Agregação e Construção da Variável-Alvo Trienal (Y)
   4.8. Estratégia de Validação e Prevenção de Data Leakage
   4.9. Modelagem Preditiva Supervisionada
   4.10. Interpretabilidade e Explicabilidade Algorítmica via SHAP

5. DESENVOLVIMENTO E ANÁLISE EXPLORATÓRIA DOS DADOS [SEÇÃO VIVA]
   5.1. Perfil Sociodemográfico e de Infraestrutura das Unidades Escolares
   5.2. Análise Espacial e Assimetrias Regionais de Rendimento
   5.3. Correlações Lineares e Não-Lineares entre Insumos e Proficiência

6. RESULTADOS E DISCUSSÕES [PREVISTO - FASE DE MODELAGEM]
   6.1. Desempenho Comparativo dos Modelos Preditivos
   6.2. Importância Global dos Fatores Escolares via Valores SHAP
   6.3. O Efeito Moderador Protetivo da Estabilidade Docente
   6.4. Análise de Casos Locais e Diagnósticos Escolares

7. CONSIDERAÇÕES FINAIS E PROPOSTA DE APLICAÇÃO [PREVISTO]
   7.1. Síntese das Contribuições em Relação às Hipóteses
   7.2. Matriz Diagnóstica Acionável para Políticas Públicas Educacionais
   7.3. Limitações do Estudo e Direcionamentos Futuros

REFERÊNCIAS
APÊNDICE A – Dicionário Completo de Variáveis e Metadados
APÊNDICE B – Scripts dos Pipelines de Extração, Limpeza e Carga (ETL)
```

---

<br>

# 1. INTRODUÇÃO

## 1.1. Contextualização da Defasagem em Matemática no Ensino Médio Paulista

A etapa final da Educação Básica no Brasil vivencia desafios estruturais profundos e persistentes no que tange ao desenvolvimento e à consolidação de competências quantitativas fundamentais. No Estado de São Paulo — detentor da maior rede escolar pública da América Latina —, os resultados históricos de avaliações diagnósticas padronizadas em larga escala, com destaque para o Sistema de Avaliação do Rendimento Escolar do Estado de São Paulo (SARESP) e o recente Provão Paulista Seriado, revelam um cenário de severa estagnação: parcela expressiva dos estudantes concluintes da 3ª série do Ensino Médio encerra seu ciclo compulsório classificada nos níveis de proficiência "Abaixo do Básico" e "Básico".

Esse contingente de estudantes conclui a Educação Básica sem o domínio de operações matemáticas elementares, raciocínio lógico-algébrico e interpretação quantitativa de fenômenos cotidianos. Essa defasagem não apenas obstaculiza o ingresso e a permanência no ensino superior técnico e universitário, mas consolida barreiras quase intransponíveis para a inserção qualificada no mercado de trabalho formal, crescentemente pautado pela digitalização e pela tomada de decisão orientada a dados. Em última análise, a defasagem matemática crônica atua como um potente mecanismo de reprodução e aprofundamento das desigualdades socioeconômicas geracionais.

## 1.2. Fatores Intraescolares versus Condicionantes Socioeconômicos

A literatura clássica e contemporânea em Sociologia da Educação e Eficácia Escolar — desde o seminal Relatório Coleman até produções contemporâneas nacionais — converge em reconhecer que fatores exógenos à escola, com ênfase no nível socioeconômico das famílias (INSE), no capital cultural e na localização geográfica, exercem correlação preponderante sobre a variância do rendimento acadêmico dos estudantes.

Entretanto, limitar a lente analítica aos determinantes socioeconômicos produz uma perspectiva essencialmente determinista e de reduzida utilidade prática para a formulação e execução de políticas educacionais. O meio familiar e as condições econômicas dos estudantes fogem à governabilidade imediata da gestão escolar e dos órgãos executivos educacionais. Torna-se, por conseguinte, imperativo investigar e mensurar em que magnitude os **fatores intraescolares controláveis** — aqueles passíveis de intervenção deliberada por políticas públicas setoriais — são capazes de modular e atenuar a desvantagem socioeconômica de partida.

Entre esses fatores, ganham centralidade:
1. A **regularidade do corpo docente (IRD)**, representativa da permanência e continuidade dos professores na mesma unidade escolar ao longo dos anos letivos;
2. O **esforço e sobrecarga docente (IED)**, quantificado pelo número de turmas, escolas de atuação e turnos acumulados;
3. A **adequação da formação profissional (AFD)** dos docentes que lecionam o componente curricular de Matemática;
4. Os **recursos de infraestrutura escolar**, abrangendo conectividade tecnológica, laboratórios didáticos e condições físicas dos edifícios escolares.

## 1.3. Relevância da Inteligência Artificial Explicável (XAI) na Gestão Pública

A fundamentação técnica e acadêmica deste estudo assenta-se na mobilização de técnicas contemporâneas da Ciência de Dados para além da modelagem puramente preditiva. Modelos preditivos complexos baseados em aprendizado de máquina (como algoritmos de *ensemble learning* baseados em árvores de decisão) alcançam patamares superiores de acurácia em comparação com regressões paramétricas clássicas, todavia comportam-se como "caixas-pretas" (*black-boxes*), opacificando as relações funcionais subjacentes.

Para superar essa barreira epistêmica e viabilizar a aplicação dos resultados no setor público, incorpora-se o ferramental de **Inteligência Artificial Explicável (XAI)**, operacionalizado via valores SHAP (*SHapley Additive exPlanations*). Fundamentado na teoria dos jogos cooperativos, o método decompõe a contribuição marginal de cada atributo escolar na predição do desfecho de proficiência, preservando propriedades fundamentais de aditividade e consistência local. Essa abordagem permite quantificar não apenas a relevância global de cada fator, mas também desvelar não-linearidades e efeitos moderadores locais — avaliando, empiricamente, se e em que intensidade uma elevada estabilidade do corpo docente consegue exercer efeito protetivo em unidades escolares inseridas em contextos de severa vulnerabilidade socioeconômica.

## 1.4. Organização do Documento

Para proporcionar leitura fluida e alinhada ao rigor metodológico exigido pela Universidade Virtual do Estado de São Paulo (UNIVESP), este relatório técnico-científico está estruturado em sete capítulos principais:
- O **Capítulo 2 (Delimitação do Problema e Objetivos)** formaliza a questão norteadora, os limites temporais, espaciais e amostrais, as hipóteses estatísticas ($H_0, H_1, H_2$) e os objetivos geral e específicos.
- O **Capítulo 3 (Materiais e Ambiente Computacional)** discrimina detalhadamente as bases de dados governamentais utilizadas, o enquadramento legal de transparência e privacidade (LAI e LGPD), os dicionários de variáveis e a especificação completa do ferramental tecnológico adotado.
- O **Capítulo 4 (Metodologia e Engenharia de Dados)** apresenta o delineamento metodológico, a Arquitetura Medalhão empregada na pipeline, os testes de validação da estabilidade longitudinal das variáveis no triênio (2022–2024), o processo de engenharia de atributos e a parametrização dos modelos preditivos e do arcabouço SHAP.
- O **Capítulo 5 (Desenvolvimento e Análise Exploratória dos Dados)** compõe a seção viva do relatório, documentando os resultados parciais da limpeza, consolidação relacional, estatísticas descritivas e análises bivariadas espaciais e contextuais.
- O **Capítulo 6 (Resultados e Discussões)** sintetizará a performance preditiva dos modelos supervisionados, o ranqueamento de importância via SHAP e a verificação empírica das hipóteses formuladas.
- O **Capítulo 7 (Considerações Finais e Proposta de Aplicação)** sintetiza as conclusões da pesquisa, apresenta a proposta de Matriz Diagnóstica para a gestão educacional, debate as limitações do estudo e sinaliza caminhos para trabalhos futuros.

---

<br>

# 2. DELIMITAÇÃO DO PROBLEMA E OBJETIVOS

## 2.1. Formulação da Pergunta-Problema

Com base no cenário diagnosticado, formula-se a seguinte questão de pesquisa norteadora:

> *"Em que magnitude os fatores intraescolares controláveis — prioritariamente a regularidade do corpo docente (IRD), a adequação formativa e os recursos de infraestrutura pedagógica — atenuam a probabilidade de defasagem crítica em Matemática (nível Abaixo do Básico) entre os concluintes da 3ª série do Ensino Médio da rede pública estadual paulista, após o controle dos condicionantes socioeconômicos?"*

## 2.2. Critérios de Demarcação do Campo de Estudo

- **Delimitação Populacional**: Estabelecimentos públicos de ensino vinculados exclusivamente à rede estadual administrada pela Secretaria da Educação do Estado de São Paulo (SEDUC-SP).
- **Objeto e Unidade Observacional**: A unidade de análise é a **escola**, permitindo articular agregados contextuais institucionais com distribuições de proficiência sem violar o sigilo individual dos estudantes, atendendo estritamente à LGPD.
- **Público-Alvo**: Alunos matriculados e avaliados nas turmas regulares ativas da 3ª série do Ensino Médio.
- **Delimitação Espacial**: Estado de São Paulo, abrangendo as unidades distribuídas na Capital, Região Metropolitana de São Paulo e Interior, contemplando as 91 Diretorias Regionais de Ensino.
- **Delimitação Temporal**: Recorte trienal consolidado pós-pandêmico (2022, 2023 e 2024), capturando tanto a transição dos modelos avaliativos (SARESP tradicional para Provão Paulista Seriado) quanto a evolução dos indicadores contextuais federais.

## 2.3. Hipóteses de Pesquisa

Para guiar a modelagem estatística e a interpretação causal orientada por XAI, estabelecem-se as seguintes hipóteses:

- **Hipótese Nula ($H_0$)**: Os fatores intraescolares controláveis (regularidade docente, esforço docente e infraestrutura física/tecnológica) não exercem contribuição marginal estatisticamente relevante na predição do percentual de estudantes no nível Abaixo do Básico em Matemática, sendo o desfecho acadêmico explicado preponderantemente pelo nível socioeconômico (INSE).
- **Hipótese Principal ($H_1$)**: Unidades escolares que sustentam maior regularidade docente (alto IRD) e menor sobrecarga de esforço (baixo IED) exibem percentuais significativamente menores de estudantes no padrão Abaixo do Básico, mantendo-se essa relação mesmo após o controle estrito do nível socioeconômico da unidade.
- **Hipótese Secundária ($H_2$)**: A regularidade docente atua como um fator moderador protetivo, amortecendo o efeito adverso da alta vulnerabilidade socioeconômica (baixo INSE) nas escolas periféricas e atenuando o percentual de defasagem crítica.

## 2.4. Objetivos

### 2.4.1. Objetivo Geral
Investigar e quantificar a influência dos fatores intraescolares controláveis na mitigação da defasagem crítica em Matemática entre concluintes do Ensino Médio da rede pública estadual paulista (2022–2024), mediante a aplicação de modelos de aprendizado de máquina supervisionado e algoritmos de Inteligência Artificial Explicável (XAI).

### 2.4.2. Objetivos Específicos
1. **Integrar e tratar microdados educacionais públicos**: Construir uma base relacional unificada por escola, cruzando chaves estaduais (CIE) e federais (INEP), consolidando atributos do Censo Escolar, indicadores docentes do INEP (IRD, IED, INSE) e os desfechos de proficiência do SARESP (2022) e Provão Paulista (2023 e 2024).
2. **Validar a consistência temporal dos dados**: Testar a estabilidade longitudinal dos indicadores escolares entre 2022 e 2024 para justificar matematicamente a escolha do ano de 2023 como pivô representativo das variáveis independentes ($X$).
3. **Mapear assimetrias espaciais e socioeducacionais**: Executar análise exploratória espacial e tabular para caracterizar a heterogeneidade da rede estadual quanto à regularidade docente, infraestrutura tecnológica e taxas de defasagem em Matemática.
4. **Treinar e comparar modelos preditivos supervisionados**: Ajustar algoritmos lineares regularizados e modelos baseados em árvores de decisão (*Random Forest*, *LightGBM*), avaliando-os sob validação cruzada estratificada em $k$-folds para prevenir vazamento de dados (*data leakage*).
5. **Decompor as contribuições marginais com SHAP**: Mensurar os impactos globais e locais das variáveis escolares e estimar a curva de dependência e moderação entre regularidade docente e vulnerabilidade socioeconômica.
6. **Propor uma matriz diagnóstica acionável**: Estruturar um modelo conceitual de suporte à decisão para gestores educacionais e Diretorias de Ensino, traduzindo as inferências do modelo em subsídios de alocação de pessoal e infraestrutura.

---

<br>

# 3. MATERIAIS E AMBIENTE COMPUTACIONAL

## 3.1. Fontes de Dados e Arcabouço Jurídico-Institucional (LAI e LGPD)

A integridade metodológica e a legitimidade ética da pesquisa fundamentam-se na utilização exclusiva de **dados públicos abertos e desidentificados**, obtidos diretamente dos repositórios oficiais governamentais:
- **Secretaria da Educação do Estado de São Paulo (SEDUC-SP)**: Portal de Dados Abertos (`dados.educacao.sp.gov.br`), de onde foram extraídos o Cadastro Oficial de Escolas Ativas e os microdados de desempenho escolar (SARESP 2022 e Provão Paulista 2023–2024);
- **Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP)**: Portal de Dados Abertos (`gov.br/inep`), fonte dos microdados do Censo Escolar da Educação Básica e dos Indicadores Educacionais Especializados (INSE, IRD, IED e AFD).

A extração e manipulação dos dados atendem com rigor à **Lei de Acesso à Informação (Lei Federal nº 12.527/2011)**, assegurando publicidade e transparência da informação estatal. Adicionalmente, em conformidade com a **Lei Geral de Proteção de Dados Pessoais (LGPD - Lei Federal nº 13.709/2018)**, todas as agregações de desempenho e proficiência foram efetuadas na granularidade da **unidade escolar** (escola), com eliminação de identificadores individuais de estudantes (nome, CPF, RA discente), inviabilizando qualquer processo de reidentificação ou estigmatização de sujeitos.

*Tabela 2 – Síntese das Fontes de Dados Governamentais Integradas*

| Órgão Produtor | Base / Indicador | Granularidade Original | Período Coletado | Chave Identificadora |
| :--- | :--- | :--- | :---: | :--- |
| **SEDUC-SP** | Cadastro de Escolas Ativas | Unidade Escolar | 2023 | `CD_ESCOLA` (CIE) / `CD_INEP` |
| **SEDUC-SP** | Microdados SARESP | Aluno / Turma | 2022 | `CD_ESCOLA` / `SERIE_ANO` |
| **SEDUC-SP** | Microdados Provão Paulista | Aluno | 2023 e 2024 | `CODESC` / `SERIE_ANO` |
| **INEP** | Censo Escolar (Educação Básica)| Escola / Matrícula | 2022, 2023, 2024| `CO_ENTIDADE` (8 dígitos) |
| **INEP** | Nível Socioeconômico (INSE) | Escola | 2021 (Saeb 2021) | `CO_ESCOLA` |
| **INEP** | Regularidade Docente (IRD) | Escola | 2022, 2023, 2024| `CO_ENTIDADE` |
| **INEP** | Esforço Docente (IED) | Escola | 2022, 2023, 2024| `CO_ENTIDADE` |
| **INEP** | Adequação Formativa (AFD) | Escola | 2022, 2023, 2024| `CO_ENTIDADE` |

*Fonte: Elaborado pelos autores (2026).*

## 3.2. Caracterização das Bases e Dicionário de Atributos

As variáveis independentes ($X$) e dependentes ($Y$) foram estruturadas em grupos semânticos homogêneos para alimentar os modelos preditivos:

*Tabela 3 – Dicionário de Variáveis das Features Independentes ($X$)*

| Domínio | Nome da Variável | Tipo | Descrição Técnica e Operacionalização |
| :--- | :--- | :--- | :--- |
| **Identificação** | `CO_ENTIDADE` | `string` | Código de identificação federal da escola no INEP (8 dígitos). |
| **Identificação** | `CODESC` | `string` | Código de identificação estadual da escola na SEDUC (6 dígitos). |
| **Geográfico** | `NOMEMUN` / `NM_MUNICIPIO` | `string` | Município de localização da unidade escolar no Estado de SP. |
| **Geográfico** | `DS_LATITUDE` / `DS_LONGITUDE` | `float64` | Coordenadas geográficas padronizadas em graus decimais. |
| **Infraestrutura** | `QT_SALAS_UTILIZADAS` | `int64` | Número de salas de aula ativas utilizadas no funcionamento regular. |
| **Infraestrutura** | `QT_COMP_ALUNO` | `int64` | Total de computadores (desktop e portáteis) para uso exclusivo de alunos. |
| **Infraestrutura** | `IN_INTERNET_BANDA_LARGA` | `int64` | Indicador binário de presença de internet de alta velocidade na unidade. |
| **Infraestrutura** | `IN_LABORATORIO_INFORMATICA`| `int64` | Indicador binário de presença de laboratório de informática escolar. |
| **Infraestrutura** | `IN_LABORATORIO_CIENCIAS` | `int64` | Indicador binário de presença de laboratório de ciências da natureza. |
| **Contexto Docente** | `IRD_VALOR` | `float64` | Indicador de Regularidade do Corpo Docente no Ensino Médio (0.0 a 5.0). |
| **Contexto Docente** | `IED_SCORE_MEDIO` | `float64` | Score médio ponderado de esforço docente no Ensino Médio (1.0 a 6.0). |
| **Contexto Docente** | `IED_ESFORCO_ALTO` | `float64` | Percentual de docentes da escola enquadrados nos níveis 5 e 6 de sobrecarga. |
| **Socioeconômico** | `INSE_VALOR_ABSOLUTO` | `float64` | Média contínua padronizada do nível socioeconômico da escola (Saeb). |
| **Socioeconômico** | `INSE_CLASSIFICACAO` | `string` | Classificação ordinal do nível socioeconômico (Grupo I a VI). |

*Fonte: Elaborado pelos autores (2026).*

A **variável-alvo dependente ($Y$)** corresponde à proporção agregada de alunos concluintes da 3ª série do Ensino Médio que obtiveram desempenho insuficiente em Matemática:
$$\text{PERC\_ABAIXO\_TRIENAL} = \frac{\sum_{t \in \{2022, 2023, 2024\}} \text{Alunos\_Abaixo}_{t}}{\sum_{t \in \{2022, 2023, 2024\}} \text{Alunos\_Avaliados}_{t}} \times 100$$

## 3.3. Infraestrutura Tecnológica e Bibliotecas Utilizadas

O pipeline de dados e os experimentos computacionais foram desenvolvidos em linguagem **Python (versão 3.11+)**, estruturados no ambiente de desenvolvimento integrado (IDE) e gerenciados sob controle de versão Git/GitHub:
- **Engenharia e Processamento Tabular**: `pandas` (leitura, limpeza e transformação) acoplado ao motor `pyarrow` para persistência e serialização de alto desempenho no formato **Apache Parquet**;
- **Computação Científica e Estatística**: `numpy` e `scipy.stats` (para estimativas paramétricas, testes de normalidade e correlações bivariadas);
- **Visualização Analítica**: `matplotlib` e `seaborn` para produção de figuras vetoriais de alta resolução gráfica (300 DPI);
- **Modelagem Preditiva**: `scikit-learn` (pré-processamento, imputação estatística, padronização, validação cruzada $k$-fold e algoritmos de regressão/árvores) e `lightgbm` (modelo de *gradient boosting* otimizado para árvores de decisão);
- **Inteligência Artificial Explicável (XAI)**: biblioteca `shap` para cálculo exato de valores de Shapley (*TreeExplainer*), visualizações de ranqueamento global (*summary plot*) e curvas de dependência de efeitos moderadores (*dependence plot*).

---

<br>

# 4. METODOLOGIA E ENGENHARIA DE DADOS

## 4.1. Delineamento Metodológico da Pesquisa

Esta investigação classifica-se como de **natureza quantitativa e aplicada**, com objetivos **descritivos, explicativos e prescritivos**. O procedimento técnico adota a pesquisa documental a partir de dados secundários abertos do poder público, guiada pelo ciclo de vida formal da Ciência de Dados:
1. Ingestão e perfilamento de dados brutos (*Data Profiling*);
2. Limpeza, padronização e enriquecimento (*ETL*);
3. Validação estatística longitudinal das hipóteses metodológicas;
4. Modelagem preditiva supervisionada multialgorítmica;
5. Interpretação algorítmica por explicabilidade pós-hoc (*XAI*);
6. Proposição de matriz prescritiva para políticas públicas.

## 4.2. Arquitetura Medalhão de Dados

Para garantir **auditabilidade, reproducibilidade e isolamento de dependências** no processamento de dezenas de gigabytes de microdados educacionais, adotou-se o padrão da **Arquitetura Medalhão (Medallion Architecture)**:

```mermaid
flowchart LR
    subgraph Bronze["1. Camada Bronze (Raw)"]
        B1["Censo Escolar SP (.csv)"]
        B2["Indicadores INEP (.xlsx/.csv)"]
        B3["SARESP e Provão Paulista (.csv)"]
    end

    subgraph Silver["2. Camada Silver (Cleaned)"]
        S1["01_escolas_base.parquet"]
        S2["02_indicadores_inep.parquet"]
        S3["03_saresp_2022_escola.parquet"]
        S4["04_05_provao_escola.parquet"]
        S5["06_target_trienal.parquet"]
    end

    subgraph Gold["3. Camada Gold (Analytical)"]
        G1["tcc_dataset_analitico_final.parquet"]
        G2["Feature Store (X) + Target (Y)"]
    end

    B1 --> S1
    B2 --> S2
    B3 --> S3 & S4
    S3 & S4 --> S5
    S1 & S2 & S5 --> G1 --> G2
```

- **Camada Bronze (Raw)**: Repositório somente-leitura dos arquivos brutos baixados diretamente do INEP e da SEDUC-SP, mantidos sem qualquer alteração manual.
- **Camada Silver (Padronizada e Validada)**: Conjunto de tabelas intermediárias processadas por domínio temático. Cada script de pipeline é responsável exclusivo por uma fonte, padronizando chaves primárias, tratando codificações de caracteres, saneando valores nulos e gerando artefatos compactados em `.parquet`.
- **Camada Gold (Analítica / Feature Store)**: Base tabular final unificada no nível da escola, contendo exclusivamente unidades que satisfazem os critérios amostrais estatísticos, contendo todas as variáveis preditoras ($X$) e a variável-alvo trienal ponderada ($Y$).

## 4.3. Funil Amostral e Critérios de Elegibilidade

A delimitação exata da população escolar paulista obedeceu a um funil de filtragem rigoroso implementado sobre o Censo Escolar da Educação Básica (ano-base 2023):

*Tabela 4 – Funil Amostral de Seleção das Escolas Estaduais de Ensino Médio (SP)*

| Etapa | Critério de Filtragem Aplicado | Registros Resultantes | Redução Relativa |
| :---: | :--- | :---: | :---: |
| 1 | Universo Brasil de Estabelecimentos de Ensino Básico (2023) | 217.625 | – |
| 2 | Filtragem por Unidade da Federação (`SG_UF == 'SP'`) | 34.099 | -84,33% |
| 3 | Filtragem por Dependência Administrativa Estadual (`TP_DEPENDENCIA == 2`) | 6.524 | -80,87% |
| 4 | Filtro de Funcionamento Ativo (`TP_SITUACAO_FUNCIONAMENTO == 1`) | 5.750 | -11,86% |
| 5 | Filtro de Ensino Regular Ativo (`IN_REGULAR == 1`) | 5.400 | -6,09% |
| 6 | Oferta Ativa de Ensino Médio Regular (`IN_MED == 1`) | 3.964 | -26,59% |
| 7 | **Cruzamento Relacional com Cadastro Oficial SEDUC-SP** | **3.734** | -5,80% |

*Fonte: Elaborado pelos autores (2026).*

As **3.734 escolas** constituem a espinha dorsal (*spine*) definitiva de análise institucional.

## 4.4. Padronização de Chaves Primárias Duplas e Resolução de Inconsistências

Durante a execução dos pipelines da Camada Silver, foram identificadas e solucionadas inconsistências fundamentais de engenharia de dados:
1. **Padronização das Chaves Primárias**:
   - Código Estadual da Escola (CIE / `CODESC`): Convertido para string de texto padronizada em **6 dígitos** preenchidos com zeros à esquerda (`zfill(6)`), por exemplo, `"000024"`.
   - Código Federal da Escola (INEP / `CO_ENTIDADE`): Convertido para string de texto em **8 dígitos** (`zfill(8)`), por exemplo, `"35000024"`.
   - Verificou-se a relação determinística estrutural para o Estado de São Paulo:
     $$\text{CO\_ENTIDADE} = \text{"35"} + \text{CODESC}$$
2. **Correção do Bug Numérico de Escala do IRD**: Na base de dados aberta em formato textual/CSV, o Indicador de Regularidade Docente apresentava valores distorcidos em ordens de trilhões (`2.739.558.666...`) em virtude da conversão inadequada de separadores de milhar e decimais do padrão brasileiro. O saneamento foi implementado consumindo diretamente o arquivo oficial `.xlsx` com o cabeçalho técnico localizado na linha 10 (`header=10`), restaurando com sucesso a escala contínua canônica do indicador entre **0.0 e 5.0**.
3. **Tratamento do Byte Order Mark (BOM)**: Identificou-se a presença de cabeçalhos ocultos corrompidos (`ï»¿NOMEDEP`) nas exportações de dados da SEDUC-SP originadas de ambientes Windows, devidamente saneados nos scripts via leitura com codificação `utf-8-sig`.

## 4.5. Engenharia de Atributos e Construção das Features (X)

A engenharia de atributos sintetizou variáveis primárias em métricas compostas:
- **Tecnologia por Aluno**: Totalização de infraestrutura de computação discente:
  $$\text{QT\_COMP\_ALUNO} = \text{QT\_DESKTOP\_ALUNO} + \text{QT\_COMP\_PORTATIL\_ALUNO}$$
- **Score Ponderado de Esforço Docente (IED Médio)**: O INEP categoriza o esforço docente no Ensino Médio em 6 níveis ordinais crescentes de sobrecarga (`MED_CAT_1` a `MED_CAT_6`). Sintetizou-se um índice contínuo contido no intervalo $[1,0; 6,0]$:
  $$\text{IED\_SCORE\_MEDIO} = \frac{\sum_{i=1}^{6} i \cdot \text{MED\_CAT\_i}}{100}$$
- **Sobrecarga Extrema de Esforço Docente**: Percentual acumulado de docentes da escola nos níveis 5 e 6 de esforço (professores que lecionam em 3 turnos, com mais de 300 alunos ou em múltiplas escolas):
  $$\text{IED\_ESFORCO\_ALTO} = \text{MED\_CAT\_5} + \text{MED\_CAT\_6}$$

## 4.6. Validação Científica da Estabilidade Trienal do Ano-Pivô (2023)

Uma das decisões metodológicas basilares deste estudo foi a seleção de **2023 como ano-pivô representativo** dos fatores intraescolares independentes ($X$). Para conferir sustentação empírica a essa escolha e comprovar que as características de infraestrutura e do corpo docente não sofreram flutuações estruturais espúrias no triênio, executou-se uma **validação longitudinal estrita sobre as 3.691 escolas estaduais presentes simultaneamente nos três anos avaliados (2022, 2023 e 2024)**.

*Tabela 5 – Estatísticas Descritivas e Validação da Estabilidade Trienal (2022–2024)*

| Indicador Escolar | Média 2022 (±DP) | Média 2023 (±DP) | Média 2024 (±DP) | Variação Global (22–24) |
| :--- | :---: | :---: | :---: | :---: |
| **IRD (Regularidade Docente)** | 2,64 (±0,46) | 2,65 (±0,45) | 2,54 (±0,46) | -0,10 (-3,79%) |
| **IED (Score Médio de Esforço)**| 3,71 (±0,56) | 3,69 (±0,46) | 3,68 (±0,45) | -0,03 (-0,81%) |
| **Salas de Aula Utilizadas** | 13,14 (±4,58) | 13,29 (±4,55) | 13,30 (±4,52) | +0,16 (+1,22%) |
| **Computadores para Alunos** | 43,13 (±31,60) | 68,04 (±49,87) | 86,94 (±59,70) | Expansão planejada |

*Fonte: Elaborado pelos autores (2026).*

*Tabela 6 – Matriz de Correlação Interanual de Pearson ($r$) dos Fatores Escolares*

| Indicador Escolar | $r$ (2022–2023) | $r$ (2023–2024) | $r$ (2022–2024) | Interpretação Científica |
| :--- | :---: | :---: | :---: | :--- |
| **Salas de Aula Utilizadas** | **0,968** | **0,966** | **0,949** | Estabilidade física estrutural quase perfeita |
| **IRD (Regularidade Docente)** | **0,856** | **0,911** | **0,715** | Altíssima persistência temporal do corpo docente |
| **IED (Score Médio de Esforço)**| **0,706** | **0,730** | **0,684** | Forte consistência na alocação de carga horária |
| **Computadores para Alunos** | **0,547** | **0,616** | **0,446** | Dinâmica evolutiva decorrente do programa da SEDUC |

*Fonte: Elaborado pelos autores (2026).*

A altíssima correlação linear de Pearson ($r > 0,70$ em todos os indicadores estruturais e docentes) valida cientificamente que as características das escolas no ano de 2023 representam com extrema fidelidade a realidade institucional do triênio avaliado, afastando riscos de viés temporal na modelagem preditiva.

## 4.7. Agregação e Construção da Variável-Alvo Trienal (Y)

A consolidação de $Y$ agregou os microdados discentes dos exames censitários de Matemática da 3ª série do Ensino Médio:
1. **SARESP 2022**: Extração dos alunos com participação e proficiência válidas em Matemática;
2. **Provão Paulista 2023 e 2024**: Extração e calibração das notas padronizadas do exame estadual unificado;
3. **Ponderação pelo Volume de Avaliados**: Cálculo da proporção ponderada de alunos no padrão crítico de proficiência;
4. **Filtro de Corte Amostral**: Exclusão de microclasses e unidades com menos de 10 a 15 alunos avaliados no acumulado trienal, expurgando ruídos provenientes de unidades prisionais, centros socioeducativos ou classes hospitalares.

## 4.8. Estratégia de Validação e Prevenção de Data Leakage

Para prevenir vazamento de dados (*data leakage*) e assegurar generalização robusta:
- **Particionamento Estratificado**: Divisão da base analítica em subconjuntos de Treino (80%) e Teste (20%), estratificados por quintis de vulnerabilidade socioeconômica (`INSE`) e Diretorias Regionais de Ensino;
- **Validação Cruzada em $k$-Folds ($k=5$)**: Todo ajuste de hiperparâmetros e imputação de variáveis faltantes é realizado estritamente dentro dos folds de treino;
- **Desacoplamento Causal**: Nenhuma métrica derivada de exames posteriores ou indicadores de fluxo pós-evento é utilizada como preditor de entrada.

## 4.9. Modelagem Preditiva Supervisionada

Serão treinados e comparados três algoritmos de complexidades complementares:
1. **Regressão Ridge e Lasso (Lineares Regularizadas)**: Modelo de referência linear para captura de efeitos aditivos diretos;
2. **Random Forest Regressor**: Algoritmo de *ensemble* baseado em ensacamento (*bagging*) de árvores de decisão, capaz de capturar relações não-lineares;
3. **LightGBM Regressor**: Algoritmo de *gradient boosting* baseado em crescimento foliar (*leaf-wise*), altamente eficiente para dados tabulares com interações complexas.

As métricas formais de avaliação adotadas serão o Coeficiente de Determinação ($R^2$), a Raiz do Erro Quadrático Médio (RMSE) e o Erro Médio Absoluto (MAE).

## 4.10. Arcabouço de Interpretabilidade e Explicabilidade Algorítmica via SHAP

Para romper a opacidade do melhor modelo preditivo, será implementado o framework SHAP (*SHapley Additive exPlanations*):
- **Importância Global (*SHAP Summary Plot*)**: Ranqueamento da magnitude absoluta média dos valores de Shapley ($E[|\phi_j|]$), contrastando a relevância dos fatores intraescolares em relação ao INSE;
- **Interação Local (*SHAP Dependence Plot*)**: Análise detalhada da relação bidirecional entre o IRD e o INSE, identificando empiricamente os limiares em que a estabilidade do professor atenua o efeito adverso da desvantagem socioeconômica.

---

<br>

# 5. DESENVOLVIMENTO E ANÁLISE EXPLORATÓRIA DOS DADOS [SEÇÃO VIVA]

> *Nota Técnica: Esta seção é atualizada continuamente conforme a execução dos scripts 03 a 07 da pipeline na pasta `reports/`.*

## 5.1. Perfil Sociodemográfico e de Infraestrutura das Unidades Escolares

A análise preliminar da base Silver de escolas (`01_escolas_base.parquet`) e indicadores (`02_indicadores_inep.parquet`) demonstra expressiva heterogeneidade na rede pública estadual paulista:
- **Cobertura do INSE**: O Indicador de Nível Socioeconômico cobre **96,9%** das escolas estaduais elegíveis (3.618 unidades de 3.734). A distribuição concentra-se majoritariamente nos Grupos III e IV do INEP, revelando um perfil de vulnerabilidade moderada a alta;
- **Regularidade Docente (IRD)**: A média estadual do IRD situou-se em **2,65 (±0,45)** na escala de 0 a 5, com cobertura de **99,7%** das unidades escolares;
- **Esforço Docente (IED)**: A média estadual do score ponderado de esforço alcançou **3,69 (±0,46)**, evidenciando que os docentes de Ensino Médio enfrentam, em média, sobrecarga intermediária a alta (múltiplas turmas e turnos).

## 5.2. Análise Espacial e Assimetrias Regionais de Rendimento

*(Em consolidação a partir dos dados do SARESP 2022 e Provão Paulista 2023–2024)*

## 5.3. Correlações Lineares e Não-Lineares entre Insumos e Proficiência

*(Em consolidação após execução da junção relacional na Camada Gold)*

---

<br>

# 6. RESULTADOS E DISCUSSÕES [PREVISTO - FASE DE MODELAGEM]

> *Nota Técnica: Esta seção receberá os resultados consolidados do treinamento dos modelos de Machine Learning e da decomposição de explicabilidade via SHAP (Quinzena 5).*

## 6.1. Desempenho Comparativo dos Modelos Preditivos
*(Métricas $R^2$, RMSE e MAE para Ridge, Random Forest e LightGBM).*

## 6.2. Importância Global dos Fatores Escolares via Valores SHAP
*(Identificação do peso relativo da estabilidade docente versus fatores socioeconômicos).*

## 6.3. O Efeito Moderador Protetivo da Estabilidade Docente
*(Verificação empírica da Hipótese H2).*

## 6.4. Análise de Casos Locais e Diagnósticos Escolares
*(Decomposição em cascata de escolas de alta e baixa eficácia sob mesmo contexto socioeconômico).*

---

<br>

# 7. CONSIDERAÇÕES FINAIS E PROPOSTA DE APLICAÇÃO [PREVISTO]

> *Nota Técnica: Esta seção receberá a síntese conclusiva e a Matriz Diagnóstica para subsidiar Diretorias de Ensino (Quinzena 6).*

## 7.1. Síntese das Contribuições em Relação às Hipóteses
## 7.2. Matriz Diagnóstica Acionável para Políticas Públicas Educacionais
## 7.3. Limitações do Estudo e Direcionamentos Futuros

---

<br>

# REFERÊNCIAS

1. BRASIL. Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP). **Nota Técnica nº 037/2014: Indicador de Esforço Docente da Educação Básica (IED)**. Brasília, DF: INEP, 2014. Disponível em: `https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/esforco-docente`. Acesso em: 02 set. 2026.
2. BRASIL. Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP). **Nota Técnica nº 038/2015: Indicador de Regularidade do Corpo Docente da Educação Básica (IRD)**. Brasília, DF: INEP, 2015. Disponível em: `https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/regularidade-do-corpo-docente`. Acesso em: 02 set. 2026.
3. BRASIL. Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP). **Nota Técnica nº 064/2021: Indicador de Nível Socioeconômico das Escolas de Educação Básica (INSE) 2021**. Brasília, DF: INEP, 2021. Disponível em: `https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico`. Acesso em: 02 set. 2026.
4. BRASIL. Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP). **Censo Escolar da Educação Básica: Caderno de Instruções e Variáveis de Infraestrutura**. Brasília, DF: INEP, 2023. Disponível em: `https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar`. Acesso em: 02 set. 2026.
5. BRASIL. **Lei nº 12.527, de 18 de novembro de 2011**. Regula o acesso a informações previsto no inciso XXXIII do art. 5º, no inciso II do § 3º do art. 37 e no § 2º do art. 216 da Constituição Federal. Brasília, DF: Presidência da República, 2011.
6. BRASIL. **Lei nº 13.709, de 14 de agosto de 2018**. Lei Geral de Proteção de Dados Pessoais (LGPD). Brasília, DF: Presidência da República, 2018.
7. COLEMAN, James S. et al. **Equality of Educational Opportunity**. Washington, D.C.: U.S. Department of Health, Education, and Welfare, 1966.
8. FACELI, Katti; LORENA, Ana Carolina; GAMA, João; ALMEIDA, Tiago Agostinho de; CARVALHO, André C. P. L. F. **Inteligência Artificial: Uma Abordagem de Aprendizado de Máquina**. 2. ed. Rio de Janeiro: LTC, 2021.
9. LUNDBERG, Scott M.; LEE, Su-In. A unified approach to interpreting model predictions. In: **Advances in Neural Information Processing Systems (NeurIPS)**, v. 30, p. 4765–4774, 2017.
10. RUSSELL, Stuart; NORVIG, Peter. **Inteligência Artificial: Uma Abordagem Moderna**. 4. ed. Rio de Janeiro: GEN LTC, 2022.
11. SÃO PAULO (Estado). Secretaria da Educação do Estado de São Paulo (SEDUC-SP). **Relatório Pedagógico SARESP 2023: Desempenho e Padrões de Proficiência em Matemática no Ensino Médio**. São Paulo: SEDUC-SP/CIMA, 2024. Disponível em: `https://dados.educacao.sp.gov.br`. Acesso em: 02 set. 2026.

---

<br>

# APÊNDICE A – Dicionário Completo de Variáveis e Metadados
*(A ser alimentado com as especificações integrais das tabelas Gold).*

<br>

# APÊNDICE B – Scripts dos Pipelines de Extração, Limpeza e Carga (ETL)
*(A ser alimentado com os códigos executáveis comentados).*

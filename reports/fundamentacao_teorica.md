# FUNDAMENTAÇÃO TEÓRICA

A investigação do desempenho escolar em larga escala e sua relação com fatores intraescolares e socioeconômicos exige a convergência de múltiplos saberes teóricos e metodológicos. No âmbito do Bacharelado em Ciência de Dados da Universidade Virtual do Estado de São Paulo (UNIVESP), essa abordagem interdisciplinar articula conceitos fundamentais de estatística, mineração de dados, aprendizado de máquina, engenharia de dados, visualização computacional e ética na gestão pública. A seguir, detalham-se os eixos conceituais que sustentam a arquitetura analítica deste estudo, relacionando-os diretamente às disciplinas da matriz curricular do curso.

---

## 1. Estatística e Inferência Aplicada à Educação

A análise do rendimento acadêmico fundamenta-se nos princípios da **Estatística Aplicada** e da **Modelagem e Inferência Estatística**. Em consonância com a tradição dos estudos de eficácia escolar — inaugurada historicamente pelo Relatório Coleman (1966) e aprofundada no contexto brasileiro por Soares e Alves (2003) —, a avaliação do desempenho discente requer a mensuração precisa da variabilidade das proficiências em relação ao nível socioeconômico (INSE).

Por meio de testes de hipóteses estatísticas (como o teste $t$ de Student para comparação de médias entre infraestruturas e o uso de coeficientes de correlação de Pearson e Spearman), a disciplina de Estatística Aplicada permite testar a significância estatística das diferenças de rendimento entre os agrupamentos escolares. Além disso, a Modelagem e Inferência Estatística fundamenta a construção da reta de determinação socioeconômica e a análise da variância residual ($R^2$), permitindo isolar o efeito líquido dos fatores intraescolares em relação ao contexto sociofamiliar dos estudantes.

---

## 2. Engenharia e Gestão de Dados Educacionais em Larga Escala

O tratamento de grandes volumes de microdados governamentais — integrando o SARESP, o Provão Paulista e o Censo Escolar — demanda competências consolidadas nas disciplinas de **Introdução à Ciência de Dados**, **Mineração de Dados**, **Banco de Dados** e **Arquitetura de Dados**.

A extração, transformação e carga (ETL) desses dados estruturados e semiestruturados exige a aplicação de conceitos de modelagem relacional, estabelecimento de chaves primárias compostas (como o cruzamento entre o código estadual CIE e o código federal INEP) e a mitigação de inconsistências cadastrais. A adoção da **Arquitetura Medalhão** (camadas *Bronze*, *Silver* e *Gold*) operacionaliza os conceitos de mineração de dados e preparação de bases (*data wrangling*), garantindo a rastreabilidade, a integridade longitudinal dos indicadores (como a validação do ano-pivô de 2023) e o rigor exigido nos portões de qualidade de dados (*quality gates*), conforme as diretrizes teóricas de McKinney (2018) aplicadas à análise de dados com Python.

---

## 3. Aprendizado de Máquina e Modelagem Preditiva Supervisionada

Para além da mera descrição estatística, a predição da defasagem em Matemática apoia-se nos fundamentos da disciplina de **Aprendizado de Máquinas** (*Machine Learning*). Algoritmos de aprendizado supervisionado baseados em árvores de decisão e métodos de *ensemble* (como *Random Forest* e *LightGBM*) são empregados para modelar as relações complexas e não-lineares entre as *features* independentes ($X$) — tais como a regularidade docente (IRD), a sobrecarga de esforço docente (IED) e a infraestrutura tecnológica — e a variável-alvo de desempenho ($Y$).

A prevenção de sobreajuste (*overfitting*) e de vazamento de dados (*data leakage*) é assegurada mediante estratégias rigorosas de validação cruzada (*k-fold cross-validation*), capacitando o modelo a generalizar padrões preditivos para toda a rede pública estadual.

---

## 4. Inteligência Artificial Explicável (XAI) e Visualização Computacional

Modelos preditivos de alta performance operam frequentemente sob a alcunha de "caixas-pretas", o que limita sua utilidade direta para a formulação de políticas públicas. Para solucionar essa limitação, a pesquisa integra os conceitos da **Visualização Computacional** e da interpretabilidade algorítmica por meio da **Inteligência Artificial Explicável (XAI)**, operacionalizada através dos valores SHAP (*SHapley Additive exPlanations*).

Fundamentada na teoria dos jogos cooperativos, a metodologia SHAP decompõe a contribuição marginal de cada fator escolar na predição individual e global do rendimento. Graficamente traduzidos por meio de ferramentas de visualização computacional (como *SHAP summary plots* e *dependence plots*), esses métodos permitem desvelar não apenas a importância relativa de cada indicador, mas também identificar efeitos moderadores — como a capacidade protetiva da estabilidade docente em mitigar os impactos adversos da vulnerabilidade socioeconômica.

---

## 5. Ética, Cidadania e Governança de Dados no Setor Público

A salvaguarda ética e legal da pesquisa encontra amparo na disciplina de **Ética, Cidadania e Sociedade** (bem como em diretrizes de **Impactos da Computação na Sociedade**). O tratamento de bases educacionais públicas impõe o estrito cumprimento da **Lei de Acesso à Informação (LAI - Lei nº 12.527/2011)** no tocante à transparência ativa de dados estatais, bem como a observância rigorosa da **Lei Geral de Proteção de Dados Pessoais (LGPD - Lei nº 13.709/2018)**.

Ao operar exclusivamente na granularidade agregada da unidade escolar e desidentificar qualquer registro individual discente, assegura-se que o uso da ciência de dados na gestão pública ocorra de forma socialmente responsável, combatendo vieses discriminatórios e orientando políticas educacionais inclusivas e baseadas em evidências.

---

## REFERÊNCIAS

> *Nota: As referências abaixo seguem rigorosamente as normas da Associação Brasileira de Normas Técnicas (ABNT), em especial a NBR 6023.*

ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **NBR 6023**: Informação e documentação: referências: elaboração. Rio de Janeiro: ABNT, 2018.

BRASIL. **Lei nº 12.527, de 18 de novembro de 2011**. Regula o acesso a informações previsto no inciso XXXIII do art. 5º, no inciso II do § 3º do art. 37 e no § 2º do art. 216 da Constituição Federal. Brasília, DF: Presidência da República, 2011.

BRASIL. **Lei nº 13.709, de 14 de agosto de 2018**. Lei Geral de Proteção de Dados Pessoais (LGPD). Brasília, DF: Presidência da República, 2018.

BOURDIEU, Pierre; PASSERON, Jean-Claude. **A reprodução: elementos para uma teoria do sistema de ensino**. Rio de Janeiro: Francisco Alves, 1970.

CARVALHO, André C. P. L. F. de et al. **Inteligência artificial: uma abordagem de aprendizado de máquina**. São Paulo: LTC, 2011.

COLEMAN, James S. et al. **Equality of educational opportunity**. Washington, D.C.: U.S. Government Printing Office, 1966.

FRANCO, Creso et al. Qualidade e equidade em educação: reconsiderando o significado de "escola eficaz". **Ensaio: Avaliação e Políticas Públicas em Educação**, Rio de Janeiro, v. 15, n. 55, p. 273-298, abr./jun. 2007.

MCKINNEY, Wes. **Python para análise de dados: tratamento de dados com Pandas, NumPy e IPython**. São Paulo: Novatec, 2018.

SOARES, José Francisco; ALVES, Maria Teresa Gonzaga. Desigualdades socioeconômicas no desempenho cognitivo dos alunos do ensino básico brasileiro. **Revista Brasileira de Educação**, Rio de Janeiro, n. 22, p. 20-39, abr. 2003.

UNIVERSIDADE VIRTUAL DO ESTADO DE SÃO PAULO (UNIVESP). **Projeto Pedagógico do Curso (PPC) de Bacharelado em Ciência de Dados**. São Paulo: Univesp, 2026. Disponível em: [https://apps.univesp.br/manual-do-aluno/assets/PPC/ciencia-de-dados/PPC-BCD-2026.pdf](https://www.google.com/search?q=https%3A%2F%2Fapps.univesp.br%2Fmanual-do-aluno%2Fassets%2FPPC%2Fciencia-de-dados%2FPPC-BCD-2026.pdf). Acesso em: 30 set. 2026.

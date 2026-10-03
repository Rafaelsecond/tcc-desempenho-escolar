# Caderno Metodológico e de Engenharia de Dados do TCC
**Projeto**: Modelagem Preditiva do Desempenho Escolar no Ensino Médio Paulista (2022–2024)  
**Data de Atualização**: 29/09/2026  
**Status**: Camada Gold Concluída; Análise Exploratória de Dados (EDA) Avançada (Passos 1 a 6 Concluídos; Passo 7 em Preparação)

---

## 1. Arquitetura de Dados: O Padrão Medalhão

Para lidar com microdados massivos de avaliações educacionais e censos escolares (milhões de registros com dezenas de tabelas anuais), adotou-se a **Arquitetura Medalhão (Medallion Architecture)**, que garante reprodutibilidade, auditabilidade e desacoplamento entre limpeza e modelagem:

> **Decisão Técnica de Engenharia**: O uso do formato colunar **Apache Parquet (.parquet)** via `pyarrow` preserva os tipos exatos dos dados (inteiros, reais e textos), reduz o tamanho em disco em mais de **75% a 90%** em relação aos arquivos brutos e viabiliza leituras em milissegundos para os algoritmos de aprendizado de máquina.

---

## 2. Passo 1: Espinha Dorsal de Escolas e Infraestrutura (Censo + SEDUC)

### 2.1 Funil Amostral de Filtragem
A identificação da coorte exata do estudo seguiu um funil estrito aplicado sobre os microdados do Censo Escolar da Educação Básica (INEP):
1. **Total Brasil (2023)**: 217.625 estabelecimentos de ensino;
2. **Estado de São Paulo (`SG_UF == 'SP'`)**: 34.099 escolas;
3. **Rede Estadual (`TP_DEPENDENCIA == 2`)**: 6.524 escolas;
4. **Em Atividade (`TP_SITUACAO_FUNCIONAMENTO == 1`)**: 5.750 escolas;
5. **Ensino Regular (`IN_REGULAR == 1`)**: 5.400 escolas;
6. **Ensino Médio Regular (`IN_MED == 1`)**: 3.964 escolas;
7. **Cruzamento Relacional com Cadastro SEDUC (`ESTADUAL - SE`)**: **3.734 escolas** (2023).

### 2.2 Descobertas e Decisões de Engenharia
- **Padronização das Chaves Primárias Duplas**:
  - Código Estadual (CIE / `CODESC`): Padronizado rigorosamente em **6 dígitos** com preenchimento de zeros à esquerda (`zfill(6)`), ex: `"000024"`.
  - Código Federal (INEP / `CO_ENTIDADE`): Padronizado em **8 dígitos** (`zfill(8)`), ex: `"35000024"`.
  - No estado de São Paulo, verificou-se a relação fundamental: $\text{CO\_ENTIDADE} = 35 + \text{CODESC}$.
- **Tratamento de Coordenadas Geográficas**:
  - As variáveis `DS_LATITUDE` e `DS_LONGITUDE` provenientes do cadastro da SEDUC foram convertidas do padrão brasileiro (vírgula decimal) para ponto decimal e tipadas como `float64`.
- **Tratamento do Caractere Oculto (BOM)**:
  - Identificado e removido o Byte Order Mark (`ï»¿NOMEDEP`) presente nos arquivos exportados do ecossistema Windows da SEDUC.
- **Engenharia de Recursos (Feature Engineering)**:
  - Criada a variável totalizadora de tecnologia para estudantes:
    $$\text{QT\_COMP\_ALUNO} = \text{QT\_DESKTOP\_ALUNO} + \text{QT\_COMP\_PORTATIL\_ALUNO}$$

---

## 3. Passo 2: Fatores Docentes e Socioeconômicos (INEP)

### 3.1 Nível Socioeconômico das Escolas (INSE)
- **Origem**: INEP / Diretoria de Avaliação da Educação Básica.
- **Especificidade Metodológica**: O INSE é calculado a partir dos questionários do SAEB, que possui periodicidade **bienal** (anos ímpares: 2021, 2023). Por definição do órgão federal, **não existem edições em 2022 e 2024**. O INSE 2023 é a medida oficial representativa para todo o ciclo avaliativo.
- **Cobertura Obtida**: **96,9%** das escolas estaduais paulistas de Ensino Médio (3.618 de 3.734 unidades).

### 3.2 Regularidade do Corpo Docente (IRD)
- **Origem**: INEP / Indicadores Educacionais.
- **Resolução de Bug Crítico**: Na base preliminar, o IRD apresentava valores corrompidos na ordem de trilhões (`2.739.558.666...`) devido à conversão equivocada de separadores decimais e de milhar. Ao ler diretamente a planilha oficial `.xlsx` com o cabeçalho técnico na Linha 10 (`header=10`), os valores foram restaurados à sua escala contínua real de **0.0 a 5.0**.
- **Comportamento de Cauda**: Identificou-se que 65 escolas apresentavam IRD < 1.0 (valores como 0.37 e 0.80). A documentação do INEP esclarece que escolas com alta rotatividade de docentes temporários ou contratos recentes podem pontuar abaixo de 1.0, estabelecendo o limite teórico inferior real em **0.0**.
- **Cobertura Obtida**: **99,7%** (2022 e 2023) e **99,9%** (2024).

### 3.3 Esforço Docente (IED)
- **Origem**: INEP / Indicadores Educacionais.
- **Engenharia de Recursos**: As categorias de esforço do Ensino Médio (`MED_CAT_1` a `MED_CAT_6`), que medem a sobrecarga de turmas, escolas e turnos dos professores, foram modeladas em duas novas métricas contínuas:
  1. **Score Ponderado de Esforço Docente (1.0 a 6.0)**:
     $$\text{IED\_SCORE\_MEDIO} = \frac{\sum_{i=1}^{6} i \cdot \text{MED\_CAT\_i}}{100}$$
  2. **Percentual de Docentes com Sobrecarga Alta**:
     $$\text{IED\_ESFORCO\_ALTO} = \text{MED\_CAT\_5} + \text{MED\_CAT\_6}$$
- **Cobertura Obtida**: **100,0%** em todos os três anos analisados.

---

## 4. Validação Científica da Estabilidade Trienal (2022–2024)

Para fundamentar a adoção de **2023 como ano-pivô representativo** das variáveis preditoras ($X$), executou-se uma validação longitudinal comparando as **3.691 escolas estaduais presentes simultaneamente nos 3 anos**.

### 4.1 Médias e Desvios Padrão
| Indicador | Média 2022 (±DP) | Média 2023 (±DP) | Média 2024 (±DP) | Variação Global |
| :--- | :---: | :---: | :---: | :---: |
| **IRD (Regularidade Docente)** | 2.64 (±0.46) | 2.65 (±0.45) | 2.54 (±0.46) | -0.10 (-3.8%) |
| **IED (Score Esforço Docente)** | 3.71 (±0.56) | 3.69 (±0.46) | 3.68 (±0.45) | -0.03 (-0.8%) |
| **Salas Utilizadas** | 13.14 (±4.58) | 13.29 (±4.55) | 13.30 (±4.52) | +0.16 (+1.2%) |
| **Computadores para Alunos** | 43.13 (±31.60) | 68.04 (±49.87) | 86.94 (±59.70) | Expansão Digital |

### 4.2 Matriz de Correlação Interanual (Pearson $r$)
| Indicador | r (2022–2023) | r (2023–2024) | r (2022–2024) | Interpretação |
| :--- | :---: | :---: | :---: | :--- |
| **Salas Utilizadas** | **0.968** | **0.966** | **0.949** | Estabilidade física quase perfeita |
| **IRD (Regularidade)** | **0.856** | **0.911** | **0.715** | Altíssima persistência temporal |
| **IED (Esforço)** | **0.706** | **0.730** | **0.684** | Forte estabilidade de alocação |
| **Computadores** | **0.547** | **0.616** | **0.446** | Programa progressivo de expansão da SEDUC |

> **Conclusão Metodológica para a Monografia**: A estabilidade das características físicas e docentes comprovada matematicamente valida a escolha de 2023 como o retrato representativo da infraestrutura e corpo docente da rede estadual durante o ciclo avaliativo do triênio.

---

## 5. Passo 3: Avaliação de Desempenho Escolar — SARESP 2022 (Silver)

### 5.1 Funil Amostral dos Microdados de Alunos
A extração da variável de desempenho em Matemática de 2022 partiu da base completa de estudantes do SARESP (`MICRODADOS SARESP 2022 - DADOS ABERTO_0.csv`, 387,7 MB):
1. **Total de Registros Brutos**: 1.330.650 avaliações de estudantes;
2. **Filtro de Coorte**: `SERIE_ANO == 'EM-3 serie'` (3ª série do Ensino Médio);
3. **Filtro de Classe Regular**: `TIPOCLASSE == '0'` (exclusão de classes de recuperação/aceleração);
4. **Filtro de Validade Estatística**: `validade == '1'` (critério oficial de notas válidas da SEDUC);
5. **Presença em Matemática**: `particip_mat == '1'` e nota de acertos não nula (`porc_ACERT_MAT.notna()`);
6. **Total de Alunos Válidos**: **307.827 estudantes regulares**.

### 5.2 Agregação por Escola e Métricas Criadas
Os microdados a nível de aluno foram agregados no nível da unidade escolar (`CODESC` padronizado com 6 dígitos), gerando o artefato `03_saresp_2022_escola.parquet` (84,3 KB):
- `QTD_ALUNOS_2022`: Contagem de estudantes participantes válidos na escola;
- `MEDIA_ACERTOS_2022`: Média percentual de acertos em Matemática ($0.0 \le x \le 100.0$);
- `MEDIA_PROFIC_2022`: Média da proficiência equalizada em Matemática (escala SARESP);
- `PERC_ABAIXO_2022`: Percentual de estudantes classificados no nível "Abaixo do Básico";
- `PERC_ADEQ_AVANC_2022`: Percentual de estudantes nos níveis "Adequado" ou "Avançado".

### 5.3 Diagnóstico Amostral e Identificação de Microclasses
- **Cobertura Escolar**: Das 3.650 escolas avaliadas no SARESP 2022, **3.404 escolas cruzaram perfeitamente com a base de escolas do Censo (91,2% de cobertura)**.
- **Identificação de Microclasses Atípicas**: Identificou-se que **103 escolas possuíam menos de 10 alunos avaliados ($N < 10$)**, correspondendo a unidades prisionais, centros da Fundação CASA e classes hospitalares.
- **Decisão Metodológica**: Essas 103 unidades foram preservadas na camada Silver (com o registro de `QTD_ALUNOS_2022`) e serão filtradas na camada Gold de forma transparente, permitindo demonstrar à banca o impacto da remoção de ruído na variância do modelo.

### 5.4 Diagnóstico Pedagógico da Rede em 2022 (Pós-Pandemia)
A análise dos 307.827 estudantes revelou o impacto pedagógico severo do retorno presencial pós-pandemia:
- **57,7%** (177.487 alunos) encontravam-se no nível **Abaixo do Básico**;
- **36,9%** (113.608 alunos) no nível **Básico**;
- Apenas **5,4%** (16.732 alunos) atingiram proficiência considerada adequada ou avançada.

---

## 6. Passo 4: Avaliação de Desempenho Escolar — Provão Paulista 2023 (Silver)

### 6.1 Contextualização Institucional e Estrutura da Avaliação
Em 2023, a SEDUC-SP implementou o **Provão Paulista Seriado**, uma inovação avaliativa de grande escala que unificou o diagnóstico pedagógico com o acesso direto e gratuito dos estudantes da rede pública às vagas das universidades públicas estaduais (USP, UNICAMP, UNESP, FATEC e UNIVESP). Por ser uma avaliação com alto valor agregado e impacto direto na vida dos estudantes, o exame apresentou engajamento e participação expressivos na rede.

### 6.2 Funil Amostral dos Microdados de Alunos
A extração da variável de desempenho em Matemática de 2023 partiu da base completa de estudantes do Provão (`Microdados de Alunos - Anos Finais SARESP - 2023.csv`, 384,5 MB):
1. **Total de Registros Brutos**: 1.280.227 avaliações (abrangendo 1ª, 2ª e 3ª séries do EM);
2. **Filtro de Coorte**: `SERIE_ANO.str.contains('EM-3', na=False)` (identificando a 3ª série do EM independentemente de acentuação/encoding);
3. **Filtro de Validade Estatística**: `validade == '1'` (critério oficial de notas válidas da SEDUC);
4. **Presença em Matemática**: `particip_mat_ch == '1'` (presença confirmada no Dia 2 - Prova de Matemática e Ciências Humanas) com pontuação percentual de acertos não nula (`porc_mat.notna()`);
5. **Total de Alunos Válidos**: **266.761 estudantes da 3ª série do EM**.

### 6.3 Agregação por Escola e Métricas Criadas
Os microdados a nível de aluno foram agregados no nível da unidade escolar (`CODESC` padronizado com 6 dígitos), gerando o artefato `04_provao_2023_escola.parquet` (62,7 KB):
- `QTD_ALUNOS_2023`: Contagem de estudantes participantes válidos na escola;
- `MEDIA_ACERTOS_2023`: Média percentual de acertos em Matemática ($0.0 \le x \le 100.0$), derivada de `porc_mat`;
- `ACERTOS_MED_MAT_2023`: Média do número absoluto de questões corretas em Matemática, derivada de `acertos_mat`.

### 6.4 Diagnóstico Amostral e Cruzamento Relacional
- **Cobertura Escolar Excepcional**: Das 3.944 escolas com alunos participantes no Provão Paulista 2023, **3.663 escolas cruzaram perfeitamente com a base de escolas do Censo Escolar (98,1% de cobertura da rede regular)**.
- **Identificação de Microclasses Atípicas**: Identificou-se que **205 escolas possuíam menos de 10 alunos avaliados ($N < 10$)**, em geral unidades de atendimento especializado e socioeducativo.
- **Decisão Metodológica**: Preservação na camada Silver e documentação para o corte amostral rigoroso na camada Gold ($N \ge 10$), prevenindo distorções estocásticas causadas por médias baseadas em poucos indivíduos.

---

## 7. Passo 5: Avaliação de Desempenho Escolar — Provão Paulista 2024 (Silver)

### 7.1 Consolidação Institucional do Provão Paulista
Em 2024, a segunda edição do Provão Paulista consolidou o modelo avaliativo da rede estadual. O exame manteve a estrutura de vestibular seriado com reserva de vagas nas universidades públicas estaduais, resultando no maior contingente histórico de participação de estudantes da 3ª série do Ensino Médio no triênio estudado.

### 7.2 Funil Amostral dos Microdados de Alunos
A extração da variável de desempenho em Matemática de 2024 partiu da base completa de estudantes do Provão (`Microdados de Alunos - Ensino Medio PROVAO - 2024.csv`, 427,3 MB):
1. **Total de Registros Brutos**: 1.279.758 avaliações (1ª, 2ª e 3ª séries do EM);
2. **Filtro de Coorte**: `SERIE_ANO.str.contains('EM-3', na=False)` (identificação imune a distorções de encoding no caractere ordinal);
3. **Filtro de Validade Estatística**: `validade == '1'` (critério oficial de notas válidas da SEDUC);
4. **Presença em Matemática**: `particip_mat_ch == '1'` (presença confirmada no Dia 2 - Prova de Matemática e Ciências Humanas) com nota válida em `porc_mat.notna()`;
5. **Total de Alunos Válidos**: **309.829 estudantes da 3ª série do EM**.

### 7.3 Agregação por Escola e Métricas Criadas
Os microdados a nível de aluno foram agregados no nível da unidade escolar (`CODESC` padronizado com 6 dígitos), gerando o artefato `05_provao_2024_escola.parquet` (58,1 KB):
- `QTD_ALUNOS_2024`: Contagem de estudantes participantes válidos na escola ($\mu = 78,6$ alunos/escola);
- `MEDIA_ACERTOS_2024`: Média percentual de acertos em Matemática ($0.0 \le x \le 100.0$, $\mu = 28,53\%$, $\sigma = 5,54\%$);
- `ACERTOS_MED_MAT_2024`: Média do número absoluto de questões corretas em Matemática ($\mu = 5,13$ acertos de 18);
- `NOTA_MED_MAT_2024`: Média da nota padronizada de Matemática ($\mu = 2,75$).

### 7.4 Diagnóstico Amostral e Cruzamento Relacional
- **Cobertura Escolar**: Das 3.940 escolas com alunos participantes no Provão Paulista 2024, **3.658 escolas cruzaram perfeitamente com a base de escolas do Censo Escolar (98,0% de cobertura da rede regular)**.
- **Identificação de Microclasses Atípicas**: Identificou-se que **183 escolas possuíam menos de 10 alunos avaliados ($N < 10$)**.
- **Decisão Metodológica**: Preservação na camada Silver e documentação para o corte amostral rigoroso na camada Gold ($N \ge 10$), prevenindo distorções estocásticas causadas por médias baseadas em poucos indivíduos.

---

## 8. Passo 6: Consolidação do Target Trienal Ponderado (Silver)

### 8.1 Fundamentação Metodológica da Média Ponderada
Em econometria da educação e avaliação em larga escala, o desempenho de uma escola em um único ano letivo está sujeito a flutuações estocásticas decorrentes do tamanho da turma, rotatividade pontual de turmas específicas ou eventos contextuais do dia da prova. A consolidação longitudinal de múltiplos anos em uma **média ponderada pelo volume de alunos avaliados** atua diretamente como um mecanismo de suavização de ruído amostral (fundamentado no princípio psicométrico de Spearman-Brown):

$$\text{TARGET\_TRIENAL\_MAT} = \frac{\sum_{t \in \{2022, 2023, 2024\}} (QTD\_ALUNOS_t \cdot MEDIA\_ACERTOS_t)}{\sum_{t \in \{2022, 2023, 2024\}} QTD\_ALUNOS_t}$$

Essa formulação garante que:
1. O peso relativo de cada edição no escore final da escola seja estritamente proporcional ao número de estudantes efetivamente submetidos ao exame;
2. Escolas com turmas reduzidas em determinado ano não tenham sua média histórica distorcida por pequenos grupos pontuais;
3. As notas individuais de cada edição anual sejam preservadas no artefato para fins de auditoria e análises de sensibilidade.

### 8.2 Cobertura, Continuidade e Diagnóstico Amostral
A união completa (*outer merge*) das três avaliações estaduais gerou o artefato `06_target_trienal.parquet` (130,9 KB), totalizando 4.007 escolas no universo amplo e apresentando indicadores de qualidade excepcionais:
- **Cobertura Quase Universal da Rede Regular**: Das 3.734 escolas ativas de Ensino Médio regular do Censo Escolar, **3.705 escolas possuem Target Trienal consolidado (99,2% de cobertura)**.
- **Altíssima Persistência Temporal**:
  - **3.597 escolas (89,8%)** participaram das **3 edições ininterruptamente**;
  - **333 escolas (8,3%)** participaram de 2 edições;
  - Apenas **77 escolas (1,9%)** possuíam registro em somente 1 edição.
- **Isolamento de Microclasses Acumuladas**:
  - Apenas **96 escolas** apresentaram menos de 10 alunos somados em todo o triênio ($N_{\text{triênio}} < 10$);
  - **116 escolas** apresentaram menos de 15 alunos somados ($N_{\text{triênio}} < 15$).

### 8.3 Resumo Estatístico da Variável-Alvo ($Y$)
A variável-alvo consolidada apresenta distribuição contínua bem-comportada, compatível com premissas de modelos de regressão linear, regularizada (Ridge/Lasso) e algoritmos baseados em árvores (Random Forest, XGBoost, LightGBM):
- **Média Global**: **31,51%** de acertos em Matemática;
- **Mediana**: **30,55%**;
- **Desvio Padrão**: **5,34%**;
- **Amplitude**: Intervalo empírico de **[5,00%, 67,46%]**;
- **Volume Médio de Avaliados por Escola**: **220,7 estudantes** ao longo do triênio ($\text{mediana} = 172$ alunos, $\text{máximo} = 1.436$ alunos).

---

## 9. A Camada Gold: O Dataset Analítico Final (`tcc_dataset_analitico_final`)

### 9.1 Funil Amostral Metodológico Consolidado da Pesquisa
O rigor metodológico da pesquisa materializa-se na rastreabilidade completa de cada filtro aplicado, desde o censo nacional até a coorte final de treinamento dos modelos:

```
[1] Estabelecimentos de Ensino Brasil (Censo 2023):               217.625 escolas
 └── [2] Estado de São Paulo (SG_UF == 'SP'):                       34.099 escolas
      └── [3] Dependência Estadual (TP_DEPENDENCIA == 2):            6.524 escolas
           └── [4] Em Atividade (TP_SITUACAO_FUNCIONAMENTO == 1):    5.750 escolas
                └── [5] Ensino Regular (IN_REGULAR == 1):            5.400 escolas
                     └── [6] Ensino Médio Regular (IN_MED == 1):     3.964 escolas
                          └── [7] Cadastro Estadual Ativo (SEDUC):   3.734 escolas (Espinha Silver)
                               └── [8] Avaliadas no Triênio (Target): 3.705 escolas (99,2% de cobertura)
                                    └── [9] Corte Amostral (N >= 10): 3.611 escolas (DATASET GOLD FINAL)
```

> **Nota sobre o Corte Amostral ($N < 10$)**: Foram excluídas **94 unidades escolares (2,54% da rede)** caracterizadas como microclasses atípicas com menos de 10 estudantes avaliados na soma de todo o triênio (ex: classes em assentamentos isolados, unidades de internação socioeducativa da Fundação CASA e classes hospitalares). Essa decisão metodológica assegura a eliminação de ruído estocástico sem comprometer a representatividade da rede regular, que mantém **3.611 escolas ativas (96,7% do universo estadual)**.

### 9.2 Resumo Estatístico das Variáveis Centrais (Gold)
| Variável | Descrição Técnica | Média (±DP) | Mediana | Mínimo | Máximo | Cobertura |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **TARGET_TRIENAL_MAT** | Variável-Alvo Y (% acertos ponderada) | **30,93%** (±3,86%) | **30,35%** | 21,01% | 67,46% | **100,0%** |
| **TOTAL_ALUNOS_TRIENIO** | Estudantes avaliados no triênio | **218,7** (±179,3) | **171,0** | 10,0 | 1.436,0 | **100,0%** |
| **MEDIA_INSE** | Nível Socioeconômico Médio (INEP) | **5,25** (±0,23) | **5,24** | 4,26 | 6,00 | **99,5%** |
| **IED_SCORE_MEDIO** | Score Ponderado Esforço Docente (1-6) | **3,69** (±0,46) | **3,77** | 2,00 | 4,87 | **100,0%** |
| **MEDIA_IRD** | Regularidade do Corpo Docente (0-5) | **2,65** (±0,45) | **2,67** | 0.80 | 4,14 | **99,9%** |
| **QT_SALAS_UTILIZADAS** | Capacidade Física da Escola | **13,45** (±4,47) | **13,0** | 3,0 | 35,0 | **100,0%** |
| **QT_COMP_ALUNO** | Parque Computacional para Estudantes | **69,52** (±49,48) | **62,0** | 0,0 | 476,0 | **100,0%** |

### 9.3 Diagnóstico de Valores Ausentes (Data Quality)
O dataset analítico final apresenta integridade de preenchimento excepcional:
- **Variável-Alvo ($Y$)**: **Zero valores nulos** em 3.611 registros;
- **Chaves Primárias**: `CODESC` e `CO_ENTIDADE` rigorosamente únicas e sem nulos;
- **Infraestrutura**: 100% preenchida para salas e computadores; apenas 7 nulos (0,2%) em banda larga;
- **Docentes e Contexto**: Apenas 3 escolas sem IRD (99,9% de preenchimento) e 17 escolas sem INSE (99,5% de preenchimento).

### 9.4 Artefatos Produzidos e Disponíveis
- **Dataset Analítico Oficial (Machine Learning)**:
  - Caminho: `data/gold/tcc_dataset_analitico_final.parquet`
  - Tamanho: **417,3 KB**
  - Formato: Apache Parquet colunar otimizado com tipos de dados estritos.
- **Dataset Tabular para Auditoria e Visualização**:
  - Caminho: `data/gold/tcc_dataset_analitico_final.csv`
  - Tamanho: **983,4 KB**
  - Formato: CSV formatado no padrão brasileiro (separador `;` e decimal `,`).

---

## 10. Fase de Análise Exploratória de Dados (EDA Modular)

Para além de uma análise descritiva superficial, a EDA foi estruturada de forma modular e atômica, investigando cientificamente as principais teorias da sociologia da educação (Coleman, 1966; Bourdieu, 1970) e da eficácia escolar (Soares & Alves, 2003; Franco et al., 2007).

### 10.1 Passo 1 da EDA: A Anatomia da Variável-Alvo ($Y$)
A investigação aprofundada da média trienal ponderada de acertos em Matemática (`TARGET_TRIENAL_MAT`) revelou propriedades estatísticas determinantes para a modelagem:
- **Tendência Central e Homogeneidade**: Média de **30,93%** e mediana de **30,35%**, com distância interquartil (IQR) de apenas **4,50 pontos percentuais** ($[28,36\%, 32,86\%]$). Metade exata de toda a rede estadual gravita estreitamente em torno de 30% de aproveitamento.
- **Geometria da Distribuição**:
  - **Assimetria Positiva (*Skewness* = +1,327)**: A curva não é estritamente gaussiana; apresenta uma cauda alongada à direita, indicando a existência de um contingente de escolas que se descola da média para patamares elevados;
  - **Curtose Leptocúrtica (*Kurtosis* = +5,008)**: Pico central pronunciado com caudas mais densas do que a normal clássica.
- **Diagnóstico e Valor Científico dos Outliers**:
  - Pela regra de Tukey ($Q \pm 1,5 \times \text{IQR}$), identificaram-se apenas 4 escolas abaixo do limite inferior ($0,11\%$, piso real em $21,01\%$) e **106 escolas acima do limite superior de 39,60% (2,94% da rede)**;
  - Essas 106 escolas representam unidades regulares de alta eficácia (*outperforming schools*), com médias que atingem até $67,46\%$, constituindo o objeto empírico central da análise de eficácia escolar.
- **Artefato Gráfico**: `reports/figures/eda_01_distribuicao_target.png` (painel conjugado com Boxplot e Histograma/KDE em 300 DPI).

### 10.2 Passo 2 da EDA: O Teste Empírico de Coleman (Origem Social vs. Desempenho)
Confrontou-se o desempenho em Matemática com o Nível Socioeconômico das famílias das escolas (`MEDIA_INSE`, $N = 3.594$ unidades):
- **Associação Bivariada**:
  - Correlação Linear de Pearson: $r = +0,4129$ ($p < 0,001$);
  - Correlação Monotônica de Spearman: $\rho = +0,4331$ ($p < 0,001$);
  - Confirmação de associação positiva moderada entre a condição socioeconômica e a nota escolar.
- **A Reta de Coleman e o Coeficiente de Determinação ($R^2$)**:
  $$\text{TARGET\_TRIENAL\_MAT} = -4,77 + (6,80 \cdot \text{MEDIA\_INSE})$$
  - Cada ponto adicional na escala INSE eleva a média em $+6,80$ pontos percentuais;
  - **O $R^2$ obtido foi de apenas 17,05%**: Apenas $17,1\%$ da variabilidade das notas de Matemática decorre diretamente do nível socioeconômico das famílias;
  - **Variância Residual de 82,95%**: Quase 83% do resultado escolar na rede pública paulista é livre do determinismo socioeconômico, abrindo espaço para a atuação de fatores intraescolares (professores, gestão, infraestrutura e tecnologia).
- **Gap Social**: A diferença média entre as escolas do Quartil 4 (menos vulneráveis, $\mu = 33,26\%$) e do Quartil 1 (mais vulneráveis, $\mu = 29,28\%$) é de **3,98 pontos percentuais**.
- **Evidência das Escolas Resilientes (A Superação da Reta)**:
  - Unidades como a **EE Assentamento Santa Clara** (Mirante do Paranapanema), com INSE modesto de $4,92$, atingiram média de **61,57%** (superando a previsão teórica de Coleman em expressivos $+32,88$ pontos percentuais).
- **Artefato Gráfico**: `reports/figures/eda_02_teste_coleman_inse.png` (gráfico de dispersão com a Reta de Coleman e destaque das escolas de alta eficácia).

### 10.3 Passo 3 da EDA: O Radar de Influências (Ranking Completo de Correlações)
Confrontaram-se todas as 26 variáveis preditoras ($X$) da Camada Gold com a variável-alvo ($Y$, `TARGET_TRIENAL_MAT`), mensurando a correlação linear de Pearson ($r$) e a monotônica de Spearman ($\rho$), ambas com testes de hipótese bicaudais ($p$-valor):

| Pos | Variável Preditora | Pearson ($r$) | Spearman ($\rho$) | Significância | Dimensão Temática |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | `MEDIA_INSE` | **+0,4129** | +0,4331 | $p < 0,001$ (***) | Nível Socioeconômico Familiar |
| **2** | `IED_ESFORCO_ALTO` | **-0,2348** | -0,2553 | $p < 0,001$ (***) | Docente: % Professores Categoria 5 e 6 |
| **3** | `QTD_ALUNOS_INSE` | **-0,2277** | -0,2280 | $p < 0,001$ (***) | Porte / Tamanho da Escola |
| **4** | `MED_CAT_5` | **-0,2201** | -0,2413 | $p < 0,001$ (***) | Docente: Sobrecarga Severa (>300 alunos) |
| **5** | `IED_SCORE_MEDIO` | **-0,2139** | -0,2372 | $p < 0,001$ (***) | Docente: Score Ponderado de Esforço |
| **6** | `MED_CAT_3` | **+0,2113** | +0,2140 | $p < 0,001$ (***) | Docente: Carga Equilibrada |
| **7** | `IRD_MEDIO` | **+0,1734** | +0,0949 | $p < 0,001$ (***) | Docente: Regularidade do Vínculo |
| **8** | `MED_CAT_6` | **-0,1733** | -0,2134 | $p < 0,001$ (***) | Docente: Sobrecarga Extrema (>400 alunos) |
| **9** | `DS_LATITUDE` | **+0,1500** | +0,1274 | $p < 0,001$ (***) | Geografia: Eixo Norte/Noroeste Paulista |
| **10** | `IN_LABORATORIO_CIENCIAS` | **+0,1124** | +0,1159 | $p < 0,001$ (***) | Infraestrutura: Experimentos Práticos |
| **14** | `QT_SALAS_UTILIZADAS` | **-0,0730** | -0,0617 | $p < 0,001$ (***) | Infraestrutura: Porte Físico da Unidade |
| **17** | `QT_COMP_ALUNO` | **+0,0417** | +0,0602 | $p = 0,012$ (*) | Tecnologia: Computadores para Alunos |
| **19** | `IN_BANDA_LARGA` | **+0,0374** | +0,0368 | $p = 0,025$ (*) | Tecnologia: Conectividade |
| **25** | `IN_LABORATORIO_INFORMATICA`| **+0,0056** | +0,0049 | $p = 0,738$ (ns) | Tecnologia: Não Significante |

#### Principais Revelações do Ranking:
1. **O Fator Docente como o Maior Motor Intraescolar**: Excluindo o INSE familiar, as variáveis que mais influenciam o resultado das escolas pertencem ao bloco docente. A sobrecarga de trabalho dos professores (`IED_ESFORCO_ALTO`, $r = -0,2348$) e o esforço médio (`IED_SCORE_MEDIO`, $r = -0,2139$) correlacionam-se fortemente de forma negativa com a nota de Matemática. Por outro lado, professores com vínculos estáveis e contínuos (`IRD_MEDIO`, $r = +0,1734$) impulsionam o aprendizado.
2. **A Validação Empírica do "Paradoxo de Coleman"**: Ter computadores para alunos ($r = +0,0417$) ou laboratório de informática ($r = +0,0056$, sem significância estatística) praticamente não afeta a nota de Matemática. O impacto da sobrecarga de um professor ($r = -0,23$) é **mais de 40 vezes superior** ao fato de a escola possuir ou não laboratório de computática!
3. **A Exceção da Infraestrutura (Ciências)**: O único insumo físico que apresentou relevância estatística robusta foi o **Laboratório de Ciências** ($r = +0,1124$, $p < 0,001$), indicando que a infraestrutura voltada para o método empírico e experimental transborda positivamente para o raciocínio matemático.
4. **Efeito de Porte e Aglomeração**: Escolas de grande porte com centenas de alunos (`QTD_ALUNOS_INSE`, $r = -0,2277$) e muitas salas de aula ($r = -0,0730$) apresentam desempenho médio inferior ao de escolas menores.
- **Artefato Gráfico**: `reports/figures/eda_03_ranking_correlacoes.png` (gráfico horizontal comparativo em 300 DPI, com azul para alavancas e vermelho para gargalos).

---

### 10.4 Auditoria Cirúrgica e Longitudinal das Escolas Resilientes
Para testar a hipótese de que as escolas com maior superação da Reta de Coleman pudessem ser meras anomalias amostrais ou erros de mensuração de um único ano, executou-se uma auditoria histórica detalhada (2022–2024) sobre o Top 5 das escolas de maior resíduo positivo:

| Escola / Município | INSE | Nota Trienal ($Y$) | Previsto Coleman | Superação (Resíduo) | Alunos Triênio | SARESP 2022 | Provão 2023 | Provão 2024 | IED Médio | IRD Médio | Computadores |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **EE Assentamento Santa Clara** (Mirante do Paranapanema) | 4,92 | **61,57%** | 28,69% | **+32,88 p.p.** | 30 | 60,26% | 42,50% | 91,24% | 4,05 | 2,82 | 11 |
| **EE Rizzieri Poletti** (Cândido Rodrigues) | 5,21 | **53,86%** | 30,66% | **+23,20 p.p.** | 49 | 55,73% | 33,57% | 59,27% | 4,14 | 2,69 | 78 |
| **EE Maria de Lourdes G. Stefano** (Itápolis) | 4,99 | **49,95%** | 29,17% | **+20,78 p.p.** | 25 | 42,13% | 25,00% | 67,68% | 3,60 | 2,36 | 54 |
| **EE Odila Bovolenta de Mendonça** (Adolfo) | 5,18 | **50,72%** | 30,46% | **+20,26 p.p.** | 68 | 60,18% | 23,57% | 55,35% | 4,09 | 2,84 | 27 |
| **EE Terezinha Mariano Magnani** (Espírito Santo do Turvo) | 4,86 | **47,48%** | 28,28% | **+19,20 p.p.** | **111** | 58,78% | 22,43% | 59,40% | **2,40** | **3,26** | **0** |

#### Conclusões Científicas da Auditoria:
1. **Consistência Longitudinal Comprovada**: Todas as 5 escolas apresentaram desempenho excepcional tanto em 2022 quanto em 2024, confirmando que os resultados decorrem de uma **cultura pedagógica permanente** e não de ruído aleatório.
2. **O "Efeito 2023" e a Validação da Média Trienal**: Em todas as unidades auditadas, observou-se uma queda pontual em 2023, ano de estreia do Provão Paulista (formato inédito aplicado pela Vunesp). O retorno a patamares elevados em 2024 comprova a adaptação institucional e legitima a opção metodológica por consolidar o desempenho escolar na **média ponderada pelo número de alunos do triênio**.
3. **A Geografia do Capital Social Comunitário**: Todas as escolas resilientes situam-se em **municípios de pequeno porte do interior paulista**, onde turmas menores viabilizam acompanhamento pedagógico individualizado, controle de frequência e forte integração entre famílias e direção escolar.
4. **O Caso Emblemático da EE Terezinha Mariano Magnani**: Com uma amostra robusta de 111 estudantes avaliados e INSE de baixa renda ($4,86$), a escola atingiu média de **47,48%** tendo **zero computadores para alunos**, mas ostentando o menor esforço docente da amostra ($\text{IED} = 2,40$, apenas 5% de sobrecarga alta) e a maior regularidade de vínculo ($\text{IRD} = 3,26$). É a confirmação empírica máxima de que **o fator humano e as condições estáveis de trabalho docente superam qualquer insumo tecnológico**.

### 10.5 Passo 4 da EDA: O Fator Humano Intraescolar (Docentes: IED vs. IRD)
O aprofundamento das duas forças intraescolares mais relevantes — o Esforço Docente (`IED`) e a Regularidade do Vínculo (`IRD`) — em $3.591$ escolas regulares ($99,4\%$ da base) revelou o mecanismo central de funcionamento da rede:

#### A Matriz dos 4 Quadrantes Docentes:
Dividindo a rede pelas medianas estaduais de esforço ($\text{IED} = 3,77$) e regularidade ($\text{IRD} = 2,61$), a rede distribui-se em quatro grupos homogêneos de cerca de $900$ escolas cada:

| Quadrante Docente | Perfil Pedagógico | Escolas ($N$) | % Rede | IED Médio | IRD Médio | INSE Médio | Nota Matemática ($\mu$) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Q1 (Crítico)** | Alta Sobrecarga & Baixa Regularidade | 904 | 25,2% | 4,08 | 2,32 | 5,25 | **30,08%** |
| **Q2 (Sobrecarga)** | Alta Sobrecarga & Alta Regularidade | 890 | 24,8% | 4,08 | 2,91 | 5,19 | **30,08%** |
| **Q3 (Rotatividade)**| Baixa Sobrecarga & Baixa Regularidade | 892 | 24,8% | 3,29 | 2,27 | 5,25 | **31,20%** |
| **Q4 (Ideal)** | Baixa Sobrecarga & Alta Regularidade | 905 | 25,2% | 3,33 | 3,07 | 5,29 | **32,28%** |

#### Conclusões do Diagnóstico Docente:
1. **O "Teto da Sobrecarga"**: A nota média em Q1 e Q2 é rigorosamente idêntica ($30,08\%$). Isso comprova que **quando os professores estão submetidos a regimes severos de sobrecarga de turmas (IED alto), a estabilidade de vínculo não consegue se traduzir em ganhos pedagógicos**. A estafa física e cognitiva do professor neutraliza os potenciais benefícios da permanência na escola.
2. **O Salto da Carga Equilibrada**: Apenas ao reduzir o esforço para patamares humanos (Q3 e Q4), a nota da escola salta para $31,20\%$ e atinge o ápice de $32,28\%$.
3. **O "Gap do Corpo Docente"**: O ambiente docente ideal (Q4) supera o ambiente crítico (Q1) em **$+2,20$ pontos percentuais**, diferença substantiva que equivale a quase um ano letivo a mais de aprendizado acumulado em Matemática.
4. **O Teste de Controle Social**: Ajustou-se uma regressão múltipla controlando pelo INSE familiar:
   $$\text{TARGET\_TRIENAL\_MAT} = \beta_0 + (6,384 \cdot \text{MEDIA\_INSE}) - (1,475 \cdot \text{IED\_SCORE\_MEDIO}) + (1,269 \cdot \text{IRD\_MEDIO})$$
   - O $R^2$ saltou de $17,05\%$ para **$22,72\%$** (ganho líquido de $+5,67$ p.p.);
   - Mesmo para escolas com o mesmo nível de riqueza familiar, cada ponto a mais de esforço docente reduz a nota em $-1,48$ p.p., enquanto cada ponto a mais de regularidade eleva em $+1,27$ p.p. O efeito docente é **autônomo e independente do perfil social dos estudantes**.
- **Artefato Gráfico**: `reports/figures/eda_04_fatores_docentes_ied_ird.png` (painel conjugado com dispersão IED vs. Target com gradiente por IRD e boxplot dos 4 quadrantes em 300 DPI).

---

### 10.6 Passo 5 da EDA: A Fábula dos Insumos Físicos e Digitais (Infraestrutura & Tecnologia)
Confrontou-se formalmente o peso dos insumos físicos e tecnológicos contra os resultados de Matemática, testando empiricamente as conclusões originais de Coleman:

#### Testes de Hipóteses para Insumos Binários (Com vs. Sem):
| Insumo Escolar | Sem Insumo ($\mu$) | Com Insumo ($\mu$) | Gap Líquido ($\Delta$) | Estatística $t$ | $p$-valor | Conclusão |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Laboratório de Ciências** | 30,68% | 31,68% | **+1,00 p.p.** | $t = +6,60$ | $p < 0,001$ (***) | Relevante e significante |
| **Laboratório de Informática** | 30,88% | 30,94% | **+0,06 p.p.** | $t = +0,33$ | $p = 0,7419$ (ns) | **Estatisticamente Irrelevante** |
| **Biblioteca / Sala de Leitura**| 30,23% | 31,03% | **+0,80 p.p.** | $t = +4,33$ | $p < 0,001$ (***) | Relevante e significante |
| **Internet Banda Larga** | 30,30% | 30,97% | **+0,67 p.p.** | $t = +2,50$ | $p = 0,013$ (*) | Modesto mas significante |
| **Lousa Digital** | 30,80% | 31,27% | **+0,47 p.p.** | $t = +3,16$ | $p = 0,002$ (**) | Modesto |

#### A Ilusão da Tecnologia Isolada (Computadores para Alunos):
- Escolas com **Zero Computadores** ($N = 41$): Média = **30,28%**
- Escolas com **1 a 20 PCs** ($N = 576$): Média = **30,50%**
- Escolas com **21 a 50 PCs** ($N = 855$): Média = **30,94%**
- Escolas com **51 a 100 PCs** ($N = 1.316$): Média = **30,97%**
- Escolas com **Mais de 100 PCs** ($N = 823$, média de 140 PCs): Média = **31,20%**
- A distância entre ter **nenhum computador** e ter **140 máquinas** é de modestos **0,92 pontos percentuais**!

#### O Efeito do Porte Escolar:
- Pequeno Porte ($\le 8$ salas): Média = **31,44%** ($\mu = 110$ alunos)
- Médio Porte ($9$ a $14$ salas): Média = **31,11%** ($\mu = 182$ alunos)
- Grande Porte ($15+$ salas): Média = **30,54%** ($\mu = 302$ alunos)
- Escolas massificadas sofrem de despersonalização e maior dificuldade de controle pedagógico.

#### A Comparação Definitiva dos Três Modelos Econométricos ($R^2$ Cumulativo):
1. **Modelo 1 (Só INSE / Background Familiar)**: $R^2 = \mathbf{17,04\%}$
2. **Modelo 2 (INSE + Professores: IED e IRD)**: $R^2 = \mathbf{22,72\%}$ (Ganho Docente: **+5,68 p.p.**)
3. **Modelo 3 (INSE + Docentes + Infraestrutura Completa)**: $R^2 = \mathbf{24,01\%}$ (Ganho da Infraestrutura: **apenas +1,29 p.p.**)
- **Conclusão Teórica Central**: O fator humano docente explica **4,4 vezes mais da variabilidade das notas do que todos os prédios, salas e computadores combinados**. Na regressão controlada, o ganho líquido puro de um laboratório de ciências é de cerca de $+0,50$ p.p., enquanto cada máquina de computador tem coeficiente residual de $+0,0009$.
- **Artefato Gráfico**: `reports/figures/eda_05_infraestrutura_e_tecnologia.png` (painel conjugado com gaps dos insumos binários e boxplot por densidade de computadores em 300 DPI).

---

### 10.7 Passo 6 da EDA: O Mapeamento Sistemático das Escolas Resilientes (Efeito-Escola)
A literatura de Eficácia Escolar (Soares & Alves, 2003; Brooke, 2008) define resiliência educacional a partir do resíduo padronizado da regressão socioeconômica ($e_i = Y_i - \hat{Y}_i$). Classificaram-se as $3.594$ escolas em três regimes a partir do limiar de $1,5 \times \text{RMSE}$ ($+5,17$ p.p. acima da Reta de Coleman):

- **Desempenho Típico (Alinhado ao INSE)**: $3.211$ escolas (**89,34%** da rede);
- **Escolas Resilientes de Alta Eficácia**: **263 escolas (7,32% da rede)**;
- **Subdesempenho Crítico**: $120$ escolas (**3,34%** da rede).

#### O Raio-X Coletivo das 263 Escolas Resilientes:
Comparadas à rede geral, as escolas resilientes apresentam uma assinatura institucional inconfundível:
- **Desempenho Escolar**: Média de **39,23%** de acertos em Matemática (**+8,31 pontos percentuais acima da rede geral**);
- **Nível Socioeconômico Familiar**: $\text{INSE} = 5,29$ vs $5,25$ da rede geral (diferença nula de apenas $+0,05$ p.p. — **as famílias atendidas têm rigorosamente a mesma condição econômica da rede**);
- **Sobrecarga Docente Severa (% Cat 5 e 6)**: Apenas **9,35%** da equipe docente, contra **17,24%** na rede geral (**redução de quase a metade na sobrecarga!**);
- **Regularidade Docente (IRD)**: **2,90** vs **2,65** (professores mais estáveis e vinculados à unidade);
- **Porte Escolar**: Média de **140,6 alunos avaliados** contra **219,5** na rede geral (unidades menores e mais acolhedoras);
- **Parque Computacional**: **69,6 computadores** vs **69,7** na rede geral (diferença rigorosamente nula de $-0,12$ máquinas);
- **Laboratório de Ciências**: **34,2%** de presença contra **25,4%** na rede geral (+8,8 p.p.).

#### Concentração Geográfica e Polos Regionais:
- **Destaque Absoluto para a DE Apiaí (Vale do Ribeira)**: **9 escolas resilientes em 30 unidades (30,0% da diretoria inteira!)**, provando que uma das regiões de menor IDH do estado abriga o maior polo proporcional de resiliência e eficácia escolar paulista;
- Outras Diretorias Líderes: **DE Sertãozinho** ($28,0\%$), **DE Centro Oeste / Capital** ($20,6\%$, com a histórica EE Caetano de Campos Consolação atingindo superação de $+16,77$ p.p.), **DE Franca** ($19,5\%$) e **DE Campinas Leste** ($18,4\%$).
- **Artefato Gráfico**: `reports/figures/eda_06_escolas_resilientes_efeito_escola.png` (gráfico de dispersão com destaque para as 263 escolas resilientes e as faixas de resíduo em 300 DPI).

---

### 10.8 Passo 7 da EDA: O Acoplamento Interdisciplinar (Língua Portuguesa vs. Matemática)

Conforme problematizado durante a concepção da pesquisa, investigou-se a relação empírica entre a proficiência em Língua Portuguesa e o desempenho em Matemática no triênio 2022–2024 para as $3.611$ escolas estaduais da Camada Gold.

#### Delimitação Metodológica: Por que NÃO incluir Língua Portuguesa no Modelo de Machine Learning?
Adotou-se o rigor econométrico de **excluir Língua Portuguesa da matriz de variáveis preditivas** do modelo supervisionado:
1. **Prevenção de Vazamento de Alvo (*Target Leakage*) e Simultaneidade**: Ambas as notas foram aferidas no mesmo exame e sofrem a influência dos mesmos traços latentes cognitivos gerais do estudante e do clima escolar do dia da prova. 
2. **Preservação da Relevância para Políticas Públicas**: Ao incluir Língua Portuguesa como regressor, ela "roubaria" a maior parte da variância explicada, mascarando as variáveis institucionais acionáveis (sobrecarga docente, regularidade do corpo de professores, porte da unidade). O algoritmo se limitaria a prever que "escolas com notas altas em Português também pontuam bem em Matemática", esvaziando a finalidade diagnóstica da pesquisa.
3. **Enquadramento no TCC**: A análise entra como uma **Seção Especial de Validação Epistemológica e Visão Sistêmica de 360º**, alertando o leitor para a interdisciplinaridade sem criar falsas pretensões de causalidade unidirecional.

#### Principais Achados Empíricos:

1. **A Assimetria Estrutural Disciplinar (O Gap de 11 p.p.)**:
   - Média da Rede em Língua Portuguesa: **41,92%** ($\text{Mediana} = 41,42\%$; $\text{DP} = 4,53$);
   - Média da Rede em Matemática: **30,93%** ($\text{Mediana} = 30,35\%$; $\text{DP} = 3,86$);
   - **Gap Estrutural**: A proficiência média em Língua Portuguesa é **$+10,99$ pontos percentuais superior** à de Matemática. Conforme a teoria de Bourdieu (1986), o letramento linguístico é estimulado cotidianamente no meio social e familiar (conversação, mídias, redes sociais), enquanto os conteúdos do ciclo terminal de Matemática do Ensino Médio (trigonometria, análise combinatória, funções) dependem quase que exclusivamente da instrução formal escolar.

2. **A Força do Acoplamento Linear e Monotônico**:
   - Correlação Linear de Pearson: $r = \mathbf{+0,7932}$ ($p < 0,0001$);
   - Correlação de Postos de Spearman: $\rho = \mathbf{+0,8168}$ ($p < 0,0001$);
   - Coeficiente de Determinação ($R^2$): **$62,91\%$ da variância das notas de Matemática é compartilhada com Língua Portuguesa**!
   - Regressão Simples: $\text{TARGET\_TRIENAL\_MAT} = 2,60 + (0,676 \cdot \text{TARGET\_TRIENAL\_LP})$ com $\text{RMSE} = 2,35$ p.p.

3. **A Absorção do Fator Socioeconômico**:
   - Ao ajustar o modelo múltiplo: $\text{MAT} = -0,53 + (0,663 \cdot \text{MEDIA\_INSE}) + (0,667 \cdot \text{LP})$ ($R^2 = 66,69\%$);
   - O coeficiente do INSE desabou de $+6,80$ para apenas $+0,66$ (redução de $90,3\%$). Isso prova empiricamente que a linguagem atua como o principal veículo transmissor do capital cultural familiar: os estudantes com maior nível socioeconômico apresentam melhor letramento de leitura, o que por sua vez facilita a decodificação dos enunciados matemáticos.

4. **Matriz de Desempenho Interdisciplinar (4 Quadrantes)**:
   - **Q1: Dupla Vulnerabilidade (Baixo LP / Baixo MAT)**: $1.489$ escolas (**41,2%** da rede) — gargalo cognitivo e institucional generalizado;
   - **Q2: O Dilema da Linguagem (Alto LP / Baixo MAT)**: $315$ escolas (**8,7%** da rede) — alunos interpretam enunciados, mas a escola falha no ensino formal das exatas;
   - **Q3: Raciocínio Dissociado (Baixo LP / Alto MAT)**: $316$ escolas (**8,8%** da rede) — exceção estatística de unidades com foco específico em cálculo;
   - **Q4: Excelência Interdisciplinar (Alto LP / Alto MAT)**: $1.491$ escolas (**41,3%** da rede) — sinergia pedagógica e eficácia integral.

5. **A Assinatura das 263 Escolas Resilientes**:
   - As 263 escolas mapeadas no Passo 6 como tendo alto "Efeito-Escola" em Matemática atingem média de **49,13%** em Língua Portuguesa (**+7,20 p.p. acima da rede estadual**);
   - **93,5% (246 de 263) estão situadas no Quadrante de Excelência Integral (Q4)**. Isso comprova que a resiliência escolar não é uma anomalia isolada de um departamento disciplinar, mas decorre de uma cultura de gestão escolar eficiente e mobilizadora de toda a comunidade.
- **Artefato Gráfico**: `reports/figures/eda_07_portugues_vs_matematica.png` (painel conjugado com dispersão interdisciplinar, destaque para as escolas resilientes, assimetria estrutural das densidades KDE e boxplot por quartis em 300 DPI).

---

## 11. Conclusão da Fase Exploratória e Transição para Modelagem Preditiva

Com os 7 passos da Análise Exploratória de Dados (EDA) rigorosamente concluídos, mapearam-se todos os fenômenos empíricos da rede estadual paulista:
1. **Target Trienal Ponderado**: Distribuição leptocúrtica com cauda longa de alta proficiência ($N = 3.611$ escolas);
2. **Teste de Coleman**: O INSE explica apenas $17,05\%$ da variabilidade, deixando $82,95\%$ livres para o efeito institucional;
3. **Ranking de Features**: O corpo docente é o elemento intraescolar de maior impacto; a informática isolada é nula;
4. **Fatores Docentes**: O ambiente com baixa sobrecarga (IED) e alta regularidade (IRD) gera um ganho de $+2,20$ p.p.;
5. **Infraestrutura**: Confirmação empírica do paradoxo de Coleman (insumos físicos agregam apenas $+1,29$ p.p. ao $R^2$);
6. **Escolas Resilientes**: Mapeamento de 263 escolas de alta eficácia com INSE idêntico à rede e polos regionais como Apiaí ($30\%$ da diretoria);
7. **Acoplamento Interdisciplinar**: Forte correlação com Língua Portuguesa ($r = +0,793$), absorção do INSE pela linguagem e isolamento metodológico de LP para preservação do modelo preditivo.

### 11.1 Governança do Ambiente Computacional e Reprodutibilidade Científica (.venv)

Para assegurar os princípios **FAIR** (*Findable, Accessible, Interoperable, and Reusable*) da pesquisa científica moderna, adotou-se o isolamento estrito do ambiente de execução do projeto através de um ambiente virtual Python (`.venv`):

1. **Encapsulamento Local do Ecossistema**:
   - Criação de um ambiente virtual dedicado (`tcc_desempenho_escolar/.venv`), garantindo que todas as versões de interpretador, compiladores numéricos e bibliotecas de aprendizado de máquina não sofram interferências de pacotes externos do sistema operacional.
   - O arquivo `.gitignore` foi configurado para ignorar o binário do ambiente, mantendo o repositório enxuto e seguro para versionamento.

2. **Pilha de Software e Manifesto de Dependências (`requirements.txt`)**:
   - **Engenharia e Processamento de Dados**: `numpy`, `pandas`, `pyarrow`, `scipy`;
   - **Visualização Científica e Diagnóstico Gráfico**: `matplotlib`, `seaborn`;
   - **Modelagem Preditiva e Machine Learning**: `scikit-learn` (modelos lineares e ensembles baseados em árvores), `xgboost` e `lightgbm` (algoritmos de *Gradient Boosting* de alto desempenho);
   - **Explicabilidade e Teoria dos Jogos Cooperativos**: `shap` (*Shapley Additive exPlanations*) para auditoria transparente de relevância das *features*.
   - Todas as versões exatas foram congeladas no arquivo `requirements.txt` na raiz do projeto, permitindo que a banca examinadora ou futuros pesquisadores reproduzam a totalidade dos resultados empíricos com um único comando de instalação.

### 11.2 Roteiro Metodológico da Modelagem Preditiva (Pequenos Passos):
1. **Passo 1 — Preparação da Matriz de Features ($X$ e $y$)**:
   - Seleção das variáveis preditivas (infraestrutura, fatores docentes, porte escolar e controle do INSE);
   - Validação da ausência de valores nulos e confirmação do isolamento de vazamento de alvo (*Target Leakage*);
2. **Passo 2 — Linha de Base (*Baselines* Lineares com $K$-Fold)**:
   - Estratégia de validação cruzada ($5$-Fold com semente reprodutível);
   - Treinamento e avaliação de OLS, Ridge e Lasso ($R^2$, RMSE e MAE);
3. **Passo 3 — Captura de Não-Linearidades e Interações (Random Forest)**:
   - Treinamento do *ensemble* de árvores sob o mesmo protocolo de dobras e comparação com os baselines lineares;
4. **Passo 4 — Gradient Boosting (LightGBM / XGBoost)**:
   - Avaliação dos algoritmos de reforço por gradiente e consolidação da tabela unificada de performance;
5. **Passo 5 — Explicabilidade Global e Local via SHAP**:
   - Extração dos valores de Shapley para mensuração do impacto prático e hierarquia de cada decisão de gestão sobre a nota escolar.

---

## 12. Fase de Modelagem Preditiva: Algoritmos, Métricas e Interpretação

Nesta seção são documentadas as etapas de modelagem preditiva aplicadas sobre as 3.611 escolas estaduais paulistas, estruturadas sob os 5 pilares metodológicos: métodos e hiperparâmetros, motivações estratégicas, resultados empíricos consolidados, descobertas substantivas e fundamentação teórica.

### 12.1 Etapa 1 — Preparação e Auditoria da Matriz Analítica ($X$ e $y$)
1. **Métodos e Técnicas**:
   - Isolamento de 18 variáveis preditivas ($X$) agregadas na Camada Gold, abrangendo: Fator Docente (`IRD_MEDIO`, `IED_SCORE_MEDIO`, `IED_ESFORCO_ALTO`, `MED_CAT_1` a `MED_CAT_6`), Insumos Materiais/TI (`IN_LABORATORIO_CIENCIAS`, `IN_LABORATORIO_INFORMATICA`, `IN_BIBLIOTECA_SALA_LEITURA`, `IN_EQUIP_LOUSA_DIGITAL`, `IN_BANDA_LARGA`, `QT_SALAS_UTILIZADAS`, `QT_COMP_ALUNO`), Dinâmica Escolar (`TOTAL_ALUNOS_TRIENIO`) e Controle Socioeconômico (`MEDIA_INSE`).
   - Variável-alvo ($y$): `TARGET_TRIENAL_MAT` (média ponderada 2022–2024 de Matemática).
   - Auditoria de valores faltantes e imputação pontual via mediana da rede: `MEDIA_INSE` (17 escolas - 0,47%), `IRD_MEDIO` (3 escolas - 0,08%) e `IN_BANDA_LARGA` (7 escolas - 0,19%).
   - Preservação da amostra total íntegra de 3.611 unidades escolares em formato colunar otimizado (`matriz_features_modelagem.parquet`).
2. **Motivações Estratégicas**:
   - Eliminação estrita de *Target Leakage*: exclusão deliberada de notas contemporâneas de Língua Portuguesa e de anos individuais para garantir que o modelo capture exclusivamente a capacidade preditiva de fatores escolares estruturais e acionáveis.
3. **Fundamentação Teórica**:
   - Princípio de Eficácia Escolar (Soares & Alves, 2013): a modelagem preditiva só é epistemologicamente legítima se as variáveis de entrada refletirem políticas públicas e condições pedagógicas preexistentes, mantendo o controle sociológico familiar de partida (Coleman, 1966).

---

### 12.2 Etapa 2 — Linhas de Base Lineares (OLS, Ridge e Lasso com 5-Fold CV)
1. **Métodos e Técnicas**:
   - Validação cruzada com 5 dobras aleatórias (`KFold(n_splits=5, shuffle=True, random_state=42)`).
   - Encapsulamento de pré-processamento via `Pipeline(StandardScaler(), Model)` dentro de cada dobra para impedir qualquer vazamento de escala (*Data Leakage*).
   - Algoritmos testados: Mínimos Quadrados Ordinários (OLS), Regressão Ridge ($\alpha = 10,0$ / penalização $L_2$) e Regressão Lasso ($\alpha = 0,05$ / penalização $L_1$).
2. **Motivações Estratégicas**:
   - Estabelecer o "chão de fábrica" econométrico: determinar qual fração da proficiência escolar pode ser explicada por relações aditivas estritamente lineares.
   - Avaliar a presença de multicolinearidade entre os indicadores docentes via amortecimento de coeficientes (Ridge) e testar a esparsidade de variáveis redundantes (Lasso).
3. **Resumo dos Resultados Oficiais (5-Fold CV)**:

| Modelo | $R^2$ Médio (%) | $R^2$ DP (%) | RMSE (p.p.) | RMSE DP | MAE (p.p.) | MAE DP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1. OLS (Regressão Múltipla) | 23,09% | 0,37% | 3,385 | 0,070 | 2,433 | 0,073 |
| 2. Ridge (Regularização $L_2$) | 23,09% | 0,37% | 3,385 | 0,070 | 2,433 | 0,073 |
| 3. Lasso (Regularização $L_1$) | **23,14%** | 0,28% | **3,384** | 0,071 | **2,433** | 0,075 |

4. **Partes Descobertas e Diagnósticos Empíricos**:
   - Coeficientes padronizados ($\beta$) do Ridge:
     * `MEDIA_INSE`: $\beta = +1,436$ (ancoragem familiar decisiva);
     * `IRD_MEDIO` (Regularidade Docente): $\beta = +0,553$ (o maior efeito escolar isolado);
     * `QT_SALAS_UTILIZADAS` (Tamanho da escola): $\beta = -0,426$ (escolas massificadas apresentam penalização de escala);
     * `MED_CAT_5` e `IED_ESFORCO_ALTO`: $\beta = -0,262$ e $-0,191$ (a sobrecarga de trabalho docente reduz as médias escolares);
     * `IN_LABORATORIO_CIENCIAS`: $\beta = +0,185$ (único insumo físico com relevância positiva mensurável);
     * Insumos de TI: `QT_COMP_ALUNO` ($\beta = +0,037$), `IN_BANDA_LARGA` ($\beta = +0,034$) e `IN_LABORATORIO_INFORMATICA` ($\beta = +0,025$) situam-se na insignificância prática.
5. **Fundamentação Teórica**:
   - Confirmação do Paradoxo de Coleman (1966) e achados de Franco et al. (2007): a qualidade do corpo docente e a estabilidade da equipe (`IRD_MEDIO`) superam em uma ordem de grandeza o aporte de equipamentos físicos e digitais.

---

### 12.3 Etapa 3 — Captura de Não-Linearidades: Random Forest Regressor
1. **Métodos e Técnicas**:
   - Algoritmo: `RandomForestRegressor(n_estimators=200, min_samples_leaf=5, random_state=42, n_jobs=-1)`.
   - Protocolo: Exata mesma partição de 5-Fold CV (`random_state=42`).
   - Métrica de relevância: *Mean Decrease in Impurity* (MDI) baseada na redução acumulada da variância residual dos nós.
2. **Motivações Estratégicas**:
   - Quebrar a premissa de linearidade e declives constantes: testar se árvores particionadoras identificam efeitos de limiar (ex: se insumos físicos só operam ganhos em escolas com docentes estáveis).
   - Utilizar o princípio de agregação *Bagging* (Bootstrap Aggregating) para redução de variância frente aos modelos lineares.
3. **Resumo dos Resultados e Comparativo com Baselines**:

| Modelo | $R^2$ Médio (%) | $R^2$ DP (%) | RMSE (p.p.) | RMSE DP | MAE (p.p.) | MAE DP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Lasso (Melhor Linear) | 23,14% | 0,28% | 3,384 | 0,071 | 2,433 | 0,075 |
| **Random Forest Regressor** | **24,08%** | **0,89%** | **3,363** | **0,081** | **2,398** | **0,069** |
| *Ganho Empírico do Ensemble* | *+0,94 p.p.* | — | *-0,021 p.p.* | — | *-0,035 p.p.* | — |

4. **Partes Descobertas e Auditoria Crítica (Saneamento de ID Leakage)**:
   - **Auditoria Metodológica**: Na execução preliminar, o código identificador da escola (`CODESC`) foi inadvertidamente admitido no conjunto de features, obtendo $6,88\%$ de importância devido à capacidade das árvores de memorizarem faixas numéricas geográficas. A auditoria humana imediata detectou o vazamento (*spurious ID correlation*) e saneou o código, restringindo o modelo estritamente às 18 variáveis substantivas.
   - **Ranking MDI Limpo**:
     1. `MEDIA_INSE`: $32,64\%$
     2. `IRD_MEDIO`: $11,97\%$ (líder intraescolar absoluto)
     3. `TOTAL_ALUNOS_TRIENIO`: $10,76\%$
     4. `MED_CAT_3`: $6,18\%$
     5. `IED_SCORE_MEDIO` e `IED_ESFORCO_ALTO`: $5,58\%$ cada
     6. `QT_COMP_ALUNO`: $5,37\%$
     7. `QT_SALAS_UTILIZADAS`: $5,06\%$
     ...
     Lanternas: `IN_LABORATORIO_CIENCIAS` ($0,81\%$), `IN_EQUIP_LOUSA_DIGITAL` ($0,78\%$), `IN_LABORATORIO_INFORMATICA` ($0,46\%$), `IN_BIBLIOTECA_SALA_LEITURA` ($0,30\%$), `IN_BANDA_LARGA` ($0,06\%$).
5. **Fundamentação Teórica**:
   - O avanço de quase 1 ponto percentual em $R^2$ confirma que a dinâmica escolar envolve não-linearidades reais, corroborando as teses de Crahay (2000) e Bressoux (2003) sobre os efeitos conjugados e não aditivos das condições de trabalho docente.

---

### 12.4 Etapa 4 — Gradient Boosting (LightGBM): Paradigma Sequencial e Ruído Social
1. **Métodos e Técnicas**:
   - Algoritmo: `LGBMRegressor(n_estimators=150, learning_rate=0.05, num_leaves=20, min_child_samples=20, random_state=42)`.
   - Protocolo: Idêntico 5-Fold CV (`random_state=42`).
   - Métrica de relevância: Importância por Ganho Acumulado (*Gain Importance*), quantificando a redução total da perda quadrática ao longo das rodadas de boosting.
2. **Motivações Estratégicas**:
   - Avaliar a abordagem de reforço por gradiente (*Boosting*), na qual cada árvore subsequente foca exclusivamente na correção dos resíduos deixados pelas árvores anteriores.
3. **Resumo dos Resultados (LightGBM)**:

| Modelo | $R^2$ Médio (%) | $R^2$ DP (%) | RMSE (p.p.) | RMSE DP | MAE (p.p.) | MAE DP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gradient Boosting (LightGBM) | 22,72% | 1,94% | 3,393 | 0,107 | 2,429 | 0,090 |

4. **Partes Descobertas: Por que o Random Forest superou o LightGBM?**:
   - **Diagnóstico Teórico-Computacional**: Em bases educacionais e sociais com ruído comportamental não capturado, o aprendizado sequencial do *Boosting* tende a tentar "modelar" pequenas oscilações aleatórias nos resíduos. O *Bagging* (Random Forest), ao calcular a média de 200 árvores independentes, atua como um filtro robusto de redução de variância, consagrando-se como o modelo preditivo campeão da pesquisa.
   - **Ranking de Ganho (Gain)**:
     1. `MEDIA_INSE`: $37,20\%$
     2. `TOTAL_ALUNOS_TRIENIO`: $12,63\%$
     3. `IRD_MEDIO`: $11,83\%$
     ...
     Lanternas: `IN_LABORATORIO_CIENCIAS` ($0,87\%$), `IN_EQUIP_LOUSA_DIGITAL` ($0,68\%$), `IN_BIBLIOTECA` ($0,28\%$), `IN_LABORATORIO_INFORMATICA` ($0,25\%$), `IN_BANDA_LARGA` ($0,06\%$).
5. **Fundamentação Teórica**:
   - Demonstração empírica da resiliência de modelos ensembles tipo *Bagging* frente à aleatoriedade intrínseca dos fenômenos humanos (Breiman, 2001; Hastie, Tibshirani & Friedman, 2009).

---

### 12.5 Tabela Unificada de Benchmark e a Invariância Epistemológica dos Fatores

| Posição | Modelo | Paradigma | $R^2$ Médio | RMSE (p.p.) | MAE (p.p.) | Situação |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 🥇 | **Random Forest Regressor** | Ensemble (Bagging) | **24,08%** | **3,363** | **2,398** | **Modelo Campeão Oficial** |
| 🥈 | **Lasso Regression** | Linear Regularizado ($L_1$) | 23,14% | 3,384 | 2,433 | Baseline Esparso |
| 🥉 | **Ridge Regression** | Linear Regularizado ($L_2$) | 23,09% | 3,385 | 2,433 | Baseline Amortecido |
| 4º | **OLS (Regressão Múltipla)** | Linear Clássico | 23,09% | 3,385 | 2,433 | Baseline Econométrico |
| 5º | **Gradient Boosting (LightGBM)** | Ensemble (Boosting) | 22,72% | 3,393 | 2,429 | Sensível ao Ruído Residual |

#### Conclusão Epistemológica da Modelagem:
A hierarquia dos fatores preditivos mostrou-se **estritamente invariante à especificação algorítmica**: sob todos os modelos (paramétricos lineares, árvores em paralelo ou sequenciais), o capital socioeconômico (`MEDIA_INSE`) e a regularidade docente (`IRD_MEDIO`) dominam a variabilidade do desempenho, enquanto recursos digitais e equipamentos isolados exercem impacto nulo. Essa invariância confere ao TCC o mais elevado grau de robustez econométrica e validade interna.

---

## 13. Fase 07: Análise de Explicabilidade com SHAP e Interpretação Causal-Estatística

A transição da acurácia preditiva para a explicabilidade constitui a etapa culminante da pesquisa. Para superar a opacidade intrínseca dos modelos de aprendizado de máquina (*black-box*), aplicou-se a metodologia **SHAP** (*Shapley Additive exPlanations*) sobre o modelo campeão (**Random Forest Regressor**), estruturada sob os 5 pilares do protocolo metodológico.

### 13.1 Métodos e Técnicas Utilizadas
1. **Fundamentação Algorítmica (Teoria dos Jogos Cooperativos)**:
   - Utilização do algoritmo `shap.TreeExplainer` (Lundberg & Lee, 2017), otimizado para ensembles de árvores de decisão.
   - O algoritmo calcula as contribuições marginais justas de Shapley para cada uma das 18 variáveis preditivas em relação à proficiência média da rede estadual ($\mathbb{E}[f(x)] \approx 30,93\%$), garantindo as propriedades matemáticas de **Eficiência Aditiva**, **Simetria**, **Monotonicidade** e **Dummy/Inocuidade**.
2. **Ambiente Computacional e Escopo Amostral**:
   - Aplicação sobre o total de $N = 3.611$ escolas estaduais da Camada Gold, com matriz analítica 100% íntegra (zero valores nulos e 18 preditores limpos de identificadores).
3. **Artefatos Produzidos**:
   - Gráfico de Dispersão e Direcionalidade (*Beeswarm Plot*): `reports/figures/shap_01_summary_beeswarm.png` (300 DPI);
   - Gráfico de Importância Global Desenviesada (*Bar Plot*): `reports/figures/shap_02_bar_importance.png` (300 DPI);
   - Tabela Oficial de Impactos Marginais: `data/gold/importancias_shap_random_forest.csv`.

---

### 13.2 Motivações Estratégicas das Escolhas
1. **Superação do Viés de Impureza de Gini/MDI**:
   - Métricas tradicionais de importância em árvores (*Mean Decrease in Impurity*) apresentam viés favorável a variáveis contínuas com muitos valores únicos (como número de alunos ou salas). O SHAP calcula a contribuição marginal baseada em teoria dos jogos, fornecendo uma leitura desprovida de viés de escala.
2. **Identificação da Direcionalidade Causal-Estatística**:
   - O ranking MDI apenas indicava se a variável era relevante, mas não explicitava se "ter mais" daquela característica aumentava ou diminuía a nota da escola. O SHAP resolve essa lacuna ao separar os efeitos positivos e negativos com precisão em pontos percentuais.

---

### 13.3 Resumo Consolidado dos Resultados (Métricas SHAP Oficiais)

A tabela abaixo sintetiza o impacto médio absoluto de cada fator escolar na nota média trienal de Matemática, medido em pontos percentuais ($\text{p.p.}$):

| Posição | Variável (Feature) | Dimensão Avaliada | Impacto Médio SHAP (p.p.) | Comportamento no Beeswarm |
| :---: | :--- | :--- | :---: | :--- |
| 1º | `MEDIA_INSE` | Contexto Socioeconômico | **1,170** | Alto = Positivo (até $+7,5$ p.p.) / Baixo = Negativo (até $-2,5$ p.p.) |
| 2º | `IRD_MEDIO` | Fator Humano (Regularidade Docente) | **0,370** | Alto = Fortemente Positivo (até $+3,2$ p.p.) / Baixo = Negativo |
| 3º | `IED_ESFORCO_ALTO` | Fator Humano (Sobrecarga Docente) | **0,327** | Alto = Negativo (até $-1,0$ p.p.) / Baixo = Positivo (até $+1,3$ p.p.) |
| 4º | `MED_CAT_3` | Fator Humano (Esforço Intermediário) | **0,165** | Impacto moderado disperso em torno de zero |
| 5º | `TOTAL_ALUNOS_TRIENIO` | Porte da Unidade (Total de Alunos) | **0,149** | Alto = Negativo (despersonalização) / Baixo = Positivo |
| 6º | `QT_SALAS_UTILIZADAS` | Porte da Unidade (Infraestrutura) | **0,145** | Alto = Negativo (até $-1,5$ p.p.) / Baixo = Positivo (até $+3,0$ p.p.) |
| 7º | `IED_SCORE_MEDIO` | Fator Humano (Média de Esforço) | **0,144** | Alto = Negativo / Baixo = Positivo |
| 8º | `MED_CAT_5` | Fator Humano (Sobrecarga Elevada) | **0,104** | Alto = Negativo (redução acentuada de proficiência) |
| 9º | `QT_COMP_ALUNO` | Equipamento Tecnológico | **0,085** | Dispersão mínima em torno de zero |
| 10º | `MED_CAT_4` | Fator Humano (Esforço Médio-Alto) | **0,084** | Leve penalização em níveis elevados |
| 11º | `IN_LABORATORIO_CIENCIAS` | Insumo Pedagógico Físico | **0,055** | Presença = Leve ganho marginal ($+0,3$ p.p.) |
| 12º | `MED_CAT_2` | Fator Humano (Baixo Esforço) | **0,047** | Efeito protetivo suave |
| 13º | `MED_CAT_6` | Fator Humano (Sobrecarga Extrema) | **0,037** | Efeito negativo concentrado |
| 14º | `IN_EQUIP_LOUSA_DIGITAL` | Equipamento Tecnológico | **0,033** | Impacto marginal desprezível |
| 15º | `MED_CAT_1` | Fator Humano (Esforço Mínimo Ideal) | **0,027** | Presença = Ganho positivo de até $+1,2$ p.p. |
| 16º | `IN_LABORATORIO_INFORMATICA`| Equipamento Tecnológico | **0,011** | Efeito prático nulo |
| 17º | `IN_BIBLIOTECA_SALA_LEITURA`| Insumo Pedagógico Físico | **0,008** | Efeito prático nulo |
| 18º | `IN_BANDA_LARGA` | Infraestrutura Conectividade | **0,003** | Efeito prático nulo |

---

### 13.4 Partes Descobertas e Diagnósticos Substantivos

1. **A Magnitude do "Efeito-Escola Humano" Frente ao Contexto Social**:
   - A soma dos impactos dos dois principais fatores docentes — **Regularidade Docente** ($0,370$ p.p.) e **Sobrecarga Docente** ($0,327$ p.p.) — totaliza **$0,697$ p.p.**
   - Este valor representa **$59,6\%$ de toda a força explicativa do nível socioeconômico familiar (`MEDIA_INSE` = $1,170$ p.p.)**. Trata-se de uma constatação de imenso valor para as políticas educacionais: a gestão da equipe de professores tem poder institucional para contrabalançar a maior parte das desvantagens de partida dos estudantes.
2. **A Alavanca da Regularidade Docente (`IRD_MEDIO`)**:
   - Escolas com alta fixação do corpo docente (pontos rosas no *Beeswarm*) impulsionam a proficiência em até **$+3,2$ pontos percentuais**, enquanto unidades com rotatividade crônica (pontos azuis) sofrem penalizações de até $-1,2$ p.p.
3. **O Efeito Negativo de Escala e Despersonalização Escolar**:
   - Tanto `QT_SALAS_UTILIZADAS` quanto `TOTAL_ALUNOS_TRIENIO` apresentam correlação estatística negativa nas caudas: escolas de porte massificado (mais de 1.500 alunos e dezenas de salas) perdem até $-1,5$ p.p., ao passo que escolas de porte menor ou intermediário obtêm bônus preditivos de até $+3,0$ p.p., refletindo melhor ambiência escolar e proximidade comunitária.
4. **O Mito da Infraestrutura Isolada e a Falácia Tecnocêntrica**:
   - A soma de todas as variáveis de informática e conectividade (`IN_BANDA_LARGA`, `IN_LABORATORIO_INFORMATICA`, `IN_EQUIP_LOUSA_DIGITAL`, `QT_COMP_ALUNO`) totaliza meros **$0,132$ p.p.**, sendo superada em quase **três vezes** apenas pelo índice de regularidade docente isolado ($0,370$ p.p.).
   - O diagnóstico empírico evidencia o subaproveitamento de infraestruturas escolares: a entrega de hardware sem formação continuada, mediação pedagógica em sala de aula e planejamento curricular integrado gera retorno nulo na aprendizagem de Matemática.

---

### 13.5 Fundamentação Teórica e Sociológica dos Resultados

1. **A Teoria dos Jogos Cooperativos de Lloyd Shapley**:
   - A decomposição axiomática permitiu isolar o valor de Shapley de cada insumo, solucionando o problema clássico de multicolinearidade e atribuição de mérito em ambientes complexos.
2. **James Coleman (1966) e Pierre Bourdieu (1970)**:
   - A predominância de `MEDIA_INSE` ratifica a tese sociológica de que o capital cultural familiar constitui o alicerce fundamental do rendimento escolar, delimitando as condições de partida.
3. **Soares & Alves (2003, 2013) e Franco et al. (2007)**:
   - A constatação de que a estabilidade e as condições de trabalho docente explicam mais de metade do peso do INSE corrobora a literatura nacional de Eficácia Escolar: a escola pública faz diferença real quando garante vínculos pedagógicos consistentes e preserva a integridade de sua equipe docente.
4. **Cristia et al. (2014) e OCDE/PISA (2015)**:
   - O impacto residual da tecnologia sem mediação pedagógica confirma os achados empíricos de avaliações internacionais, demonstrando que a transformação digital na educação depende estritamente do protagonismo humano do educador.
5. **Lee & Smith (1997) e Crahay (2000)**:
   - A penalização de escolas de grande porte confirma os estudos de clima escolar e despersonalização, sugerindo que unidades com escalas mais humanas favorecem o acompanhamento individualizado e a eficácia pedagógica.

---

### 13.6 Explicabilidade Local (SHAP Waterfall): Comparação Pareada de Casos e o Efeito Moderador

A explicabilidade local investiga o comportamento do modelo preditivo no nível micro de unidades escolares individuais. Para ilustrar o funcionamento das árvores de decisão em situações concretas, realizou-se um pareamento metodológico estrito: selecionaram-se duas escolas estaduais situadas exatamente no mesmo estrato de vulnerabilidade socioeconômica ($\text{INSE} \approx 5,0$, correspondente à média das famílias da rede estadual), porém com trajetórias de proficiência diametralmente opostas.

#### 1. Métodos e Técnicas Utilizadas
- **Algoritmo de Decomposição**: `shap.plots.waterfall` aplicado sobre o modelo Random Forest treinado.
- **Ponto de Partida e Chegada**: A decomposição parte do valor esperado da rede ($\mathbb{E}[f(X)] = 30,923\%$) e adiciona contribuições positivas marginais ($+X$ em vermelho) ou subtrai penalizações ($-Y$ em azul) até alcançar o valor predito individual $f(x)$.
- **Critério de Amostragem Pareada**: Filtro no intervalo $4,90 \le \text{MEDIA\_INSE} \le 5,10$, isolando:
  * **Caso 1 (Escola Resiliente de Alta Eficácia)**: EE Assentamento Santa Clara (Mirante do Paranapanema);
  * **Caso 2 (Escola em Vulnerabilidade Institucional)**: EE Jardim Aracati II (São Paulo Capital — D.E. Sul 2).
- **Artefatos Produzidos**:
  * `reports/figures/shap_03_waterfall_escola_resiliente.png` (300 DPI);
  * `reports/figures/shap_04_waterfall_escola_vulneravel.png` (300 DPI).

---

#### 2. Resumo Numérico Comparativo dos Casos

| Dimensão Metodológica | Caso 1: EE Assentamento Santa Clara | Caso 2: EE Jardim Aracati II |
| :--- | :---: | :---: |
| **Município / Diretoria de Ensino** | Mirante do Paranapanema (Área Rural) | São Paulo Capital (D.E. Sul 2 — Periferia Urbana) |
| **Nível Socioeconômico Familiar (`MEDIA_INSE`)** | **$4,92$** (Vulnerável) | **$5,01$** (Vulnerável) |
| **Nota Real em Matemática (`TARGET_TRIENAL_MAT`)** | **$\mathbf{61,57\%}$** (Excelência Absoluta) | **$\mathbf{21,03\%}$** (Gargalo Crítico) |
| **Valor Predito pelo Modelo ($f(x)$)** | **$35,61\%$** ($+4,69$ p.p. sobre a rede) | **$27,67\%$** ($-3,25$ p.p. sob a rede) |
| **Impacto do Porte Escolar no SHAP** | **$+2,80$ p.p.** (`TOTAL_ALUNOS = 30`) | **$-0,53$ p.p.** (`QT_SALAS = 22`) |
| **Impacto da Sobrecarga Docente no SHAP** | $+0,20$ p.p. (Baixo Esforço) | **$-0,65$ p.p.** (`IED_ESFORCO_ALTO = 60%`) |
| **Penalização do INSE Familiar no SHAP** | **$-0,15$ p.p.** (Impacto Amortecido) | **$-2,13$ p.p.** (Impacto Amplificado) |

---

#### 3. Partes Descobertas: A Revelação do "Efeito Moderador" do Ambiente Escolar

A comparação entre as duas escolas revela uma das propriedades mais ricas do aprendizado de máquina não-linear frente aos modelos lineares tradicionais:

1. **A Não-Linearidade do Fator Socioeconômico**:
   - Em um modelo linear estrito, escolas com INSE $4,92$ e $5,01$ receberiam penalizações idênticas. No Random Forest, a penalização de `MEDIA_INSE` no Assentamento Santa Clara foi de apenas **$-0,15$ p.p.**, enquanto no Jardim Aracati II atingiu severos **$-2,13$ p.p.**
2. **O Efeito "Amortecedor Social" da Pequena Escala (Assentamento Santa Clara)**:
   - A unidade rural atende um contingente reduzido de alunos (`TOTAL_ALUNOS_TRIENIO = 30`), gerando um bônus preditivo imediato de **$+2,80$ p.p.** no topo da cascata SHAP. A forte integração comunitária e o acompanhamento próximo dos docentes operam como uma barreira protetora que impede que a vulnerabilidade familiar contamine o rendimento acadêmico dos estudantes.
3. **O Efeito "Amplificador da Vulnerabilidade" da Massificação (Jardim Aracati II)**:
   - A unidade periférica conjuga massificação física ($22$ salas de aula em uso, penalizando a nota em $-0,53$ p.p.) com colapso do trabalho docente (**$60\%$ dos professores sob esforço extremo**, subtraindo $-0,65$ p.p.). Na ausência de suporte institucional individualizado, a escola não compensa as carências domésticas, e a pobreza familiar atinge o estudante com sua força máxima ($-2,13$ p.p.).

---

#### 4. Fundamentação Teórica da Explicabilidade Local
- **Brooke & Soares (2008) e Rutter et al. (1979)**: O conceito de escola eficaz como moderadora de risco social demonstra que escolas organizadas não apenas aumentam a média geral, mas reduzem a dependência entre a origem social do aluno e seu destino escolar.
- **Lee & Smith (1997)**: A escala humana da unidade escolar atua como fator primordial de eficácia no ensino médio, prevenindo o anonimato e fortalecendo o pertencimento institucional.
- **Franco et al. (2007)**: A precarização das condições docentes em grandes centros urbanos desestrutura a capacidade da escola de oferecer respostas pedagógicas a estudantes em situação de desvantagem.

---

## 14. Fase 08: Síntese e Matriz de Priorização de Políticas Públicas Educacionais

A etapa de síntese estratégica encerra a transição da modelagem estatística para a governança aplicada. Para transformar os achados empíricos de Machine Learning e SHAP em subsídios de tomada de decisão para a Secretaria da Educação do Estado de São Paulo (SEDUC-SP), estruturou-se a **Matriz Acionável de Políticas Públicas**, baseada nos princípios da análise de custo-efetividade educacional.

### 14.1 Métodos e Técnicas Utilizadas
1. **Estrutura Bidimensional da Matriz 2x2**:
   - **Eixo Vertical ($Y$ — Retorno Pedagógico Real)**: Mensurado diretamente pelo impacto médio absoluto dos valores SHAP ($\text{mean}(|\text{SHAP value}|)$) no desempenho em Matemática, medido em pontos percentuais ($\text{p.p.}$).
   - **Eixo Horizontal ($X$ — Custo e Complexidade de Implementação)**: Escala técnica ordinal de $1$ a $5$:
     * *Nível 1 a 2*: Reformas de gestão, protocolos normativos e resoluções de atribuição de aulas (baixo impacto orçamentário direto);
     * *Nível 3*: Reorganização de espaços físicos e formações continuadas com suporte pedagógico;
     * *Nível 4 a 5*: Obras de ampliação predial, contratação de novos quadros efetivos e pregões massivos de aquisição de equipamentos tecnológicos.
   - **Limiares de Delimitação dos Quadrantes**:
     * *Corte de Impacto*: $0,12$ p.p. (separa fatores estruturantes de impactos residuais/marginais);
     * *Corte de Custo/Esforço*: $3,0$ (separa intervenções de gestão daquelas intensivas em capital).
2. **Artefatos Produzidos**:
   - Painel Gráfico Executivo: `reports/figures/matriz_01_politicas_publicas.png` (300 DPI);
   - Tabela de Decisão para Gestores: `data/gold/matriz_priorizacao_politicas_publicas.csv`.

---

### 14.2 Motivações Estratégicas das Escolhas
1. **Ponte entre Ciência de Dados e Orçamento Público**:
   - Os modelos preditivos identificam a força dos coeficientes, mas gestores públicos enfrentam restrições orçamentárias rígidas. A matriz fornece um instrumento visual objetivo para identificar onde cada real investido produz a maior alavancagem de aprendizagem.
2. **Superação da Ineficiência Alocativa**:
   - Combater a tendência histórica de compras de equipamentos sem vinculação a projetos pedagógicos estruturados, substituindo o senso comum por evidências causais-estatísticas desenviesadas.

---

### 14.3 Resumo Consolidado dos Resultados (Tabela Executiva de Priorização)

| Quadrante Estratégico | Intervenção Proposta | Métrica SHAP Base | Impacto Real (p.p.) | Custo / Esforço (1-5) | Recomendação Executiva para a SEDUC-SP |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Q1: Prioridade Estrutural** | Fixação Docente (Permanência) | `IRD_MEDIO` | **$+0,370$** | $2,2$ | Criar bônus de permanência e pontuação de carreira vinculada à estabilidade na mesma unidade. |
| **Q1: Prioridade Estrutural** | Teto de Sobrecarga Docente | `IED_ESFORCO_ALTO`| **$+0,327$** | $2,5$ | Limitar a atribuição a no máximo 2-3 turmas por professor em escolas de maior vulnerabilidade. |
| **Q2: Estruturante de Longo Prazo**| Desmassificação Escolar (Escala Humana)| `TOTAL_ALUNOS` / `QT_SALAS`| **$+0,149$** | $4,5$ | Modular novas construções para unidades de pequeno porte (< 500 alunos) ou criar subunidades autônomas. |
| **Q3: Eficiência Marginal / Manutenção**| Laboratório de Ciências Ativo | `IN_LABORATORIO_CIENCIAS`| $+0,055$ | $1,8$ | Fornecer kits experimentais de baixo custo e protocolos curriculares ativos para uso contínuo. |
| **Q3: Eficiência Marginal / Manutenção**| Salas de Leitura e Mediação | `IN_BIBLIOTECA_SALA_LEITURA`| $+0,008$ | $1,5$ | Integrar a leitura à decodificação de problemas e enunciados matemáticos (suporte interdisciplinar). |
| **Q4: Baixa Relação Custo-Efetividade** | Aquisição Massiva de Computadores | `QT_COMP_ALUNO` | $+0,085$ | $4,6$ | Condicionar novas aquisições de hardware à prévia capacitação docente e plano curricular integrado. |
| **Q4: Baixa Relação Custo-Efetividade** | Instalação de Lousas Digitais | `IN_EQUIP_LOUSA_DIGITAL`| $+0,033$ | $4,2$ | Priorizar a formação em metodologias ativas antes de novos pregões de telas interativas. |
| **Q4: Baixa Relação Custo-Efetividade** | Laboratórios Tradicionais de TI | `IN_LABORATORIO_INFORMATICA`| $+0,011$ | $3,8$ | Reavaliar espaços ociosos ou obsoletos e readequá-los para convivência e reforço pedagógico. |

---

### 14.4 Partes Descobertas e Diretrizes de Ação por Quadrante

1. **Quadrante 1 (Prioridade Estrutural — Alto Retorno / Custo de Gestão)**:
   - Constitui a "vitória rápida" (*quick win*) da rede: intervenções no regime de trabalho docente (`IRD_MEDIO` e `IED_ESFORCO_ALTO`) têm o maior impacto positivo sobre a proficiência, com custos primariamente normativos (alteração nas regras de atribuição de aulas e bônus de permanência).
2. **Quadrante 2 (Estruturante de Longo Prazo — Alto Retorno / Alto Custo)**:
   - A desmassificação de escolas de grande porte demanda planejamento de infraestrutura e longo prazo orçamentário, mas garante um bônus de escala humana duradouro que protege contra o anonimato e a dispersão dos estudantes.
3. **Quadrante 3 (Eficiência Marginal / Manutenção — Baixo Custo / Retorno Específico)**:
   - A recomendação para salas de leitura e laboratórios de ciências existentes é: **qualificar e dinamizar sem onerar o orçamento**. O papel da sala de leitura, conforme demonstrado no acoplamento interdisciplinar (EDA Passo 7), é atuar como plataforma de suporte para a interpretação de enunciados complexos de exatas.
4. **Quadrante 4 (Baixa Relação Custo-Efetividade — Alto Custo / Retorno Prático Residual)**:
   - O investimento continuado em hardware puro sem acompanhamento pedagógico consome recursos vultosos sem reflexo mensurável na proficiência. A diretriz é redirecionar o foco das compras de equipamentos para a valorização e fixação do corpo docente.

---

### 14.5 Fundamentação Teórica e de Economia da Educação
- **Levin & McEwan (2001)**: Os princípios de análise de custo-efetividade em políticas públicas educacionais determinam que intervenções com altos custos fixos de capital (como tecnologia desvinculada da pedagogia) possuem menor retorno marginal do que intervenções centradas no fator trabalho qualificado.
- **Soares & Alves (2003, 2013) e Franco et al. (2007)**: A literatura nacional de eficácia escolar corrobora a centralidade da estabilidade da equipe como a política mais rentável em termos de valor agregado educacional.
- **Cristia et al. (2014) e OCDE/PISA (2015)**: Evidências empíricas internacionais reiteram que a introdução de recursos de informática nas escolas não produz ganhos cognitivos sustentados caso não haja formação docente intensiva e alinhamento curricular.





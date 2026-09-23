# Caderno Metodológico e de Engenharia de Dados do TCC
**Projeto**: Modelagem Preditiva do Desempenho Escolar no Ensino Médio Paulista (2022–2024)  
**Data de Atualização**: 23/09/2026  
**Status**: Fase de Engenharia de Dados CONCLUÍDA COM SUCESSO (Camadas Bronze, Silver e Gold 100% Finalizadas)

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

## 10. Conclusão da Fase de Engenharia de Dados e Próximos Passos

Com a entrega da Camada Gold, encerra-se formalmente a **Fase de Engenharia e Preparação de Dados (Quinzena 3 do TCC)**. As próximas etapas contemplam:

1. **Análise Exploratória de Dados (EDA)**:
   - Matriz de correlação de Pearson/Spearman entre as Features ($X$) e o Target ($Y$);
   - Distribuições de densidade e testes de normalidade;
   - Análise de disparidades regionais por Diretoria de Ensino (DE) e Município;
2. **Modelagem Preditiva e Machine Learning**:
   - Definição do protocolo de validação cruzada (K-Fold estratificado por INSE/Região);
   - Baseline: Regressão Linear Múltipla e Modelos Regularizados (Ridge / Lasso);
   - Modelos Não-Lineares e Ensembles: Random Forest, Gradient Boosting, XGBoost e LightGBM;
   - Interpretabilidade e Explicabilidade: Importância de variáveis e valores de SHAP (Shapley Additive exPlanations).

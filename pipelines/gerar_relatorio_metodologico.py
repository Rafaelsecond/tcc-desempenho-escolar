"""GERADOR DO RELATÓRIO METODOLÓGICO E DE ENGENHARIA DE DADOS DO TCC

Objetivo:
  Documentar de forma viva, estruturada e acadêmica todas as decisões,
  etapas de ETL/ELT, descobertas estatísticas e validações de qualidade.
Saída:
  - reports/relatorio_metodologico_tcc.md
"""

from datetime import datetime
from pathlib import Path

DIRETORIO_RAIZ = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
PASTA_REPORTS = DIRETORIO_RAIZ / "reports"
PASTA_REPORTS.mkdir(parents=True, exist_ok=True)
ARQUIVO_RELATORIO = PASTA_REPORTS / "relatorio_metodologico_tcc.md"

data_formatada = datetime.now().strftime("%d/%m/%Y")

conteudo = """# Caderno Metodológico e de Engenharia de Dados do TCC
**Projeto**: Modelagem Preditiva do Desempenho Escolar no Ensino Médio Paulista (2022–2024)  
**Data de Atualização**: DATA_ATUAL_TAG  
**Status**: Camada Silver (Features X Concluídas; Validação Trienal Concluída; Fase Y em Iniciação)

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
  - No estado de São Paulo, verificou-se a relação fundamental: $\\text{CO\\_ENTIDADE} = 35 + \\text{CODESC}$.
- **Tratamento de Coordenadas Geográficas**:
  - As variáveis `DS_LATITUDE` e `DS_LONGITUDE` provenientes do cadastro da SEDUC foram convertidas do padrão brasileiro (vírgula decimal) para ponto decimal e tipadas como `float64`.
- **Tratamento do Caractere Oculto (BOM)**:
  - Identificado e removido o Byte Order Mark (`ï»¿NOMEDEP`) presente nos arquivos exportados do ecossistema Windows da SEDUC.
- **Engenharia de Recursos (Feature Engineering)**:
  - Criada a variável totalizadora de tecnologia para estudantes:
    $$\\text{QT\\_COMP\\_ALUNO} = \\text{QT\\_DESKTOP\\_ALUNO} + \\text{QT\\_COMP\\_PORTATIL\\_ALUNO}$$

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
     $$\\text{IED\\_SCORE\\_MEDIO} = \\frac{\\sum_{i=1}^{6} i \\cdot \\text{MED\\_CAT\\_i}}{100}$$
  2. **Percentual de Docentes com Sobrecarga Alta**:
     $$\\text{IED\\_ESFORCO\\_ALTO} = \\text{MED\\_CAT\\_5} + \\text{MED\\_CAT\\_6}$$
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

## 5. Próximos Passos: Construção da Variável-Alvo ($Y$)

A próxima etapa aborda o processamento dos microdados no nível do **estudante**:
1. **Passo 3 (SARESP 2022)**: Agregação da proficiência em Matemática para a 3ª série do Ensino Médio;
2. **Passo 4 (Provão Paulista 2023)**: Agregação da 3ª série do Ensino Médio;
3. **Passo 5 (Provão Paulista 2024)**: Agregação da 3ª série do Ensino Médio;
4. **Passo 6 (Target Trienal)**: Ponderação pelo número de alunos avaliados em cada ano e consolidação de $Y$;
5. **Passo 7 (Base Gold & Amostragem)**: Aplicação do filtro de corte amostral ($N \\ge 10$ ou $N \\ge 15$ alunos acumulados) para expurgar microclasses atípicas (unidades prisionais, socioeducativas e hospitalares).
"""

conteudo = conteudo.replace("DATA_ATUAL_TAG", data_formatada)
ARQUIVO_RELATORIO.write_text(conteudo, encoding="utf-8")

print(f"[SUCESSO] Relatório Metodológico gerado com sucesso!")
print(f"Destino: {ARQUIVO_RELATORIO}")
print(f"Tamanho: {ARQUIVO_RELATORIO.stat().st_size / 1024:.1f} KB")
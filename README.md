# TCC: Análise de Desempenho Escolar e Indicadores Educacionais (INEP)

Este repositório contém a base de código, pipelines de processamento e documentação metodológica do Trabalho de Conclusão de Curso (TCC) focado na análise do desempenho escolar e fatores educacionais a partir de microdados do INEP (Censo Escolar e Indicadores Educacionais).

---

## 📁 Estrutura do Projeto

O projeto segue a arquitetura em camadas (Medallion: *Raw*, *Silver*, *Gold*) para garantir rastreabilidade, reprodutibilidade e qualidade dos dados:

```text
├── data/
│   ├── raw/             # Microdados brutos do INEP (Censo Escolar e Indicadores) [ignorado no Git]
│   ├── silver/          # Dados tratados, normalizados e salvos em formato Parquet [ignorado no Git]
│   └── gold/            # Bases analíticas consolidadas para modelagem estatística [ignorado no Git]
├── pipelines/
│   ├── 01_Preparacao_censo/                 # Scripts de extração, limpeza e filtros do Censo Escolar
│   ├── 02_Indicadores_Educacionais_do_INEP/ # Scripts de inspeção, cálculo e integração dos indicadores
│   └── verificar_estrutura_trienal.py       # Validação da estabilidade e coerência das variáveis trienais
├── reports/
│   ├── metodos/         # Documentação dos métodos de limpeza e organização dos dados
│   ├── planejamento/    # Notas técnicas e planejamento de execução dos pipelines
│   └── validacao_estabilidade_trienal.md
├── .gitignore
└── README.md
```

---

## ⚙️ Pré-requisitos e Ambiente

- **Python 3.10+**
- Principais bibliotecas:
  - `pandas`
  - `pyarrow` / `fastparquet`
  - `numpy`

Recomenda-se o uso de um ambiente virtual para isolamento das dependências:

```bash
# Criação do ambiente virtual
python -m venv .venv

# Ativação no Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Instalação dos pacotes
pip install pandas pyarrow
```

---

## 📊 Pipeline de Processamento

1. **Camada Raw**: Os microdados oficiais baixados do portal do INEP são depositados em `data/raw/`.
2. **Camada Silver**:
   - `pipelines/01_Preparacao_censo/`: Limpeza, de-para de códigos e padronização dos Censos Escolares.
   - `pipelines/02_Indicadores_Educacionais_do_INEP/`: Processamento e enriquecimento com os indicadores educacionais (Adequação da Formação Docente, Complexidade da Gestão, Nível Socioeconômico, etc.).
3. **Validação**: Execução de scripts de validação de consistência temporal e estabilidade estrutural das variáveis.

---

## 📝 Observações sobre os Dados

Devido ao grande volume de dados brutos e intermediários (arquivos com centenas de megabytes ou gigabytes), os arquivos contidos na pasta `data/` estão desconsiderados pelo versionamento Git através do arquivo `.gitignore`. Apenas a estrutura de pastas é mantida.

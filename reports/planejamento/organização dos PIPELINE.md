[Raw Censo] ────────► Script 01 ──► 01_escolas_base
[Raw INEP Indic.] ──► Script 02 ──► 02_indicadores_inep
[Raw SARESP 2022] ──► Script 03 ──► 03_saresp_2022_escola ┐
[Raw Provão 2023] ──► Script 04 ──► 04_provao_2023_escola ┼► Script 06 ──► 06_target_trienal
[Raw Provão 2024] ──► Script 05 ──► 05_provao_2024_escola ┘                         │
                                                                                                                                   ▼
                      [01_escolas_base] + [02_indicadores_inep] + [06_target] ──► Script 07 ──► Final Dataset (Gold)


A modular pipeline follows the **Medallion Architecture (Bronze to Silver to Gold)**:

- **Bronze (Raw):** Immutable raw CSV files as downloaded from INEP and SEDUC.
- **Silver (Intermediate/Cleaned):** Cleaned, filtered, and aggregated tables saved per domain (one script per data source).
- **Gold (Analytical / Feature Store):** The final merged dataset ready for Machine Learning (`X` and `y`), with statistical quality filters applied.

---



### Pipeline Architecture & Directory Structure

To keep your project clean and reproducible, organize your repository like this:

```text
tcc_desempenho_escolar/
│
├── data/
│   ├── raw/                  # Original CSV files (never modified)
│   │   ├── censo_escolar_sp_2023.csv
│   │   ├── inep_inse_2021.csv
│   │   ├── inep_ird_2023.csv
│   │   ├── saresp_2022.csv
│   │   ├── provao_paulista_2023.csv
│   │   └── provao_paulista_2024.csv
│   │
│   ├── silver/               # Standardized tables & aggregates
│   │   ├── 01_escolas_base.parquet
│   │   ├── 02_indicadores_inep.parquet
│   │   ├── 03_saresp_2022_escola.parquet
│   │   ├── 04_provao_2023_escola.parquet
│   │   ├── 05_provao_2024_escola.parquet
│   │   └── 06_target_trienal.parquet
│   │
│   └── gold/                 # Final modeling dataset
│       └── tcc_dataset_analitico_final.parquet (and .csv)
│
├── pipelines/                # Numbered executable scripts
│   ├── 01_prep_censo_escolas.py
│   ├── 02_prep_indicadores_inep.py
│   ├── 03_prep_saresp_2022.py
│   ├── 04_prep_provao_2023.py
│   ├── 05_prep_provao_2024.py
│   ├── 06_build_target_trienal.py
│   └── 07_build_master_dataset.py
│
└── reports/                  # Validation logs and summary stats
    └── pipeline_quality_log.md

```

> **Engineering Tip:** Saving intermediate files in **Apache Parquet** format (`.parquet` via `pandas` / `pyarrow`) preserves exact data types (integers, floats, booleans), compresses files by 70–80%, and loads up to 10x faster than reading large CSVs repeatedly.

---



### Step-by-Step Implementation Roadmap

Each step below is a self-contained script with a **clear input**, **transformation rules**, **quality gates (validations)**, and an **output artifact**.

```
[Raw Censo] ────────► Script 01 ──► 01_escolas_base
[Raw INEP Indic.] ──► Script 02 ──► 02_indicadores_inep
[Raw SARESP 2022] ──► Script 03 ──► 03_saresp_2022_escola ┐
[Raw Provão 2023] ──► Script 04 ──► 04_provao_2023_escola ┼► Script 06 ──► 06_target_trienal
[Raw Provão 2024] ──► Script 05 ──► 05_provao_2024_escola ┘                         │
                                                                                    ▼
                      [01_escolas_base] + [02_indicadores_inep] + [06_target] ──► Script 07 ──► Final Dataset (Gold)

```

---



#### Step 1: School Master Spine (`01_prep_censo_escolas.py`)

- **Objective:** Establish the master spine of all eligible public high schools in São Paulo.
- **Input:** Raw Censo Escolar SP / Cadastro de Escolas.
- **Transformations:**
- Filter: State public network (`TP_DEPENDENCIA == 2`), active status, regular secondary education offering (`IN_REGULAR == 1` and `IN_MED == 1`).
- Pad codes: Format `CODESC` as 6-digit strings and `CO_ENTIDADE` as 8-digit strings (preventing lost leading zeros).
- Extract school characteristics: Geographic location (`DE`, `MUN`, coordinates) and infrastructure indicators (labs, internet, student computers).
- **Quality Gates (Validation):**
- Check for duplicate primary keys (`CODESC` and `CO_ENTIDADE` must be unique).
- Confirm zero missing values in primary identifiers.
- **Output:** `data/silver/01_escolas_base.parquet`

---



#### Step 2: Contextual School Indicators (`02_prep_indicadores_inep.py`)

- **Objective:** Process external socioeconomic and teacher-level features from INEP.
- **Inputs:** INEP tables (INSE - Nível Socioeconômico, IRD - Regularidade Docente, IED - Esforço Docente).
- **Transformations:**
- Parse Brazilian decimal commas (`"3,45"` $\to$ `3.45`).
- Filter records for SP state network schools.
- Standardize columns to snake_case or canonical prefixes (`INSE`_, `IRD`_).
- **Quality Gates (Validation):**
- Measure join coverage against `01_escolas_base` (identifying schools without INSE).
- Check value distributions (e.g., IRD must be bounded within the INEP scale).
- **Output:** `data/silver/02_indicadores_inep.parquet`

---



#### Step 3: SARESP 2022 Microdata Aggregation (`03_prep_saresp_2022.py`)

- **Objective:** Process individual student microdata from SARESP 2022 and aggregate to school level.
- **Input:** `Microdados SARESP 2022.csv`.
- **Transformations:**
- Filter cohort: 3ª série do Ensino Médio (`SERIE_ANO`).
- Filter test validity: Present and valid math test (`validade == 1`, `particip_mat == 1`, `porc_ACERT_MAT.notna()`).
- Compute school metrics:
- `QTD_ALUNOS_2022`: Count of valid participants.
- `MEDIA_ACERTOS_2022`: Mean percentage of correct math questions.
- `PERC_ABAIXO_2022`: Percentage of students with proficiency marked as "Abaixo do Básico".
- **Quality Gates (Validation):**
- Verify metric bounds ($0.0 \le \text{percentages} \le 100.0$).
- Check school-level count distribution (identify micro-classes with $N < 5$).
- **Output:** `data/silver/03_saresp_2022_escola.parquet`

---



#### Step 4 & Step 5: Provão Paulista 2023 & 2024 Aggregation (`04_...py` & `05_...py`)

- **Objective:** Process individual student microdata from Provão Paulista 2023 and 2024.
- **Inputs:** `Microdados de Alunos - Ensino Medio PROVAO - 2023.csv` and `2024.csv`.
- **Transformations:**
- Filter cohort: 3ª série do Ensino Médio.
- Filter test validity: Present in math exam (`particip_mat_ch == 1`, valid numeric score).
- Compute school metrics:
- `QTD_ALUNOS_202X`
- `MEDIA_ACERTOS_202X`
- `PERC_ABAIXO_202X` (using either calibrated percentile or defined cutoff).
- **Quality Gates (Validation):**
- Check participation rate across schools.
- Check score correlation against the 2022 baseline to verify consistent school ordering.
- **Outputs:** `data/silver/04_provao_2023_escola.parquet` and `data/silver/05_provao_2024_escola.parquet`

---



#### Step 6: Target Consolidation & Triennial Weighting (`06_build_target_trienal.py`)

- **Objective:** Consolidate the assessment outputs into clean triennial dependent variables ($Y$).
- **Inputs:** Silver artifacts from Steps 3, 4, and 5.
- **Transformations:**
- Full outer join across 2022, 2023, and 2024 on `CODESC`.
- Compute **cohort-weighted averages** (giving proportional weight to student sample sizes).
- Compute participation metadata: `TOTAL_ALUNOS_TRIENIO` and `ANOS_COM_DADOS` ($1, 2, \text{or } 3$).
- **Quality Gates (Validation):**
- Compare weighted vs. unweighted distributions to measure impact.
- Check for schools with missing assessment data across all 3 years.
- **Output:** `data/silver/06_target_trienal.parquet`

---



#### Step 7: Master Analytical Dataset & Modeling Cohort (`07_build_master_dataset.py`)

- **Objective:** Assemble the final dataset combining Features ($X$) and Target ($Y$).
- **Inputs:** `01_escolas_base`, `02_indicadores_inep`, and `06_target_trienal`.
- **Transformations:**
- Relational merge on `CODESC` / `CO_ENTIDADE`.
- Apply **statistical filtering for machine learning**:
- Remove non-assessed or newly opened units without target data.
- Apply sample size threshold (e.g., `TOTAL_ALUNOS_TRIENIO >= 10` or $\ge 15$) to exclude high-noise micro-classes (prisons, hospital classes).
- Document missing values across feature columns.
- **Quality Gates (Validation):**
- Verify that target variables have zero missing values in the modeling subset.
- Ensure no data leakage (features only represent school inputs, not post-exam scores).
- Generate summary statistics report.
- **Output:** `data/gold/tcc_dataset_analitico_final.parquet` (and `.csv`)

---



### How to Proceed

We will build and test these scripts **one by one**:

1. Run the script.
2. Inspect the output summary (row count, distributions, null counts).
3. Confirm that the quality gate passes.
4. Move to the next script.



---


"""
=============================================================================
FASE 06: MODELAGEM PREDITIVA — ETAPA 1: PREPARAÇÃO DA MATRIZ (X e y)
=============================================================================
Objetivo:
  Construir e auditar a matriz de features explicativas (X) e a variável-alvo (y)
  para o treinamento dos algoritmos de Machine Learning do TCC.

Critérios Metodológicos:
  1. Variável-Alvo (y):
     - TARGET_TRIENAL_MAT (Proficiência média ponderada de Matemática [0 - 100%])
  2. Variáveis Preditivas (X):
     - Fator Docente: IED_SCORE_MEDIO, IED_ESFORCO_ALTO, IRD_MEDIO, categorias de esforço
     - Infraestrutura: IN_LABORATORIO_CIENCIAS, IN_LABORATORIO_INFORMATICA,
       IN_BIBLIOTECA_SALA_LEITURA, IN_EQUIP_LOUSA_DIGITAL, IN_BANDA_LARGA,
       QT_SALAS_UTILIZADAS, QT_COMP_ALUNO
     - Porte da Unidade: TOTAL_ALUNOS_TRIENIO
     - Controle Social: MEDIA_INSE (Nível socioeconômico das famílias)
  3. Prevenção Rigorosa de Vazamento (Target Leakage):
     - Exclusão de notas anuais (2022, 2023, 2024) e de Língua Portuguesa.

Saída:
  - data/gold/matriz_features_modelagem.parquet
=============================================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np

# 1. Configuração de Caminhos
PROJECT_ROOT = Path(r"D:\TCC\Quinzena 3 - Material e metodo\tcc_desempenho_escolar")
ARQUIVO_GOLD = PROJECT_ROOT / "data" / "gold" / "tcc_dataset_analitico_final.parquet"
ARQUIVO_SAIDA = PROJECT_ROOT / "data" / "gold" / "matriz_features_modelagem.parquet"


def preparar_matriz():
    print("=" * 70)
    print("MODELAGEM PREDITIVA: ETAPA 1 — PREPARAÇÃO DA MATRIZ (X e y)")
    print("=" * 70)

    # 2. Carregar Camada Gold
    print("\n1. Carregando a Camada Gold consolidada...")
    df = pd.read_parquet(ARQUIVO_GOLD)
    print(f"   -> Escolas carregadas: {len(df):,} unidades")

    # 3. Definição do Alvo (y) e das Features (X)
    coluna_target = "TARGET_TRIENAL_MAT"
    
    colunas_features = [
        # Controle Socioeconômico Familiar
        "MEDIA_INSE",
        
        # Fator Humano Intraescolar (Docentes)
        "IED_SCORE_MEDIO",
        "IED_ESFORCO_ALTO",
        "IRD_MEDIO",
        "MED_CAT_1",
        "MED_CAT_2",
        "MED_CAT_3",
        "MED_CAT_4",
        "MED_CAT_5",
        "MED_CAT_6",
        
        # Insumos Físicos e Tecnológicos
        "IN_LABORATORIO_CIENCIAS",
        "IN_LABORATORIO_INFORMATICA",
        "IN_BIBLIOTECA_SALA_LEITURA",
        "IN_EQUIP_LOUSA_DIGITAL",
        "IN_BANDA_LARGA",
        "QT_SALAS_UTILIZADAS",
        "QT_COMP_ALUNO",
        
        # Porte Escolar e Dinâmica
        "TOTAL_ALUNOS_TRIENIO",
    ]

    print("\n2. Selecionando variáveis preditivas (Features)...")
    print(f"   -> Total de variáveis selecionadas em X: {len(colunas_features)}")
    for i, col in enumerate(colunas_features, 1):
        print(f"      {i:02d}. {col}")

    # 4. Tratamento de Valores Faltantes (Quality Gate)
    print("\n3. Auditoria de valores ausentes (Missing Values)...")
    df_modelo = df[["CODESC", coluna_target] + colunas_features].copy()
    
    nulos_antes = df_modelo[colunas_features].isna().sum()
    cols_com_nulos = nulos_antes[nulos_antes > 0]
    
    if len(cols_com_nulos) > 0:
        print("   -> Variáveis com valores ausentes identificadas:")
        for col, qtd in cols_com_nulos.items():
            print(f"      * {col}: {qtd} escolas sem dado ({qtd/len(df)*100:.2f}%)")
        
        # Imputação pela mediana da rede para preservar as escolas no modelo
        print("   -> Imputando valores faltantes pela mediana da rede...")
        for col in cols_com_nulos.index:
            mediana = df_modelo[col].median()
            df_modelo[col] = df_modelo[col].fillna(mediana)
            print(f"      * {col}: preenchido com mediana = {mediana:.3f}")
    else:
        print("   [PERFEITO] Nenhuma variável possui valores ausentes!")

    assert df_modelo.isna().sum().sum() == 0, "[FALHA] Ainda restam valores nulos na matriz!"
    print("   [PASS] Matriz 100% íntegra (zero valores nulos).")

    # 5. Dimensões Finais e Salvamento
    print("\n4. Salvando a matriz analítica para os algoritmos de ML...")
    ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)
    df_modelo.to_parquet(ARQUIVO_SAIDA, index=False)
    
    print(f"   -> Destino: {ARQUIVO_SAIDA}")
    print(f"   -> Dimensões: {df_modelo.shape[0]:,} escolas x {df_modelo.shape[1]-1} variáveis (X={len(colunas_features)}, y=1)")
    print("\n[SUCESSO] Etapa 1 concluída com sucesso! Matriz pronta para a modelagem.")


if __name__ == "__main__":
    preparar_matriz()

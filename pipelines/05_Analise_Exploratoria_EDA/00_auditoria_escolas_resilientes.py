"""
=============================================================================
AUDITORIA CIRÚRGICA: AS 5 ESCOLAS RESILIENTES NO DETALHE LONGITUDINAL
=============================================================================
Objetivo:
  Dissecar o comportamento histórico das 5 escolas de maior superação da
  Reta de Coleman, verificando:
  1. O volume de alunos e notas ano a ano (2022, 2023, 2024);
  2. Se as notas foram consistentemente altas ou se houve anomalia em algum ano;
  3. Características dos docentes (IED, IRD) e infraestrutura dessas escolas;
  4. Localização, município e contexto geográfico.
=============================================================================
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD_DIR = PROJECT_ROOT / "data" / "gold"
ARQUIVO_GOLD = GOLD_DIR / "tcc_dataset_analitico_final.parquet"

def auditar_resilientes():
    print("=" * 75)
    print("AUDITORIA DETALHADA DAS TOP 5 ESCOLAS RESILIENTES (SUPERAÇÃO DE COLEMAN)")
    print("=" * 75)

    df = pd.read_parquet(ARQUIVO_GOLD)
    
    # Calcular Reta de Coleman
    sub_inse = df[['MEDIA_INSE', 'TARGET_TRIENAL_MAT']].dropna()
    b1, b0 = pd.Series(pd.np.polyfit(sub_inse['MEDIA_INSE'], sub_inse['TARGET_TRIENAL_MAT'], deg=1)) if hasattr(pd, 'np') else (6.8003, -4.7674)
    # Cálculo exato usando numpy
    import numpy as np
    b1, b0 = np.polyfit(sub_inse['MEDIA_INSE'], sub_inse['TARGET_TRIENAL_MAT'], deg=1)
    
    df['PREVISTO_COLEMAN'] = b0 + b1 * df['MEDIA_INSE']
    df['RESIDUO_COLEMAN'] = df['TARGET_TRIENAL_MAT'] - df['PREVISTO_COLEMAN']

    # Top 5
    top5 = df.sort_values(by='RESIDUO_COLEMAN', ascending=False).head(5)

    for i, (_, row) in enumerate(top5.iterrows(), 1):
        print(f"\n[{i}] {row['NOMESC']} - CODESC: {row['CODESC']}")
        print(f"    Município: {row['MUN']} | Diretoria de Ensino: {row['DE']}")
        print(f"    Nível Socioeconômico (INSE): {row['MEDIA_INSE']:.2f} (Classificação: {row.get('INSE_CLASSIFICACAO', 'N/D')})")
        print(f"    Nota Trienal Ponderada (Y):  {row['TARGET_TRIENAL_MAT']:.2f}% de acertos")
        print(f"    Previsto por Coleman:        {row['PREVISTO_COLEMAN']:.2f}%")
        print(f"    Efeito Superação (Resíduo):  +{row['RESIDUO_COLEMAN']:.2f} p.p. acima do esperado")
        print(f"    Total Acumulado de Alunos:   {row['TOTAL_ALUNOS_TRIENIO']} estudantes no triênio")
        print(f"    Anos Avaliados:              {row['ANOS_AVALIADOS']} edições")
        print("-" * 65)
        print("    DESEMPENHO ANO A ANO:")
        print(f"      * 2022 (SARESP): {row.get('MEDIA_ACERTOS_2022', 'N/D')}% (Alunos: {row.get('QTD_ALUNOS_2022', 'N/D')})")
        print(f"      * 2023 (Provão): {row.get('MEDIA_ACERTOS_2023', 'N/D')}% (Alunos: {row.get('QTD_ALUNOS_2023', 'N/D')})")
        print(f"      * 2024 (Provão): {row.get('MEDIA_ACERTOS_2024', 'N/D')}% (Alunos: {row.get('QTD_ALUNOS_2024', 'N/D')})")
        print("-" * 65)
        print("    FATORES DOCENTES E INFRAESTRUTURA:")
        print(f"      * Esforço Docente Médio (IED):  {row.get('IED_SCORE_MEDIO', 'N/D'):.2f} (Escala 1 a 6 | Rede = 3.69)")
        print(f"      * Sobrecarga Alta (% Cat 5+6):  {row.get('IED_ESFORCO_ALTO', 'N/D')}% da equipe")
        print(f"      * Regularidade Docente (IRD):   {row.get('IRD_MEDIO', 'N/D'):.2f} (Escala 0 a 5 | Rede = 2.65)")
        print(f"      * Salas de Aula Utilizadas:     {row.get('QT_SALAS_UTILIZADAS', 'N/D')} salas")
        print(f"      * Computadores para Alunos:     {row.get('QT_COMP_ALUNO', 'N/D')} máquinas")
        print(f"      * Laboratório de Ciências:      {'SIM' if row.get('IN_LABORATORIO_CIENCIAS') == 1 else 'NÃO'}")
        print(f"      * Laboratório de Informática:   {'SIM' if row.get('IN_LABORATORIO_INFORMATICA') == 1 else 'NÃO'}")

if __name__ == "__main__":
    auditar_resilientes()

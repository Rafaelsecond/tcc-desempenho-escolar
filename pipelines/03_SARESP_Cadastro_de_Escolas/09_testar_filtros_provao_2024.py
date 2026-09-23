"""
=============================================================================
PIPELINE 05: TESTE DE FILTROS E COBERTURA DO PROVÃO PAULISTA 2024
=============================================================================
Objetivo:
  Validar a estratégia de filtragem para a 3ª série do Ensino Médio de 2024:
  1. Contabilizar total de registros no arquivo bruto;
  2. Mapear categorias de SERIE_ANO e TIPOCLASSE;
  3. Verificar formato numérico de 'porc_mat', 'acertos_mat' e 'nota_mat';
  4. Contar alunos válidos da 3ª série EM com presença em Matemática;
  5. Contar escolas distintas e calcular taxa de cruzamento com a base Silver.
=============================================================================
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "1. SEDUC-SP — SARESP & Cadastro de Escolas" / "A - Microdados do SARESP (Variável-Alvo Y)" / "Microdados de Alunos - SARESP_Provao - 2024"
ARQUIVO_PROVAO_2024 = RAW_DIR / "Microdados de Alunos - Ensino Medio PROVAO - 2024.csv"
ARQUIVO_ESCOLAS_SILVER = PROJECT_ROOT / "data" / "silver" / "01_escolas_base.parquet"

def testar_filtros():
    print("Lendo colunas essenciais do Provão 2024 (otimizado via usecols)...\n")
    
    cols = ['CODESC', 'SERIE_ANO', 'TIPOCLASSE', 'validade', 'particip_mat_ch', 'porc_mat', 'acertos_mat', 'nota_mat']
    
    # Leitura como string para auditoria precisa
    df = pd.read_csv(
        ARQUIVO_PROVAO_2024,
        sep=';',
        encoding='latin1',
        usecols=cols,
        dtype=str
    )
    
    print(f"Total de registros de alunos no Provão 2024: {len(df):,}")
    
    # 1. Analisar SERIE_ANO
    series = df['SERIE_ANO'].dropna().unique().tolist()
    print(f"\nValores de SERIE_ANO encontrados no arquivo:\n{series}")
    
    # 2. Analisar TIPOCLASSE
    print(f"\nDistribuição de TIPOCLASSE:\n{df['TIPOCLASSE'].value_counts(dropna=False).head(10).to_dict()}")
    
    # 3. Identificar rótulo da 3ª série do EM
    serie_em3 = [s for s in series if '3' in s and 'EM' in s]
    print(f"\nRótulos identificados da 3ª série: {serie_em3}")
    
    # 4. Aplicar filtros passo a passo
    mask_em3 = df['SERIE_ANO'].str.contains('EM-3', na=False)
    mask_valid = df['validade'] == '1'
    mask_partic = df['particip_mat_ch'] == '1'
    mask_nota = df['porc_mat'].notna() & (df['porc_mat'].str.strip() != '')
    
    df_filtrado = df[mask_em3 & mask_valid & mask_partic & mask_nota].copy()
    
    print(f"\nTotal de alunos da 3ª série EM com prova de Matemática válida em 2024: {len(df_filtrado):,}")
    
    # 5. Análise do CODESC e cruzamento
    df_filtrado['CODESC_PADRAO'] = df_filtrado['CODESC'].str.split('.').str[0].str.zfill(6)
    escolas_provao = set(df_filtrado['CODESC_PADRAO'].unique())
    print(f"Total de escolas distintas no Provão 2024: {len(escolas_provao):,}")
    
    # 6. Cruzamento com base Silver do Censo
    df_escolas_silver = pd.read_parquet(ARQUIVO_ESCOLAS_SILVER)
    escolas_silver = set(df_escolas_silver['CODESC'].unique())
    
    escolas_em_comum = escolas_provao.intersection(escolas_silver)
    taxa_cobertura = (len(escolas_em_comum) / len(escolas_silver)) * 100
    print(f"Escolas que cruzam com a base Silver (Passo 1): {len(escolas_em_comum):,} de {len(escolas_silver):,} ({taxa_cobertura:.1f}%)")
    
    # 7. Amostra de conversão numérica
    print("\nVerificando conversão numérica das métricas de Matemática:")
    exemplo_porc = df_filtrado['porc_mat'].str.replace(',', '.').astype(float)
    exemplo_acertos = df_filtrado['acertos_mat'].str.replace(',', '.').astype(float)
    exemplo_nota = df_filtrado['nota_mat'].str.replace(',', '.').astype(float)
    
    print(f" - porc_mat   -> Média: {exemplo_porc.mean():.2f}% | Min: {exemplo_porc.min():.2f}% | Max: {exemplo_porc.max():.2f}%")
    print(f" - acertos_mat-> Média: {exemplo_acertos.mean():.2f} acertos | Min: {exemplo_acertos.min():.2f} | Max: {exemplo_acertos.max():.2f}")
    print(f" - nota_mat   -> Média: {exemplo_nota.mean():.2f} | Min: {exemplo_nota.min():.2f} | Max: {exemplo_nota.max():.2f}")

if __name__ == "__main__":
    testar_filtros()

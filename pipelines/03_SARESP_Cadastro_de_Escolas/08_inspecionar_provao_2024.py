"""
=============================================================================
PIPELINE 05: INSPEÇÃO PRELIMINAR DOS MICRODADOS DO PROVÃO PAULISTA 2024
=============================================================================
Objetivo:
  Inspecionar as primeiras linhas do arquivo de 2024 para identificar:
  1. Encoding e separador;
  2. Nomes exatos das colunas (CODESC, SERIE_ANO, particip_mat, porc_mat, etc.);
  3. Valores presentes na coluna de série do Ensino Médio.
=============================================================================
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "1. SEDUC-SP — SARESP & Cadastro de Escolas" / "A - Microdados do SARESP (Variável-Alvo Y)" / "Microdados de Alunos - SARESP_Provao - 2024"
ARQUIVO_PROVAO_2024 = RAW_DIR / "Microdados de Alunos - Ensino Medio PROVAO - 2024.csv"

def inspecionar():
    print(f"Verificando existência do arquivo:\n{ARQUIVO_PROVAO_2024}\n")
    if not ARQUIVO_PROVAO_2024.exists():
        print(f"[ERRO] Arquivo não encontrado!")
        return

    print("Tentando ler primeiras 5 linhas com diferentes encodings...")
    encodings = ['latin1', 'utf-8', 'cp1252']
    separadores = [';', ',']
    
    df_sample = None
    enc_usado = None
    sep_usado = None
    
    for enc in encodings:
        for sep in separadores:
            try:
                df = pd.read_csv(ARQUIVO_PROVAO_2024, sep=sep, encoding=enc, nrows=5)
                if len(df.columns) > 10:
                    df_sample = df
                    enc_usado = enc
                    sep_usado = sep
                    break
            except Exception:
                continue
        if df_sample is not None:
            break
            
    if df_sample is None:
        print("[ERRO] Não foi possível ler as primeiras linhas com as combinações testadas.")
        return

    print(f"[SUCESSO] Lido com encoding='{enc_usado}' e separador='{sep_usado}'!")
    print(f"Total de colunas detectadas: {len(df_sample.columns)}\n")
    
    print("Colunas presentes:")
    for col in df_sample.columns:
        print(f" - {col}")
        
    print("\n" + "="*50)
    print("AMOSTRA DAS VARIÁVEIS CHAVE:")
    print("="*50)
    colunas_interesse = [c for c in df_sample.columns if any(k in c.lower() for k in ['cod', 'mun', 'esc', 'serie', 'ano', 'valid', 'partic', 'mat', 'porc', 'acerto'])]
    print("Colunas de interesse identificadas:", colunas_interesse)
    print(df_sample[colunas_interesse].head(3))

if __name__ == "__main__":
    inspecionar()

"""
Teste rápido da interface atualizada
"""

import pandas as pd
from pathlib import Path
from conversor_utm import ConversorUTM

def testar_conversao_letras():
    """Testa a conversão usando letras de colunas"""
    
    # Cria o conversor
    conversor = ConversorUTM(zona_utm=23, hemisferio='S', datum='SIRGAS2000')
    
    # Carrega um arquivo de teste
    arquivo_teste = Path("csv/Prlc_FazendaTamandua_001 - Pnt.csv")
    
    if not arquivo_teste.exists():
        print("❌ Arquivo de teste não encontrado")
        return
    
    try:
        # Carrega o arquivo
        df = pd.read_csv(arquivo_teste, encoding='latin-1', sep=';')
        print(f"✅ Arquivo carregado: {len(df)} linhas")
        print(f"📊 Colunas: {list(df.columns)}")
        
        # Converte letras para índices
        col_x = 'B'  # E/Long
        col_y = 'D'  # N/Lat
        
        idx_x = ord(col_x.upper()) - ord('A')
        idx_y = ord(col_y.upper()) - ord('A')
        
        print(f"🎯 Coluna X: {col_x} (índice {idx_x})")
        print(f"🎯 Coluna Y: {col_y} (índice {idx_y})")
        
        # Testa algumas linhas
        print("\n📋 Primeiras 3 linhas:")
        for i in range(min(3, len(df))):
            if i == 0:
                print(f"Linha {i+1} (cabeçalho): {df.iloc[i, idx_x]} | {df.iloc[i, idx_y]}")
            else:
                valor_x = str(df.iloc[i, idx_x]).replace(',', '.')
                valor_y = str(df.iloc[i, idx_y]).replace(',', '.')
                print(f"Linha {i+1}: {valor_x} | {valor_y}")
                
                # Testa conversão
                try:
                    utm_x = float(valor_x)
                    utm_y = float(valor_y)
                    resultado = conversor.converter_utm_para_dms(utm_x, utm_y)
                    print(f"  → {resultado['longitude_dms']} | {resultado['latitude_dms']}")
                except Exception as e:
                    print(f"  → Erro: {e}")
        
        print("\n✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    testar_conversao_letras()

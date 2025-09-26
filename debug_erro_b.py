"""
Debug específico do erro 'B'
"""

import pandas as pd
from pathlib import Path

def debug_erro():
    arquivo = Path("csv/Prlc_FazendaTamandua_001 - Pnt.csv")
    
    try:
        # Carrega o arquivo
        df = pd.read_csv(arquivo, encoding='latin-1', sep=';')
        print(f"Arquivo carregado: {len(df)} linhas")
        print(f"Colunas: {list(df.columns)}")
        
        # Verifica as primeiras linhas
        print(f"\nPrimeiras 5 linhas:")
        for i in range(min(5, len(df))):
            row = df.iloc[i]
            print(f"Linha {i+1}:")
            print(f"  E/Long: '{row['E/Long']}' (tipo: {type(row['E/Long'])})")
            print(f"  N/Lat: '{row['N/Lat']}' (tipo: {type(row['N/Lat'])})")
            
            # Testa conversão
            try:
                valor_x = str(row['E/Long']).replace(',', '.').strip()
                valor_y = str(row['N/Lat']).replace(',', '.').strip()
                
                print(f"  Valor X processado: '{valor_x}'")
                print(f"  Valor Y processado: '{valor_y}'")
                
                if valor_x and valor_y:
                    utm_x = float(valor_x)
                    utm_y = float(valor_y)
                    print(f"  ✅ Conversão OK: X={utm_x}, Y={utm_y}")
                else:
                    print(f"  ❌ Valores vazios")
                    
            except Exception as e:
                print(f"  ❌ Erro na conversão: {e}")
            
            print()
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    debug_erro()

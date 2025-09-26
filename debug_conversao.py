"""
Debug da conversão para identificar o problema
"""

import pandas as pd
from conversor_utm import ConversorUTM

# Cria o conversor
conversor = ConversorUTM(zona_utm=23, hemisferio='S', datum='SIRGAS2000')

# Testa com dados simples
print("=== TESTE 1: Conversão Simples ===")
try:
    resultado = conversor.converter_utm_para_dms(500000, 7000000)
    print(f"✅ Conversão simples OK: {resultado}")
except Exception as e:
    print(f"❌ Erro na conversão simples: {e}")

# Testa com DataFrame
print("\n=== TESTE 2: Com DataFrame ===")
try:
    # Cria DataFrame de teste
    df = pd.DataFrame({
        'ID': [1, 2, 3],
        'X': [500000, 501000, 502000],
        'Y': [7000000, 7001000, 7002000]
    })
    
    print("DataFrame criado:")
    print(df)
    print(f"Tipos das colunas: {df.dtypes}")
    
    # Testa conversão linha por linha
    for i, row in df.iterrows():
        print(f"\nLinha {i}:")
        print(f"  X: {row['X']} (tipo: {type(row['X'])})")
        print(f"  Y: {row['Y']} (tipo: {type(row['Y'])})")
        
        try:
            utm_x = float(row['X'])
            utm_y = float(row['Y'])
            print(f"  Convertido para float: X={utm_x}, Y={utm_y}")
            
            resultado = conversor.converter_utm_para_dms(utm_x, utm_y)
            print(f"  ✅ Conversão OK: {resultado['longitude_dms']}, {resultado['latitude_dms']}")
            
        except Exception as e:
            print(f"  ❌ Erro na linha {i}: {e}")
            import traceback
            traceback.print_exc()

except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()

print("\n=== TESTE 3: Com arquivo CSV ===")
try:
    # Testa carregar arquivo CSV
    df_csv = pd.read_csv('teste.csv')
    print("Arquivo CSV carregado:")
    print(df_csv)
    print(f"Tipos: {df_csv.dtypes}")
    
    # Testa primeira linha
    primeira_linha = df_csv.iloc[0]
    print(f"\nPrimeira linha: {primeira_linha}")
    print(f"X: {primeira_linha['X']} (tipo: {type(primeira_linha['X'])})")
    print(f"Y: {primeira_linha['Y']} (tipo: {type(primeira_linha['Y'])})")
    
    utm_x = float(primeira_linha['X'])
    utm_y = float(primeira_linha['Y'])
    
    resultado = conversor.converter_utm_para_dms(utm_x, utm_y)
    print(f"✅ Conversão CSV OK: {resultado}")
    
except Exception as e:
    print(f"❌ Erro com CSV: {e}")
    import traceback
    traceback.print_exc()

"""
Teste rápido da correção
"""

import pandas as pd
from conversor_utm import ConversorUTM
from pathlib import Path

def teste_rapido():
    conversor = ConversorUTM(zona_utm=23, hemisferio='S', datum='SIRGAS2000')
    
    # Testa com um arquivo específico
    arquivo = Path("csv/Prlc_FazendaTamandua_001 - Pnt.csv")
    
    try:
        # Carrega o arquivo
        df = pd.read_csv(arquivo, encoding='latin-1', sep=';')
        print(f"Arquivo carregado: {len(df)} linhas")
        print(f"Colunas: {list(df.columns)}")
        
        # Testa conversão das primeiras 3 linhas
        for i in range(min(3, len(df))):
            try:
                row = df.iloc[i]
                
                # Converte vírgula para ponto
                valor_x = str(row['E/Long']).replace(',', '.').strip()
                valor_y = str(row['N/Lat']).replace(',', '.').strip()
                
                print(f"\nLinha {i+1}:")
                print(f"  Valor X original: '{row['E/Long']}' -> '{valor_x}'")
                print(f"  Valor Y original: '{row['N/Lat']}' -> '{valor_y}'")
                
                if valor_x and valor_y:
                    utm_x = float(valor_x)
                    utm_y = float(valor_y)
                    
                    resultado = conversor.converter_utm_para_dms(utm_x, utm_y)
                    print(f"  ✅ Conversão OK: {resultado['longitude_dms']}, {resultado['latitude_dms']}")
                else:
                    print(f"  ❌ Valores vazios")
                    
            except Exception as e:
                print(f"  ❌ Erro na linha {i+1}: {e}")
        
        print("\n✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    teste_rapido()

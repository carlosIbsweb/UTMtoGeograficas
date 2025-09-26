"""
Teste da correção final
"""

import pandas as pd
from conversor_utm import ConversorUTM
from pathlib import Path

def teste_final():
    conversor = ConversorUTM(zona_utm=23, hemisferio='S', datum='SIRGAS2000')
    
    # Testa com um arquivo específico
    arquivo = Path("csv/Prlc_FazendaTamandua_001 - Pnt.csv")
    
    try:
        # Carrega o arquivo
        df = pd.read_csv(arquivo, encoding='latin-1', sep=';')
        print(f"Arquivo carregado: {len(df)} linhas")
        print(f"Colunas: {list(df.columns)}")
        
        # Simula a conversão como no sistema
        longitudes_dms = []
        latitudes_dms = []
        sucessos = 0
        erros = 0
        
        for i, row in df.iterrows():
            try:
                # Converte valores para float, tratando vírgula como separador decimal
                valor_x = str(row['E/Long']).replace(',', '.')
                valor_y = str(row['N/Lat']).replace(',', '.')
                
                # Remove espaços
                valor_x = valor_x.strip()
                valor_y = valor_y.strip()
                
                # Verifica se é um número válido
                if not valor_x or not valor_y:
                    raise ValueError("Valor vazio")
                
                # Tenta converter para float
                try:
                    utm_x = float(valor_x)
                    utm_y = float(valor_y)
                except ValueError:
                    raise ValueError(f"Valor não numérico: X='{valor_x}', Y='{valor_y}'")
                
                # Converte as coordenadas
                resultado = conversor.converter_utm_para_dms(utm_x, utm_y)
                
                longitudes_dms.append(resultado['longitude_dms'])
                latitudes_dms.append(resultado['latitude_dms'])
                sucessos += 1
                
                if sucessos <= 3:  # Mostra apenas as primeiras 3 conversões
                    print(f"Linha {i+1}: UTM({utm_x}, {utm_y}) → {resultado['longitude_dms']}, {resultado['latitude_dms']}")
                
            except Exception as e:
                print(f"Linha {i+1} pulada: {e}")
                longitudes_dms.append('')
                latitudes_dms.append('')
                erros += 1
        
        print(f"\nResultado:")
        print(f"✅ Sucessos: {sucessos}")
        print(f"❌ Erros: {erros}")
        print(f"📊 Total de linhas: {len(df)}")
        
        if sucessos > 0:
            print(f"\n✅ Conversão funcionando!")
        else:
            print(f"\n❌ Nenhuma conversão bem-sucedida")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    teste_final()

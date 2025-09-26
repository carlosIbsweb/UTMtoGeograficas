"""
Teste específico para os arquivos CSV da pasta csv/
"""

import pandas as pd
from conversor_utm import ConversorUTM
from pathlib import Path

def testar_conversao_csv():
    """Testa a conversão dos arquivos CSV reais"""
    
    # Cria o conversor
    conversor = ConversorUTM(zona_utm=23, hemisferio='S', datum='SIRGAS2000')
    
    # Pasta com os arquivos CSV
    pasta_csv = Path("csv")
    
    if not pasta_csv.exists():
        print("❌ Pasta 'csv' não encontrada!")
        return
    
    # Lista arquivos CSV
    arquivos_csv = list(pasta_csv.glob("*.csv"))
    print(f"📁 Encontrados {len(arquivos_csv)} arquivos CSV:")
    for arquivo in arquivos_csv:
        print(f"  • {arquivo.name}")
    
    print("\n" + "="*60)
    
    # Testa cada arquivo
    for arquivo_csv in arquivos_csv:
        print(f"\n🔍 Testando: {arquivo_csv.name}")
        
        try:
            # Tenta diferentes codificações e separadores
            df = None
            codificacao_usada = None
            separador_usado = None
            
            codificacoes = ['latin-1', 'cp1252', 'utf-8', 'iso-8859-1']
            separadores = [';', ',', '\t']
            
            for encoding in codificacoes:
                for sep in separadores:
                    try:
                        df = pd.read_csv(arquivo_csv, encoding=encoding, sep=sep)
                        codificacao_usada = encoding
                        separador_usado = sep
                        print(f"✅ Carregado com codificação: {encoding}, separador: '{sep}'")
                        break
                    except:
                        continue
                if df is not None:
                    break
            
            if df is None:
                print(f"❌ Não foi possível carregar {arquivo_csv.name}")
                continue
            
            print(f"📊 Colunas encontradas: {list(df.columns)}")
            print(f"📊 Linhas: {len(df)}")
            
            # Procura colunas X e Y
            col_x = None
            col_y = None
            
            # Padrões para coluna X
            x_patterns = ['E/Long', 'E/LONG', 'Easting', 'E', 'X', 'Longitude']
            for pattern in x_patterns:
                for col in df.columns:
                    if pattern.lower() in col.lower():
                        col_x = col
                        break
                if col_x:
                    break
            
            # Padrões para coluna Y
            y_patterns = ['N/Lat', 'N/LAT', 'Northing', 'N', 'Y', 'Latitude']
            for pattern in y_patterns:
                for col in df.columns:
                    if pattern.lower() in col.lower():
                        col_y = col
                        break
                if col_y:
                    break
            
            if not col_x or not col_y:
                print(f"❌ Colunas X/Y não encontradas em {arquivo_csv.name}")
                print(f"   Colunas disponíveis: {list(df.columns)}")
                continue
            
            print(f"🎯 Coluna X encontrada: '{col_x}'")
            print(f"🎯 Coluna Y encontrada: '{col_y}'")
            
            # Testa conversão das primeiras 3 linhas
            print(f"🔄 Testando conversão das primeiras 3 linhas...")
            
            for i in range(min(3, len(df))):
                try:
                    row = df.iloc[i]
                    
                    # Converte vírgula para ponto (formato brasileiro)
                    valor_x = str(row[col_x]).replace(',', '.')
                    valor_y = str(row[col_y]).replace(',', '.')
                    
                    utm_x = float(valor_x)
                    utm_y = float(valor_y)
                    
                    resultado = conversor.converter_utm_para_dms(utm_x, utm_y)
                    
                    print(f"   Linha {i+1}:")
                    print(f"     UTM: X={utm_x}, Y={utm_y}")
                    print(f"     Geográficas: {resultado['longitude_dms']}, {resultado['latitude_dms']}")
                    
                except Exception as e:
                    print(f"   ❌ Erro na linha {i+1}: {e}")
            
            print(f"✅ Arquivo {arquivo_csv.name} - TESTE OK!")
            
        except Exception as e:
            print(f"❌ Erro geral em {arquivo_csv.name}: {e}")
    
    print("\n" + "="*60)
    print("🎉 Teste concluído!")

if __name__ == "__main__":
    testar_conversao_csv()

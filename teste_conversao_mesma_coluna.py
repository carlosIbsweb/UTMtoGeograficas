"""
Teste da conversão na mesma coluna com formato brasileiro
"""

import pandas as pd
from pathlib import Path
from conversor_utm import ConversorUTM

def testar_conversao_mesma_coluna():
    """Testa a conversão substituindo na mesma coluna"""
    
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
        
        # Cria cópia do DataFrame
        df_convertido = df.copy()
        
        # Testa algumas linhas
        print("\n📋 Primeiras 3 linhas:")
        for i in range(min(3, len(df))):
            if i == 0:
                print(f"Linha {i+1} (cabeçalho): {df.iloc[i, idx_x]} | {df.iloc[i, idx_y]}")
            else:
                valor_x = str(df.iloc[i, idx_x]).replace(',', '.')
                valor_y = str(df.iloc[i, idx_y]).replace(',', '.')
                print(f"Linha {i+1} ORIGINAL: {valor_x} | {valor_y}")
                
                # Testa conversão
                try:
                    utm_x = float(valor_x)
                    utm_y = float(valor_y)
                    resultado = conversor.converter_utm_para_dms(utm_x, utm_y)
                    
                    # Formata no estilo brasileiro
                    lon_g, lon_m, lon_s = conversor.graus_decimais_para_dms(resultado['longitude_dec'])
                    lat_g, lat_m, lat_s = conversor.graus_decimais_para_dms(resultado['latitude_dec'])
                    
                    # Formata com vírgula e direção
                    lon_formatado = f"{abs(lon_g)} {lon_m:02d} {lon_s:.3f}".replace('.', ',')
                    lat_formatado = f"{abs(lat_g)} {lat_m:02d} {lat_s:.3f}".replace('.', ',')
                    
                    # Adiciona direção
                    lon_formatado += " W" if lon_g < 0 else " E"
                    lat_formatado += " S" if lat_g < 0 else " N"
                    
                    print(f"Linha {i+1} CONVERTIDO: {lon_formatado} | {lat_formatado}")
                    
                    # Substitui no DataFrame
                    df_convertido.iloc[i, idx_x] = lon_formatado
                    df_convertido.iloc[i, idx_y] = lat_formatado
                    
                except Exception as e:
                    print(f"Linha {i+1} ERRO: {e}")
        
        # Salva arquivo de teste
        arquivo_teste_saida = Path("teste_convertido_mesma_coluna.csv")
        df_convertido.to_csv(arquivo_teste_saida, index=False, encoding='utf-8-sig', sep=';')
        print(f"\n✅ Arquivo de teste salvo: {arquivo_teste_saida}")
        
        print("\n✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    testar_conversao_mesma_coluna()

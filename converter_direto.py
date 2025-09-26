"""
Conversor direto para os arquivos CSV da pasta csv/
Converte diretamente para a pasta convertido/
"""

import pandas as pd
from conversor_utm import ConversorUTM
from pathlib import Path

def converter_arquivos_csv():
    """Converte os arquivos CSV diretamente"""
    
    # Cria o conversor
    conversor = ConversorUTM(zona_utm=23, hemisferio='S', datum='SIRGAS2000')
    
    # Pasta origem e destino
    pasta_origem = Path("csv")
    pasta_destino = Path("convertido")
    
    # Cria pasta de destino se não existir
    pasta_destino.mkdir(exist_ok=True)
    
    # Lista arquivos CSV
    arquivos_csv = list(pasta_origem.glob("*.csv"))
    
    if not arquivos_csv:
        print("❌ Nenhum arquivo CSV encontrado na pasta 'csv'")
        return
    
    print(f"📁 Encontrados {len(arquivos_csv)} arquivos CSV:")
    for arquivo in arquivos_csv:
        print(f"  • {arquivo.name}")
    
    print("\n" + "="*60)
    
    sucessos = 0
    erros = 0
    
    # Processa cada arquivo
    for arquivo_csv in arquivos_csv:
        print(f"\n🔄 Processando: {arquivo_csv.name}")
        
        try:
            # Carrega o arquivo
            df = pd.read_csv(arquivo_csv, encoding='latin-1', sep=';')
            print(f"  ✅ Arquivo carregado: {len(df)} linhas")
            
            # Converte coordenadas
            longitudes_dms = []
            latitudes_dms = []
            longitudes_dec = []
            latitudes_dec = []
            
            for i, row in df.iterrows():
                try:
                    # Converte valores para float, tratando vírgula como separador decimal
                    valor_x = str(row['E/Long']).replace(',', '.').strip()
                    valor_y = str(row['N/Lat']).replace(',', '.').strip()
                    
                    # Verifica se é um número válido
                    if not valor_x or not valor_y:
                        raise ValueError("Valor vazio")
                    
                    # Converte para float
                    utm_x = float(valor_x)
                    utm_y = float(valor_y)
                    
                    # Converte as coordenadas
                    resultado = conversor.converter_utm_para_dms(utm_x, utm_y)
                    
                    longitudes_dms.append(resultado['longitude_dms'])
                    latitudes_dms.append(resultado['latitude_dms'])
                    longitudes_dec.append(resultado['longitude_dec'])
                    latitudes_dec.append(resultado['latitude_dec'])
                    
                except Exception as e:
                    print(f"    ⚠️ Linha {i+1} pulada: {e}")
                    longitudes_dms.append('')
                    latitudes_dms.append('')
                    longitudes_dec.append('')
                    latitudes_dec.append('')
            
            # Adiciona as novas colunas
            df['Longitude_DMS'] = longitudes_dms
            df['Latitude_DMS'] = latitudes_dms
            df['Longitude_Decimal'] = longitudes_dec
            df['Latitude_Decimal'] = latitudes_dec
            
            # Salva o arquivo convertido
            nome_sem_ext = arquivo_csv.stem
            arquivo_destino = pasta_destino / f"{nome_sem_ext}_convertido.csv"
            
            df.to_csv(arquivo_destino, index=False, encoding='utf-8-sig', sep=';')
            
            print(f"  ✅ Arquivo salvo: {arquivo_destino}")
            sucessos += 1
            
        except Exception as e:
            print(f"  ❌ Erro ao processar {arquivo_csv.name}: {e}")
            erros += 1
    
    # Resultado final
    print("\n" + "="*60)
    print(f"🎉 CONVERSÃO CONCLUÍDA!")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    
    if sucessos > 0:
        print(f"\n📁 Arquivos convertidos salvos em: {pasta_destino.absolute()}")
        print("\n📊 Novas colunas adicionadas:")
        print("  • Longitude_DMS (formato GG° MM' SS.SS\")")
        print("  • Latitude_DMS (formato GG° MM' SS.SS\")")
        print("  • Longitude_Decimal (graus decimais)")
        print("  • Latitude_Decimal (graus decimais)")

if __name__ == "__main__":
    converter_arquivos_csv()

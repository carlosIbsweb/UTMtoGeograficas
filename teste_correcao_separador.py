"""
Teste final da correção do separador
"""

import pandas as pd
from conversor_utm import ConversorUTM
from pathlib import Path

def teste_correcao_separador():
    conversor = ConversorUTM(zona_utm=23, hemisferio='S', datum='SIRGAS2000')
    
    # Simula a função carregar_arquivo_para_conversao
    arquivo = Path("csv/Prlc_FazendaTamandua_001 - Pnt.csv")
    
    try:
        # Tenta diferentes codificações e separadores
        codificacoes = ['latin-1', 'cp1252', 'utf-8', 'utf-8-sig', 'iso-8859-1']
        separadores = [';', ',', '\t']
        
        df = None
        for encoding in codificacoes:
            for sep in separadores:
                try:
                    df = pd.read_csv(arquivo, encoding=encoding, sep=sep)
                    # Verifica se carregou corretamente (mais de 1 coluna)
                    if len(df.columns) > 1:
                        print(f"✅ Arquivo carregado: {arquivo.name} (encoding: {encoding}, sep: '{sep}')")
                        break
                except:
                    continue
            if df is not None:
                break
        
        if df is None:
            print(f"❌ Não foi possível carregar {arquivo.name}")
            return
        
        print(f"📊 Colunas: {list(df.columns)}")
        print(f"📊 Linhas: {len(df)}")
        
        # Testa conversão
        col_x = 'E/Long'
        col_y = 'N/Lat'
        
        sucessos = 0
        erros = 0
        
        for i, row in df.iterrows():
            try:
                # Converte valores para float, tratando vírgula como separador decimal
                valor_x = str(row[col_x]).replace(',', '.')
                valor_y = str(row[col_y]).replace(',', '.')
                
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
                sucessos += 1
                
                if sucessos <= 3:  # Mostra apenas as primeiras 3 conversões
                    print(f"Linha {i+1}: UTM({utm_x}, {utm_y}) → {resultado['longitude_dms']}, {resultado['latitude_dms']}")
                
            except Exception as e:
                print(f"Linha {i+1} pulada: {e}")
                erros += 1
        
        print(f"\nResultado:")
        print(f"✅ Sucessos: {sucessos}")
        print(f"❌ Erros: {erros}")
        
        if sucessos > 0:
            print(f"\n✅ CORREÇÃO FUNCIONOU!")
        else:
            print(f"\n❌ Ainda há problemas")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    teste_correcao_separador()

"""
Módulo para conversão de coordenadas UTM para coordenadas geográficas (GG MM SS)
"""

import math
from pyproj import Proj, transform
import pandas as pd


class ConversorUTM:
    def __init__(self, zona_utm=23, hemisferio='S', datum='SIRGAS2000'):
        """
        Inicializa o conversor UTM
        
        Args:
            zona_utm (int): Zona UTM (padrão: 23 para Brasil)
            hemisferio (str): 'N' para Norte ou 'S' para Sul (padrão: 'S')
            datum (str): Sistema de referência (padrão: 'SIRGAS2000')
        """
        self.zona_utm = zona_utm
        self.hemisferio = hemisferio
        self.datum = datum
    
    def utm_para_geografica(self, utm_x, utm_y, zona_utm=None, hemisferio=None):
        """
        Converte coordenadas UTM para coordenadas geográficas
        
        Args:
            utm_x (float): Coordenada X UTM (Easting)
            utm_y (float): Coordenada Y UTM (Northing)
            zona_utm (int): Zona UTM (usa a padrão se não especificada)
            hemisferio (str): 'N' para Norte ou 'S' para Sul (usa a padrão se não especificado)
        
        Returns:
            tuple: (longitude, latitude) em graus decimais
        """
        try:
            # Usa valores padrão se não especificados
            zona = zona_utm if zona_utm is not None else self.zona_utm
            hem = hemisferio if hemisferio is not None else self.hemisferio
            
            # Define o sistema de coordenadas UTM com SIRGAS2000
            # SIRGAS2000 usa o elipsoide GRS80 que é compatível com WGS84
            utm_proj = Proj(proj='utm', zone=zona, ellps='GRS80', 
                           south=(hem == 'S'))
            
            # Converte para coordenadas geográficas
            lon, lat = utm_proj(utm_x, utm_y, inverse=True)
            
            return lon, lat
        except Exception as e:
            raise Exception(f"Erro na conversão UTM: {str(e)}")
    
    def graus_decimais_para_dms(self, graus_decimais):
        """
        Converte graus decimais para formato GG MM SS
        
        Args:
            graus_decimais (float): Coordenada em graus decimais
        
        Returns:
            tuple: (graus, minutos, segundos)
        """
        # Determina o sinal
        sinal = 1 if graus_decimais >= 0 else -1
        graus_decimais = abs(graus_decimais)
        
        # Extrai graus, minutos e segundos
        graus = int(graus_decimais)
        minutos_float = (graus_decimais - graus) * 60
        minutos = int(minutos_float)
        segundos = (minutos_float - minutos) * 60
        
        # Aplica o sinal aos graus
        graus = graus * sinal
        
        return graus, minutos, segundos
    
    def formatar_dms(self, graus, minutos, segundos, casas_decimais=2):
        """
        Formata coordenadas DMS para string
        
        Args:
            graus (int): Graus
            minutos (int): Minutos
            segundos (float): Segundos
            casas_decimais (int): Número de casas decimais para segundos
        
        Returns:
            str: String formatada como "GG° MM' SS.SS\""
        """
        return f"{graus}° {minutos:02d}' {segundos:.{casas_decimais}f}\""
    
    def converter_utm_para_dms(self, utm_x, utm_y, zona_utm=None, hemisferio=None):
        """
        Converte coordenadas UTM diretamente para formato DMS
        
        Args:
            utm_x (float): Coordenada X UTM
            utm_y (float): Coordenada Y UTM
            zona_utm (int): Zona UTM (usa a padrão se não especificada)
            hemisferio (str): 'N' ou 'S' (usa a padrão se não especificado)
        
        Returns:
            dict: {'longitude_dms': str, 'latitude_dms': str, 
                   'longitude_dec': float, 'latitude_dec': float}
        """
        try:
            # Converte UTM para geográficas
            lon_dec, lat_dec = self.utm_para_geografica(utm_x, utm_y, zona_utm, hemisferio)
            
            # Converte para DMS
            lon_g, lon_m, lon_s = self.graus_decimais_para_dms(lon_dec)
            lat_g, lat_m, lat_s = self.graus_decimais_para_dms(lat_dec)
            
            # Formata as strings
            lon_dms = self.formatar_dms(lon_g, lon_m, lon_s)
            lat_dms = self.formatar_dms(lat_g, lat_m, lat_s)
            
            return {
                'longitude_dms': lon_dms,
                'latitude_dms': lat_dms,
                'longitude_dec': lon_dec,
                'latitude_dec': lat_dec
            }
        except Exception as e:
            raise Exception(f"Erro na conversão completa: {str(e)}")


def detectar_colunas_utm(df):
    """
    Detecta automaticamente colunas UTM no DataFrame
    
    Args:
        df (pandas.DataFrame): DataFrame com os dados
    
    Returns:
        dict: {'x_col': str, 'y_col': str, 'zona_col': str} ou None se não encontrar
    """
    colunas = df.columns.str.lower()
    
    # Possíveis nomes para colunas X (Easting)
    x_patterns = ['x', 'easting', 'este', 'e', 'utm_x', 'coord_x']
    y_patterns = ['y', 'northing', 'norte', 'n', 'utm_y', 'coord_y']
    zona_patterns = ['zona', 'zone', 'utm_zone', 'fuso']
    
    x_col = None
    y_col = None
    zona_col = None
    
    # Procura coluna X
    for pattern in x_patterns:
        matches = [col for col in colunas if pattern in col]
        if matches:
            x_col = df.columns[colunas.tolist().index(matches[0])]
            break
    
    # Procura coluna Y
    for pattern in y_patterns:
        matches = [col for col in colunas if pattern in col]
        if matches:
            y_col = df.columns[colunas.tolist().index(matches[0])]
            break
    
    # Procura coluna Zona
    for pattern in zona_patterns:
        matches = [col for col in colunas if pattern in col]
        if matches:
            zona_col = df.columns[colunas.tolist().index(matches[0])]
            break
    
    if x_col and y_col:
        return {
            'x_col': x_col,
            'y_col': y_col,
            'zona_col': zona_col
        }
    
    return None


if __name__ == "__main__":
    # Teste do módulo
    conversor = ConversorUTM()
    
    # Exemplo de conversão
    utm_x = 500000
    utm_y = 7000000
    zona = 23
    
    resultado = conversor.converter_utm_para_dms(utm_x, utm_y, zona, 'S')
    print(f"UTM: X={utm_x}, Y={utm_y}, Zona={zona}")
    print(f"Geográficas: {resultado['longitude_dms']}, {resultado['latitude_dms']}")

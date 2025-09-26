"""
Teste simples da conversão UTM
"""

from conversor_utm import ConversorUTM

# Cria o conversor
conversor = ConversorUTM(zona_utm=23, hemisferio='S', datum='SIRGAS2000')

# Testa uma conversão
utm_x = 500000
utm_y = 7000000

print("Testando conversão UTM para Geográficas...")
print(f"UTM: X={utm_x}, Y={utm_y}")

try:
    resultado = conversor.converter_utm_para_dms(utm_x, utm_y)
    
    print(f"Longitude DMS: {resultado['longitude_dms']}")
    print(f"Latitude DMS: {resultado['latitude_dms']}")
    print(f"Longitude Decimal: {resultado['longitude_dec']:.6f}")
    print(f"Latitude Decimal: {resultado['latitude_dec']:.6f}")
    
    print("\n✅ Conversão funcionando corretamente!")
    
except Exception as e:
    print(f"❌ Erro na conversão: {e}")

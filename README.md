# Sistema de Conversão UTM para Coordenadas Geográficas

Sistema em Python para converter coordenadas UTM para coordenadas geográficas no formato GG MM SS (graus, minutos, segundos).

**Configurado especificamente para:**
- **Sistema:** SIRGAS 2000
- **Zona UTM:** 23S (Hemisfério Sul)
- **Meridiano Central:** -45°

## 📋 Funcionalidades

- ✅ Interface gráfica intuitiva
- ✅ Seleção de pasta com arquivos CSV
- ✅ Prévia dos dados antes da conversão
- ✅ Seleção manual das colunas UTM (X e Y)
- ✅ Detecção automática de colunas (quando possível)
- ✅ Conversão para formato DMS (GG° MM' SS.SS")
- ✅ Também gera coordenadas decimais
- ✅ Salva arquivos convertidos com sufixo "_convertido"
- ✅ Instalação automática de dependências

## 🚀 Como Usar

### 1. Instalação
```bash
# Execute o instalador automático
install.bat
```

### 2. Executar o Sistema
```bash
# Inicie o programa
python conversao_utm.py
```

### 3. Processo de Conversão

1. **Selecione a pasta** com seus arquivos CSV
2. **Escolha o arquivo CSV** que deseja converter
3. **Visualize a prévia** dos dados na tabela
4. **Selecione as colunas**:
   - Coluna X (Easting/Este)
   - Coluna Y (Northing/Norte)
5. **Escolha a pasta de destino** para salvar o arquivo convertido
6. **Clique em "Converter Arquivo"**

## 📁 Estrutura dos Arquivos

```
ConversaoUTM/
├── conversao_utm.py          # Arquivo principal (execute este)
├── interface_grafica.py      # Interface gráfica
├── conversor_utm.py          # Módulo de conversão
├── requirements.txt          # Dependências Python
├── install.bat              # Instalador automático
└── README.md               # Este arquivo
```

## 📊 Formato de Saída

O sistema adiciona as seguintes colunas ao arquivo original:

- **Longitude_DMS**: Longitude em formato GG° MM' SS.SS"
- **Latitude_DMS**: Latitude em formato GG° MM' SS.SS"
- **Longitude_Decimal**: Longitude em graus decimais
- **Latitude_Decimal**: Latitude em graus decimais

### Exemplo:
```
Longitude_DMS: -45° 30' 25.67"
Latitude_DMS: -23° 15' 42.89"
```

## 🔧 Dependências

- **Python 3.7+**
- **pandas**: Manipulação de dados CSV
- **pyproj**: Conversões de coordenadas
- **tkinter**: Interface gráfica (já vem com Python)

## ⚙️ Configurações Técnicas

- **Datum**: SIRGAS2000
- **Elipsoide**: GRS80
- **Zona UTM**: 23S
- **Hemisfério**: Sul
- **Meridiano Central**: -45°

## 🐛 Solução de Problemas

### Erro de Dependências
```
Execute: install.bat
```

### Erro ao Abrir CSV
- Verifique se o arquivo está em formato CSV válido
- Certifique-se de que não há caracteres especiais no nome do arquivo

### Coordenadas Incorretas
- Verifique se as colunas X e Y estão corretas
- Confirme se os dados estão em UTM Zone 23S
- Verifique se os valores não têm caracteres não numéricos

### Interface não Abre
- Verifique se o Python está instalado
- Execute `python --version` para confirmar
- Reinstale as dependências com `install.bat`

## 📝 Notas Importantes

1. **Zona UTM Fixa**: O sistema está configurado para Zone 23S. Para outras zonas, seria necessário modificar o código.

2. **Formato dos Dados**: Os dados UTM devem estar em metros (padrão UTM).

3. **Encoding**: Os arquivos são salvos com encoding UTF-8 com BOM para compatibilidade com Excel.

4. **Backup**: O sistema não modifica o arquivo original, sempre cria um novo com sufixo "_convertido".

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se todas as dependências estão instaladas
2. Confirme se o arquivo CSV está no formato correto
3. Verifique se as colunas selecionadas contêm dados numéricos válidos
4. Certifique-se de que tem permissões para escrever na pasta de destino

---

**Desenvolvido para conversão de coordenadas UTM SIRGAS 2000 Zone 23S para coordenadas geográficas.**

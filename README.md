# Conversor UTM para Coordenadas Geográficas

Sistema para converter coordenadas UTM para coordenadas geográficas no formato brasileiro (GG MM SS,SSS).

## 🎯 Características

- **Sistema**: SIRGAS 2000 UTM Zone 23S
- **Formato de saída**: `48 05 57,108 W` (graus, minutos, segundos com vírgula)
- **Processamento em lote**: Converte todos os arquivos CSV de uma pasta
- **Interface gráfica**: Fácil de usar
- **Configuração por letras**: Usa letras de colunas (A, B, C, D...)

## 📋 Requisitos

- Python 3.7 ou superior
- Windows (testado no Windows 10/11)

## 🚀 Instalação

1. **Baixe o projeto** ou clone o repositório
2. **Execute o instalador automático**:
   ```bash
   install.bat
   ```
   
   O instalador irá:
   - Verificar se Python está instalado
   - Instalar automaticamente as dependências (pandas, pyproj)
   - Mostrar mensagens de erro se necessário

## 💻 Como Usar

1. **Execute o programa**:
   ```bash
   py executar_conversor.py
   ```

2. **Configure a conversão**:
   - **Pasta Origem**: Selecione a pasta com os arquivos CSV
   - **Coluna X**: Digite a letra da coluna com coordenadas X (ex: B)
   - **Coluna Y**: Digite a letra da coluna com coordenadas Y (ex: D)
   - **Pasta Destino**: Selecione onde salvar os arquivos convertidos

3. **Execute a conversão**:
   - Clique em "Converter TODOS os Arquivos"
   - Aguarde o processamento
   - Os arquivos serão salvos com o mesmo nome

## 📊 Formato dos Arquivos

### Entrada (UTM)
```csv
Vertice;E/Long;Sigma long;N/Lat;Sigma lat;h;Sigma h;...
BSLL-M-B0945;168104,21;0,005;8239998,82;0,005;1168,08;0,018;...
```

### Saída (Geográfico)
```csv
Vertice;E/Long;Sigma long;N/Lat;Sigma lat;h;Sigma h;...
BSLL-M-B0945;48 05 57,108 W;0,005;15 53 49,155 S;0,005;1168,08;0,018;...
```

## ⚙️ Configurações

- **Sistema de coordenadas**: SIRGAS 2000 UTM Zone 23S
- **Hemisfério**: Sul
- **Meridiano central**: -45°
- **Separador CSV**: Ponto e vírgula (;)
- **Separador decimal**: Vírgula (,)

## 📁 Estrutura do Projeto

```
ConversaoUTM/
├── executar_conversor.py # Arquivo principal
├── interface_grafica.py  # Interface gráfica
├── conversor_utm.py      # Lógica de conversão
├── install.bat          # Instalador automático
├── requirements.txt     # Dependências Python
├── config.json         # Configurações salvas (ignorado pelo Git)
└── README.md           # Este arquivo
```

## 🔧 Funcionalidades

- ✅ Conversão em lote de múltiplos arquivos CSV
- ✅ Interface gráfica intuitiva
- ✅ Configuração por letras de colunas
- ✅ Salva configurações automaticamente
- ✅ Detecta automaticamente codificação e separador
- ✅ Tratamento de erros robusto
- ✅ Formato brasileiro de coordenadas

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"
- Instale Python em: https://www.python.org/downloads/
- Certifique-se de marcar "Add Python to PATH" durante a instalação

### Erro: "Falha ao instalar dependências"
- Execute como administrador
- Verifique sua conexão com a internet
- Tente executar: `py -m pip install --upgrade pip`

### Arquivo não carrega
- Verifique se o arquivo está em formato CSV
- Teste com diferentes codificações (UTF-8, Latin-1)
- Verifique se o separador está correto (; ou ,)

## 📝 Exemplos de Uso

### Configuração típica:
- **Coluna X**: B (E/Long)
- **Coluna Y**: D (N/Lat)
- **Pasta origem**: C:\Dados\UTM\
- **Pasta destino**: C:\Dados\Convertido\

### Resultado:
- Arquivo original: `dados.csv`
- Arquivo convertido: `dados.csv` (mesmo nome)

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no repositório
- Verifique a seção de solução de problemas
- Consulte a documentação do pyproj e pandas

---

**Desenvolvido para conversão de coordenadas UTM para o sistema geográfico brasileiro.**
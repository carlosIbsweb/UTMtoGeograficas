"""
Interface Gráfica para Conversão UTM para Coordenadas Geográficas
Sistema específico para SIRGAS 2000 UTM Zone 23S
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import json
from pathlib import Path
from conversor_utm import ConversorUTM


class InterfaceConversaoUTM:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Conversão UTM para Geográficas - SIRGAS 2000 Zone 23S")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variáveis
        self.pasta_origem = tk.StringVar()
        self.pasta_destino = tk.StringVar()
        self.coluna_x = tk.StringVar()
        self.coluna_y = tk.StringVar()
        self.conversor = ConversorUTM(zona_utm=23, hemisferio='S', datum='SIRGAS2000')
        
        # Carrega configurações salvas
        self.carregar_configuracoes()
        
        # Define valores padrão se não houver configurações
        if not self.coluna_x.get():
            self.coluna_x.set('B')
        if not self.coluna_y.get():
            self.coluna_y.set('D')
        
        self.criar_interface()
    
    def criar_interface(self):
        """Cria a interface gráfica"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuração do grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Conversão UTM → Geográficas (GG MM SS)", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Info do sistema
        info_label = ttk.Label(main_frame, text="Sistema: SIRGAS 2000 UTM Zone 23S", 
                              font=('Arial', 10), foreground='blue')
        info_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Seção 1: Seleção de pasta origem
        ttk.Label(main_frame, text="1. Pasta com TODOS os arquivos CSV:", 
                 font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        ttk.Entry(main_frame, textvariable=self.pasta_origem, width=50).grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(main_frame, text="Selecionar Pasta", 
                  command=self.selecionar_pasta_origem).grid(row=3, column=2, padx=(5, 0))
        
        # Seção 2: Configuração das colunas (sem seleção de arquivo)
        ttk.Label(main_frame, text="2. Configuração das Colunas UTM:", 
                 font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        
        # Frame para configuração manual das colunas
        config_frame = ttk.LabelFrame(main_frame, text="Colunas UTM", padding="10")
        config_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        config_frame.columnconfigure(1, weight=1)
        config_frame.columnconfigure(3, weight=1)
        
        ttk.Label(config_frame, text="Coluna X (Easting):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.entry_col_x = ttk.Entry(config_frame, textvariable=self.coluna_x, width=5)
        self.entry_col_x.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Label(config_frame, text="Coluna Y (Northing):").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.entry_col_y = ttk.Entry(config_frame, textvariable=self.coluna_y, width=5)
        self.entry_col_y.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5)
        
        # Dica para o usuário
        ttk.Label(config_frame, text="Digite as LETRAS das colunas (A, B, C, D, E...) como aparecem no Excel", 
                 font=('Arial', 8), foreground='gray').grid(row=1, column=0, columnspan=4, pady=(5, 0))
        
        # Exemplos comuns
        ttk.Label(config_frame, text="Exemplos: B, D | A, C | E, F | X, Y (pula linha 0 automaticamente)", 
                 font=('Arial', 8), foreground='blue').grid(row=2, column=0, columnspan=4, pady=(2, 0))
        
        # Seção 3: Pasta destino
        ttk.Label(main_frame, text="3. Pasta de Destino:", 
                 font=('Arial', 10, 'bold')).grid(row=6, column=0, sticky=tk.W, pady=(20, 5))
        
        ttk.Entry(main_frame, textvariable=self.pasta_destino, width=50).grid(
            row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(main_frame, text="Selecionar Pasta", 
                  command=self.selecionar_pasta_destino).grid(row=7, column=2, padx=(5, 0))
        
        # Seção 4: Botões de ação
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=8, column=0, columnspan=3, pady=(30, 0))
        
        ttk.Button(buttons_frame, text="Converter TODOS os Arquivos", 
                  command=self.converter_todos_arquivos, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Salvar Configurações", 
                  command=self.salvar_configuracoes).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Limpar", 
                  command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Sair", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Configurar peso das linhas
        main_frame.rowconfigure(9, weight=1)
    
    def carregar_configuracoes(self):
        """Carrega configurações salvas"""
        try:
            config_file = Path("config.json")
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # Define pasta inicial se existir
                if 'pasta_origem' in config and Path(config['pasta_origem']).exists():
                    self.pasta_origem.set(config['pasta_origem'])
                
                if 'pasta_destino' in config and Path(config['pasta_destino']).exists():
                    self.pasta_destino.set(config['pasta_destino'])
                
                if 'coluna_x' in config:
                    self.coluna_x.set(config['coluna_x'])
                
                if 'coluna_y' in config:
                    self.coluna_y.set(config['coluna_y'])
                    
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
    
    def salvar_configuracoes(self):
        """Salva configurações atuais"""
        try:
            config = {
                'pasta_origem': self.pasta_origem.get(),
                'pasta_destino': self.pasta_destino.get(),
                'coluna_x': self.coluna_x.get(),
                'coluna_y': self.coluna_y.get()
            }
            
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def selecionar_pasta_origem(self):
        """Seleciona a pasta com os arquivos CSV"""
        pasta = filedialog.askdirectory(title="Selecionar pasta com arquivos CSV")
        if pasta:
            self.pasta_origem.set(pasta)
            # Verifica se há arquivos CSV na pasta
            try:
                pasta_path = Path(pasta)
                arquivos_csv = list(pasta_path.glob("*.csv"))
                print(f"Encontrados {len(arquivos_csv)} arquivos CSV na pasta selecionada")
            except Exception as e:
                print(f"Erro ao verificar pasta: {e}")
            # Salva configuração
            self.salvar_configuracoes()
    
    def selecionar_pasta_destino(self):
        """Seleciona a pasta de destino"""
        pasta = filedialog.askdirectory(title="Selecionar pasta de destino")
        if pasta:
            self.pasta_destino.set(pasta)
            # Salva configuração
            self.salvar_configuracoes()
    
    
    def converter_todos_arquivos(self):
        """Converte todos os arquivos CSV da pasta"""
        # Validações básicas
        if not self.pasta_origem.get():
            messagebox.showerror("Erro", "Selecione a pasta de origem.")
            return
        
        if not self.pasta_destino.get():
            messagebox.showerror("Erro", "Selecione a pasta de destino.")
            return
        
        if not self.coluna_x.get() or not self.coluna_y.get():
            messagebox.showerror("Erro", "Digite as letras das colunas X e Y primeiro.")
            return
        
        try:
            # Lista todos os arquivos CSV da pasta
            pasta = Path(self.pasta_origem.get())
            arquivos_csv = list(pasta.glob("*.csv"))
            
            if not arquivos_csv:
                messagebox.showwarning("Aviso", "Nenhum arquivo CSV encontrado na pasta.")
                return
            
            # Confirma com o usuário
            resposta = messagebox.askyesno(
                "Confirmar Conversão", 
                f"Converter {len(arquivos_csv)} arquivos CSV?\n\n"
                f"Coluna X: {self.coluna_x.get()} (Easting)\n"
                f"Coluna Y: {self.coluna_y.get()} (Northing)\n"
                f"Pula linha 0 (cabeçalho) automaticamente\n\n"
                f"Arquivos serão salvos em: {self.pasta_destino.get()}"
            )
            
            if not resposta:
                return
            
            # Processa cada arquivo
            sucessos = 0
            erros = 0
            arquivos_processados = []
            
            for arquivo_csv in arquivos_csv:
                try:
                    print(f"Processando: {arquivo_csv.name}")
                    
                    # Carrega o arquivo
                    df = self.carregar_arquivo_para_conversao(arquivo_csv)
                    if df is None:
                        erros += 1
                        continue
                    
                    # Converte as coordenadas
                    df_convertido = self.converter_coordenadas_df(df, self.coluna_x.get(), self.coluna_y.get())
                    
                    # Salva o arquivo convertido
                    nome_sem_ext = arquivo_csv.stem
                    arquivo_destino = Path(self.pasta_destino.get()) / f"{nome_sem_ext}_convertido.csv"
                    
                    df_convertido.to_csv(arquivo_destino, index=False, encoding='utf-8-sig', sep=';')
                    
                    sucessos += 1
                    arquivos_processados.append(arquivo_csv.name)
                    print(f"✅ Convertido: {arquivo_csv.name}")
                    
                except Exception as e:
                    erros += 1
                    print(f"❌ Erro em {arquivo_csv.name}: {str(e)}")
            
            # Mostra resultado final
            mensagem = f"Conversão concluída!\n\n"
            mensagem += f"✅ Sucessos: {sucessos}\n"
            mensagem += f"❌ Erros: {erros}\n\n"
            
            if sucessos > 0:
                mensagem += f"Arquivos convertidos:\n"
                for arquivo in arquivos_processados:
                    mensagem += f"• {arquivo}\n"
            
            if erros > 0:
                mensagem += f"\nVerifique os erros no console."
            
            messagebox.showinfo("Resultado", mensagem)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante a conversão em lote: {str(e)}")
    
    def carregar_arquivo_para_conversao(self, arquivo_path):
        """Carrega um arquivo CSV para conversão"""
        try:
            # Tenta diferentes codificações e separadores
            codificacoes = ['latin-1', 'cp1252', 'utf-8', 'utf-8-sig', 'iso-8859-1']
            separadores = [';', ',', '\t']
            
            for encoding in codificacoes:
                for sep in separadores:
                    try:
                        df = pd.read_csv(arquivo_path, encoding=encoding, sep=sep)
                        # Verifica se carregou corretamente (mais de 1 coluna)
                        if len(df.columns) > 1:
                            print(f"✅ Arquivo carregado: {arquivo_path.name} (encoding: {encoding}, sep: '{sep}')")
                            return df
                    except:
                        continue
            
            print(f"❌ Não foi possível carregar {arquivo_path.name}")
            return None
            
        except Exception as e:
            print(f"❌ Erro ao carregar {arquivo_path.name}: {str(e)}")
            return None
    
    def converter_coordenadas_df(self, df, col_x, col_y):
        """Converte coordenadas de um DataFrame usando letras de colunas - substitui na mesma coluna"""
        try:
            # Converte letras para índices (A=0, B=1, C=2, etc.)
            try:
                idx_x = ord(col_x.upper()) - ord('A')
                idx_y = ord(col_y.upper()) - ord('A')
            except:
                raise Exception(f"Letras de colunas inválidas: {col_x}, {col_y}")
            
            # Cria cópia do DataFrame
            df_convertido = df.copy()
            
            for i, row in df.iterrows():
                try:
                    # Pula a linha 0 (cabeçalho)
                    if i == 0:
                        continue
                    
                    # Usa índices das colunas
                    valor_x = str(row.iloc[idx_x]).replace(',', '.')
                    valor_y = str(row.iloc[idx_y]).replace(',', '.')
                    
                    # Remove espaços e caracteres não numéricos
                    valor_x = valor_x.strip()
                    valor_y = valor_y.strip()
                    
                    # Verifica se é um número válido
                    if not valor_x or not valor_y:
                        raise ValueError("Valor vazio")
                    
                    # Tenta converter para float - se falhar, pula a linha
                    try:
                        utm_x = float(valor_x)
                        utm_y = float(valor_y)
                    except ValueError:
                        raise ValueError(f"Valor não numérico: X='{valor_x}', Y='{valor_y}'")
                    
                    # Converte as coordenadas
                    resultado = self.conversor.converter_utm_para_dms(utm_x, utm_y)
                    
                    # Formata no estilo brasileiro: "48 04 35,347 W"
                    lon_g, lon_m, lon_s = self.conversor.graus_decimais_para_dms(resultado['longitude_dec'])
                    lat_g, lat_m, lat_s = self.conversor.graus_decimais_para_dms(resultado['latitude_dec'])
                    
                    # Formata com vírgula e direção
                    lon_formatado = f"{abs(lon_g)} {lon_m:02d} {lon_s:.3f}".replace('.', ',')
                    lat_formatado = f"{abs(lat_g)} {lat_m:02d} {lat_s:.3f}".replace('.', ',')
                    
                    # Adiciona direção
                    lon_formatado += " W" if lon_g < 0 else " E"
                    lat_formatado += " S" if lat_g < 0 else " N"
                    
                    # Substitui os valores nas colunas originais
                    df_convertido.iloc[i, idx_x] = lon_formatado
                    df_convertido.iloc[i, idx_y] = lat_formatado
                    
                except (ValueError, TypeError) as e:
                    # Se houver erro na conversão, mantém o valor original
                    print(f"Linha {i+1} mantida original: {e}")
                    continue
            
            return df_convertido
            
        except Exception as e:
            raise Exception(f"Erro na conversão de coordenadas: {str(e)}")
    
    
    def limpar_campos(self):
        """Limpa todos os campos"""
        self.pasta_origem.set('')
        self.pasta_destino.set('')
        self.coluna_x.set('')
        self.coluna_y.set('')
        print("Campos limpos. Use 'Salvar Configurações' para salvar as configurações atuais.")
    
    def executar(self):
        """Inicia a aplicação"""
        self.root.mainloop()


if __name__ == "__main__":
    app = InterfaceConversaoUTM()
    app.executar()

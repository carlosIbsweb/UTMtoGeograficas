"""
Sistema Principal para Conversão UTM para Coordenadas Geográficas
Integra a interface gráfica com o módulo de conversão

Configurado para SIRGAS 2000 UTM Zone 23S (Brasil)
"""

from interface_grafica import InterfaceConversaoUTM
import sys
import tkinter as tk
from tkinter import messagebox


def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias_faltando = []
    
    try:
        import pandas
    except ImportError:
        dependencias_faltando.append("pandas")
    
    try:
        import pyproj
    except ImportError:
        dependencias_faltando.append("pyproj")
    
    if dependencias_faltando:
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal
        
        mensagem = (
            "Dependências não encontradas:\n\n" +
            "\n".join(f"• {dep}" for dep in dependencias_faltando) +
            "\n\nPor favor, execute o arquivo 'install.bat' primeiro para instalar as dependências necessárias."
        )
        
        messagebox.showerror("Dependências Faltando", mensagem)
        root.destroy()
        return False
    
    return True


def main():
    """Função principal do sistema"""
    print("=" * 60)
    print("Sistema de Conversão UTM para Coordenadas Geográficas")
    print("SIRGAS 2000 UTM Zone 23S")
    print("=" * 60)
    
    # Verifica dependências
    if not verificar_dependencias():
        print("\nERRO: Dependências não encontradas!")
        print("Execute 'install.bat' primeiro para instalar as dependências.")
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    try:
        # Inicia a interface gráfica
        print("\nIniciando interface gráfica...")
        app = InterfaceConversaoUTM()
        app.executar()
        
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        
        # Mostra erro em janela se possível
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erro", f"Erro ao iniciar o sistema:\n\n{str(e)}")
            root.destroy()
        except:
            pass
        
        input("\nPressione Enter para sair...")
        sys.exit(1)


if __name__ == "__main__":
    main()

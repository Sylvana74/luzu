# main.py
"""
SandTech - Sistema de Gestión de Clientes
Aplicación desarrollada con arquitectura MVC
Utilizando Python, Tkinter y SQLite

Autor: Sistema de Gestión SandTech
Fecha: 2024
"""

import tkinter as tk
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from view.cliente_view import ClienteView
    from controller.cliente_controller import ClienteController
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrese de que los archivos estén en las carpetas correctas:")
    print("- view/cliente_view.py")
    print("- controller/cliente_controller.py") 
    print("- model/cliente_model.py")
    sys.exit(1)

class SandTechApp:
    """Clase principal de la aplicación SandTech"""
    
    def __init__(self):
        """Inicializa la aplicación"""
        self.root = None
        self.view = None
        self.controller = None
        
    def inicializar_aplicacion(self):
        """Inicializa todos los componentes de la aplicación"""
        try:
            # Crear ventana principal
            self.root = tk.Tk()
            
            # Configurar la ventana principal
            self.configurar_ventana_principal()
            
            # Crear vista
            self.view = ClienteView(self.root)
            
            # Crear controlador (se conecta automáticamente con la vista)
            self.controller = ClienteController(self.view)
            
            print("="*60)
            print("    SANDTECH - SISTEMA DE GESTIÓN DE CLIENTES")
            print("="*60)
            print("Aplicación inicializada correctamente")
            print("Arquitectura: Modelo-Vista-Controlador (MVC)")
            print("Base de datos: SQLite")
            print("Interfaz gráfica: Tkinter")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"Error al inicializar la aplicación: {e}")
            return False
    
    def configurar_ventana_principal(self):
        """Configura las propiedades de la ventana principal"""
        # Centrar la ventana en la pantalla
        self.centrar_ventana()
        
        # Configurar el cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        # Configurar icono si existe
        try:
            # Intentar cargar icono (opcional)
            pass
        except:
            pass
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Obtener dimensiones de la ventana
        window_width = 1000
        window_height = 700
        
        # Calcular posición para centrar
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Establecer geometría
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def cerrar_aplicacion(self):
        """Maneja el cierre de la aplicación"""
        try:
            print("\n" + "="*60)
            print("Cerrando aplicación SandTech...")
            
            # Aquí podrías agregar lógica adicional de limpieza si fuera necesaria
            # Por ejemplo, cerrar conexiones de base de datos, guardar configuraciones, etc.
            
            print("Aplicación cerrada correctamente")
            print("="*60)
            
        except Exception as e:
            print(f"Error al cerrar la aplicación: {e}")
        finally:
            self.root.quit()
            self.root.destroy()
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        if self.inicializar_aplicacion():
            # Iniciar el loop principal de Tkinter
            self.root.mainloop()
        else:
            print("No se pudo inicializar la aplicación")
            sys.exit(1)

def verificar_estructura_proyecto():
    """Verifica que existe la estructura de carpetas necesaria"""
    carpetas_necesarias = ['model', 'view', 'controller']
    archivos_necesarios = [
        'model/cliente_model.py',
        'view/cliente_view.py', 
        'controller/cliente_controller.py'
    ]
    
    print("Verificando estructura del proyecto...")
    
    # Verificar carpetas
    for carpeta in carpetas_necesarias:
        if not os.path.exists(carpeta):
            print(f"Creando carpeta: {carpeta}")
            os.makedirs(carpeta, exist_ok=True)
            
            # Crear __init__.py para que Python reconozca como paquete
            init_file = os.path.join(carpeta, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write(f'# Paquete {carpeta}\n')
    
    # Verificar archivos
    faltantes = []
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
    
    if faltantes:
        print("ADVERTENCIA: Faltan los siguientes archivos:")
        for archivo in faltantes:
            print(f"  - {archivo}")
        print("\nAsegúrese de copiar todos los archivos en sus carpetas correspondientes.")
        return False
    
    print("Estructura del proyecto verificada correctamente ✓")
    return True

def mostrar_ayuda():
    """Muestra información de ayuda sobre la aplicación"""
    print("\n" + "="*60)
    print("    SANDTECH - SISTEMA DE GESTIÓN DE CLIENTES")
    print("="*60)
    print("\nEstructura del proyecto (Arquitectura MVC):")
    print("├── main.py                     # Archivo principal")
    print("├── model/")
    print("│   ├── __init__.py")
    print("│   └── cliente_model.py        # Lógica de datos")
    print("├── view/")
    print("│   ├── __init__.py")
    print("│   └── cliente_view.py         # Interfaz gráfica")
    print("├── controller/")
    print("│   ├── __init__.py")
    print("│   └── cliente_controller.py   # Lógica de control")
    print("└── sandtech_clientes.db        # Base de datos SQLite")
    print("\nFuncionalidades disponibles:")
    print("• Crear nuevos clientes (código automático desde 100)")
    print("• Buscar clientes por código")
    print("• Modificar datos de clientes existentes")
    print("• Eliminar clientes")
    print("• Listar todos los clientes")
    print("• Log de transacciones en consola")
    print("\nPara ejecutar: python main.py")
    print("="*60)

if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        mostrar_ayuda()
        sys.exit(0)
    
    # Verificar estructura del proyecto
    if not verificar_estructura_proyecto():
        print("\nPor favor, corrija la estructura del proyecto antes de ejecutar.")
        sys.exit(1)
    
    try:
        # Crear y ejecutar aplicación
        app = SandTechApp()
        app.ejecutar()
        
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario")
        sys.exit(0)
        
    except Exception as e:
        print(f"\nError crítico en la aplicación: {e}")
        print("Revise los archivos del proyecto y la configuración")
        sys.exit(1)
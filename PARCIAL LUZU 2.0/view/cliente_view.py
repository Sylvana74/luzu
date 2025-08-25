# view/cliente_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font

class ClienteView:
    def __init__(self, root):
        self.root = root
        self.root.title("SandTech - Gestión de Clientes")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.setup_styles()
        
        # Variables de los campos
        self.setup_variables()
        
        # Crear interfaz
        self.create_main_interface()
        
        # Referencias para callbacks del controlador
        self.controller = None
        
    def setup_styles(self):
        """Configura los estilos de la aplicación"""
        # Configurar el estilo general
        style = ttk.Style()
        style.theme_use('clam')
        
        # Fuentes
        self.title_font = font.Font(family="Arial", size=16, weight="bold")
        self.label_font = font.Font(family="Arial", size=10)
        self.button_font = font.Font(family="Arial", size=9, weight="bold")
        
    def setup_variables(self):
        """Configura las variables de Tkinter"""
        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_direccion = tk.StringVar()
        
    def create_main_interface(self):
        """Crea la interfaz principal"""
        # Título principal
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="SANDTECH - GESTIÓN DE CLIENTES", 
                              font=self.title_font, bg="#2c3e50", fg="white")
        title_label.pack(expand=True)
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Columna izquierda - Formulario y botones
        left_frame = tk.Frame(main_frame, bg="#ecf0f1", width=400)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)
        
        self.create_form_section(left_frame)
        self.create_buttons_section(left_frame)
        
        # Columna derecha - Lista de clientes
        right_frame = tk.Frame(main_frame, bg="#ecf0f1")
        right_frame.pack(side="right", fill="both", expand=True)
        
        self.create_list_section(right_frame)
        
    def create_form_section(self, parent):
        """Crea la sección del formulario"""
        # Frame del formulario
        form_frame = tk.LabelFrame(parent, text="Datos del Cliente", 
                                  font=self.label_font, bg="#ecf0f1", padx=10, pady=10)
        form_frame.pack(fill="x", pady=(0, 10))
        
        # Código (solo lectura)
        tk.Label(form_frame, text="Código:", font=self.label_font, bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_codigo = tk.Entry(form_frame, textvariable=self.var_codigo, state="readonly", width=30)
        self.entry_codigo.grid(row=0, column=1, sticky="ew", pady=2)
        
        # Nombre
        tk.Label(form_frame, text="Nombre:", font=self.label_font, bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_nombre = tk.Entry(form_frame, textvariable=self.var_nombre, width=30)
        self.entry_nombre.grid(row=1, column=1, sticky="ew", pady=2)
        
        # Apellido
        tk.Label(form_frame, text="Apellido:", font=self.label_font, bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_apellido = tk.Entry(form_frame, textvariable=self.var_apellido, width=30)
        self.entry_apellido.grid(row=2, column=1, sticky="ew", pady=2)
        
        # Email
        tk.Label(form_frame, text="Email:", font=self.label_font, bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=2)
        self.entry_email = tk.Entry(form_frame, textvariable=self.var_email, width=30)
        self.entry_email.grid(row=3, column=1, sticky="ew", pady=2)
        
        # Teléfono
        tk.Label(form_frame, text="Teléfono:", font=self.label_font, bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=2)
        self.entry_telefono = tk.Entry(form_frame, textvariable=self.var_telefono, width=30)
        self.entry_telefono.grid(row=4, column=1, sticky="ew", pady=2)
        
        # Dirección
        tk.Label(form_frame, text="Dirección:", font=self.label_font, bg="#ecf0f1").grid(row=5, column=0, sticky="w", pady=2)
        self.entry_direccion = tk.Entry(form_frame, textvariable=self.var_direccion, width=30)
        self.entry_direccion.grid(row=5, column=1, sticky="ew", pady=2)
        
        # Configurar grid
        form_frame.grid_columnconfigure(1, weight=1)
        
    def create_buttons_section(self, parent):
        """Crea la sección de botones"""
        # Frame de botones CRUD
        crud_frame = tk.LabelFrame(parent, text="Operaciones CRUD", 
                                  font=self.label_font, bg="#ecf0f1", padx=10, pady=10)
        crud_frame.pack(fill="x", pady=(0, 10))
        
        # Botones en dos filas
        self.btn_nuevo = tk.Button(crud_frame, text="Nuevo Cliente", font=self.button_font, 
                                  bg="#27ae60", fg="white", width=15, height=2)
        self.btn_nuevo.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_guardar = tk.Button(crud_frame, text="Guardar", font=self.button_font, 
                                    bg="#3498db", fg="white", width=15, height=2)
        self.btn_guardar.grid(row=0, column=1, padx=5, pady=5)
        
        self.btn_actualizar = tk.Button(crud_frame, text="Actualizar", font=self.button_font, 
                                       bg="#f39c12", fg="white", width=15, height=2)
        self.btn_actualizar.grid(row=1, column=0, padx=5, pady=5)
        
        self.btn_eliminar = tk.Button(crud_frame, text="Eliminar", font=self.button_font, 
                                     bg="#e74c3c", fg="white", width=15, height=2)
        self.btn_eliminar.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame de búsqueda
        search_frame = tk.LabelFrame(parent, text="Búsqueda", 
                                    font=self.label_font, bg="#ecf0f1", padx=10, pady=10)
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(search_frame, text="Código a buscar:", font=self.label_font, bg="#ecf0f1").pack(anchor="w")
        
        search_entry_frame = tk.Frame(search_frame, bg="#ecf0f1")
        search_entry_frame.pack(fill="x", pady=5)
        
        self.var_buscar_codigo = tk.StringVar()
        self.entry_buscar = tk.Entry(search_entry_frame, textvariable=self.var_buscar_codigo, width=20)
        self.entry_buscar.pack(side="left", fill="x", expand=True)
        
        self.btn_buscar = tk.Button(search_entry_frame, text="Buscar", font=self.button_font, 
                                   bg="#9b59b6", fg="white", width=10)
        self.btn_buscar.pack(side="right", padx=(5, 0))
        
        # Botones adicionales
        extra_frame = tk.LabelFrame(parent, text="Otras Operaciones", 
                                   font=self.label_font, bg="#ecf0f1", padx=10, pady=10)
        extra_frame.pack(fill="x")
        
        self.btn_limpiar = tk.Button(extra_frame, text="Limpiar Formulario", font=self.button_font, 
                                    bg="#95a5a6", fg="white", width=20, height=2)
        self.btn_limpiar.pack(pady=5)
        
        self.btn_actualizar_lista = tk.Button(extra_frame, text="Actualizar Lista", font=self.button_font, 
                                             bg="#34495e", fg="white", width=20, height=2)
        self.btn_actualizar_lista.pack(pady=5)
        
    def create_list_section(self, parent):
        """Crea la sección de lista de clientes"""
        list_frame = tk.LabelFrame(parent, text="Lista de Clientes", 
                                  font=self.label_font, bg="#ecf0f1", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True)
        
        # Crear Treeview con scrollbars
        tree_frame = tk.Frame(list_frame, bg="#ecf0f1")
        tree_frame.pack(fill="both", expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Treeview
        columns = ("Código", "Nombre", "Apellido", "Email", "Teléfono", "Dirección", "Fecha Registro")
        self.tree_clientes = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                                         yscrollcommand=v_scrollbar.set, 
                                         xscrollcommand=h_scrollbar.set)
        
        # Configurar scrollbars
        v_scrollbar.config(command=self.tree_clientes.yview)
        h_scrollbar.config(command=self.tree_clientes.xview)
        
        # Configurar columnas
        column_widths = [80, 120, 120, 150, 100, 150, 130]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            self.tree_clientes.heading(col, text=col, anchor="center")
            self.tree_clientes.column(col, width=width, anchor="center")
        
        self.tree_clientes.pack(fill="both", expand=True)
        
        # Bind para seleccionar cliente
        self.tree_clientes.bind("<<TreeviewSelect>>", self.on_cliente_select)
        
    def set_controller(self, controller):
        """Establece la referencia al controlador y configura los callbacks"""
        self.controller = controller
        
        # Configurar callbacks de botones
        self.btn_nuevo.config(command=self.controller.nuevo_cliente)
        self.btn_guardar.config(command=self.controller.guardar_cliente)
        self.btn_actualizar.config(command=self.controller.actualizar_cliente)
        self.btn_eliminar.config(command=self.controller.eliminar_cliente)
        self.btn_buscar.config(command=self.controller.buscar_cliente)
        self.btn_limpiar.config(command=self.controller.limpiar_formulario)
        self.btn_actualizar_lista.config(command=self.controller.actualizar_lista_clientes)
        
        # Bind para Enter en búsqueda
        self.entry_buscar.bind("<Return>", lambda e: self.controller.buscar_cliente())
        
    def on_cliente_select(self, event):
        """Maneja la selección de cliente en la lista"""
        if self.controller:
            self.controller.on_cliente_seleccionado()
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.var_codigo.set("")
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_email.set("")
        self.var_telefono.set("")
        self.var_direccion.set("")
        self.var_buscar_codigo.set("")
        
    def cargar_cliente_en_formulario(self, cliente):
        """Carga los datos de un cliente en el formulario"""
        self.var_codigo.set(str(cliente['codigo']))
        self.var_nombre.set(cliente['nombre'])
        self.var_apellido.set(cliente['apellido'])
        self.var_email.set(cliente['email'])
        self.var_telefono.set(cliente['telefono'])
        self.var_direccion.set(cliente['direccion'])
        
    def obtener_datos_formulario(self):
        """Obtiene los datos del formulario"""
        return {
            'codigo': self.var_codigo.get(),
            'nombre': self.var_nombre.get().strip(),
            'apellido': self.var_apellido.get().strip(),
            'email': self.var_email.get().strip(),
            'telefono': self.var_telefono.get().strip(),
            'direccion': self.var_direccion.get().strip()
        }
        
    def cargar_lista_clientes(self, clientes):
        """Carga la lista de clientes en el Treeview"""
        # Limpiar lista actual
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
            
        # Cargar nuevos datos
        for cliente in clientes:
            self.tree_clientes.insert("", "end", values=(
                cliente['codigo'],
                cliente['nombre'],
                cliente['apellido'],
                cliente['email'],
                cliente['telefono'],
                cliente['direccion'],
                cliente['fecha_registro']
            ))
    
    def obtener_cliente_seleccionado(self):
        """Obtiene el código del cliente seleccionado en la lista"""
        selection = self.tree_clientes.selection()
        if selection:
            item = self.tree_clientes.item(selection[0])
            return int(item['values'][0])  # Código del cliente
        return None
        
    def mostrar_mensaje(self, tipo, titulo, mensaje):
        """Muestra un mensaje al usuario"""
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "question":
            return messagebox.askyesno(titulo, mensaje)
    
    def obtener_codigo_busqueda(self):
        """Obtiene el código ingresado para búsqueda"""
        return self.var_buscar_codigo.get().strip()
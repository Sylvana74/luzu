# controller/cliente_controller.py
import re
from model.cliente_model import ClienteModel

class ClienteController:
    def __init__(self, view):
        self.view = view
        self.model = ClienteModel()
        self.view.set_controller(self)
        self.modo_edicion = False  # False = nuevo, True = editando
        
        # Cargar lista inicial
        self.actualizar_lista_clientes()
        
    def validar_datos(self, datos):
        """Valida los datos del formulario"""
        errores = []
        
        if not datos['nombre']:
            errores.append("El nombre es obligatorio")
        elif len(datos['nombre']) < 2:
            errores.append("El nombre debe tener al menos 2 caracteres")
            
        if not datos['apellido']:
            errores.append("El apellido es obligatorio")
        elif len(datos['apellido']) < 2:
            errores.append("El apellido debe tener al menos 2 caracteres")
            
        if not datos['email']:
            errores.append("El email es obligatorio")
        else:
            # Validar formato de email
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron_email, datos['email']):
                errores.append("El formato del email no es válido")
                
        if not datos['telefono']:
            errores.append("El teléfono es obligatorio")
        elif len(datos['telefono']) < 8:
            errores.append("El teléfono debe tener al menos 8 dígitos")
            
        if not datos['direccion']:
            errores.append("La dirección es obligatoria")
        elif len(datos['direccion']) < 5:
            errores.append("La dirección debe tener al menos 5 caracteres")
            
        return errores
    
    def nuevo_cliente(self):
        """Prepara el formulario para un nuevo cliente"""
        self.limpiar_formulario()
        self.modo_edicion = False
        self.view.var_codigo.set(f"Nuevo cliente - Código: {self.model.next_codigo}")
        self.view.mostrar_mensaje("info", "Nuevo Cliente", 
                                 "Formulario preparado para nuevo cliente.\nComplete los datos y presione 'Guardar'.")
        
        # Enfocar el primer campo
        self.view.entry_nombre.focus()
        
    def guardar_cliente(self):
        """Guarda un nuevo cliente"""
        if self.modo_edicion:
            self.view.mostrar_mensaje("warning", "Modo Edición", 
                                     "Está en modo edición. Use 'Actualizar' para guardar cambios.")
            return
            
        datos = self.view.obtener_datos_formulario()
        
        # Validar datos
        errores = self.validar_datos(datos)
        if errores:
            mensaje_error = "Errores encontrados:\n\n" + "\n".join(f"• {error}" for error in errores)
            self.view.mostrar_mensaje("error", "Error de Validación", mensaje_error)
            return
        
        # Guardar en base de datos
        exito, codigo = self.model.crear_cliente(
            datos['nombre'], 
            datos['apellido'], 
            datos['email'], 
            datos['telefono'], 
            datos['direccion']
        )
        
        if exito:
            self.view.mostrar_mensaje("info", "Cliente Guardado", 
                                     f"Cliente guardado exitosamente.\nCódigo asignado: {codigo}")
            self.limpiar_formulario()
            self.actualizar_lista_clientes()
        else:
            self.view.mostrar_mensaje("error", "Error", "No se pudo guardar el cliente")
    
    def actualizar_cliente(self):
        """Actualiza los datos de un cliente existente"""
        if not self.modo_edicion:
            self.view.mostrar_mensaje("warning", "Modo Nuevo", 
                                     "No hay cliente seleccionado para actualizar.\nSeleccione un cliente de la lista o use 'Buscar'.")
            return
            
        datos = self.view.obtener_datos_formulario()
        
        if not datos['codigo']:
            self.view.mostrar_mensaje("error", "Error", "No hay código de cliente para actualizar")
            return
        
        # Validar datos
        errores = self.validar_datos(datos)
        if errores:
            mensaje_error = "Errores encontrados:\n\n" + "\n".join(f"• {error}" for error in errores)
            self.view.mostrar_mensaje("error", "Error de Validación", mensaje_error)
            return
        
        # Confirmar actualización
        confirmar = self.view.mostrar_mensaje("question", "Confirmar Actualización", 
                                             f"¿Está seguro que desea actualizar el cliente {datos['codigo']}?")
        
        if confirmar:
            exito = self.model.actualizar_cliente(
                int(datos['codigo']),
                datos['nombre'], 
                datos['apellido'], 
                datos['email'], 
                datos['telefono'], 
                datos['direccion']
            )
            
            if exito:
                self.view.mostrar_mensaje("info", "Cliente Actualizado", 
                                         f"Cliente {datos['codigo']} actualizado exitosamente.")
                self.actualizar_lista_clientes()
            else:
                self.view.mostrar_mensaje("error", "Error", "No se pudo actualizar el cliente")
    
    def eliminar_cliente(self):
        """Elimina un cliente"""
        # Verificar si hay cliente seleccionado
        codigo_seleccionado = self.view.obtener_cliente_seleccionado()
        if not codigo_seleccionado:
            datos = self.view.obtener_datos_formulario()
            if datos['codigo']:
                try:
                    codigo_seleccionado = int(datos['codigo'])
                except ValueError:
                    self.view.mostrar_mensaje("error", "Error", 
                                             "Seleccione un cliente de la lista o búsquelo primero")
                    return
            else:
                self.view.mostrar_mensaje("error", "Error", 
                                         "Seleccione un cliente de la lista o búsquelo primero")
                return
        
        # Obtener datos del cliente para mostrar en confirmación
        cliente = self.model.obtener_cliente(codigo_seleccionado)
        if not cliente:
            self.view.mostrar_mensaje("error", "Error", "Cliente no encontrado")
            return
        
        # Confirmar eliminación
        mensaje_confirmacion = (f"¿Está seguro que desea eliminar el cliente?\n\n"
                               f"Código: {cliente['codigo']}\n"
                               f"Nombre: {cliente['nombre']} {cliente['apellido']}\n"
                               f"Email: {cliente['email']}\n\n"
                               f"Esta acción no se puede deshacer.")
        
        confirmar = self.view.mostrar_mensaje("question", "Confirmar Eliminación", mensaje_confirmacion)
        
        if confirmar:
            exito = self.model.eliminar_cliente(codigo_seleccionado)
            
            if exito:
                self.view.mostrar_mensaje("info", "Cliente Eliminado", 
                                         f"Cliente {codigo_seleccionado} eliminado exitosamente.")
                self.limpiar_formulario()
                self.actualizar_lista_clientes()
            else:
                self.view.mostrar_mensaje("error", "Error", "No se pudo eliminar el cliente")
    
    def buscar_cliente(self):
        """Busca un cliente por código"""
        codigo_buscar = self.view.obtener_codigo_busqueda()
        
        if not codigo_buscar:
            self.view.mostrar_mensaje("warning", "Código Requerido", 
                                     "Ingrese un código de cliente para buscar")
            return
        
        try:
            codigo = int(codigo_buscar)
        except ValueError:
            self.view.mostrar_mensaje("error", "Error", "El código debe ser un número")
            return
        
        # Buscar cliente
        cliente = self.model.obtener_cliente(codigo)
        
        if cliente:
            # Cargar datos en formulario
            self.view.cargar_cliente_en_formulario(cliente)
            self.modo_edicion = True
            
            # Seleccionar en la lista si existe
            self.seleccionar_cliente_en_lista(codigo)
            
            self.view.mostrar_mensaje("info", "Cliente Encontrado", 
                                     f"Cliente {codigo} encontrado y cargado en el formulario.")
        else:
            self.view.mostrar_mensaje("warning", "Cliente No Encontrado", 
                                     f"No se encontró ningún cliente con el código {codigo}")
    
    def seleccionar_cliente_en_lista(self, codigo):
        """Selecciona un cliente específico en la lista"""
        for item in self.view.tree_clientes.get_children():
            valores = self.view.tree_clientes.item(item)['values']
            if valores and int(valores[0]) == codigo:
                self.view.tree_clientes.selection_set(item)
                self.view.tree_clientes.see(item)
                break
    
    def limpiar_formulario(self):
        """Limpia el formulario y resetea el modo"""
        self.view.limpiar_formulario()
        self.modo_edicion = False
        
        # Limpiar selección de la lista
        self.view.tree_clientes.selection_remove(self.view.tree_clientes.selection())
    
    def actualizar_lista_clientes(self):
        """Actualiza la lista de clientes desde la base de datos"""
        clientes = self.model.obtener_todos_clientes()
        self.view.cargar_lista_clientes(clientes)
        
        if not clientes:
            print("LOG: No hay clientes registrados en el sistema")
        else:
            print(f"LOG: Lista actualizada con {len(clientes)} clientes")
    
    def on_cliente_seleccionado(self):
        """Maneja la selección de un cliente en la lista"""
        codigo_seleccionado = self.view.obtener_cliente_seleccionado()
        
        if codigo_seleccionado:
            # Obtener datos completos del cliente
            cliente = self.model.obtener_cliente(codigo_seleccionado)
            
            if cliente:
                # Cargar en formulario
                self.view.cargar_cliente_en_formulario(cliente)
                self.modo_edicion = True
                
                # Actualizar campo de búsqueda
                self.view.var_buscar_codigo.set(str(codigo_seleccionado))
            else:
                self.view.mostrar_mensaje("error", "Error", "No se pudieron cargar los datos del cliente")
    
    def validar_codigo_numerico(self, codigo_str):
        """Valida que el código sea un número válido"""
        try:
            codigo = int(codigo_str)
            if codigo < 100:
                return False, "El código debe ser mayor o igual a 100"
            return True, codigo
        except ValueError:
            return False, "El código debe ser un número"
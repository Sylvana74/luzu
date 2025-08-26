# model/cliente_model.py
import sqlite3
import os
from datetime import datetime

class ClienteModel:
    def __init__(self, db_name="sandtech_clientes.db"):
        self.db_name = db_name
        self.init_db()
        self.next_codigo = self.get_next_codigo()
    
    def init_db(self):
        """Inicializa la base de datos y crea la tabla si no existe"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    codigo INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    fecha_registro TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            self.log_transaction("Base de datos inicializada correctamente")
            
        except sqlite3.Error as e:
            self.log_transaction(f"Error al inicializar base de datos: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def log_transaction(self, mensaje):
        """Registra las transacciones en consola con timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] LOG: {mensaje}")
    
    def get_next_codigo(self):
        """Obtiene el siguiente código de cliente (comenzando en 100)"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT MAX(codigo) FROM clientes")
            result = cursor.fetchone()[0]
            
            if result is None:
                return 100
            else:
                return result + 1
                
        except sqlite3.Error as e:
            self.log_transaction(f"Error al obtener siguiente código: {e}")
            return 100
        finally:
            if conn:
                conn.close()
    
    def crear_cliente(self, nombre, apellido, email, telefono, direccion):
        """Crea un nuevo cliente en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            codigo = self.next_codigo
            fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO clientes (codigo, nombre, apellido, email, telefono, direccion, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (codigo, nombre, apellido, email, telefono, direccion, fecha_registro))
            
            conn.commit()
            self.next_codigo += 1
            
            self.log_transaction(f"Cliente creado - Código: {codigo}, Nombre: {nombre} {apellido}")
            return True, codigo
            
        except sqlite3.Error as e:
            self.log_transaction(f"Error al crear cliente: {e}")
            return False, None
        finally:
            if conn:
                conn.close()
    
    def obtener_cliente(self, codigo):
        """Obtiene un cliente por su código"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM clientes WHERE codigo = ?", (codigo,))
            result = cursor.fetchone()
            
            if result:
                self.log_transaction(f"Cliente encontrado - Código: {codigo}")
                return {
                    'codigo': result[0],
                    'nombre': result[1],
                    'apellido': result[2],
                    'email': result[3],
                    'telefono': result[4],
                    'direccion': result[5],
                    'fecha_registro': result[6]
                }
            else:
                self.log_transaction(f"Cliente no encontrado - Código: {codigo}")
                return None
                
        except sqlite3.Error as e:
            self.log_transaction(f"Error al obtener cliente: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def obtener_todos_clientes(self):
        """Obtiene todos los clientes de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM clientes ORDER BY codigo")
            results = cursor.fetchall()
            
            clientes = []
            for result in results:
                clientes.append({
                    'codigo': result[0],
                    'nombre': result[1],
                    'apellido': result[2],
                    'email': result[3],
                    'telefono': result[4],
                    'direccion': result[5],
                    'fecha_registro': result[6]
                })
            
            self.log_transaction(f"Obtenidos {len(clientes)} clientes")
            return clientes
            
        except sqlite3.Error as e:
            self.log_transaction(f"Error al obtener todos los clientes: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def actualizar_cliente(self, codigo, nombre, apellido, email, telefono, direccion):
        """Actualiza los datos de un cliente"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE clientes 
                SET nombre = ?, apellido = ?, email = ?, telefono = ?, direccion = ?
                WHERE codigo = ?
            ''', (nombre, apellido, email, telefono, direccion, codigo))
            
            if cursor.rowcount > 0:
                conn.commit()
                self.log_transaction(f"Cliente actualizado - Código: {codigo}")
                return True
            else:
                self.log_transaction(f"No se pudo actualizar cliente - Código: {codigo}")
                return False
                
        except sqlite3.Error as e:
            self.log_transaction(f"Error al actualizar cliente: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def eliminar_cliente(self, codigo):
        """Elimina un cliente de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Primero verificamos si existe
            cursor.execute("SELECT nombre, apellido FROM clientes WHERE codigo = ?", (codigo,))
            cliente = cursor.fetchone()
            
            if cliente:
                cursor.execute("DELETE FROM clientes WHERE codigo = ?", (codigo,))
                conn.commit()
                self.log_transaction(f"Cliente eliminado - Código: {codigo}, Nombre: {cliente[0]} {cliente[1]}")
                return True
            else:
                self.log_transaction(f"No se pudo eliminar cliente - Código: {codigo} no existe")
                return False
                
        except sqlite3.Error as e:
            self.log_transaction(f"Error al eliminar cliente: {e}")
            return False
        finally:
            if conn:
                conn.close()